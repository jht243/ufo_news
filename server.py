from __future__ import annotations
import gzip, hmac, io, json, logging, time
from datetime import date, datetime, timezone
from pathlib import Path
import httpx
from flask import Flask, Response, abort, jsonify, request
from src.config import settings
from src.data.uap_cases import evidence_grade, get_case, list_cases, search_cases
from src.data.uap_library import (
    SEEDED_CLAIMS,
    SEEDED_DOCUMENTS,
    case_clusters,
    claims_for_case,
    documents_for_case,
    facets as library_facets,
    filter_claims,
    filter_documents,
    group_by,
    library_stats,
)
from src.data.uap_programs import group_programs, program_facets, program_stats, search_programs
from src.models import BlogPost, ExternalArticleEntry, GazetteStatus, SessionLocal, init_db
from src.page_renderer import _base_url, _env, seo_payload
from src.storage_remote import fetch_report_html, supabase_storage_enabled, supabase_storage_read_enabled, upload_report_html
logger = logging.getLogger(__name__)
_STATIC_DIR = Path(__file__).resolve().parent / "static"
_STATIC_DIR.mkdir(parents=True, exist_ok=True)
app = Flask(__name__, static_folder=str(_STATIC_DIR), static_url_path="/static")
BUTTONDOWN_API_URL = "https://api.buttondown.com/v1/subscribers"
_REPORT_CACHE = {"html": None, "fetched_at": 0.0}
_NAV_CACHE_PATHS = frozenset({"/briefing", "/tools", "/cases", "/documents", "/timeline", "/sources", "/explainers"})
_NAV_PAGE_CACHE = {}
EXPLAINERS = {
    "what-is-aaro": {"title": "What is AARO?", "summary": "The Defense Department office responsible for receiving, analyzing, and resolving UAP reports across domains.", "body": "AARO, the All-domain Anomaly Resolution Office, is the primary U.S. government office for UAP case intake and analysis. The UAP Index treats AARO releases as official records while still separating a released record from a complete public explanation."},
    "what-is-nara-uap-collection": {"title": "What is the NARA UAP Collection?", "summary": "The National Archives maintains Record Group 615 for UAP records transferred by agencies under the 2024 NDAA.", "body": "NARA's UAP collection creates a public archival lane for agency records. The Index tracks NARA pages as official records and uses them as source anchors for document discovery."},
    "how-to-read-uap-claims": {"title": "How to Read UAP Claims", "summary": "Separate official records, witness reports, research claims, media summaries, and unsupported viral interpretations.", "body": "A claim is only as strong as its source chain. The UAP Index labels each item by source type, evidence level, status, and unresolved gaps so readers can navigate without treating every mention as proof."},
}

CASE_HUB = {
    "kicker": "UAP case files hub",
    "intro": "Use this UAP cases hub to compare official case resolutions, unresolved UFO reports, AARO case files, public videos, source-backed claims, and original documents. The page is built as a navigation layer: start with the case directory, then move into claim checking, document filtering, evidence grading, or an individual case file.",
    "spokes": [
        {"title": "Resolved AARO UAP cases", "url": "/tools/uap-case-resolver?status=resolved", "summary": "Case files where an official public explanation is available, including GoFast, Puerto Rico Object, Mt. Etna, Western U.S. Objects, and Southeast Asia Triangles."},
        {"title": "UAP cases still under review", "url": "/tools/uap-case-resolver?status=under_review", "summary": "Open or partial public records such as Eglin, Gimbal, and South Asian Objects where the public evidence trail remains incomplete."},
        {"title": "UFO claim checker", "url": "/tools/uap-claim-checker", "summary": "Check claims about speed, altitude, transmedium movement, triangle formations, atmospheric wakes, and record releases against source-linked evidence."},
        {"title": "UAP evidence grader", "url": "/tools/uap-evidence-grader", "summary": "Compare cases by official record strength, video availability, multi-sensor context, official resolution, and source count."},
    ],
    "questions": [
        {"q": "What are the most documented UAP cases?", "a": "The strongest public records in this index are the cases with official AARO material, video or sensor context, and a public resolution document. GoFast, Puerto Rico Object, Mt. Etna, Al Taqaddum, Western U.S. Objects, and Southeast Asia Triangles currently have the most direct case-document trails."},
        {"q": "Which UAP cases are unresolved?", "a": "Unresolved or under-review entries include cases where no complete public explanation is available, where raw sensor context is limited, or where AARO has not published a final case-resolution report in the seeded record. Gimbal, Tic Tac / Nimitz, Eglin, and South Asian Objects are useful starting points."},
        {"q": "Does a resolved UAP case mean every question is closed?", "a": "No. A resolved status means an official public explanation exists in the indexed record. It does not mean every raw sensor file, witness statement, or chain-of-custody detail is public."},
        {"q": "How should I research a UFO case?", "a": "Start with the original document, then compare the claim being made, the official explanation, the unresolved questions, and the evidence grade. The case file links all of those pieces together."},
    ],
}

DOCUMENT_HUB = {
    "kicker": "UAP documents hub",
    "intro": "Use this UAP documents hub to find original UFO and UAP source material from AARO, NARA, NASA, official index pages, case-resolution PDFs, records-management guidance, and methodology sources. The document finder is designed for source inspection first: every card links outward to the original document or public agency page.",
    "spokes": [
        {"title": "AARO UAP case documents", "url": "/tools/uap-document-finder?source=aaro_cases", "summary": "Official case-resolution PDFs and index pages for GoFast, Puerto Rico Object, Mt. Etna, Al Taqaddum, Eglin, and other public AARO case files."},
        {"title": "NARA UAP records collection", "url": "/tools/uap-document-finder?source=nara_uap", "summary": "National Archives UAP collection pages, Record Group 615 references, and agency transfer guidance for federal UAP records."},
        {"title": "Official analysis documents", "url": "/tools/uap-document-finder?evidence=official_analysis", "summary": "Documents that interpret a case or method, including AARO case-resolution PDFs and NASA UAP study material."},
        {"title": "Documents by case", "url": "/tools/uap-document-finder?group=location", "summary": "Filter original records by case, location, year, agency, evidence level, and official status."},
    ],
    "questions": [
        {"q": "Where can I find official UAP documents?", "a": "Start with AARO case-resolution reports for individual cases, NARA Record Group 615 for the federal UAP records collection, and NASA UAP study material for methodology and data-quality context."},
        {"q": "What is the NARA UAP collection?", "a": "NARA maintains public UAP collection pages for records transferred by federal agencies under the 2024 NDAA framework. The collection is a records gateway, not a single complete case database."},
        {"q": "Are AARO case-resolution PDFs original documents?", "a": "Yes. In this index, AARO PDFs and official AARO source pages are treated as original public records because they come from the government office publishing the case analysis."},
        {"q": "How do I verify a UFO document claim?", "a": "Open the original document, identify the exact claim, then compare it with the case file and claim checker. The Index separates what is sourced from what remains interpretation or unresolved context."},
    ],
}


def _hub_jsonld(path: str, title: str, description: str, faqs: list[dict], items: list[dict]) -> str:
    base = _base_url()
    graph = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "description": description,
            "url": f"{base}{path}",
            "isPartOf": {"@type": "WebSite", "name": settings.site_name, "url": base},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in faqs
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": idx, "name": item["title"], "url": f"{base}{item['url']}"}
                for idx, item in enumerate(items, start=1)
            ],
        },
    ]
    return json.dumps(graph)

@app.after_request
def _gzip_response(response: Response) -> Response:
    try:
        if response.direct_passthrough or response.status_code < 200 or response.status_code >= 300 or "Content-Encoding" in response.headers:
            return response
        if "gzip" not in (request.headers.get("Accept-Encoding", "") or "").lower():
            return response
        if not (response.mimetype or "").startswith(("text/", "application/json", "application/xml")):
            return response
        data = response.get_data()
        if len(data) < 500:
            return response
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
            gz.write(data)
        response.set_data(buf.getvalue())
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(response.get_data()))
        response.headers["Vary"] = "Accept-Encoding"
    except Exception as exc:
        logger.warning("gzip skipped: %s", exc)
    return response

def _get_report_html() -> str | None:
    if supabase_storage_read_enabled():
        now = time.time()
        if _REPORT_CACHE["html"] and now - _REPORT_CACHE["fetched_at"] < 60:
            return _REPORT_CACHE["html"]
        html = fetch_report_html()
        if html:
            _REPORT_CACHE.update({"html": html, "fetched_at": now})
            return html
        if _REPORT_CACHE["html"]:
            return _REPORT_CACHE["html"]
    report = settings.output_dir / "report.html"
    return report.read_text(encoding="utf-8") if report.exists() else None

def _normalize(path: str) -> str:
    return (path or "/").rstrip("/") or "/"

@app.before_request
def _serve_nav_cache():
    if request.method != "GET" or request.query_string:
        return None
    path = _normalize(request.path)
    cached = _NAV_PAGE_CACHE.get(path)
    if path in _NAV_CACHE_PATHS and cached and time.time() - cached["at"] < 90:
        resp = Response(cached["body"], mimetype="text/html")
        resp.headers["X-Page-Cache"] = "HIT"
        return resp
    return None

@app.after_request
def _store_nav_cache(response: Response) -> Response:
    try:
        path = _normalize(request.path)
        if request.method == "GET" and not request.query_string and response.status_code == 200 and response.mimetype == "text/html" and path in _NAV_CACHE_PATHS:
            _NAV_PAGE_CACHE[path] = {"body": response.get_data(), "at": time.time()}
            response.headers["X-Page-Cache"] = "MISS"
    except Exception:
        pass
    return response

@app.route("/")
def index():
    html = _get_report_html()
    if not html:
        abort(503, description="Report not yet generated. Run python run_daily.py --report-only first.")
    return Response(html, mimetype="text/html")

@app.post("/admin/regen-report")
def admin_regen_report():
    if not settings.admin_token:
        return jsonify({"ok": False, "error": "ADMIN_TOKEN not configured"}), 503
    supplied = request.args.get("token") or request.headers.get("X-Admin-Token", "")
    if not hmac.compare_digest(supplied, settings.admin_token):
        return jsonify({"ok": False, "error": "Invalid token"}), 403
    from src.report_generator import generate_report
    out = generate_report()
    upload_status = "skipped"
    if supabase_storage_enabled():
        upload_report_html(out.read_text(encoding="utf-8"))
        upload_status = "uploaded"
    _REPORT_CACHE.update({"html": None, "fetched_at": 0.0})
    return jsonify({"ok": True, "path": str(out), "supabase_upload": upload_status})

@app.post("/api/subscribe")
def subscribe():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    if not email or "@" not in email:
        return jsonify({"ok": False, "error": "Valid email required"}), 400
    if not settings.buttondown_api_key:
        return jsonify({"ok": False, "error": "Newsletter signup is not configured"}), 503
    try:
        resp = httpx.post(BUTTONDOWN_API_URL, json={"email_address": email, "type": "regular"}, headers={"Authorization": f"Token {settings.buttondown_api_key}"}, timeout=15)
        return jsonify({"ok": resp.status_code in (200, 201, 409)})
    except Exception:
        return jsonify({"ok": False, "error": "Service unavailable"}), 503

def _recent_briefings(limit=6):
    init_db()
    db = SessionLocal()
    try:
        return db.query(BlogPost).order_by(BlogPost.published_date.desc(), BlogPost.created_at.desc()).limit(limit).all()
    finally:
        db.close()

def _articles(limit=80):
    init_db()
    db = SessionLocal()
    try:
        return db.query(ExternalArticleEntry).filter(ExternalArticleEntry.status == GazetteStatus.ANALYZED).order_by(ExternalArticleEntry.published_date.desc()).limit(limit).all()
    finally:
        db.close()

def _render(template, **ctx):
    ctx.setdefault("current_year", date.today().year)
    ctx.setdefault("recent_briefings", _recent_briefings())
    return Response(_env.get_template(template).render(**ctx), mimetype="text/html")

@app.route("/tools")
@app.route("/tools/")
def tools_index():
    stats = library_stats()
    tools = [
        {"url": "/tools/uap-claim-checker", "name": "UAP Claim Checker", "category": "Verification", "count": stats["claims"], "summary": "Browse claim cards by year, location, category, case, and status; each claim links back to original source documents."},
        {"url": "/tools/uap-case-resolver", "name": "UAP Case Resolver", "category": "Cases", "count": stats["cases"], "summary": "Resolve the case directory by status, region, source documents, videos, and unresolved gaps."},
        {"url": "/tools/uap-document-finder", "name": "UAP Document Finder", "category": "Documents", "count": stats["documents"], "summary": "Filter original AARO, NARA, NASA, and archive records by source, year, evidence level, agency, status, and case."},
        {"url": "/tools/uap-government-program-search", "name": "UAP Government Program Search", "category": "Programs", "count": program_stats()["total"], "summary": "Search known, active, proposed, disputed, and alleged government UFO/UAP programs with source labels and caveats."},
        {"url": "/tools/uap-evidence-grader", "name": "UAP Evidence Grader", "category": "Methodology", "count": stats["cases"], "summary": "Compare cases using a transparent public-record score and inspect which documents support the grade."},
    ]
    seo = seo_payload("/tools", "UAP Tools - Claim Checker, Case Resolver, Document Finder", "Free tools for browsing source-backed UAP claims, cases, original documents, and public evidence grades.", "UAP tools, UFO claim checker, UAP document finder")
    return _render("tools_index.html.j2", tools=tools, stats=stats, claim_groups=group_by(SEEDED_CLAIMS, "year"), doc_groups=group_by(SEEDED_DOCUMENTS, "source_name"), seo=seo)

@app.route("/tools/uap-government-program-search")
@app.route("/tools/uap-government-program-search/")
@app.route("/tools/government-uap-program-search")
@app.route("/tools/government-uap-program-search/")
@app.route("/tools/government-program-search")
@app.route("/tools/government-program-search/")
def tool_government_program_search():
    filters = {
        "q": request.args.get("q", "").strip(),
        "status": request.args.get("status", "").strip(),
        "agency": request.args.get("agency", "").strip(),
        "era": request.args.get("era", "").strip(),
        "source_strength": request.args.get("source_strength", "").strip(),
        "group": request.args.get("group", "era").strip() or "era",
    }
    programs = search_programs(q=filters["q"], status=filters["status"], agency=filters["agency"], era=filters["era"], source_strength=filters["source_strength"])
    group_key = filters["group"] if filters["group"] in {"era", "status", "agency", "source_strength"} else "era"
    seo = seo_payload(
        "/tools/uap-government-program-search",
        "UAP Government Program Search - UFO Programs, AARO, Blue Book, AATIP",
        "Search confirmed, active, proposed, disputed, and alleged U.S. government UFO and UAP programs including Project Blue Book, UAPTF, AARO, AAWSAP, AATIP, KONA BLUE, and Immaculate Constellation.",
        "UAP government programs, UFO programs, Project Blue Book, AATIP, AAWSAP, AARO, UAPTF, Immaculate Constellation, KONA BLUE, MJ-12",
    )
    jsonld = _hub_jsonld(
        "/tools/uap-government-program-search",
        seo["title"],
        seo["description"],
        [
            {"q": "What changed in 2021 for UAP programs?", "a": "The June 25, 2021 ODNI preliminary assessment publicly summarized UAPTF work and moved UAP from scattered military reporting into a formal intelligence and policy process that led to AOIMSG and AARO."},
            {"q": "Which U.S. government UFO programs are confirmed?", "a": "Confirmed programs and offices include Project Sign, Project Grudge, Project Blue Book, UAPTF, AOIMSG, AARO, the NASA UAP Independent Study Team, and the NARA UAP Records Collection."},
            {"q": "Are alleged programs like IMMACULATE CONSTELLATION confirmed?", "a": "No. This tool labels IMMACULATE CONSTELLATION as alleged and officially denied based on an ODNI FOIA release summarizing press allegations and DoD's denial."},
        ],
        [{"title": p["name"], "url": "/tools/uap-government-program-search"} for p in programs[:20]],
    )
    return _render("tools/government_program_search.html.j2", programs=programs, program_groups=group_programs(programs, group_key), facets=program_facets(), stats=program_stats(), filters=filters, group_key=group_key, seo=seo, jsonld=jsonld)

def _claim_results(query):
    cases = search_cases(query)[:8]
    q = (query or "").lower().strip()
    rows = []
    if q:
        for row in _articles(120):
            hay = f"{row.headline} {row.body_text or ''} {row.source_name or ''}".lower()
            if q in hay:
                rows.append(row)
                if len(rows) >= 12:
                    break
    return cases, rows

@app.route("/tools/uap-claim-checker")
@app.route("/tools/uap-claim-checker/")
def tool_claim_checker():
    q = request.args.get("q", "").strip()
    selected = {
        "year": request.args.get("year", "").strip(),
        "location": request.args.get("location", "").strip(),
        "status": request.args.get("status", "").strip(),
        "category": request.args.get("category", "").strip(),
        "case": request.args.get("case", "").strip(),
        "group": request.args.get("group", "year").strip() or "year",
    }
    claims = filter_claims(q=q, year=selected["year"], location=selected["location"], status=selected["status"], category=selected["category"], case_slug=selected["case"])
    cases, rows = _claim_results(q) if q else ([], [])
    group_key = selected["group"] if selected["group"] in {"year", "location", "category", "status"} else "year"
    seo = seo_payload("/tools/uap-claim-checker", "UAP Claim Checker - Source-Backed UFO and UAP Claims", "Browse UAP and UFO claims by year, location, category, status, and case with original source documents and what is actually sourced.", "UFO claim checker, UAP claim checker, AARO source checker")
    return _render("tools/claim_checker.html.j2", q=q, claims=claims, claim_groups=group_by(claims, group_key), group_key=group_key, facets=library_facets(), selected=selected, cases=cases, rows=rows, grades={c["slug"]: evidence_grade(c) for c in cases}, seo=seo)

@app.route("/tools/uap-case-resolver")
@app.route("/tools/uap-case-resolver/")
def tool_case_resolver():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    region = request.args.get("region", "").strip()
    cases = case_clusters()
    if q:
        allowed = {c["slug"] for c in search_cases(q)}
        cases = [c for c in cases if c["slug"] in allowed]
    if status:
        cases = [c for c in cases if c["status"] == status]
    if region:
        cases = [c for c in cases if c["region"] == region]
    seo = seo_payload("/tools/uap-case-resolver", "UAP Case Resolver - Official Status, Claims and Source Links", "Search UAP cases by name, status, region, source documents, official explanation, and unresolved questions.", "UAP cases, UFO case resolver, GoFast, Gimbal, Tic Tac")
    return _render("cases_index.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, q=q, selected={"status": status, "region": region}, facets=library_facets(), regions=sorted({c["region"] for c in case_clusters()}), seo=seo, tool_mode=True)

@app.route("/tools/uap-document-finder")
@app.route("/tools/uap-document-finder/")
def tool_document_finder():
    filters = {
        "q": request.args.get("q", "").strip(),
        "source": request.args.get("source", "").strip(),
        "evidence": request.args.get("evidence", "").strip(),
        "year": request.args.get("year", "").strip(),
        "agency": request.args.get("agency", "").strip(),
        "status": request.args.get("status", "").strip(),
        "case": request.args.get("case", "").strip(),
        "group": request.args.get("group", "source_name").strip() or "source_name",
    }
    docs = filter_documents(q=filters["q"], source=filters["source"], evidence=filters["evidence"], year=filters["year"], agency=filters["agency"], status=filters["status"], case_slug=filters["case"])
    scraped_rows = _articles(200)
    group_key = filters["group"] if filters["group"] in {"source_name", "year", "evidence_level", "status", "location"} else "source_name"
    seo = seo_payload("/tools/uap-document-finder", "UAP Document Finder - Original AARO, NARA, NASA and FOIA Sources", "Filter original UAP documents and source records by source, year, evidence type, agency, status, and case.", "UAP documents, AARO records, NARA UAP, UFO documents")
    return _render("documents.html.j2", docs=docs, doc_groups=group_by(docs, group_key), group_key=group_key, rows=scraped_rows, seo=seo, facets=library_facets(), filters=filters, tool_mode=True)

@app.route("/tools/uap-evidence-grader")
@app.route("/tools/uap-evidence-grader/")
def tool_evidence_grader():
    cases = case_clusters()
    seo = seo_payload("/tools/uap-evidence-grader", "UAP Evidence Grader - Compare Public Record Strength", "Compare UAP cases using a public evidence rubric built around official records, video, multiple sensors, official resolution, and original source count.", "UAP evidence, UFO evidence grading, UAP methodology")
    return _render("evidence_grader.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, seo=seo)

@app.route("/cases")
@app.route("/cases/")
def cases_index():
    cases = case_clusters()
    seo = seo_payload(
        "/cases",
        "UAP Cases - Official UFO Case Files, AARO Reports and Evidence",
        "Browse source-backed UAP cases, UFO case files, AARO case-resolution reports, public videos, unresolved questions, original documents, and evidence grades.",
        "UAP cases, UFO cases, AARO case resolution, GoFast UAP, Gimbal UFO, Tic Tac UAP, Puerto Rico object, UAP evidence",
    )
    jsonld = _hub_jsonld("/cases", seo["title"], seo["description"], CASE_HUB["questions"], [{"title": c["title"], "url": f"/cases/{c['slug']}"} for c in cases])
    return _render("cases_index.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, q="", selected={}, facets=library_facets(), regions=sorted({c["region"] for c in cases}), seo=seo, jsonld=jsonld, hub=CASE_HUB, tool_mode=False)

@app.route("/cases/<slug>")
@app.route("/cases/<slug>/")
def case_detail(slug):
    case = get_case(slug)
    if not case:
        abort(404)
    seo = seo_payload(f"/cases/{slug}", f"{case['title']} - UAP Case File", f"Source-backed UAP case file for {case['title']}: status, official explanation, unresolved questions, and public evidence grade.", f"{case['title']}, UAP case, UFO case")
    related = [r for r in _articles(80) if case["title"].lower() in f"{r.headline} {r.body_text or ''}".lower()]
    return _render("case_detail.html.j2", case=case, grade=evidence_grade(case), claims=claims_for_case(slug), documents=documents_for_case(slug), related=related, seo=seo)

@app.route("/documents")
@app.route("/documents/")
def documents_index():
    docs = filter_documents()
    seo = seo_payload(
        "/documents",
        "UAP Documents - Original AARO, NARA, NASA and UFO Records",
        "Find original UAP documents, UFO records, AARO case-resolution PDFs, NARA UAP collection pages, NASA UAP study material, and source-linked case records.",
        "UAP documents, UFO documents, AARO records, NARA UAP, UAP records collection, UFO files, AARO case reports",
    )
    jsonld = _hub_jsonld("/documents", seo["title"], seo["description"], DOCUMENT_HUB["questions"], [{"title": d["title"], "url": "/tools/uap-document-finder"} for d in docs[:12]])
    return _render("documents.html.j2", docs=docs, doc_groups=group_by(docs, "source_name"), group_key="source_name", rows=_articles(200), seo=seo, jsonld=jsonld, filters={}, facets=library_facets(), hub=DOCUMENT_HUB, tool_mode=False)

@app.route("/timeline")
@app.route("/timeline/")
def timeline():
    events = []
    for r in _articles(200):
        ev = (r.analysis_json or {}).get("timeline_event")
        if ev:
            ev = dict(ev); ev["source_url"] = r.source_url; ev["source_name"] = r.source_name; events.append(ev)
    for c in list_cases():
        events.append({"date_label": c["event_date"], "title": c["title"], "note": c["status"].replace("_", " "), "source_url": f"/cases/{c['slug']}", "source_name": "Case file"})
    seo = seo_payload("/timeline", "UAP Timeline - Cases, Hearings, Reports and Releases", "A source-linked UAP timeline covering known cases, official reports, hearings, document releases, and indexed source updates.", "UAP timeline, UFO timeline, AARO timeline")
    return _render("timeline.html.j2", events=events, seo=seo)

@app.route("/sources")
@app.route("/sources/")
def sources():
    seo = seo_payload("/sources", "Sources and Methodology - The UAP Index", "How The UAP Index labels sources, confidence, evidence levels, official records, FOIA archives, witness reports, research outlets, and news.", "UAP sources, UFO methodology, AARO NARA sources")
    return _render("sources.html.j2", seo=seo)

@app.route("/explainers")
@app.route("/explainers/")
def explainers_index():
    seo = seo_payload("/explainers", "UAP Explainers - AARO, NARA, Claims and Evidence", "Plain-English guides for UAP records, official agencies, claims, evidence levels, and disclosure terminology.", "UAP explainers, UFO explainers, AARO explained")
    return _render("explainers_index.html.j2", explainers=EXPLAINERS, seo=seo)

@app.route("/explainers/<slug>")
@app.route("/explainers/<slug>/")
def explainer(slug):
    page = EXPLAINERS.get(slug)
    if not page:
        abort(404)
    seo = seo_payload(f"/explainers/{slug}", page["title"], page["summary"], "UAP, UFO, AARO, NARA")
    return _render("explainer.html.j2", page=page, seo=seo)

@app.route("/briefing")
@app.route("/briefing/")
def briefing_index():
    seo = seo_payload("/briefing", "UAP Briefings - The UAP Index", "Source-labeled UAP briefings from official records, FOIA archives, witness databases, research outlets, and news.", "UAP briefing, UFO news, AARO updates")
    return _render("blog_index.html.j2", posts=_recent_briefings(40), seo=seo)

@app.route("/briefing/<slug>")
@app.route("/briefing/<slug>/")
def briefing_post(slug):
    init_db(); db = SessionLocal()
    try:
        post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
        if not post:
            abort(404)
        seo = seo_payload(f"/briefing/{slug}", post.title, post.summary or post.subtitle or "UAP source briefing from The UAP Index.", "UAP briefing, UFO news, AARO")
        return _render("blog_post.html.j2", post=post, seo=seo)
    finally:
        db.close()

@app.route("/robots.txt")
def robots_txt():
    base = _base_url()
    return Response(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\nSitemap: {base}/news-sitemap.xml\n", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap_xml():
    base = _base_url()
    urls = ["/", "/tools", "/tools/uap-claim-checker", "/tools/uap-case-resolver", "/tools/uap-document-finder", "/tools/uap-government-program-search", "/tools/uap-evidence-grader", "/cases", "/documents", "/timeline", "/sources", "/explainers", "/briefing"]
    urls += [f"/cases/{c['slug']}" for c in list_cases()]
    urls += [f"/explainers/{s}" for s in EXPLAINERS]
    urls += [f"/briefing/{p.slug}" for p in _recent_briefings(100)]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append(f"<url><loc>{base}{u}</loc><changefreq>daily</changefreq></url>")
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")

@app.route("/news-sitemap.xml")
def news_sitemap_xml():
    base = _base_url(); posts = _recent_briefings(100)
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for p in posts:
        pub = datetime.combine(p.published_date, datetime.min.time(), tzinfo=timezone.utc).isoformat()
        body.append(f"<url><loc>{base}/briefing/{p.slug}</loc><news:news><news:publication><news:name>{settings.site_name}</news:name><news:language>en</news:language></news:publication><news:publication_date>{pub}</news:publication_date><news:title>{_xml(p.title)}</news:title></news:news></url>")
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")

def _xml(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

@app.route("/<key>.txt")
def indexnow_key_file(key):
    if key == settings.indexnow_key:
        return Response(key, mimetype="text/plain")
    abort(404)

@app.route("/health")
def health():
    return jsonify({"ok": True, "site": settings.site_name, "supabase_read": supabase_storage_read_enabled(), "supabase_write": supabase_storage_enabled()})

@app.errorhandler(404)
def not_found(exc):
    return _render("404.html.j2", seo=seo_payload("/404", "Page not found - The UAP Index", "The requested UAP Index page was not found.")), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.server_port)
