from __future__ import annotations

import enum
from datetime import datetime, date
from threading import Lock

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, Date, DateTime,
    Enum, Boolean, JSON, LargeBinary, UniqueConstraint, text as sa_text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings

Base = declarative_base()
_engine = None
_SessionLocal = None
_init_lock = Lock()


def _snake_case(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def _enum_values(enum_cls):
    return Enum(enum_cls, values_callable=lambda x: [e.value for e in x], name=_snake_case(enum_cls.__name__), native_enum=False)


class SourceType(str, enum.Enum):
    AARO_CASES = "aaro_cases"
    AARO_RECORDS = "aaro_records"
    NARA_UAP = "nara_uap"
    NASA_UAP = "nasa_uap"
    CONGRESS = "congress"
    FEDERAL_REGISTER = "federal_register"
    BLACK_VAULT = "black_vault"
    NUFORC = "nuforc"
    THE_DEBRIEF = "the_debrief"
    LIBERATION_TIMES = "liberation_times"
    GOOGLE_NEWS = "google_news"


class CredibilityTier(str, enum.Enum):
    OFFICIAL = "official"
    FOIA = "foia"
    RESEARCH = "research"
    WITNESS = "witness"
    NEWS = "news"


class GazetteStatus(str, enum.Enum):
    SCRAPED = "scraped"
    ANALYZED = "analyzed"
    APPROVED = "approved"
    SENT = "sent"


class ExternalArticleEntry(Base):
    __tablename__ = "external_articles"
    __table_args__ = (UniqueConstraint("source", "source_url", name="uq_ext_source_url"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(_enum_values(SourceType), nullable=False, index=True)
    source_url = Column(String(1000), nullable=False)
    source_name = Column(String(200), nullable=True)
    credibility = Column(_enum_values(CredibilityTier), default=CredibilityTier.NEWS)
    headline = Column(Text, nullable=False)
    published_date = Column(Date, nullable=False, index=True)
    body_text = Column(Text, nullable=True)
    article_type = Column(String(100), nullable=True)
    tone_score = Column(Float, nullable=True)
    extra_metadata = Column(JSON, nullable=True)
    analysis_json = Column(JSON, nullable=True)
    status = Column(_enum_values(GazetteStatus), default=GazetteStatus.SCRAPED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BlogPost(Base):
    __tablename__ = "blog_posts"
    __table_args__ = (UniqueConstraint("source_table", "source_id", name="uq_blog_source"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_table = Column(String(50), nullable=False, index=True)
    source_id = Column(Integer, nullable=False, index=True)
    slug = Column(String(220), nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    subtitle = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    body_html = Column(Text, nullable=False)
    social_hook = Column(Text, nullable=True)
    og_image_bytes = Column(LargeBinary, nullable=True)
    primary_sector = Column(String(80), nullable=True, index=True)
    sectors_json = Column(JSON, nullable=True)
    keywords_json = Column(JSON, nullable=True)
    related_slugs_json = Column(JSON, nullable=True)
    takeaways_json = Column(JSON, nullable=True)
    word_count = Column(Integer, nullable=True)
    reading_minutes = Column(Integer, nullable=True)
    published_date = Column(Date, nullable=False, index=True)
    canonical_source_url = Column(String(1000), nullable=True)
    llm_model = Column(String(100), nullable=True)
    llm_input_tokens = Column(Integer, nullable=True)
    llm_output_tokens = Column(Integer, nullable=True)
    llm_cost_usd = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LandingPage(Base):
    __tablename__ = "landing_pages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_key = Column(String(120), nullable=False, unique=True, index=True)
    page_type = Column(String(40), nullable=False, index=True)
    title = Column(Text, nullable=False)
    subtitle = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    body_html = Column(Text, nullable=False)
    canonical_path = Column(String(300), nullable=False, unique=True)
    keywords_json = Column(JSON, nullable=True)
    llm_model = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(100), nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    success = Column(Boolean, default=False)
    items_found = Column(Integer, default=0)
    items_new = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_engine():
    global _engine
    if _engine is None:
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


class _SessionProxy:
    def __call__(self):
        return get_session_local()()


SessionLocal = _SessionProxy()


def init_db():
    with _init_lock:
        Base.metadata.create_all(bind=get_engine())
        if settings.database_url.startswith("sqlite"):
            with get_engine().connect() as conn:
                conn.execute(sa_text("PRAGMA journal_mode=WAL"))
                conn.commit()
