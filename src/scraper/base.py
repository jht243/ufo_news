from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.config import settings

logger = logging.getLogger(__name__)


@dataclass
class ScrapedArticle:
    headline: str
    published_date: date
    source_url: str
    body_text: Optional[str] = None
    source_name: str = ""
    source_credibility: str = "news"
    article_type: str = "news"
    extra_metadata: dict = field(default_factory=dict)


@dataclass
class ScrapeResult:
    source: str
    success: bool
    articles: list[ScrapedArticle] = field(default_factory=list)
    error: Optional[str] = None
    duration_seconds: int = 0


class BaseScraper(ABC):
    def __init__(self):
        self.client = httpx.Client(
            timeout=settings.scraper_timeout_seconds,
            follow_redirects=True,
            headers={
                "User-Agent": "The UAP Index research crawler (+https://uapindex.com/sources)",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )

    @abstractmethod
    def get_source_id(self) -> str:
        ...

    @abstractmethod
    def scrape(self, target_date: Optional[date] = None) -> ScrapeResult:
        ...

    def close(self):
        self.client.close()

    @retry(stop=stop_after_attempt(settings.scraper_max_retries), wait=wait_exponential(multiplier=1, min=2, max=30), retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException)))
    def _fetch(self, url: str) -> httpx.Response:
        logger.info("Fetching %s", url)
        resp = self.client.get(url)
        resp.raise_for_status()
        return resp

    def _result(self, started: float, articles: list[ScrapedArticle]) -> ScrapeResult:
        return ScrapeResult(source=self.get_source_id(), success=True, articles=articles, duration_seconds=int(time.time() - started))
