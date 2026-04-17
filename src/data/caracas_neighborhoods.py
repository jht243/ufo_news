"""
Curated Caracas neighborhood safety, accommodation, and business-suitability
dataset. Scores are 1 (highest concern) to 5 (most stable for foreign
visitors and businesses), based on published State Department / FCDO
context, OSAC reporting trends, and aggregated expat-community feedback.

This is NOT a real-time crime feed — it is a one-page reference for
investors and business travellers planning a trip. Always confirm with
local security advisors before travel.

Update when local on-the-ground sources signal a sustained shift.
"""

from __future__ import annotations


CARACAS_NEIGHBORHOODS: list[dict] = [
    {
        "name": "Las Mercedes",
        "municipality": "Baruta",
        "safety_score": 4,
        "category": "Business / dining hub",
        "summary": "The closest thing Caracas has to an international business district. Concentration of corporate offices, embassies, banks, and upscale restaurants. Reasonable security infrastructure during business hours.",
        "business_use": "Default district for foreign-investor meetings, corporate offices, and after-hours dining. Most major hotels routinely send drivers here.",
        "what_to_avoid": "Avoid walking alone after dark; use authorised hotel transport.",
        "lat": 10.4688,
        "lng": -66.8569,
    },
    {
        "name": "Altamira",
        "municipality": "Chacao",
        "safety_score": 4,
        "category": "Business / residential",
        "summary": "Long-standing diplomatic and residential district with a relatively visible private-security presence. Plaza Altamira has been a focal point of historical political demonstrations.",
        "business_use": "Common location for law firms, advisory shops, and family-office representatives. Well served by quality residential rentals.",
        "what_to_avoid": "Stay alert during politically charged periods; demonstrations have flared at Plaza Altamira.",
        "lat": 10.4970,
        "lng": -66.8533,
    },
    {
        "name": "Chacao",
        "municipality": "Chacao",
        "safety_score": 4,
        "category": "Commercial / mixed-use",
        "summary": "Active commercial municipality covering several adjoining neighborhoods (El Rosal, La Castellana, Country Club). Generally considered the most operationally functional part of Caracas.",
        "business_use": "Banking sector hub. Main branches of national and international banks operating in Venezuela. Many fintechs and consultancies headquartered here.",
        "what_to_avoid": "Express kidnapping risk in evening hours; do not flag street taxis.",
        "lat": 10.4980,
        "lng": -66.8510,
    },
    {
        "name": "La Castellana",
        "municipality": "Chacao",
        "safety_score": 4,
        "category": "Upscale residential",
        "summary": "Upscale residential area with a notable concentration of business-class hotels. Good walkability for the area in daylight hours.",
        "business_use": "Hotels here host most foreign-investor delegations. Good choice for short-stay accommodation.",
        "what_to_avoid": "Use only authorised transport between hotel and meetings.",
        "lat": 10.5040,
        "lng": -66.8500,
    },
    {
        "name": "El Hatillo",
        "municipality": "El Hatillo",
        "safety_score": 4,
        "category": "Tourist / colonial",
        "summary": "Colonial-era historic town centre on the eastern edge of metropolitan Caracas. Popular for daytime tourism, restaurants, and craft markets.",
        "business_use": "Limited business use; pleasant for off-day excursions for visitors.",
        "what_to_avoid": "Roads connecting to El Hatillo can be congested; avoid driving at night.",
        "lat": 10.4250,
        "lng": -66.8253,
    },
    {
        "name": "Los Palos Grandes",
        "municipality": "Chacao",
        "safety_score": 3,
        "category": "Residential / mixed",
        "summary": "Established residential area popular with the diplomatic community and middle-class professionals. Generally functional services.",
        "business_use": "Practical for medium-term rentals; some boutique offices and consultancies.",
        "what_to_avoid": "Do not display electronics or valuables in public.",
        "lat": 10.5080,
        "lng": -66.8450,
    },
    {
        "name": "Sabana Grande",
        "municipality": "Libertador",
        "safety_score": 2,
        "category": "Commercial / dense urban",
        "summary": "Historic commercial spine with mixed economic activity. Has experienced significant decline; pickpocketing and street crime are persistent.",
        "business_use": "Limited investor relevance; some legacy retail interests.",
        "what_to_avoid": "Avoid all but essential daytime visits; keep valuables out of sight.",
        "lat": 10.4960,
        "lng": -66.8780,
    },
    {
        "name": "El Centro / Catedral",
        "municipality": "Libertador",
        "safety_score": 2,
        "category": "Government / historic",
        "summary": "Historic colonial centre and seat of national government (Capitolio, Miraflores, Asamblea Nacional). Heavy security presence around government buildings, but petty crime risk elevated.",
        "business_use": "Necessary visits to the National Assembly, ministries, and Gaceta Oficial. Always with local fixer.",
        "what_to_avoid": "No casual sightseeing; visits should be purpose-driven and chaperoned.",
        "lat": 10.5060,
        "lng": -66.9135,
    },
    {
        "name": "Petare",
        "municipality": "Sucre",
        "safety_score": 1,
        "category": "Dense informal settlement",
        "summary": "One of Latin America's largest informal settlements. High homicide rates, active gang presence; not safe for foreign visitors at any time.",
        "business_use": "None.",
        "what_to_avoid": "Do not enter — including by metro or taxi pass-through.",
        "lat": 10.4700,
        "lng": -66.8200,
    },
    {
        "name": "Catia",
        "municipality": "Libertador",
        "safety_score": 1,
        "category": "Dense urban / informal",
        "summary": "Western Caracas working-class district with persistent gang activity and historic security challenges.",
        "business_use": "None.",
        "what_to_avoid": "Do not enter except with vetted local security on a documented purpose.",
        "lat": 10.5170,
        "lng": -66.9490,
    },
    {
        "name": "23 de Enero",
        "municipality": "Libertador",
        "safety_score": 1,
        "category": "Politicised housing project",
        "summary": "Dense housing project with active organised political collectives ('colectivos') and elevated crime metrics. High politicisation.",
        "business_use": "None.",
        "what_to_avoid": "No visits.",
        "lat": 10.5240,
        "lng": -66.9290,
    },
    {
        "name": "Maiquetía / Catia La Mar",
        "municipality": "Vargas (La Guaira)",
        "safety_score": 2,
        "category": "Airport / coastal",
        "summary": "Coastal corridor connecting Simón Bolívar International Airport to Caracas. Highway robbery risk on the airport-to-city road, especially at night.",
        "business_use": "Unavoidable transit on arrival/departure.",
        "what_to_avoid": "Never drive yourself between airport and city. Pre-arrange a vetted driver and travel during daylight when possible.",
        "lat": 10.6000,
        "lng": -66.9900,
    },
]


def list_caracas_neighborhoods() -> list[dict]:
    return CARACAS_NEIGHBORHOODS
