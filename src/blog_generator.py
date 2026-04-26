from __future__ import annotations

import html
import re
from datetime import date, timedelta

from src.config import settings
from src.models import SessionLocal, ExternalArticleEntry, BlogPost, GazetteStatus, init_db


def run_blog_generation() -> dict:
    init_db()
    db = SessionLocal()
    made = 0
    try:
        cutoff = date.today() - timedelta(days=settings.blog_gen_lookback_days)
        rows = db.query(ExternalArticleEntry).filter(ExternalArticleEntry.status == GazetteStatus.ANALYZED).filter(ExternalArticleEntry.published_date >= cutoff).order_by(ExternalArticleEntry.published_date.desc()).limit(settings.blog_gen_budget_per_run * 3).all()
        for row in rows:
            if made >= settings.blog_gen_budget_per_run:
                break
            exists = db.query(BlogPost).filter(BlogPost.source_table == "external_articles", BlogPost.source_id == row.id).first()
            score = (row.analysis_json or {}).get("relevance_score", 0)
            if exists or score < settings.blog_gen_min_relevance:
                continue
            post = _post_from_row(row)
            db.add(post)
            made += 1
        db.commit()
        return {"created": made, "skipped": max(0, len(rows) - made)}
    finally:
        db.close()


def _post_from_row(row):
    analysis = row.analysis_json or {}
    title = analysis.get("headline_short") or row.headline
    body = f"""
<p>{html.escape(analysis.get('takeaway') or 'This item was added to The UAP Index from a source-labeled record.')}</p>
<p>The source is <strong>{html.escape(row.source_name or row.source.value)}</strong>. The current evidence label is <strong>{html.escape(analysis.get('evidence_level', 'general_news').replace('_', ' '))}</strong>, and the status is <strong>{html.escape(analysis.get('status', 'background').replace('_', ' '))}</strong>.</p>
<p>Use this briefing as a navigation aid back to the primary material. A mention, claim, or sighting report is not treated as proof beyond the linked source record.</p>
""".strip()
    words = len(re.findall(r"\w+", body))
    return BlogPost(
        source_table="external_articles",
        source_id=row.id,
        slug=slugify(title) + f"-{row.id}",
        title=title,
        subtitle=analysis.get("confidence_label"),
        summary=analysis.get("takeaway"),
        body_html=body,
        social_hook=analysis.get("takeaway"),
        primary_sector=analysis.get("evidence_level"),
        sectors_json=analysis.get("topic_tags") or [],
        keywords_json=(analysis.get("case_names") or []) + (analysis.get("agency_tags") or []),
        takeaways_json=[analysis.get("confidence_label"), f"Status: {analysis.get('status', 'background').replace('_', ' ')}", f"Evidence: {analysis.get('evidence_level', 'general_news').replace('_', ' ')}"],
        word_count=words,
        reading_minutes=max(1, round(words / 220)),
        published_date=row.published_date,
        canonical_source_url=row.source_url,
        llm_model="rule-based-v1",
        llm_cost_usd=0.0,
    )


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:80] or "briefing"
