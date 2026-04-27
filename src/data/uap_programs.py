from __future__ import annotations

from collections import defaultdict


PROGRAMS: list[dict] = [
    {
        "slug": "project-sign",
        "name": "Project Sign",
        "aliases": ["Project Saucer"],
        "years": "1948-1949",
        "start_year": 1948,
        "era": "Cold War Air Force investigations",
        "agency": "U.S. Air Force",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "investigation",
        "summary": "Early Air Force UFO investigation created after the 1947 flying-saucer wave and predecessor to Project Grudge and Project Blue Book.",
        "why_it_matters": "Project Sign is the start of the modern U.S. government UFO investigation lineage. It frames later debates about whether UFO reports were mainly an air-defense problem, a public-order problem, or evidence of unknown technology.",
        "public_record": "Documented through the later Air Force and National Archives Project Blue Book record chain; AARO treats the post-1945 historical investigation lineage as part of its historical review.",
        "caveat": "Public summaries of Project Sign often rely on later histories and archival compilations rather than a single easy official landing page.",
        "sources": [
            {"label": "NARA Project Blue Book reference", "url": "https://www.archives.gov/research/military/air-force/ufos"},
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
        ],
        "related": ["project-grudge", "project-blue-book"],
    },
    {
        "slug": "project-grudge",
        "name": "Project Grudge",
        "aliases": [],
        "years": "1949-1951",
        "start_year": 1949,
        "era": "Cold War Air Force investigations",
        "agency": "U.S. Air Force",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "investigation",
        "summary": "Air Force UFO investigation that followed Project Sign and preceded Project Blue Book.",
        "why_it_matters": "Project Grudge is often cited as the point where the Air Force posture moved toward reducing public anxiety and explaining reports through conventional causes.",
        "public_record": "Part of the documented Air Force investigation sequence that culminated in Project Blue Book records now held by NARA.",
        "caveat": "The public record is more fragmented than Project Blue Book; treat dramatic claims about its intent as interpretations unless tied to documents.",
        "sources": [
            {"label": "NARA Project Blue Book reference", "url": "https://www.archives.gov/research/military/air-force/ufos"},
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
        ],
        "related": ["project-sign", "project-blue-book"],
    },
    {
        "slug": "project-blue-book",
        "name": "Project Blue Book",
        "aliases": ["Blue Book"],
        "years": "1952-1969",
        "start_year": 1952,
        "era": "Cold War Air Force investigations",
        "agency": "U.S. Air Force",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "investigation",
        "summary": "Long-running Air Force UFO investigation headquartered at Wright-Patterson Air Force Base; the Air Force reported 12,618 sightings, with 701 remaining unidentified.",
        "why_it_matters": "Project Blue Book is the main public archive for historic U.S. Air Force UFO cases and still anchors many SERP searches for official UFO files.",
        "public_record": "NARA states the Air Force retired Project Blue Book records to the National Archives; the project closed in 1969 and NARA has no post-1969 sightings in that collection.",
        "caveat": "Unidentified does not mean extraterrestrial. The Air Force fact sheet says the program found no evidence of national-security threat, beyond-current-science technology, or extraterrestrial vehicles.",
        "sources": [
            {"label": "NARA Project Blue Book - Unidentified Flying Objects", "url": "https://www.archives.gov/research/military/air-force/ufos"},
        ],
        "related": ["project-sign", "project-grudge", "condon-committee"],
    },
    {
        "slug": "robertson-panel",
        "name": "Robertson Panel",
        "aliases": ["CIA Scientific Advisory Panel on UFOs"],
        "years": "1953",
        "start_year": 1953,
        "era": "Cold War review panels",
        "agency": "CIA / Scientific Advisory Panel",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "review_panel",
        "summary": "CIA-connected scientific advisory panel convened to evaluate UFO reports and their potential national-security implications.",
        "why_it_matters": "The panel is central to claims that government policy shifted toward public debunking, stigma management, and reducing report volume rather than broad public investigation.",
        "public_record": "CIA FOIA material identifies the panel, the Robertson Report, and the relationship to Project Blue Book.",
        "caveat": "The panel was a review panel, not a case-collection program like Blue Book or AARO.",
        "sources": [
            {"label": "CIA Reading Room FOIA response on Robertson Report", "url": "https://www.cia.gov/readingroom/document/00934938"},
        ],
        "related": ["project-blue-book"],
    },
    {
        "slug": "condon-committee",
        "name": "Condon Committee / University of Colorado UFO Study",
        "aliases": ["Scientific Study of Unidentified Flying Objects", "Colorado Project"],
        "years": "1966-1968",
        "start_year": 1966,
        "era": "Cold War review panels",
        "agency": "U.S. Air Force / University of Colorado",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "contracted_study",
        "summary": "Air Force-sponsored university study used as part of the rationale for terminating Project Blue Book.",
        "why_it_matters": "The Condon Report is the bridge between the Air Force investigation era and the official closure of Blue Book in 1969.",
        "public_record": "NARA's Air Force fact-sheet text says the Blue Book termination decision relied on the University of Colorado study, National Academy of Sciences review, earlier studies, and Air Force experience.",
        "caveat": "The study remains contested among UFO researchers, but its official policy role is clear.",
        "sources": [
            {"label": "NARA Project Blue Book - Air Force fact sheet", "url": "https://www.archives.gov/research/military/air-force/ufos"},
        ],
        "related": ["project-blue-book"],
    },
    {
        "slug": "aawsap",
        "name": "Advanced Aerospace Weapon System Applications Program",
        "aliases": ["AAWSAP"],
        "years": "2008-2010",
        "start_year": 2008,
        "era": "Post-2004 defense research",
        "agency": "Defense Intelligence Agency",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "contracted_research",
        "summary": "DIA-funded contract commonly associated with Bigelow Aerospace Advanced Space Studies and broad advanced-aerospace/UAP-adjacent research.",
        "why_it_matters": "AAWSAP is the documented government-funded ancestor of many modern AATIP/UAP program narratives and is frequently confused with later informal efforts.",
        "public_record": "AARO's historical report treats AAWSAP as a real government-funded effort and discusses its relationship to later claims and program names.",
        "caveat": "AAWSAP was broader than a simple UFO desk. Some public claims blend documented contract work with paranormal or crash-retrieval allegations that are not equally sourced.",
        "sources": [
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
        ],
        "related": ["aatip", "kona-blue"],
    },
    {
        "slug": "aatip",
        "name": "Advanced Aerospace Threat Identification Program",
        "aliases": ["AATIP"],
        "years": "2009-2017 public-claim period",
        "start_year": 2009,
        "era": "Post-2004 defense research",
        "agency": "Department of Defense",
        "status": "disputed_scope",
        "source_strength": "mixed public record",
        "program_type": "informal_or_disputed_program",
        "summary": "Program name associated with post-AAWSAP UAP work and public accounts by former officials; official descriptions of its scope and status have varied.",
        "why_it_matters": "AATIP became the name most of the public associated with the 2017-era disclosure cycle, but it is also one of the messiest labels in the UAP program map.",
        "public_record": "AARO distinguishes documented AAWSAP activity from later AATIP claims; media and former-official accounts use AATIP more broadly.",
        "caveat": "Treat AATIP claims by scope: a program name may be real while specific claims about authority, funding, or recovered technology may remain unsupported.",
        "sources": [
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
        ],
        "related": ["aawsap", "uaptf"],
    },
    {
        "slug": "uaptf",
        "name": "Unidentified Aerial Phenomena Task Force",
        "aliases": ["UAPTF"],
        "years": "2020-2021",
        "start_year": 2020,
        "era": "Modern UAP offices",
        "agency": "Department of the Navy / DoD OUSD(I&S)",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "task_force",
        "summary": "Navy-led task force established by DoD to detect, analyze, and catalog UAP that could pose a national-security threat.",
        "why_it_matters": "The UAPTF is the direct predecessor to the 2021 ODNI preliminary assessment and the modern office structure that led to AOIMSG and AARO.",
        "public_record": "DoD announced the UAPTF in August 2020 and described its mission as improving understanding of the nature and origins of UAP.",
        "caveat": "The 2021 ODNI report was a limited preliminary assessment, not a full public database of every case.",
        "sources": [
            {"label": "DoD establishment of UAPTF", "url": "https://www.defense.gov/News/Releases/Release/Article/2314065/establishment-of-unidentified-aerial-phenomena-task-force/lang/establishment-of-unidentified-aerial-phenomena-task-force/"},
            {"label": "ODNI 2021 Preliminary Assessment", "url": "https://www.odni.gov/index.php/newsroom/reports-publications/reports-publications-2021/3550-preliminary-assessment-unidentified-aerial-phenomena?highlight=WzIwMjFd"},
        ],
        "related": ["aoimsg", "aaro"],
    },
    {
        "slug": "aoimsg",
        "name": "Airborne Object Identification and Management Synchronization Group",
        "aliases": ["AOIMSG", "AOIMEXEC"],
        "years": "2021-2022",
        "start_year": 2021,
        "era": "Modern UAP offices",
        "agency": "Department of Defense / Intelligence Community",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "coordination_group",
        "summary": "DoD successor to the Navy-led UAPTF, created to synchronize detection, identification, attribution, and threat mitigation for airborne objects of interest in special-use airspace.",
        "why_it_matters": "AOIMSG marks the post-2021 shift from a Navy-led task force to broader DoD and Intelligence Community coordination.",
        "public_record": "DoD announced AOIMSG on November 23, 2021 and later renamed and expanded it into AARO in July 2022.",
        "caveat": "AOIMSG had a short lifespan and is best treated as an institutional transition point.",
        "sources": [
            {"label": "DoD establishes AOIMSG", "url": "https://www.defense.gov/News/Releases/Release/Article/2853121/dod-announces-the-establishment-of-the-airborne-object-identification-and-manag/dod-announces-the-establishment-of-the-airborne-object-identification-and-manag/"},
            {"label": "DoD establishes AARO", "url": "https://www.defense.gov/News/Releases/Release/Article/3100053/dod-announces-the-establishment-of-the-all-domain-anomaly-resolution-office/%20/lang/dod-announces-the-establishment-of-the-all-domain-anomaly-resolution-office/"},
        ],
        "related": ["uaptf", "aaro"],
    },
    {
        "slug": "aaro",
        "name": "All-domain Anomaly Resolution Office",
        "aliases": ["AARO"],
        "years": "2022-present",
        "start_year": 2022,
        "era": "Modern UAP offices",
        "agency": "Department of Defense / ODNI coordination",
        "status": "active_confirmed",
        "source_strength": "officially documented",
        "program_type": "office",
        "summary": "Current DoD office for synchronizing scientific, intelligence, and operational work to detect, identify, attribute, and mitigate UAP near national-security areas.",
        "why_it_matters": "AARO is the present-day public hub for official UAP case-resolution reports, annual reporting, historical review, and declassification work.",
        "public_record": "DoD announced AARO in July 2022; federal law separately codifies the office and assigns duties to the Secretary of Defense and DNI.",
        "caveat": "AARO's conclusions are official assessments, not the same thing as releasing every underlying sensor file or classified lead.",
        "sources": [
            {"label": "DoD establishes AARO", "url": "https://www.defense.gov/News/Releases/Release/Article/3100053/dod-announces-the-establishment-of-the-all-domain-anomaly-resolution-office/%20/lang/dod-announces-the-establishment-of-the-all-domain-anomaly-resolution-office/"},
            {"label": "50 U.S.C. 3373 - Establishment of AARO", "url": "https://www.law.cornell.edu/uscode/text/50/3373"},
            {"label": "DoD announces AARO director Jon Kosloski", "url": "https://www.defense.gov/News/Releases/Release/Article/3884318/department-of-defense-announces-the-new-director-all-domain-anomaly-resolution/"},
        ],
        "related": ["uaptf", "aoimsg", "nara-uap-records-collection"],
    },
    {
        "slug": "nasa-uap-independent-study",
        "name": "NASA UAP Independent Study Team",
        "aliases": ["NASA UAP Study", "NASA UAP Research Director"],
        "years": "2022-2023",
        "start_year": 2022,
        "era": "Modern science and records",
        "agency": "NASA",
        "status": "confirmed_historical",
        "source_strength": "officially documented",
        "program_type": "scientific_study",
        "summary": "NASA-commissioned independent study team examining how NASA can contribute to UAP research through data quality, scientific methods, and future collection strategies.",
        "why_it_matters": "NASA shifted the public frame toward data quality and scientific methods rather than military case resolution or extraordinary claims.",
        "public_record": "NASA announced the study in June 2022 and released the final report in September 2023, naming a UAP research director.",
        "caveat": "NASA did not become the primary U.S. government case-resolution office; that role remains tied to AARO and national-security reporting.",
        "sources": [
            {"label": "NASA UAP study portal", "url": "https://science.nasa.gov/uap/"},
            {"label": "NASA releases UAP report and names director", "url": "https://www.nasa.gov/news-release/update-nasa-shares-uap-independent-study-report-names-director/"},
        ],
        "related": ["aaro"],
    },
    {
        "slug": "nara-uap-records-collection",
        "name": "NARA UAP Records Collection",
        "aliases": ["Record Group 615", "UAP Records Collection"],
        "years": "2024-present",
        "start_year": 2024,
        "era": "Modern science and records",
        "agency": "National Archives and Records Administration",
        "status": "active_confirmed",
        "source_strength": "officially documented",
        "program_type": "records_collection",
        "summary": "Federal archival collection for UAP records transferred by agencies under the modern disclosure and records-management framework.",
        "why_it_matters": "NARA is the public records lane. It helps separate actual released documents from claims about documents that may or may not exist.",
        "public_record": "NARA maintains UAP topic pages, Record Group 615 references, and guidance for federal agencies handling UAP records.",
        "caveat": "The collection grows as agencies identify and transfer records; it is not a complete real-time intelligence database.",
        "sources": [
            {"label": "NARA records related to UFOs and UAPs", "url": "https://www.archives.gov/research/topics/uaps"},
            {"label": "NARA Record Group 615", "url": "https://www.archives.gov/research/topics/uaps/rg-615"},
            {"label": "NARA UAP records-management guidance", "url": "https://www.archives.gov/records-mgmt/uap-guidance"},
        ],
        "related": ["aaro", "project-blue-book"],
    },
    {
        "slug": "kona-blue",
        "name": "KONA BLUE",
        "aliases": ["Kona Blue SAP proposal"],
        "years": "2011-2012 proposal period",
        "start_year": 2011,
        "era": "Alleged or proposed programs",
        "agency": "Department of Homeland Security proposal",
        "status": "proposed_not_approved",
        "source_strength": "officially discussed but not operational",
        "program_type": "proposed_special_access_program",
        "summary": "A proposed DHS Special Access Program associated with AAWSAP-era figures; AARO reports it was not approved and did not become an operational program.",
        "why_it_matters": "KONA BLUE is one of the best examples of why the directory separates proposed, alleged, and operational programs.",
        "public_record": "AARO's historical report discusses KONA BLUE and says it was proposed but not approved as a program.",
        "caveat": "Do not treat KONA BLUE as proof of an active crash-retrieval or reverse-engineering program; the public official record says it did not become operational.",
        "sources": [
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
        ],
        "related": ["aawsap", "aatip"],
    },
    {
        "slug": "majestic-12",
        "name": "Majestic 12",
        "aliases": ["MJ-12", "MJ12"],
        "years": "Alleged 1947 onward",
        "start_year": 1947,
        "era": "Alleged or rumored programs",
        "agency": "Alleged presidential / military-intelligence group",
        "status": "alleged_disputed",
        "source_strength": "unverified / disputed",
        "program_type": "alleged_program",
        "summary": "Alleged secret group said by some UFO researchers to have managed crash-retrieval or extraterrestrial materials; government archival searches have not verified the core claim.",
        "why_it_matters": "MJ-12 is the template for many later alleged secret UAP control-group narratives and needs clear evidence labeling.",
        "public_record": "NARA states that extensive searches for MJ-12-related records were negative except for a one-page Cutler memorandum that does not identify MJ-12 or its purpose.",
        "caveat": "Treat as alleged and disputed unless a specific document can be authenticated through official archives.",
        "sources": [
            {"label": "NARA Project Blue Book page - MJ-12 search note", "url": "https://www.archives.gov/research/military/air-force/ufos"},
        ],
        "related": ["project-blue-book"],
    },
    {
        "slug": "immaculate-constellation",
        "name": "IMMACULATE CONSTELLATION",
        "aliases": ["Immaculate Constellation"],
        "years": "Alleged 2017-present",
        "start_year": 2017,
        "era": "Alleged or rumored programs",
        "agency": "Alleged Department of Defense uSAP",
        "status": "alleged_denied",
        "source_strength": "alleged; officially denied",
        "program_type": "alleged_special_access_program",
        "summary": "Alleged unacknowledged Special Access Program said to hold classified UAP evidence; DoD has denied having any present or historical record of a SAP with that name.",
        "why_it_matters": "It is a current high-search-volume program name and a good stress test for evidence labeling: alleged in press and Congressional materials, denied by DoD.",
        "public_record": "An ODNI-released FOIA document summarizes press allegations and includes the DoD denial; Congress.gov lists supporting documentation from a November 2024 UAP hearing.",
        "caveat": "The tool labels this alleged, not confirmed. A hearing exhibit or whistleblower report is not the same as official verification.",
        "sources": [
            {"label": "ODNI FOIA release describing allegation and DoD denial", "url": "https://www.dni.gov/files/documents/FOIA/DF-2025-00021-Immaculate-Constellation-descrp-from-UNCLASS-Press-22-Oct-2024.pdf"},
            {"label": "Congress.gov November 2024 UAP hearing", "url": "https://www.congress.gov/event/118th-congress/house-event/117722"},
        ],
        "related": ["aaro", "legacy-crash-retrieval-claims"],
    },
    {
        "slug": "legacy-crash-retrieval-claims",
        "name": "Legacy crash-retrieval / reverse-engineering claims",
        "aliases": ["UAP crash retrieval program", "reverse engineering program"],
        "years": "Alleged 1930s-present",
        "start_year": 1930,
        "era": "Alleged or rumored programs",
        "agency": "Alleged multi-agency / contractor network",
        "status": "alleged_unverified",
        "source_strength": "whistleblower allegation",
        "program_type": "alleged_program_family",
        "summary": "Family of allegations that a hidden U.S. government or contractor program retrieved and reverse-engineered non-human craft or materials.",
        "why_it_matters": "These claims drove major Congressional attention in 2023-2024, but public evidence remains testimony and allegation rather than verified program documentation.",
        "public_record": "David Grusch testified to Congress about alleged multi-decade crash-retrieval and reverse-engineering work; AARO's historical report says it found no evidence that any U.S. government investigation verified extraterrestrial technology.",
        "caveat": "Do not collapse all legacy claims into one confirmed program. The evidence status is allegation, investigation, and denial/dispute.",
        "sources": [
            {"label": "Congress.gov 2024 UAP hearing record", "url": "https://www.congress.gov/event/118th-congress/house-event/117722"},
            {"label": "AARO Historical Record Report Vol. 1", "url": "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"},
            {"label": "NPR coverage of 2023 UAP hearing", "url": "https://www.npr.org/2023/07/27/1190390376/ufo-hearing-non-human-biologics-uaps"},
        ],
        "related": ["majestic-12", "immaculate-constellation", "kona-blue"],
    },
]


def list_programs() -> list[dict]:
    return [dict(p) for p in PROGRAMS]


def search_programs(q: str = "", status: str = "", agency: str = "", era: str = "", source_strength: str = "") -> list[dict]:
    ql = (q or "").lower().strip()
    out = []
    for program in PROGRAMS:
        hay = " ".join([
            program["name"],
            " ".join(program.get("aliases", [])),
            program["summary"],
            program["why_it_matters"],
            program["public_record"],
            program["agency"],
            program["era"],
            program["status"],
            program["source_strength"],
        ]).lower()
        if ql and ql not in hay:
            continue
        if status and program["status"] != status:
            continue
        if agency and agency.lower() not in program["agency"].lower():
            continue
        if era and program["era"] != era:
            continue
        if source_strength and program["source_strength"] != source_strength:
            continue
        out.append(dict(program))
    return out


def program_by_slug(slug: str) -> dict | None:
    for program in PROGRAMS:
        if program["slug"] == slug:
            return dict(program)
    return None


def program_facets() -> dict:
    return {
        "statuses": sorted({p["status"] for p in PROGRAMS}),
        "eras": sorted({p["era"] for p in PROGRAMS}),
        "source_strengths": sorted({p["source_strength"] for p in PROGRAMS}),
        "agencies": sorted({p["agency"] for p in PROGRAMS}),
    }


def group_programs(programs: list[dict], key: str) -> list[dict]:
    groups = defaultdict(list)
    for program in programs:
        groups[program.get(key) or "Unspecified"].append(program)
    reverse = key == "start_year"
    return [{"label": label, "items": rows} for label, rows in sorted(groups.items(), key=lambda pair: str(pair[0]), reverse=reverse)]


def program_stats() -> dict:
    confirmed = sum(1 for p in PROGRAMS if p["status"] in {"confirmed_historical", "active_confirmed"})
    alleged = sum(1 for p in PROGRAMS if p["status"].startswith("alleged"))
    active = sum(1 for p in PROGRAMS if p["status"] == "active_confirmed")
    return {"total": len(PROGRAMS), "confirmed": confirmed, "alleged": alleged, "active": active}
