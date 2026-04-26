from __future__ import annotations

import logging
import re
from datetime import date, timedelta

from src.config import settings
from src.models import SessionLocal, ExternalArticleEntry, GazetteStatus, SourceType, CredibilityTier

logger = logging.getLogger(__name__)

OFFICIAL = {SourceType.AARO_CASES, SourceType.AARO_RECORDS, SourceType.NARA_UAP, SourceType.NASA_UAP, SourceType.CONGRESS, SourceType.FEDERAL_REGISTER}
RESEARCH = {SourceType.BLACK_VAULT, SourceType.THE_DEBRIEF, SourceType.LIBERATION_TIMES}
CASE_KEYWORDS = {
    "gofast": "GoFast", "go fast": "GoFast", "gimbal": "Gimbal", "tic tac": "Tic Tac", "nimitz": "Tic Tac",
    "puerto rico": "Puerto Rico Object", "eglin": "Eglin", "al taqaddum": "Al Taqaddum", "western": "Western U.S. Objects",
    "etna": "Mt. Etna", "triangle": "Southeast Asia Triangles",
}
AGENCY_KEYWORDS = ("aaro", "nara", "nasa", "dod", "pentagon", "congress", "navy", "faa", "dni", "odNI")
TOPIC_KEYWORDS = ("uap", "ufo", "aaro", "nara", "congress", "hearing", "disclosure", "foia", "sighting", "video", "sensor", "case")


def run_analysis() -> dict:
    init_summary = {"analyzed": 0, "skipped": 0, "errors": 0}
    db = SessionLocal()
    try:
        cutoff = date.today() - timedelta(days=settings.report_lookback_days)
        rows = db.query(ExternalArticleEntry).filter(ExternalArticleEntry.status == GazetteStatus.SCRAPED).filter(ExternalArticleEntry.published_date >= cutoff).all()
        for row in rows:
            try:
                row.analysis_json = analyze_row(row)
                row.status = GazetteStatus.ANALYZED
                init_summary["analyzed"] += 1
            except Exception as exc:
                logger.exception("analysis failed for %s", row.id)
                init_summary["errors"] += 1
        db.commit()
    finally:
        db.close()
    return init_summary


def analyze_row(row: ExternalArticleEntry) -> dict:
    text = f"{row.headline} {row.body_text or ''}".lower()
    source = row.source
    case_names = sorted({label for key, label in CASE_KEYWORDS.items() if key in text})
    agencies = sorted({a.upper() for a in AGENCY_KEYWORDS if a.lower() in text})
    topics = sorted({t for t in TOPIC_KEYWORDS if t in text}) or ["uap"]
    if source in OFFICIAL:
        evidence_level = "official_record"
        source_trust = "official"
        base_score = 8
    elif source == SourceType.NUFORC:
        evidence_level = "witness_report"
        source_trust = "witness"
        base_score = 5
    elif source in RESEARCH:
        evidence_level = "foia_document" if source == SourceType.BLACK_VAULT else "research_outlet"
        source_trust = "research"
        base_score = 6
    else:
        evidence_level = "general_news"
        source_trust = "news"
        base_score = 5
    if case_names:
        base_score += 1
    if any(w in text for w in ("resolved", "resolution", "identified", "balloon", "aircraft")):
        status = "resolved"
    elif any(w in text for w in ("hearing", "bill", "amendment", "congress")):
        status = "official_release" if source in OFFICIAL else "media_report"
    elif source == SourceType.NUFORC:
        status = "witness_report"
    elif source in OFFICIAL:
        status = "official_release"
    elif source in RESEARCH:
        status = "contested" if "flaw" in text or "critic" in text else "under_review"
    else:
        status = "media_report"
    confidence = {
        "official_record": "Primary-source record",
        "official_analysis": "Official analysis",
        "foia_document": "FOIA/source archive",
        "hearing_testimony": "Hearing testimony",
        "witness_report": "Witness report",
        "research_outlet": "Research outlet",
        "general_news": "General news report",
    }.get(evidence_level, "Source-labeled")
    return {
        "relevance_score": min(base_score, 10),
        "topic_tags": topics,
        "case_names": case_names,
        "agency_tags": agencies,
        "evidence_level": evidence_level,
        "status": status,
        "confidence_label": confidence,
        "headline_short": shorten(row.headline, 82),
        "takeaway": build_takeaway(row, evidence_level, status, case_names),
        "source_trust": source_trust,
        "timeline_event": timeline_event(row, status),
    }


def shorten(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "..."


def build_takeaway(row, evidence_level: str, status: str, cases: list[str]) -> str:
    case_part = f" It is tied to {', '.join(cases)}." if cases else ""
    return f"This item is indexed as {evidence_level.replace('_', ' ')} with status {status.replace('_', ' ')}.{case_part} Read it as a source-labeled record, not as proof beyond the linked material."


def timeline_event(row, status: str):
    if status in {"official_release", "resolved", "under_review"}:
        return {"date_label": row.published_date.isoformat(), "title": shorten(row.headline, 70), "note": status.replace("_", " "), "urgency": "dated", "css_class": ""}
    return None
