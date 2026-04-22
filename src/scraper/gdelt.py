"""
Client for the GDELT DOC 2.0 API — global news monitoring for Venezuela.

GDELT monitors news in 100+ languages, updates every 15 minutes, and
provides article metadata with tone/sentiment scores. No API key required.

API docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

Reliability notes:
GDELT's edge has been intermittently flaky in production — TLS handshake
timeouts, non-JSON HTML error pages, occasional 429s. The hardening in
this module is shaped by the operational requirement that the daily
cron MUST NOT get stuck on this source. Concretely:
  - explicit short connect/read timeouts override the BaseScraper default
  - retry loop catches network-layer errors (not just 429), with bounded
    attempt count and bounded backoff
  - a hard wall-clock budget caps the entire scrape() method
  - any unexpected exception drops to success=False with empty articles
"""

from __future__ import annotations

import logging
import ssl
import time
from datetime import date
from typing import Optional

import httpx

from src.scraper.base import BaseScraper, ScrapedArticle, ScrapeResult

logger = logging.getLogger(__name__)

GDELT_DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"

INVESTMENT_QUERY = (
    "Venezuela investment OR sanctions OR oil OR economy "
    "sourcelang:english"
)

SPANISH_QUERY = (
    "Venezuela inversión OR sanciones OR petróleo OR economía "
    "sourcelang:spanish"
)

# Per-query bounds. Tuned so that the scraper can never hold up the cron
# longer than MAX_TOTAL_WALLCLOCK_SECONDS even in the worst retry path.
PER_QUERY_MAX_ATTEMPTS = 3
RATE_LIMIT_BACKOFF_SECONDS = 8       # exponential — 8, 16, 24
NETWORK_ERROR_BACKOFF_SECONDS = 5    # linear — same wait every retry
INTER_QUERY_SLEEP_SECONDS = 5

# Worst-case math for the whole scraper:
#   per query attempt: connect(10) + read(20) = 30s
#   backoffs across 3 attempts: 8 + 16 = 24s
#   per query total worst case: 3*30 + 24 = ~114s
#   two queries + inter-query sleep: ~233s
# We cap the whole scraper at 150s — if we blow past that, we return
# whatever we have rather than letting the cron wait further.
MAX_TOTAL_WALLCLOCK_SECONDS = 150


class GDELTScraper(BaseScraper):
    """
    Queries the GDELT DOC 2.0 API for English and Spanish articles
    about Venezuela relevant to investment analysis.
    """

    def __init__(self) -> None:
        super().__init__()
        # Replace BaseScraper's blanket 30s timeout with phase-specific
        # bounds. Connect=10s is critical: GDELT's failure mode in
        # production is a stalled TLS handshake, and the inherited
        # 30s connect timeout means we'd waste 30s per attempt × 3
        # attempts × 2 queries = 3 minutes just waiting on dead sockets.
        self.client.close()
        self.client = httpx.Client(
            timeout=httpx.Timeout(20.0, connect=10.0),
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "es-VE,es;q=0.9,en;q=0.8",
            },
        )

    def get_source_id(self) -> str:
        return "gdelt"

    def scrape(self, target_date: Optional[date] = None) -> ScrapeResult:
        start = time.monotonic()
        deadline = start + MAX_TOTAL_WALLCLOCK_SECONDS
        target_date = target_date or date.today()

        en_articles: list[ScrapedArticle] = []
        es_articles: list[ScrapedArticle] = []

        try:
            en_articles = self._safely_query(
                INVESTMENT_QUERY, timespan="7days", deadline=deadline
            )

            if time.monotonic() < deadline - INTER_QUERY_SLEEP_SECONDS:
                time.sleep(INTER_QUERY_SLEEP_SECONDS)
                es_articles = self._safely_query(
                    SPANISH_QUERY, timespan="7days", deadline=deadline
                )
            else:
                logger.warning(
                    "GDELT: skipping Spanish query — wall-clock budget "
                    "(%ds) exhausted by English query",
                    MAX_TOTAL_WALLCLOCK_SECONDS,
                )

            seen_urls: set[str] = set()
            deduped: list[ScrapedArticle] = []
            for a in en_articles + es_articles:
                if a.source_url and a.source_url not in seen_urls:
                    seen_urls.add(a.source_url)
                    deduped.append(a)

            elapsed = int(time.monotonic() - start)
            logger.info(
                "GDELT: %d EN + %d ES = %d unique articles in %ds",
                len(en_articles), len(es_articles), len(deduped), elapsed,
            )

            # success=True even with zero articles. A flaky GDELT day is
            # not an error condition for the pipeline — the scrape_log
            # row records duration/count for diagnostics, but the
            # downstream stages (analyze, report) treat empty results
            # the same way they treat any other quiet news day.
            return ScrapeResult(
                source=self.get_source_id(),
                success=True,
                articles=deduped,
                duration_seconds=elapsed,
            )

        except Exception as exc:
            # Last-resort safety net. Anything we missed lands here and
            # we still return a well-formed result so the pipeline keeps
            # moving instead of crashing the daily cron.
            logger.error("GDELT scrape failed unexpectedly: %s", exc, exc_info=True)
            return ScrapeResult(
                source=self.get_source_id(),
                success=False,
                error=str(exc),
                duration_seconds=int(time.monotonic() - start),
            )

    # ── internals ─────────────────────────────────────────────────────

    def _safely_query(
        self, query: str, *, timespan: str, deadline: float,
    ) -> list[ScrapedArticle]:
        """Wrapper that absorbs every exception so a single bad query
        cannot bring the whole scraper down. Returns [] on any failure."""
        try:
            return self._query_articles(query, timespan=timespan, deadline=deadline)
        except Exception as exc:
            logger.warning(
                "GDELT query %r raised unexpectedly (%s) — returning empty",
                query[:60], type(exc).__name__,
            )
            return []

    def _query_articles(
        self,
        query: str,
        *,
        timespan: str = "7days",
        max_records: int = 75,
        deadline: float,
    ) -> list[ScrapedArticle]:
        params = {
            "query": query,
            "mode": "ArtList",
            "maxrecords": str(max_records),
            "format": "json",
            "timespan": timespan,
            "sort": "DateDesc",
        }

        logger.info("GDELT query: %s", query[:80])

        resp: Optional[httpx.Response] = None
        for attempt in range(PER_QUERY_MAX_ATTEMPTS):
            if time.monotonic() >= deadline:
                logger.warning(
                    "GDELT query %r: wall-clock deadline reached after %d attempt(s)",
                    query[:60], attempt,
                )
                return []

            try:
                resp = self.client.get(GDELT_DOC_API, params=params)
            except (
                httpx.ConnectError,
                httpx.TimeoutException,
                httpx.RemoteProtocolError,
                ssl.SSLError,
            ) as exc:
                # Network-layer failure (the most common production
                # symptom). Back off briefly and try again. The whole
                # try/except block exists because BaseScraper's
                # tenacity retry was never wired into this method.
                wait = NETWORK_ERROR_BACKOFF_SECONDS
                logger.warning(
                    "GDELT network error on %r attempt %d/%d (%s) — "
                    "waiting %ds",
                    query[:60], attempt + 1, PER_QUERY_MAX_ATTEMPTS,
                    type(exc).__name__, wait,
                )
                if attempt + 1 < PER_QUERY_MAX_ATTEMPTS:
                    self._sleep_until(min(time.monotonic() + wait, deadline))
                continue

            if resp.status_code == 429:
                # Exponential — 8s, 16s, 24s. Bounded so the rate-limit
                # path can't blow our wall-clock budget on its own.
                wait = RATE_LIMIT_BACKOFF_SECONDS * (attempt + 1)
                logger.warning(
                    "GDELT rate-limited on %r attempt %d/%d — waiting %ds",
                    query[:60], attempt + 1, PER_QUERY_MAX_ATTEMPTS, wait,
                )
                if attempt + 1 < PER_QUERY_MAX_ATTEMPTS:
                    self._sleep_until(min(time.monotonic() + wait, deadline))
                continue

            try:
                resp.raise_for_status()
                break
            except httpx.HTTPStatusError as exc:
                # 5xx or unexpected 4xx. Single retry with short
                # backoff; if it's a permanent error we'll bail on the
                # next loop and the outer caller returns [].
                logger.warning(
                    "GDELT HTTP %s on %r attempt %d/%d",
                    resp.status_code, query[:60], attempt + 1,
                    PER_QUERY_MAX_ATTEMPTS,
                )
                if attempt + 1 < PER_QUERY_MAX_ATTEMPTS:
                    self._sleep_until(min(
                        time.monotonic() + NETWORK_ERROR_BACKOFF_SECONDS,
                        deadline,
                    ))
                continue
        else:
            logger.error(
                "GDELT query %r exhausted %d attempts without a 2xx response",
                query[:60], PER_QUERY_MAX_ATTEMPTS,
            )
            return []

        if resp is None:
            return []

        content_type = resp.headers.get("content-type", "")
        if "json" not in content_type:
            # GDELT serves an HTML error page when overloaded. Don't
            # retry — the same query just gave us non-JSON, hammering
            # the API harder won't help. Drop and let the next cron
            # tick have a go.
            logger.warning(
                "GDELT returned non-JSON (%s) for %r — skipping query",
                content_type, query[:60],
            )
            return []

        try:
            data = resp.json()
        except Exception:
            logger.warning("GDELT response for %r not valid JSON — skipping", query[:60])
            return []

        raw_articles = data.get("articles", [])
        articles: list[ScrapedArticle] = []

        for item in raw_articles:
            try:
                pub_date = self._parse_gdelt_date(item.get("seendate", ""))
                tone = item.get("tone", 0.0)
                domain = item.get("domain", "")
                source_country = item.get("sourcecountry", "")

                articles.append(
                    ScrapedArticle(
                        headline=item.get("title", ""),
                        published_date=pub_date or date.today(),
                        source_url=item.get("url", ""),
                        body_text=None,
                        source_name=domain,
                        source_credibility=self._infer_credibility(domain),
                        article_type="news",
                        extra_metadata={
                            "tone": tone,
                            "domain": domain,
                            "source_country": source_country,
                            "language": item.get("language", ""),
                            "image_url": item.get("socialimage", ""),
                        },
                    )
                )
            except Exception as exc:
                # Per-item parse error must not sink the whole query.
                logger.debug("GDELT item parse error: %s", exc)
                continue

        return articles

    @staticmethod
    def _sleep_until(deadline: float) -> None:
        """Sleep until the given monotonic timestamp, never longer."""
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(remaining)

    @staticmethod
    def _parse_gdelt_date(datestr: str) -> Optional[date]:
        """Parse GDELT date format: '20260414T120000Z'."""
        if not datestr or len(datestr) < 8:
            return None
        try:
            return date(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:8]))
        except (ValueError, IndexError):
            return None

    @staticmethod
    def _infer_credibility(domain: str) -> str:
        high_credibility = {
            "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk",
            "bloomberg.com", "ft.com", "economist.com", "wsj.com",
            "nytimes.com", "washingtonpost.com", "aljazeera.com",
            "theguardian.com", "france24.com", "dw.com",
        }
        state_media = {
            "telesurtv.net", "vtv.gob.ve", "correodelcaroni.com",
            "ultimasnoticias.com.ve", "avn.info.ve",
        }
        domain_lower = domain.lower()
        if any(d in domain_lower for d in high_credibility):
            return "tier1"
        if any(d in domain_lower for d in state_media):
            return "state"
        return "tier2"
