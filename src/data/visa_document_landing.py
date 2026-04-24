"""
SEO landing pages for travelers who search the exact ministry document names
(e.g. “planilla de solicitud de visa”, “declaracion jurada visa venezolana”).

Rendered by templates/visa_document_landing.html.j2 + server routes.
"""

from __future__ import annotations

# User-facing line for the planilla guide, hub cards, and cross-links.
PLANILLA_HERO_LINE = "Fill In Your Planilla De Solicitud De Visa Venezuella"


PLANILLA_DE_SOLICITUD_DE_VISA: dict = {
    "canonical_path": "/planilla-de-solicitud-de-visa",
    "title": f"{PLANILLA_HERO_LINE} | Caracas Research",
    "description": (
        f"{PLANILLA_HERO_LINE} — the MPPRE-style “planilla de solicitud de visa” you "
        "attach in Cancillería Digital. What each section means, how to print a "
        "Spanish-labelled PDF from our English-friendly type-in tool, and how to upload it."
    ),
    "keywords": (
        "Fill In Your Planilla De Solicitud De Visa Venezuella, planilla de solicitud de visa, "
        "planilla visa Venezuela, MPPRE planilla, Cancillería Digital planilla, "
        "solicitud de visa Venezuela formulario"
    ),
    "kicker": "Venezuela e-visa · MPPRE paperwork",
    "h1": PLANILLA_HERO_LINE,
    "lead": (
        f"When Cancillería Digital asks for the official "
        f"<strong>planilla de solicitud de visa</strong>, use this page as your map — "
        f"then use <strong>{PLANILLA_HERO_LINE}</strong> below to open the free "
        "type-in sheet (English labels on screen, Spanish headings on the PDF you upload)."
    ),
    "sections": [
        {
            "h2": "What the planilla is",
            "paragraphs": [
                (
                    "The planilla groups your identity, passport, address, trip "
                    "dates, lodging in Venezuela, and similar fields into numbered "
                    "sections so a consular officer (or the online portal) can scan "
                    "the file quickly. Wording can change when MPPRE updates forms — "
                    "always compare your PDF to the latest instructions in the live "
                    "portal if something looks different."
                ),
            ],
        },
        {
            "h2": "What to do if this is your first time",
            "paragraphs": [
                (
                    "Gather your passport scan, itinerary, hotel or invitation letter, "
                    "and the other items your visa class requires <em>before</em> you "
                    "sit down to type the planilla — you will copy those details in."
                ),
                (
                    "Use a desktop browser. Fill the fields, then choose "
                    "<strong>Print</strong> → <strong>Save as PDF</strong> (Chrome, "
                    "Edge, or Safari). Upload that PDF where the portal asks for the "
                    "planilla attachment."
                ),
            ],
        },
        {
            "h2": "Related documents",
            "paragraphs": [
                (
                    "Most tourist and business files also need a "
                    "<a href=\"/declaracion-jurada-visa-venezolana\">declaración jurada</a> "
                    "(short sworn statement in Spanish). The "
                    "<a href=\"/apply-for-venezuelan-visa\">full visa application guide (2026)</a> "
                    "walks the online process end-to-end."
                ),
            ],
        },
    ],
    "tool_url": "/apply-for-venezuelan-visa/planilla",
    "tool_label": PLANILLA_HERO_LINE,
    "nav_links": [
        {
            "href": "/declaracion-jurada-visa-venezolana",
            "label": "Declaración jurada (visa venezolana)",
        },
        {
            "href": "/apply-for-venezuelan-visa",
            "label": "How To Apply For A Venezuelan Visa (2026)",
        },
    ],
}

DECLARACION_JURADA_VISA_VENEZOLANA: dict = {
    "canonical_path": "/declaracion-jurada-visa-venezolana",
    "title": (
        "Declaración jurada visa venezolana — no criminal record statement "
        "| Caracas Research"
    ),
    "description": (
        "What a declaración jurada is for a Venezuelan visa file, when Cancillería "
        "Digital asks for it, and how to complete the sworn no–criminal-record text "
        "in Spanish — with a free printable PDF tool."
    ),
    "keywords": (
        "declaracion jurada visa venezolana, declaración jurada Venezuela visa, "
        "declaracion jurada visa venezuelana, sworn statement Venezuela visa, "
        "antecedentes penales declaración Venezuela"
    ),
    "kicker": "Venezuela e-visa · Sworn statement",
    "h1": "Declaración jurada (visa venezolana)",
    "lead": (
        "A <strong>declaración jurada</strong> for a Venezuelan visa is a sworn "
        "statement — in <strong>Spanish</strong> — that says you do not have a "
        "criminal record in your home country or elsewhere. Portals and consulates "
        "attach it next to your passport copy and planilla."
    ),
    "sections": [
        {
            "h2": "When you need it",
            "paragraphs": [
                (
                    "Requirements vary by visa class and channel (online vs in-person "
                    "at a consulate). If Cancillería Digital or your consulate checklist "
                    "lists “declaración jurada”, assume you must upload a signed PDF "
                    "unless they explicitly waive it."
                ),
            ],
        },
        {
            "h2": "How to complete it safely",
            "paragraphs": [
                (
                    "Read the Spanish body once so you understand what you are signing. "
                    "Fill your name, nationality, and passport number carefully so "
                    "they match your passport scan character-for-character."
                ),
                (
                    "You may type your signature as your full legal name — our tool "
                    "renders it in cursive for PDF — or print blank, sign in ink, and "
                    "scan. Do not alter the core legal wording unless a lawyer tells "
                    "you to."
                ),
            ],
        },
        {
            "h2": "Related documents",
            "paragraphs": [
                (
                    "Pair this with "
                    f"<a href=\"/planilla-de-solicitud-de-visa\">{PLANILLA_HERO_LINE}</a> "
                    "and follow the full "
                    "<a href=\"/apply-for-venezuelan-visa\">How To Apply For A Venezuelan Visa (2026)</a> "
                    "guide for fees, timeline, and portal steps."
                ),
            ],
        },
    ],
    "tool_url": "/apply-for-venezuelan-visa/declaracion-jurada",
    "tool_label": "Fill In Your Declaraction Jurada",
    "nav_links": [
        {
            "href": "/planilla-de-solicitud-de-visa",
            "label": PLANILLA_HERO_LINE,
        },
        {
            "href": "/apply-for-venezuelan-visa",
            "label": "How To Apply For A Venezuelan Visa (2026)",
        },
    ],
}


def get_planilla_landing() -> dict:
    return PLANILLA_DE_SOLICITUD_DE_VISA


def get_declaracion_landing() -> dict:
    return DECLARACION_JURADA_VISA_VENEZOLANA
