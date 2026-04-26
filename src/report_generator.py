from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.config import settings
from src.data.uap_cases import list_cases, evidence_grade
from src.models import SessionLocal, ExternalArticleEntry, BlogPost, GazetteStatus, SourceType, init_db

logger = logging.getLogger(__name__)

FILTERS = [
    {"value": "official", "label": "Official"},
    {"value": "cases", "label": "Cases"},
    {"value": "documents", "label": "Documents"},
    {"value": "congress", "label": "Congress"},
    {"value": "sightings", "label": "Sightings"},
    {"value": "research", "label": "Research"},
    {"value": "news", "label": "News"},
]


def generate_report(output_path: Path | None = None) -> Path:
    output_path = output_path or settings.output_dir / "report.html"
    init_db()
    db = SessionLocal()
    try:
        cutoff = date.today() - timedelta(days=settings.report_lookback_days)
        uap_sources = [SourceType.AARO_CASES, SourceType.AARO_RECORDS, SourceType.NARA_UAP, SourceType.NASA_UAP, SourceType.CONGRESS, SourceType.FEDERAL_REGISTER, SourceType.BLACK_VAULT, SourceType.NUFORC, SourceType.THE_DEBRIEF, SourceType.LIBERATION_TIMES, SourceType.GOOGLE_NEWS]
        rows = db.query(ExternalArticleEntry).filter(ExternalArticleEntry.status == GazetteStatus.ANALYZED).filter(ExternalArticleEntry.source.in_(uap_sources)).filter(ExternalArticleEntry.published_date >= cutoff).order_by(ExternalArticleEntry.published_date.desc()).all()
        entries = [_entry(row) for row in rows]
        _attach_blog_links(db, entries)
        cases = list_cases()
        if not entries:
            entries = _seed_case_entries(cases)
        ticker_items = build_ticker(entries, cases)
        timeline_events = [e["timeline_event"] for e in entries if e.get("timeline_event")][:8]
        generated = datetime.utcnow()
        seo = build_seo(generated)
        jsonld = build_jsonld(entries, seo, generated)
        env = Environment(loader=FileSystemLoader(str(Path(__file__).parent.parent / "templates")), autoescape=select_autoescape(["html", "xml"]))
        html = env.get_template("report.html.j2").render(entries=entries, ticker_items=ticker_items, timeline_events=timeline_events, cases=cases, filters=FILTERS, current_year=date.today().year, generated_at=generated.strftime("%Y-%m-%d %H:%M UTC"), seo=seo, jsonld=jsonld)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        try:
            from src.storage_remote import upload_report_html, supabase_storage_enabled
            if supabase_storage_enabled():
                upload_report_html(html)
        except Exception as exc:
            logger.warning("Supabase upload skipped/failed: %s", exc)
        return output_path
    finally:
        db.close()


def _entry(row):
    a = row.analysis_json or {}
    tags = set(a.get("topic_tags") or [])
    if a.get("case_names"):
        tags.add("cases")
    if a.get("evidence_level") in {"official_record", "official_analysis", "foia_document"}:
        tags.add("documents")
    if "congress" in " ".join(a.get("agency_tags") or []).lower() or row.source.value == "congress":
        tags.add("congress")
    if row.source.value == "nuforc":
        tags.add("sightings")
    if row.source.value in {"the_debrief", "liberation_times", "black_vault"}:
        tags.add("research")
    if row.source.value == "google_news":
        tags.add("news")
    if row.credibility and row.credibility.value == "official":
        tags.add("official")
    return {
        "id": f"item-{row.id}",
        "db_id": row.id,
        "headline": row.headline,
        "headline_short": a.get("headline_short") or row.headline[:82],
        "date_display": row.published_date.strftime("%B %d, %Y"),
        "published_date": row.published_date,
        "published_iso": datetime.combine(row.published_date, datetime.min.time(), tzinfo=timezone.utc).isoformat(),
        "source_url": row.source_url,
        "source_display": row.source_name or row.source.value.replace("_", " ").title(),
        "source_trust": a.get("source_trust", "news"),
        "evidence_level": a.get("evidence_level", "general_news"),
        "status": a.get("status", "background"),
        "confidence_label": a.get("confidence_label", "Source-labeled"),
        "case_names": a.get("case_names") or [],
        "agency_tags": a.get("agency_tags") or [],
        "takeaway": a.get("takeaway") or "Source-labeled UAP item.",
        "tags": " ".join(sorted(tags)),
        "relevance": a.get("relevance_score", 0),
        "timeline_event": a.get("timeline_event"),
        "slug": slugify(row.headline) + f"-{row.id}",
    }


def _attach_blog_links(db, entries):
    posts = {(p.source_table, p.source_id): p.slug for p in db.query(BlogPost).all()}
    for e in entries:
        e["blog_slug"] = posts.get(("external_articles", e["db_id"]))


def _seed_case_entries(cases):
    """Build homepage-ready records from curated case files when DB feed is empty."""
    entries = []
    today = date.today()
    for idx, case in enumerate(cases, start=1):
        grade = evidence_grade(case)
        is_resolved = case.get("status") == "resolved"
        evidence = case.get("evidence") or {}
        if evidence.get("official_resolution"):
            evidence_level = "official_analysis"
        elif evidence.get("official_record"):
            evidence_level = "official_record"
        else:
            evidence_level = "witness_report"
        status = case.get("status") or "under_review"
        tags = {"cases", "documents" if evidence.get("official_record") else "sightings"}
        if case.get("agencies") and "AARO" in case.get("agencies"):
            tags.add("official")
        entries.append({
            "id": f"case-{case['slug']}",
            "db_id": -idx,
            "headline": f"{case['title']} case file",
            "headline_short": f"{case['title']} - {status.replace('_', ' ').title()} Case File",
            "date_display": case.get("event_date") or "Case file",
            "published_date": today - timedelta(days=idx),
            "published_iso": datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc).isoformat(),
            "source_url": f"/cases/{case['slug']}",
            "source_display": "The UAP Index Case File",
            "source_trust": "official" if "AARO" in case.get("agencies", []) else "research",
            "evidence_level": evidence_level,
            "status": status,
            "confidence_label": grade["label"],
            "case_names": [case["title"]],
            "agency_tags": case.get("agencies") or [],
            "takeaway": (
                f"{case['official_explanation']} Public-record grade: {grade['score']}/100. "
                "This is a seeded case file so the homepage remains useful before the daily scraper has fresh analyzed records."
            ),
            "tags": " ".join(sorted(tags)),
            "relevance": grade["score"] // 10,
            "timeline_event": {"date_label": case.get("event_date") or "Case file", "title": case["title"], "note": status.replace("_", " "), "urgency": "ongoing", "css_class": "cal-positive" if is_resolved else "cal-urgent"},
            "slug": case["slug"],
            "blog_slug": None,
        })
    return entries


def build_ticker(entries, cases):
    official = sum(1 for e in entries if "official" in e["tags"])
    docs = sum(1 for e in entries if "documents" in e["tags"])
    congress = sum(1 for e in entries if "congress" in e["tags"])
    resolved = sum(1 for c in cases if c["status"] == "resolved")
    unresolved = sum(1 for c in cases if c["status"] != "resolved")
    return [
        {"label": "Official", "value": str(official), "note": "records"},
        {"label": "Documents", "value": str(docs), "note": "indexed"},
        {"label": "Congress", "value": str(congress), "note": "items"},
        {"label": "Cases", "value": f"{resolved}/{len(cases)}", "note": "resolved"},
        {"label": "Open", "value": str(unresolved), "note": "seeded cases"},
    ]


def build_seo(generated):
    base = settings.site_url.rstrip("/")
    return {"title": "The UAP Index - Daily UAP Briefing", "description": "Daily UAP briefing, case resolver, document finder, and claim checker for AARO, NARA, UFO and unidentified anomalous phenomena records.", "keywords": "UAP, UFO, AARO, NARA UAP, UAP documents, UAP cases, UFO claim checker, UAP disclosure", "canonical": f"{base}/", "site_name": settings.site_name, "site_url": base, "locale": settings.site_locale, "og_image": f"{base}/static/og-image.png", "og_type": "website", "published_iso": generated.replace(tzinfo=timezone.utc).isoformat(), "modified_iso": generated.replace(tzinfo=timezone.utc).isoformat()}


def build_jsonld(entries, seo, generated):
    return json.dumps({"@context": "https://schema.org", "@type": "NewsMediaOrganization", "name": settings.site_name, "url": seo["site_url"], "sameAs": [], "publishingPrinciples": f"{seo['site_url']}/sources"}, ensure_ascii=False)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:80] or "briefing"
