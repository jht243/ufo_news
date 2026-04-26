from __future__ import annotations

import re
import time
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from src.scraper.base import BaseScraper, ScrapedArticle, ScrapeResult


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _date_from_text(raw: str | None, fallback: date) -> date:
    if not raw:
        return fallback
    for parser in (
        lambda s: parsedate_to_datetime(s).date(),
        lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")).date(),
    ):
        try:
            return parser(raw)
        except Exception:
            pass
    return fallback


class StaticPageLinkScraper(BaseScraper):
    source_id = ""
    source_name = ""
    credibility = "news"
    url = ""
    article_type = "news"
    link_patterns: tuple[str, ...] = ()

    def get_source_id(self) -> str:
        return self.source_id

    def scrape(self, target_date: date | None = None) -> ScrapeResult:
        started = time.time()
        target_date = target_date or date.today()
        try:
            resp = self._fetch(self.url)
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = []
            seen = set()
            for a in soup.find_all("a", href=True):
                title = _clean(a.get_text(" "))
                href = a["href"]
                if not title or len(title) < 8:
                    continue
                if self.link_patterns and not any(p.lower() in (title + " " + href).lower() for p in self.link_patterns):
                    continue
                if href.startswith("/"):
                    base = re.match(r"https?://[^/]+", self.url).group(0)
                    href = base + href
                if not href.startswith("http") or href in seen:
                    continue
                seen.add(href)
                articles.append(ScrapedArticle(
                    headline=title[:240],
                    published_date=target_date,
                    source_url=href,
                    body_text=f"Indexed from {self.source_name}: {title}",
                    source_name=self.source_name,
                    source_credibility=self.credibility,
                    article_type=self.article_type,
                    extra_metadata={"scraper": self.source_id},
                ))
                if len(articles) >= 25:
                    break
            return self._result(started, articles)
        except Exception as exc:
            return ScrapeResult(source=self.get_source_id(), success=False, error=str(exc), duration_seconds=int(time.time() - started))


class AAROCasesScraper(StaticPageLinkScraper):
    source_id = "aaro_cases"
    source_name = "AARO UAP Case Resolution Reports"
    credibility = "official"
    url = "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"
    article_type = "case_resolution"
    link_patterns = ("case", "video", "object", "gofast", "eglin", "puerto", "western")


class AARORecordsScraper(StaticPageLinkScraper):
    source_id = "aaro_records"
    source_name = "AARO UAP Records"
    credibility = "official"
    url = "https://www.aaro.mil/UAP-Records/"
    article_type = "official_record"
    link_patterns = ("uap", "records", "paper", "nara", "nasa", "workshop")


class NARAUapScraper(StaticPageLinkScraper):
    source_id = "nara_uap"
    source_name = "National Archives UAP Collection"
    credibility = "official"
    url = "https://www.archives.gov/research/topics/uaps"
    article_type = "official_record"
    link_patterns = ("uap", "ufo", "record", "collection", "catalog", "615")


class NASAUapScraper(StaticPageLinkScraper):
    source_id = "nasa_uap"
    source_name = "NASA UAP"
    credibility = "official"
    url = "https://science.nasa.gov/uap/"
    article_type = "official_record"
    link_patterns = ("uap", "report", "study", "nasa")


class CongressUapScraper(StaticPageLinkScraper):
    source_id = "congress"
    source_name = "Congress.gov UAP Search"
    credibility = "official"
    url = "https://www.congress.gov/search?q=%7B%22search%22%3A%22unidentified+anomalous+phenomena%22%7D"
    article_type = "hearing_or_bill"
    link_patterns = ("uap", "unidentified", "phenomena", "bill", "hearing", "amendment")


class FederalRegisterUapScraper(StaticPageLinkScraper):
    source_id = "federal_register"
    source_name = "Federal Register"
    credibility = "official"
    url = "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=unidentified+anomalous+phenomena"
    article_type = "official_notice"
    link_patterns = ("unidentified", "uap", "phenomena", "notice")


class NUFORCScraper(StaticPageLinkScraper):
    source_id = "nuforc"
    source_name = "NUFORC"
    credibility = "witness"
    url = "https://nuforc.org/databank/"
    article_type = "witness_database"
    link_patterns = ("report", "tier", "pilot", "latest", "investigation", "state", "shape")


class BlackVaultScraper(StaticPageLinkScraper):
    source_id = "black_vault"
    source_name = "The Black Vault"
    credibility = "foia"
    url = "https://www.theblackvault.com/documentarchive/category/ufos/"
    article_type = "foia_archive"
    link_patterns = ("uap", "ufo", "foia", "aaro", "document", "release")


class TheDebriefScraper(StaticPageLinkScraper):
    source_id = "the_debrief"
    source_name = "The Debrief"
    credibility = "research"
    url = "https://thedebrief.org/?s=UAP"
    article_type = "research_outlet"
    link_patterns = ("uap", "ufo", "aaro", "pentagon", "congress", "phenomena")


class LiberationTimesScraper(StaticPageLinkScraper):
    source_id = "liberation_times"
    source_name = "Liberation Times"
    credibility = "research"
    url = "https://www.liberationtimes.com/home?tag=UAP"
    article_type = "research_outlet"
    link_patterns = ("uap", "ufo", "aaro", "congress", "disclosure", "phenomena")


class GoogleNewsUapScraper(BaseScraper):
    def get_source_id(self) -> str:
        return "google_news"

    def scrape(self, target_date: date | None = None) -> ScrapeResult:
        started = time.time()
        target_date = target_date or date.today()
        query = quote_plus('("UAP" OR "UFO" OR "unidentified anomalous phenomena" OR AARO)')
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            resp = self._fetch(url)
            root = ET.fromstring(resp.text)
            articles = []
            for item in root.findall(".//item")[:30]:
                title = _clean(item.findtext("title"))
                link = _clean(item.findtext("link"))
                pub = _date_from_text(item.findtext("pubDate"), target_date)
                desc = _clean(item.findtext("description"))
                if title and link:
                    articles.append(ScrapedArticle(
                        headline=title[:240],
                        published_date=pub,
                        source_url=link,
                        body_text=desc or title,
                        source_name="Google News",
                        source_credibility="news",
                        article_type="news",
                        extra_metadata={"query": "UAP UFO AARO unidentified anomalous phenomena"},
                    ))
            return self._result(started, articles)
        except Exception as exc:
            return ScrapeResult(source=self.get_source_id(), success=False, error=str(exc), duration_seconds=int(time.time() - started))


ALL_UAP_SCRAPERS = [
    AAROCasesScraper,
    AARORecordsScraper,
    NARAUapScraper,
    NASAUapScraper,
    CongressUapScraper,
    FederalRegisterUapScraper,
    NUFORCScraper,
    BlackVaultScraper,
    TheDebriefScraper,
    LiberationTimesScraper,
    GoogleNewsUapScraper,
]
