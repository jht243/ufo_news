from __future__ import annotations

import logging
from datetime import date

from sqlalchemy.exc import IntegrityError

from src.models import SessionLocal, init_db, ExternalArticleEntry, ScrapeLog, SourceType, CredibilityTier, GazetteStatus
from src.scraper.uap_sources import ALL_UAP_SCRAPERS

logger = logging.getLogger(__name__)


def run_daily_scrape(target_date: date | None = None) -> dict:
    target_date = target_date or date.today()
    init_db()
    summary = {"date": str(target_date), "articles_found": 0, "articles_new": 0, "errors": []}
    for scraper_cls in ALL_UAP_SCRAPERS:
        scraper = scraper_cls()
        try:
            result = scraper.scrape(target_date)
            found = len(result.articles)
            new_ids = _persist_articles(result.articles) if result.success else []
            _log_scrape(result.source, target_date, result.success, found, len(new_ids), result.error, result.duration_seconds)
            summary["articles_found"] += found
            summary["articles_new"] += len(new_ids)
            if not result.success:
                summary["errors"].append(f"{result.source}: {result.error}")
        except Exception as exc:
            logger.exception("Scraper crashed: %s", scraper.get_source_id())
            summary["errors"].append(f"{scraper.get_source_id()}: {exc}")
        finally:
            scraper.close()
    return summary


def _persist_articles(articles) -> list[int]:
    new_ids: list[int] = []
    db = SessionLocal()
    try:
        for a in articles:
            try:
                source = SourceType(a.extra_metadata.get("source_override") or _source_from_article(a))
            except Exception:
                source = SourceType.GOOGLE_NEWS
            try:
                credibility = CredibilityTier(a.source_credibility)
            except Exception:
                credibility = CredibilityTier.NEWS
            entry = ExternalArticleEntry(
                source=source,
                source_url=a.source_url,
                source_name=a.source_name,
                credibility=credibility,
                headline=a.headline,
                published_date=a.published_date,
                body_text=a.body_text,
                article_type=a.article_type,
                extra_metadata=a.extra_metadata,
                status=GazetteStatus.SCRAPED,
            )
            nested = db.begin_nested()
            try:
                db.add(entry)
                db.flush()
                nested.commit()
                new_ids.append(entry.id)
            except IntegrityError:
                nested.rollback()
        db.commit()
    finally:
        db.close()
    return new_ids


def _source_from_article(article) -> str:
    name = (article.extra_metadata or {}).get("scraper")
    if name:
        return name
    map_by_name = {
        "AARO UAP Case Resolution Reports": "aaro_cases",
        "AARO UAP Records": "aaro_records",
        "National Archives UAP Collection": "nara_uap",
        "NASA UAP": "nasa_uap",
        "Congress.gov UAP Search": "congress",
        "Federal Register": "federal_register",
        "NUFORC": "nuforc",
        "The Black Vault": "black_vault",
        "The Debrief": "the_debrief",
        "Liberation Times": "liberation_times",
        "Google News": "google_news",
    }
    return map_by_name.get(article.source_name, "google_news")


def _log_scrape(source: str, target_date: date, success: bool, found: int, new: int, error: str | None, duration: int) -> None:
    db = SessionLocal()
    try:
        db.add(ScrapeLog(source=source, target_date=target_date, success=success, items_found=found, items_new=new, error=error, duration_seconds=duration))
        db.commit()
    finally:
        db.close()
