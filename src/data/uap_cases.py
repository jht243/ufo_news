from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class UAPCase:
    slug: str
    title: str
    aliases: list[str]
    event_date: str
    location: str
    agencies: list[str]
    status: str
    official_explanation: str
    unresolved_questions: list[str]
    source_urls: list[dict]
    media_urls: list[dict] = field(default_factory=list)
    evidence: dict = field(default_factory=dict)


CASES: list[UAPCase] = [
    UAPCase("gofast", "GoFast", ["GOFAST", "Go Fast"], "January 2015", "Atlantic Ocean off Florida", ["U.S. Navy", "AARO"], "resolved", "AARO reports the apparent speed was a parallax effect and the object was moving with the wind.", ["The public record does not include all raw sensor and mission context data."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": True}),
    UAPCase("gimbal", "Gimbal", ["GIMBAL"], "January 2015", "Atlantic Ocean", ["U.S. Navy", "AARO"], "under_review", "Publicly discussed Navy video; no final public AARO resolution is listed in the seeded record.", ["Full sensor package and object identification remain unavailable in public records."], [{"label": "AARO UAP cases", "url": "https://www.aaro.mil/UAP-Cases/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": False}),
    UAPCase("tic-tac", "Tic Tac / Nimitz", ["Nimitz", "FLIR1", "Tic Tac"], "November 2004", "Pacific Ocean near San Diego", ["U.S. Navy"], "unresolved", "No public official case-resolution report in the seeded record.", ["Raw radar, deck logs, and complete chain-of-custody records remain fragmented publicly."], [{"label": "AARO UAP cases", "url": "https://www.aaro.mil/UAP-Cases/"}], evidence={"official_record": True, "video": True, "multi_sensor": True, "official_resolution": False}),
    UAPCase("puerto-rico-object", "Puerto Rico Object", ["Aguadilla", "Puerto Rico UAP"], "April 2013", "Aguadilla, Puerto Rico", ["AARO"], "resolved", "AARO assesses the object did not enter the water and was consistent with prosaic motion reconstructed from available data.", ["Independent researchers continue to dispute parts of the reconstruction."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": True}),
    UAPCase("eglin", "Eglin Case", ["Eglin UAP"], "2023", "Eglin Air Force Base area", ["AARO", "U.S. military"], "under_review", "AARO describes the report as a range-incursion and flight-safety concern; public details remain limited.", ["Object identity and full sensor data are not public."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": False, "multi_sensor": False, "official_resolution": False}),
    UAPCase("al-taqaddam", "Al Taqaddum", ["Al Taqaddam", "Iraq blimp object"], "October 23, 2017", "Al Taqaddum Air Base, Iraq", ["AARO"], "resolved", "AARO assesses with high confidence that the object was consistent with a cluster of balloons.", ["The public can inspect the released video and case-resolution narrative."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": True}),
    UAPCase("western-us-objects", "Western U.S. Objects", ["Western United States", "western US lights"], "2021", "Western United States military range", ["AARO"], "resolved", "AARO assessed the lights as commercial aircraft seen at distance.", ["The public case depends on matching released footage to flight tracks."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": True, "official_resolution": True}),
    UAPCase("mt-etna", "Mt. Etna", ["Etna", "Sigonella"], "December 2018", "Mediterranean Sea south of Sicily", ["AARO"], "resolved", "AARO associates the observation with Mt. Etna eruption conditions and sensor context.", ["Public users should compare the report with the released video and reconstruction details."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": True}),
    UAPCase("south-asian-objects", "South Asian Objects", ["South Asian Object", "Atmospheric Wake"], "2022-2023", "Middle East and South Asia reporting areas", ["AARO"], "under_review", "AARO grouped several atmospheric-wake reports for analysis; public material is partial.", ["The anomalous propulsion-signature claim needs raw sensor context for outside review."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": False}),
    UAPCase("southeast-asia-triangles", "Southeast Asia Triangles", ["Triangle formation", "Southeast Asia Triangles"], "2023", "Southeast Asia", ["AARO"], "resolved", "AARO reports the triangular appearance was not anomalous after review.", ["The public record is strongest where the released video and report can be read together."], [{"label": "AARO case page", "url": "https://www.aaro.mil/UAP-Cases/UAP-Case-Resolution-Reports/"}], evidence={"official_record": True, "video": True, "multi_sensor": False, "official_resolution": True}),
]


def list_cases() -> list[dict]:
    return [case.__dict__ for case in CASES]


def get_case(slug: str) -> dict | None:
    for case in CASES:
        if case.slug == slug:
            return case.__dict__
    return None


def search_cases(query: str) -> list[dict]:
    q = (query or "").lower().strip()
    if not q:
        return list_cases()
    out = []
    for case in CASES:
        haystack = " ".join([case.title, case.slug, case.location, case.status, *case.aliases, *case.agencies]).lower()
        if q in haystack:
            out.append(case.__dict__)
    return out


def evidence_grade(case: dict) -> dict:
    ev = case.get("evidence") or {}
    score = 0
    score += 30 if ev.get("official_record") else 0
    score += 20 if ev.get("video") else 0
    score += 20 if ev.get("multi_sensor") else 0
    score += 20 if ev.get("official_resolution") else 0
    score += 10 if len(case.get("source_urls") or []) > 1 else 0
    if score >= 80:
        label = "Strong public record"
    elif score >= 55:
        label = "Moderate public record"
    elif score >= 35:
        label = "Partial public record"
    else:
        label = "Thin public record"
    return {"score": score, "label": label}
