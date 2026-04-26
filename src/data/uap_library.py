from __future__ import annotations

from collections import defaultdict
from datetime import date

from src.data.uap_cases import evidence_grade, list_cases


AARO_CASE_PAGE = "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"
NARA_RG_615 = "https://www.archives.gov/research/topics/uaps/rg-615"
NARA_UAP = "https://www.archives.gov/research/topics/uaps"
NARA_GUIDANCE = "https://www.archives.gov/records-mgmt/uap-guidance"
NASA_UAP = "https://science.nasa.gov/uap/"

SEEDED_DOCUMENTS: list[dict] = [
    {
        "id": "aaro-gofast-resolution",
        "title": "AARO GoFast Case Resolution and Card Methodology",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2025,
        "date_label": "February 6, 2025",
        "location": "Eastern coast of Florida",
        "case_slugs": ["gofast"],
        "claim_ids": ["gofast-high-speed", "gofast-near-ocean"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/AARO_GoFast_Case_Resolution_Card_Methodology_Final.pdf",
        "summary": "AARO states that GoFast did not demonstrate anomalous performance characteristics and estimates the object at approximately 13,000 feet, moving within a wind-adjusted speed range.",
        "topics": ["speed", "altitude", "parallax", "video"],
    },
    {
        "id": "aaro-puerto-rico-resolution",
        "title": "AARO Puerto Rico Object Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2025,
        "date_label": "March 20, 2025",
        "location": "Aguadilla, Puerto Rico",
        "case_slugs": ["puerto-rico-object"],
        "claim_ids": ["puerto-rico-transmedium", "puerto-rico-splitting"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/AARO_Puerto_Rico_UAP_Case_Resolution.pdf",
        "summary": "AARO assesses the objects did not demonstrate anomalous behavior or transmedium capability and gives a moderate-confidence sky-lantern explanation.",
        "topics": ["transmedium", "infrared", "sky lantern", "video"],
    },
    {
        "id": "aaro-mt-etna-resolution",
        "title": "AARO Mt. Etna Object Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2025,
        "date_label": "April 28, 2025",
        "location": "Mediterranean Sea south of Sicily",
        "case_slugs": ["mt-etna"],
        "claim_ids": ["etna-high-speed-plume"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/Mt-Etna-Object.pdf",
        "summary": "AARO assesses with high confidence that the object did not exhibit anomalous behavior and with moderate confidence that it was a balloon affected by sensor and atmospheric limitations.",
        "topics": ["volcano", "plume", "sensor limitations", "balloon"],
    },
    {
        "id": "aaro-al-taqaddum-resolution",
        "title": "AARO Al Taqaddum Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2025,
        "date_label": "September 8, 2025",
        "location": "Al Taqaddum Air Base, Iraq",
        "case_slugs": ["al-taqaddum"],
        "claim_ids": ["al-taqaddum-floating-object"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/AARO_Al_Taqaddam_Case_Resolution_Final.pdf",
        "summary": "AARO assesses with high confidence that the object was consistent with a cluster of fully and partially inflated balloons and did not exhibit anomalous behavior.",
        "topics": ["balloon", "infrared", "Iraq", "video"],
    },
    {
        "id": "aaro-eglin-resolution",
        "title": "AARO Eglin UAP Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2024,
        "date_label": "2024",
        "location": "Eglin Air Force Base area",
        "case_slugs": ["eglin"],
        "claim_ids": ["eglin-range-incursion"],
        "evidence_level": "official_analysis",
        "status": "under_review",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/Case_Resolution_of_Eglin_UAP_2_508_.pdf",
        "summary": "AARO describes a military pilot report connected to a possible flight-safety hazard and range incursion; public context remains limited.",
        "topics": ["flight safety", "range incursion", "pilot report"],
    },
    {
        "id": "aaro-atmospheric-wakes-resolution",
        "title": "AARO Atmospheric Wakes Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2024,
        "date_label": "February 26, 2024",
        "location": "Middle East and South Asia reporting areas",
        "case_slugs": ["south-asian-objects"],
        "claim_ids": ["south-asian-atmospheric-wake"],
        "evidence_level": "official_analysis",
        "status": "under_review",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/Case_Resolution_of_Atmospheric_Wakes_508-02262024.pdf",
        "summary": "AARO groups several mission reports involving possible atmospheric-wake signatures and public video clips from South Asian objects.",
        "topics": ["atmospheric wake", "propulsion signature", "video"],
    },
    {
        "id": "aaro-southeast-asia-triangles-resolution",
        "title": "AARO Southeast Asia Triangles Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2024,
        "date_label": "February 26, 2024",
        "location": "Southeast Asia",
        "case_slugs": ["southeast-asia-triangles"],
        "claim_ids": ["southeast-asia-triangle-formation"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/Case_Resolution_of_Southeast_Asia_Triangles_508-02262024.pdf",
        "summary": "AARO reviews six triangular objects in formation that were initially flagged as anomalous and potentially hazardous to navigation.",
        "topics": ["triangle", "formation", "navigation"],
    },
    {
        "id": "aaro-western-us-resolution",
        "title": "AARO Western United States UAP Case Resolution",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2024,
        "date_label": "February 26, 2024",
        "location": "Western United States military range",
        "case_slugs": ["western-us-objects"],
        "claim_ids": ["western-us-lights"],
        "evidence_level": "official_analysis",
        "status": "resolved",
        "document_type": "Case resolution PDF",
        "url": "https://www.aaro.mil/Portals/136/PDFs/case_resolution_reports/Case_Resolution_of_Western_United_States_Uap_508-02262024.pdf",
        "summary": "AARO addresses equidistant lights reported as a possible restricted-airspace incursion and assesses them in relation to commercial aircraft tracks.",
        "topics": ["lights", "restricted airspace", "aircraft"],
    },
    {
        "id": "aaro-case-resolution-index",
        "title": "AARO UAP Case Resolution Reports Index",
        "source": "aaro_cases",
        "source_name": "AARO",
        "agency": "AARO / U.S. Department of Defense",
        "year": 2025,
        "date_label": "Updated source page",
        "location": "United States / global reporting areas",
        "case_slugs": ["gofast", "puerto-rico-object", "mt-etna", "al-taqaddum", "eglin", "south-asian-objects", "southeast-asia-triangles", "western-us-objects"],
        "claim_ids": [],
        "evidence_level": "official_record",
        "status": "background",
        "document_type": "Official index page",
        "url": AARO_CASE_PAGE,
        "summary": "AARO source page listing public UAP case-resolution reports and linked video products.",
        "topics": ["case index", "official records", "videos"],
    },
    {
        "id": "nara-rg-615",
        "title": "NARA Record Group 615: Unidentified Anomalous Phenomena Records Collection",
        "source": "nara_uap",
        "source_name": "National Archives",
        "agency": "NARA",
        "year": 2025,
        "date_label": "2025",
        "location": "United States",
        "case_slugs": [],
        "claim_ids": ["nara-uap-collection"],
        "evidence_level": "official_record",
        "status": "official_release",
        "document_type": "Archive collection page",
        "url": NARA_RG_615,
        "summary": "NARA's public collection page for UAP records transferred by federal agencies under the 2024 NDAA framework.",
        "topics": ["NARA", "records collection", "RG 615", "disclosure"],
    },
    {
        "id": "nara-uap-topic",
        "title": "NARA Records Related to UFOs and UAPs",
        "source": "nara_uap",
        "source_name": "National Archives",
        "agency": "NARA",
        "year": 2025,
        "date_label": "2025",
        "location": "United States",
        "case_slugs": [],
        "claim_ids": ["nara-uap-collection"],
        "evidence_level": "official_record",
        "status": "background",
        "document_type": "Research guide",
        "url": NARA_UAP,
        "summary": "NARA guide to UFO and UAP-related records across Record Group 615 and other archival collections.",
        "topics": ["NARA", "research guide", "records"],
    },
    {
        "id": "nara-agency-guidance",
        "title": "NARA Guidance to Federal Agencies on UAP Records Collection",
        "source": "nara_uap",
        "source_name": "National Archives",
        "agency": "NARA",
        "year": 2024,
        "date_label": "2024",
        "location": "United States",
        "case_slugs": [],
        "claim_ids": ["agency-record-transfer"],
        "evidence_level": "official_record",
        "status": "background",
        "document_type": "Records-management guidance",
        "url": NARA_GUIDANCE,
        "summary": "Guidance describing how federal agencies should identify, organize, and transfer UAP records to NARA.",
        "topics": ["records transfer", "agency guidance", "NDAA"],
    },
    {
        "id": "nasa-uap-study",
        "title": "NASA UAP Independent Study Portal",
        "source": "nasa_uap",
        "source_name": "NASA",
        "agency": "NASA",
        "year": 2023,
        "date_label": "2023",
        "location": "United States",
        "case_slugs": [],
        "claim_ids": ["nasa-uap-science"],
        "evidence_level": "official_analysis",
        "status": "background",
        "document_type": "Official study page",
        "url": NASA_UAP,
        "summary": "NASA's public UAP study material, useful for methodology questions rather than individual case resolution.",
        "topics": ["NASA", "scientific methodology", "data quality"],
    },
]

SEEDED_CLAIMS: list[dict] = [
    {"id": "gofast-high-speed", "claim": "The GoFast object was moving at extreme or anomalous speed near the ocean surface.", "category": "performance", "year": 2015, "date_label": "January 2015", "location": "Atlantic Ocean off Florida", "case_slug": "gofast", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. Navy", "confidence_label": "High-confidence official analysis", "what_is_sourced": "AARO says the object was about 13,000 feet up and did not demonstrate anomalous performance; apparent speed depends heavily on geometry and wind.", "open_questions": "The public still does not have every raw mission-context datum, including complete aircraft heading context in the original display.", "document_ids": ["aaro-gofast-resolution"]},
    {"id": "gofast-near-ocean", "claim": "GoFast was skimming just above the ocean.", "category": "altitude", "year": 2015, "date_label": "January 2015", "location": "Atlantic Ocean off Florida", "case_slug": "gofast", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. Navy", "confidence_label": "Official analysis contradicts claim", "what_is_sourced": "AARO assesses the object altitude at approximately 13,000 feet, not near the surface.", "open_questions": "The object identity remains unresolved publicly even though the performance claim is addressed.", "document_ids": ["aaro-gofast-resolution"]},
    {"id": "puerto-rico-transmedium", "claim": "The Puerto Rico object entered and exited the water, showing transmedium capability.", "category": "transmedium", "year": 2013, "date_label": "April 26, 2013", "location": "Aguadilla, Puerto Rico", "case_slug": "puerto-rico-object", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. Customs and Border Protection", "confidence_label": "Official analysis contradicts claim", "what_is_sourced": "AARO assesses with high confidence that the objects did not enter the water or demonstrate transmedium capability.", "open_questions": "Independent researchers dispute elements of the reconstruction, so the tool keeps the original document and case file linked.", "document_ids": ["aaro-puerto-rico-resolution"]},
    {"id": "puerto-rico-splitting", "claim": "The Puerto Rico object split into two objects during the video.", "category": "morphology", "year": 2013, "date_label": "April 26, 2013", "location": "Aguadilla, Puerto Rico", "case_slug": "puerto-rico-object", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. Customs and Border Protection", "confidence_label": "Official analysis offers prosaic reconstruction", "what_is_sourced": "AARO says the video depicts two nearby objects rather than one object splitting, and assesses moderate confidence for sky lanterns.", "open_questions": "The public-facing debate depends on reconstructing flight path, look angle, and sensor geometry.", "document_ids": ["aaro-puerto-rico-resolution"]},
    {"id": "etna-high-speed-plume", "claim": "The Mt. Etna object moved at extraordinary speed through a volcanic ash plume.", "category": "performance", "year": 2018, "date_label": "December 2018", "location": "Near Mt. Etna, Italy", "case_slug": "mt-etna", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. military", "confidence_label": "Official analysis contradicts claim", "what_is_sourced": "AARO attributes the apparent behavior to distance, motion parallax, atmospheric turbulence, and sensor limitations; it assesses the object did not pass through the plume.", "open_questions": "The object identity is assessed with moderate confidence as a balloon, not conclusively identified.", "document_ids": ["aaro-mt-etna-resolution"]},
    {"id": "al-taqaddum-floating-object", "claim": "The Al Taqaddum video shows a strange floating object over a base in Iraq.", "category": "object identity", "year": 2017, "date_label": "October 23, 2017", "location": "Al Taqaddum Air Base, Iraq", "case_slug": "al-taqaddum", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO", "confidence_label": "High-confidence official resolution", "what_is_sourced": "AARO assesses with high confidence that the object was a cluster of fully and partially inflated balloons.", "open_questions": "The public can inspect the released case report and video, but the original reporter is not publicly identified in the seeded summary.", "document_ids": ["aaro-al-taqaddum-resolution"]},
    {"id": "eglin-range-incursion", "claim": "The Eglin case involved a possible range incursion and flight-safety hazard.", "category": "flight safety", "year": 2023, "date_label": "2023", "location": "Eglin Air Force Base area", "case_slug": "eglin", "status": "under_review", "evidence_level": "official_analysis", "agency": "AARO / U.S. military", "confidence_label": "Official record, limited public detail", "what_is_sourced": "AARO describes the report as a flight-safety and sensitive-training-range concern, but public details are limited.", "open_questions": "Object identity and full sensor context are not public in the seeded record.", "document_ids": ["aaro-eglin-resolution"]},
    {"id": "south-asian-atmospheric-wake", "claim": "South Asian object videos show an anomalous atmospheric wake or propulsion signature.", "category": "signature", "year": 2022, "date_label": "2022-2023", "location": "Middle East and South Asia reporting areas", "case_slug": "south-asian-objects", "status": "under_review", "evidence_level": "official_analysis", "agency": "AARO", "confidence_label": "Official record, unresolved public context", "what_is_sourced": "AARO groups these mission reports around possible atmospheric-wake signatures and links public video clips, but the public record remains partial.", "open_questions": "Raw sensor context and a complete public explanation are not available in the seeded record.", "document_ids": ["aaro-atmospheric-wakes-resolution"]},
    {"id": "southeast-asia-triangle-formation", "claim": "Six triangle-like objects in Southeast Asia were anomalous.", "category": "formation", "year": 2023, "date_label": "2023", "location": "Southeast Asia", "case_slug": "southeast-asia-triangles", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO", "confidence_label": "Official resolution", "what_is_sourced": "AARO reviewed the triangular formation as an initially flagged navigation concern and reports it was not anomalous after review.", "open_questions": "The case is strongest when read with the official resolution and released visual material.", "document_ids": ["aaro-southeast-asia-triangles-resolution"]},
    {"id": "western-us-lights", "claim": "Equidistant lights over the western United States represented UAP in restricted airspace.", "category": "lights", "year": 2021, "date_label": "2021", "location": "Western United States military range", "case_slug": "western-us-objects", "status": "resolved", "evidence_level": "official_analysis", "agency": "AARO / U.S. military", "confidence_label": "Official resolution", "what_is_sourced": "AARO assesses the lights as commercial aircraft observed at distance and compares the released footage with flight-track context.", "open_questions": "The user should inspect the official report and video together because the explanation relies on geometry and flight-track matching.", "document_ids": ["aaro-western-us-resolution"]},
    {"id": "nara-uap-collection", "claim": "NARA has a dedicated federal UAP records collection.", "category": "records release", "year": 2025, "date_label": "2025", "location": "United States", "case_slug": "", "status": "official_release", "evidence_level": "official_record", "agency": "NARA", "confidence_label": "Official archive record", "what_is_sourced": "NARA maintains Record Group 615 and related public pages for UAP records transferred by federal agencies.", "open_questions": "NARA receives records on an ongoing basis, so the collection will change over time.", "document_ids": ["nara-rg-615", "nara-uap-topic"]},
    {"id": "agency-record-transfer", "claim": "Federal agencies must identify and prepare UAP records for transfer to NARA.", "category": "records process", "year": 2024, "date_label": "2024", "location": "United States", "case_slug": "", "status": "background", "evidence_level": "official_record", "agency": "NARA", "confidence_label": "Official guidance", "what_is_sourced": "NARA guidance describes agency obligations for UAP record identification, organization, and transfer under the NDAA framework.", "open_questions": "The guidance does not by itself reveal what each agency has already transferred.", "document_ids": ["nara-agency-guidance"]},
    {"id": "nasa-uap-science", "claim": "NASA's UAP role is mainly a data-quality and science-methodology role, not individual military case resolution.", "category": "methodology", "year": 2023, "date_label": "2023", "location": "United States", "case_slug": "", "status": "background", "evidence_level": "official_analysis", "agency": "NASA", "confidence_label": "Official methodology source", "what_is_sourced": "NASA's public UAP material is best used for methodology, data quality, and scientific-study framing.", "open_questions": "NASA pages do not resolve the seeded AARO military cases by themselves.", "document_ids": ["nasa-uap-study"]},
]


def _matches(value: str | int | None, selected: str) -> bool:
    return not selected or str(value or "").lower() == selected.lower()


def _contains(values, selected: str) -> bool:
    if not selected:
        return True
    needle = selected.lower()
    if isinstance(values, str):
        return needle in values.lower()
    return any(needle in str(v).lower() for v in (values or []))


def documents_for_case(slug: str) -> list[dict]:
    return [d for d in SEEDED_DOCUMENTS if slug in d.get("case_slugs", [])]


def claims_for_case(slug: str) -> list[dict]:
    return [c for c in SEEDED_CLAIMS if c.get("case_slug") == slug]


def documents_for_claim(claim: dict) -> list[dict]:
    ids = set(claim.get("document_ids") or [])
    return [d for d in SEEDED_DOCUMENTS if d["id"] in ids]


def document_by_id(doc_id: str) -> dict | None:
    for doc in SEEDED_DOCUMENTS:
        if doc["id"] == doc_id:
            return doc
    return None


def claim_by_id(claim_id: str) -> dict | None:
    for claim in SEEDED_CLAIMS:
        if claim["id"] == claim_id:
            return claim
    return None


def filter_claims(q: str = "", year: str = "", location: str = "", status: str = "", category: str = "", case_slug: str = "") -> list[dict]:
    ql = (q or "").lower().strip()
    out = []
    for claim in SEEDED_CLAIMS:
        hay = " ".join([claim.get("claim", ""), claim.get("location", ""), claim.get("agency", ""), claim.get("category", ""), claim.get("what_is_sourced", ""), claim.get("case_slug", "")]).lower()
        if ql and ql not in hay:
            continue
        if not _matches(claim.get("year"), year):
            continue
        if location and location.lower() not in claim.get("location", "").lower():
            continue
        if not _matches(claim.get("status"), status):
            continue
        if not _matches(claim.get("category"), category):
            continue
        if not _matches(claim.get("case_slug"), case_slug):
            continue
        enriched = dict(claim)
        enriched["documents"] = documents_for_claim(claim)
        out.append(enriched)
    return out


def filter_documents(q: str = "", source: str = "", evidence: str = "", year: str = "", agency: str = "", status: str = "", case_slug: str = "") -> list[dict]:
    ql = (q or "").lower().strip()
    out = []
    for doc in SEEDED_DOCUMENTS:
        hay = " ".join([doc.get("title", ""), doc.get("summary", ""), doc.get("source_name", ""), doc.get("agency", ""), doc.get("location", ""), " ".join(doc.get("topics", [])), " ".join(doc.get("case_slugs", []))]).lower()
        if ql and ql not in hay:
            continue
        if not _matches(doc.get("source"), source):
            continue
        if not _matches(doc.get("evidence_level"), evidence):
            continue
        if not _matches(doc.get("year"), year):
            continue
        if agency and agency.lower() not in doc.get("agency", "").lower():
            continue
        if not _matches(doc.get("status"), status):
            continue
        if case_slug and case_slug not in doc.get("case_slugs", []):
            continue
        out.append(dict(doc))
    return out


def group_by(items: list[dict], key: str) -> list[dict]:
    groups = defaultdict(list)
    for item in items:
        value = item.get(key) or "Unspecified"
        groups[value].append(item)
    def sort_key(pair):
        label, _ = pair
        return str(label)
    return [{"label": label, "items": rows} for label, rows in sorted(groups.items(), key=sort_key, reverse=(key == "year"))]


def case_clusters() -> list[dict]:
    cases = []
    for case in list_cases():
        row = dict(case)
        row["grade"] = evidence_grade(case)
        row["documents"] = documents_for_case(case["slug"])
        row["claims"] = claims_for_case(case["slug"])
        row["year"] = _case_year(case.get("event_date", ""))
        row["region"] = _case_region(case.get("location", ""))
        cases.append(row)
    return cases


def _case_year(label: str) -> str:
    for token in str(label).replace(",", " ").split():
        if token[:4].isdigit():
            return token[:4]
    return "Unknown"


def _case_region(location: str) -> str:
    loc = location.lower()
    if "puerto" in loc:
        return "Caribbean"
    if "florida" in loc or "western united states" in loc or "san diego" in loc:
        return "United States / Atlantic-Pacific ranges"
    if "iraq" in loc or "middle east" in loc or "south asia" in loc:
        return "Middle East / South Asia"
    if "sicily" in loc or "mediterranean" in loc:
        return "Mediterranean"
    if "southeast asia" in loc:
        return "Southeast Asia"
    return "Other"


def facets() -> dict:
    return {
        "claim_years": sorted({str(c["year"]) for c in SEEDED_CLAIMS}, reverse=True),
        "claim_locations": sorted({c["location"] for c in SEEDED_CLAIMS}),
        "claim_categories": sorted({c["category"] for c in SEEDED_CLAIMS}),
        "statuses": sorted({c["status"] for c in SEEDED_CLAIMS} | {d["status"] for d in SEEDED_DOCUMENTS}),
        "sources": sorted({d["source"] for d in SEEDED_DOCUMENTS}),
        "evidence_levels": sorted({d["evidence_level"] for d in SEEDED_DOCUMENTS} | {c["evidence_level"] for c in SEEDED_CLAIMS}),
        "doc_years": sorted({str(d["year"]) for d in SEEDED_DOCUMENTS}, reverse=True),
        "cases": sorted([(c["slug"], c["title"]) for c in list_cases()], key=lambda x: x[1]),
    }


def library_stats() -> dict:
    cases = list_cases()
    return {
        "claims": len(SEEDED_CLAIMS),
        "documents": len(SEEDED_DOCUMENTS),
        "cases": len(cases),
        "official_documents": sum(1 for d in SEEDED_DOCUMENTS if d["source"].startswith(("aaro", "nara", "nasa"))),
    }
