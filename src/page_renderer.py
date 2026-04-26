from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.config import settings
_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=select_autoescape(["html", "xml"]))
def _base_url() -> str:
    return settings.site_url.rstrip("/")
def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()
def seo_payload(path: str, title: str, description: str, keywords: str = "") -> dict:
    base = _base_url()
    return {"title": title, "description": description, "keywords": keywords, "canonical": f"{base}{path}", "site_name": settings.site_name, "site_url": base, "locale": settings.site_locale, "og_image": f"{base}/static/og-image.png", "og_type": "website", "published_iso": _iso(datetime.utcnow()), "modified_iso": _iso(datetime.utcnow())}
