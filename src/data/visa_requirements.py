"""
Static curated dataset of Venezuela visa and entry requirements by
passport nationality, plus current US travel-advisory level.

Authoritative sources (verify before publishing changes):
  https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/venezuela-travel-advisory.html
  https://www.gov.uk/foreign-travel-advice/venezuela
  https://embajadadevenezuela.org (consular network)

Update whenever you confirm a policy change. The tool's UI always
links the user back to the relevant embassy / state-department page.
"""

from __future__ import annotations


VISA_REQUIREMENTS: list[dict] = [
    {
        "country": "United States",
        "code": "US",
        "visa_required": True,
        "visa_type": "Tourist (TR-V) or Business (TR-N) visa required in advance",
        "visa_validity": "Tourist: up to 1 year multiple-entry; Business: up to 1 year",
        "tourist_stay": "Up to 90 days per entry",
        "embassy_url": "https://embajadadevenezuela.org/en/visa-information/",
        "advisory_level": 4,
        "advisory_summary": "Do Not Travel — wrongful detention, arbitrary enforcement of laws, crime, civil unrest, poor health infrastructure, kidnapping, and the lack of consular assistance for US citizens.",
        "advisory_url": "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/venezuela-travel-advisory.html",
        "investor_note": "Travel by US citizens is strongly discouraged by the State Department. The US has no embassy in Caracas; consular services are limited to citizens already in country. Plan all in-country meetings via local counsel and consider third-country jurisdictions for negotiations.",
    },
    {
        "country": "United Kingdom",
        "code": "GB",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days",
        "visa_validity": "Tourist entry stamp issued at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://www.gov.uk/foreign-travel-advice/venezuela/entry-requirements",
        "advisory_level": 3,
        "advisory_summary": "FCDO advises against all but essential travel, citing kidnapping risk, political unrest, deteriorating economy, and limited consular assistance.",
        "advisory_url": "https://www.gov.uk/foreign-travel-advice/venezuela",
        "investor_note": "British citizens enter visa-free for up to 90 days. The British Embassy in Caracas operates with limited staff. Comprehensive travel insurance covering medical evacuation is essential — many policies exclude Venezuela.",
    },
    {
        "country": "Canada",
        "code": "CA",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days",
        "visa_validity": "Tourist entry stamp issued at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://travel.gc.ca/destinations/venezuela",
        "advisory_level": 4,
        "advisory_summary": "Avoid all travel due to high crime rates, civil unrest, hostage-taking risk, severe shortages of medicines and food, and the absence of consular services.",
        "advisory_url": "https://travel.gc.ca/destinations/venezuela",
        "investor_note": "Canadian citizens enter visa-free. Canada has no embassy in Caracas; consular services are provided from Bogotá. Banking access is constrained by sanctions and OFAC compliance practices of correspondent banks.",
    },
    {
        "country": "Brazil",
        "code": "BR",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 60 days",
        "visa_validity": "Tourist entry stamp at port of entry",
        "tourist_stay": "Up to 60 days",
        "embassy_url": "https://www.gov.br/mre/pt-br/embaixada-caracas",
        "advisory_level": 2,
        "advisory_summary": "Brazilian government advises caution; consular and economic ties remain active.",
        "advisory_url": "https://www.gov.br/mre/pt-br",
        "investor_note": "Brazilian citizens benefit from visa-free entry and the strongest South American consular presence in Caracas. Land border crossings (Pacaraima/Santa Elena de Uairén) are open but volatile.",
    },
    {
        "country": "Colombia",
        "code": "CO",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days",
        "visa_validity": "Tourist entry stamp at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://caracas.consulado.gov.co/",
        "advisory_level": 2,
        "advisory_summary": "Colombian government has restored full consular relations as of 2022.",
        "advisory_url": "https://caracas.consulado.gov.co/",
        "investor_note": "With re-opened diplomatic ties, Colombian-Venezuelan border trade is recovering. Cross-border investment via Cúcuta is increasingly viable for goods and services.",
    },
    {
        "country": "European Union (Schengen)",
        "code": "EU",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days for most EU passports",
        "visa_validity": "Tourist entry stamp at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://www.eeas.europa.eu/venezuela_en",
        "advisory_level": 3,
        "advisory_summary": "EU member states broadly advise caution or avoidance of non-essential travel.",
        "advisory_url": "https://www.eeas.europa.eu/venezuela_en",
        "investor_note": "Most EU citizens enter visa-free. The EU and Spain maintain active diplomatic missions, providing the most consistent European consular footprint. Spanish and Italian investors benefit from cultural and language ties to Caracas business networks.",
    },
    {
        "country": "China",
        "code": "CN",
        "visa_required": True,
        "visa_type": "Visa required (Tourist L, Business F, or Investor classifications)",
        "visa_validity": "30-90 days, multiple-entry options available",
        "tourist_stay": "Per visa terms",
        "embassy_url": "http://ve.china-embassy.gov.cn/",
        "advisory_level": 2,
        "advisory_summary": "Chinese government maintains full diplomatic and economic relations.",
        "advisory_url": "http://ve.china-embassy.gov.cn/",
        "investor_note": "Despite visa requirements, Chinese investors operate one of the largest foreign investment portfolios in Venezuela, particularly in oil & gas, mining, and infrastructure. Bilateral trade arrangements smooth FX repatriation friction for Chinese SOEs.",
    },
    {
        "country": "Russia",
        "code": "RU",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days",
        "visa_validity": "Tourist entry stamp at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://venezuela.mid.ru/en/",
        "advisory_level": 2,
        "advisory_summary": "Russian government maintains a strategic relationship with Caracas.",
        "advisory_url": "https://venezuela.mid.ru/en/",
        "investor_note": "Russian citizens enter visa-free. Strategic energy and military cooperation creates pathways for Russian investors not available to Western counterparts, but secondary-sanctions risk for any non-Russian co-investor is acute.",
    },
    {
        "country": "United Arab Emirates",
        "code": "AE",
        "visa_required": False,
        "visa_type": "Visa-free for stays of up to 90 days",
        "visa_validity": "Tourist entry stamp at port of entry",
        "tourist_stay": "Up to 90 days",
        "embassy_url": "https://embajadadeemiratosarabes.org/",
        "advisory_level": 2,
        "advisory_summary": "UAE government maintains diplomatic and trade relations.",
        "advisory_url": "https://embajadadeemiratosarabes.org/",
        "investor_note": "UAE citizens enter visa-free. Dubai has emerged as a meaningful intermediation hub for Venezuelan-related trade and asset structuring, particularly post-2022.",
    },
    {
        "country": "Other (please confirm with embassy)",
        "code": "OTHER",
        "visa_required": True,
        "visa_type": "Varies by nationality",
        "visa_validity": "Confirm with the nearest Venezuelan embassy",
        "tourist_stay": "Varies",
        "embassy_url": "https://embajadadevenezuela.org/",
        "advisory_level": None,
        "advisory_summary": "Check your home country's foreign affairs ministry for the current advisory level.",
        "advisory_url": "https://embajadadevenezuela.org/",
        "investor_note": "Always confirm visa status, validity, and the current published advisory level with both the Venezuelan diplomatic mission in your country and your home country's foreign affairs ministry before booking travel.",
    },
]


def list_visa_requirements() -> list[dict]:
    return VISA_REQUIREMENTS
