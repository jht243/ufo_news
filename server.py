from __future__ import annotations
import gzip, hmac, io, logging, time
from datetime import date, datetime, timezone
from pathlib import Path
import httpx
from flask import Flask, Response, abort, jsonify, request
from src.config import settings
from src.data.uap_cases import evidence_grade, get_case, list_cases, search_cases
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
    tools = [
        {"url": "/tools/uap-claim-checker", "name": "UAP Claim Checker", "category": "Verification", "summary": "Paste a claim, case name, witness, or video title and see source-backed matches with confidence labels."},
        {"url": "/tools/uap-case-resolver", "name": "UAP Case Resolver", "category": "Cases", "summary": "Browse known UAP cases by status, agency, location, official explanation, and unresolved questions."},
        {"url": "/tools/uap-document-finder", "name": "UAP Document Finder", "category": "Documents", "summary": "Filter indexed AARO, NARA, NASA, Congress, FOIA, research, witness, and news records."},
        {"url": "/tools/uap-evidence-grader", "name": "UAP Evidence Grader", "category": "Methodology", "summary": "Compare cases using a transparent public-record score: official source, video, multiple sensors, and official resolution."},
    ]
    seo = seo_payload("/tools", "UAP Tools - Claim Checker, Case Resolver, Document Finder", "Free tools for checking UAP claims, resolving cases, finding documents, and grading public evidence.", "UAP tools, UFO claim checker, UAP document finder")
    return _render("tools_index.html.j2", tools=tools, seo=seo)

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
    cases, rows = _claim_results(q)
    seo = seo_payload("/tools/uap-claim-checker", "UAP Claim Checker - Check UFO Claims Against Sources", "Paste a UAP or UFO claim and see matching cases, records, source type, confidence labels, and what is actually sourced.", "UFO claim checker, UAP claim checker, AARO source checker")
    return _render("tools/claim_checker.html.j2", q=q, cases=cases, rows=rows, grades={c["slug"]: evidence_grade(c) for c in cases}, seo=seo)

@app.route("/tools/uap-case-resolver")
@app.route("/tools/uap-case-resolver/")
def tool_case_resolver():
    q = request.args.get("q", "").strip()
    cases = search_cases(q)
    seo = seo_payload("/tools/uap-case-resolver", "UAP Case Resolver - Official Status and Source Links", "Search UAP cases by name, alias, agency, status, official explanation, and unresolved questions.", "UAP cases, UFO case resolver, GoFast, Gimbal, Tic Tac")
    return _render("cases_index.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, q=q, seo=seo, tool_mode=True)

@app.route("/tools/uap-document-finder")
@app.route("/tools/uap-document-finder/")
def tool_document_finder():
    source = request.args.get("source", "").strip()
    evidence = request.args.get("evidence", "").strip()
    year = request.args.get("year", "").strip()
    rows = _articles(200)
    if source:
        rows = [r for r in rows if r.source.value == source]
    if evidence:
        rows = [r for r in rows if (r.analysis_json or {}).get("evidence_level") == evidence]
    if year:
        rows = [r for r in rows if str(r.published_date.year) == year]
    seo = seo_payload("/tools/uap-document-finder", "UAP Document Finder - Search AARO, NARA, FOIA and News", "Filter UAP documents and source records by source, year, evidence type, agency, status, and case.", "UAP documents, AARO records, NARA UAP, UFO documents")
    return _render("documents.html.j2", rows=rows, seo=seo, filters={"source": source, "evidence": evidence, "year": year}, tool_mode=True)

@app.route("/tools/uap-evidence-grader")
@app.route("/tools/uap-evidence-grader/")
def tool_evidence_grader():
    cases = list_cases()
    seo = seo_payload("/tools/uap-evidence-grader", "UAP Evidence Grader - Compare Public Record Strength", "Compare UAP cases using a public evidence rubric built around official records, video, multiple sensors, and official resolution.", "UAP evidence, UFO evidence grading, UAP methodology")
    return _render("evidence_grader.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, seo=seo)

@app.route("/cases")
@app.route("/cases/")
def cases_index():
    cases = list_cases()
    seo = seo_payload("/cases", "UAP Cases - Resolved, Unresolved, and Under Review", "Browse UAP cases with aliases, agencies, official explanations, unresolved questions, source links, and evidence grades.", "UAP cases, UFO cases, AARO case resolution")
    return _render("cases_index.html.j2", cases=cases, grades={c["slug"]: evidence_grade(c) for c in cases}, q="", seo=seo, tool_mode=False)

@app.route("/cases/<slug>")
@app.route("/cases/<slug>/")
def case_detail(slug):
    case = get_case(slug)
    if not case:
        abort(404)
    seo = seo_payload(f"/cases/{slug}", f"{case['title']} - UAP Case File", f"Source-backed UAP case file for {case['title']}: status, official explanation, unresolved questions, and public evidence grade.", f"{case['title']}, UAP case, UFO case")
    related = [r for r in _articles(80) if case["title"].lower() in f"{r.headline} {r.body_text or ''}".lower()]
    return _render("case_detail.html.j2", case=case, grade=evidence_grade(case), related=related, seo=seo)

@app.route("/documents")
@app.route("/documents/")
def documents_index():
    seo = seo_payload("/documents", "UAP Documents - AARO, NARA, NASA, Congress and FOIA", "Browse indexed UAP documents and source records from official agencies, FOIA archives, research outlets, witness databases, and news.", "UAP documents, NARA UAP, AARO records")
    return _render("documents.html.j2", rows=_articles(200), seo=seo, filters={}, tool_mode=False)

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
    urls = ["/", "/tools", "/tools/uap-claim-checker", "/tools/uap-case-resolver", "/tools/uap-document-finder", "/tools/uap-evidence-grader", "/cases", "/documents", "/timeline", "/sources", "/explainers", "/briefing"]
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
