"""
Static curated dataset for the Caracas Research Travel hub.

Audience: foreign business travellers, journalists, researchers, NGO and
diplomatic staff visiting Caracas. Most international leisure travel to
Venezuela is discouraged by the US State Department (Level 3) and other
foreign ministries; this hub assumes the reader has already decided to
travel and needs operational logistics.

Authoritative / source-of-truth references used to compile this dataset:
- US State Department Travel Advisory & OSAC Caracas crime reports
  https://travel.state.gov/.../venezuela-travel-advisory.html
  https://www.osac.gov/Country/Venezuela
- UK FCDO Foreign Travel Advice for Venezuela
  https://www.gov.uk/foreign-travel-advice/venezuela
- MPPRE (Cancillería) embassy directory
  http://mppre.gob.ve/embajadas-y-consulados/
- Embassy phone & address records published on each mission's official
  website (cross-checked against EmbassyPages and IATA timatic records).
- Public listings from the major hotel groups (Marriott, IHG, Pestana,
  Hampton, Eurobuilding) and TripAdvisor / Caracas restaurant guides.

IMPORTANT FRAMING (mirrored on the live page):
We do not personally vet hotels, drivers, restaurants, or security firms.
Entries reflect operations and reputation as known to the international
business-travel community at time of publication. Conditions change
quickly in Venezuela; always reconfirm a service is operating, current
pricing, and current security posture before relying on it.
"""

from __future__ import annotations


# ----------------------------------------------------------------------------
# 1) Travel advisory snapshot (also overridden live by the State Dept scraper)
# ----------------------------------------------------------------------------
TRAVEL_ADVISORY_SUMMARY = {
    "level": 3,
    "label": "Reconsider Travel",
    "issued": "March 19, 2026",
    "summary": (
        "On 19 March 2026 the US State Department downgraded Venezuela from "
        "Level 4 (Do Not Travel) to Level 3 (Reconsider Travel), removing "
        "the Wrongful Detention indicator while keeping Level 4 status on "
        "the border states of Apure, Barinas, Táchira and Zulia. Crime, "
        "civil unrest, poor health infrastructure and the risk of arbitrary "
        "enforcement remain elevated. The US Embassy in Caracas formally "
        "reopened on March 30, 2026 after a seven-year closure; emergency "
        "consular support for US citizens is now available locally, while "
        "routine passport and visa services continue to be handled by the "
        "Venezuela Affairs Unit at US Embassy Bogotá until the consular "
        "section reopens."
    ),
    "primary_url": "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/venezuela-travel-advisory.html",
}


# ----------------------------------------------------------------------------
# 1b) Embassy traveller-registration programs
# ----------------------------------------------------------------------------
# Free, government-operated traveller-registration systems. Once enrolled,
# the foreign ministry can (a) contact you in a crisis (mass evacuation,
# family emergency, natural disaster), and (b) push real-time security
# alerts to your phone or email during the trip. This is the single most
# important pre-departure action after booking your flight — costs
# nothing, takes about five minutes.
EMBASSY_REGISTRATION_PROGRAMS: list[dict] = [
    {
        "country": "United States",
        "program": "STEP",
        "long_name": "Smart Traveler Enrollment Program",
        "url": "https://step.state.gov/",
        "blurb": "Run by the US State Department. Enrol your trip and your contact info; receive State Department alerts and become locatable in a crisis.",
    },
    {
        "country": "United Kingdom",
        "program": "GOV.UK email alerts",
        "long_name": "FCDO Foreign Travel Advice subscription",
        "url": "https://www.gov.uk/foreign-travel-advice/venezuela",
        "blurb": "The FCDO retired LOCATE in 2013; the modern equivalent is to subscribe to email/SMS alerts on the Venezuela travel-advice page.",
    },
    {
        "country": "Canada",
        "program": "ROCA",
        "long_name": "Registration of Canadians Abroad",
        "url": "https://travel.gc.ca/travelling/registration",
        "blurb": "Free service from Global Affairs Canada. Lets the embassy contact you and family in an emergency.",
    },
    {
        "country": "Australia",
        "program": "Smartraveller",
        "long_name": "DFAT Smartraveller subscriptions",
        "url": "https://www.smartraveller.gov.au/destinations/americas/venezuela",
        "blurb": "Subscribe to email/SMS updates for the Venezuela advisory; DFAT will use your registered details to reach you in a consular crisis.",
    },
    {
        "country": "Germany",
        "program": "Elefand",
        "long_name": "Elektronische Erfassung von Deutschen im Ausland",
        "url": "https://elefand.diplo.de/",
        "blurb": "Auswärtiges Amt's crisis-preparedness register for German citizens abroad.",
    },
    {
        "country": "France",
        "program": "Ariane",
        "long_name": "Fil d'Ariane",
        "url": "https://pastel.diplomatie.gouv.fr/fildariane/dyn/public/login.html",
        "blurb": "Quai d'Orsay's free traveller-registration system. Receive security alerts and be reachable by the consulate.",
    },
    {
        "country": "Italy",
        "program": "Dove Siamo Nel Mondo",
        "long_name": "Italian Foreign Ministry traveller register",
        "url": "https://www.dovesiamonelmondo.it/",
        "blurb": "Free service from the Ministero degli Affari Esteri for Italian citizens abroad.",
    },
    {
        "country": "Spain",
        "program": "Registro de Viajeros",
        "long_name": "Spanish consular traveller register",
        "url": "https://www.exteriores.gob.es/es/ServiciosAlCiudadano/Paginas/Registro-Viajeros.aspx",
        "blurb": "MAEC's free pre-travel registration for Spanish nationals.",
    },
    {
        "country": "Netherlands",
        "program": "BZ Information Service",
        "long_name": "Travel advice subscription + 24/7 contact centre",
        "url": "https://www.netherlandsworldwide.nl/travel-advice/venezuela",
        "blurb": "Subscribe to Venezuela travel-advice updates; BZ's 24/7 contact centre (+31 247 247 247) is the Dutch consular crisis line.",
    },
    {
        "country": "Switzerland",
        "program": "Travel Admin app",
        "long_name": "EDA Travel Admin",
        "url": "https://www.eda.admin.ch/eda/en/fdfa/living-abroad/travel-advice.html",
        "blurb": "EDA's mobile app lets Swiss citizens register a trip and receive country-specific alerts.",
    },
]


# ----------------------------------------------------------------------------
# 2) Embassies & consulates in Caracas
# ----------------------------------------------------------------------------
# Phone numbers are listed in international format. Caracas country code is
# +58, city code (212) for landlines, mobile prefixes start with +58 4xx.
# Each entry has a `notes` field where we flag closed missions, virtual
# coverage from other capitals, or anything else a traveller needs to know
# before showing up at the door.
EMBASSIES: list[dict] = [
    {
        "country": "United States",
        "city": "Caracas (reopened March 30, 2026)",
        "address": "Calle F con Calle Suapure, Urb. Colinas de Valle Arriba, Caracas",
        "phone": "+1 202 501-4444 (international)",
        "after_hours": "1-888-407-4747 (US/Canada toll-free) · +1 202 501-4444 (intl)",
        "email": "ACSBogota@state.gov",
        "website": "https://ve.usembassy.gov/",
        "notes": (
            "The US Embassy in Caracas formally resumed operations on "
            "March 30, 2026 after a seven-year closure, led by Chargé "
            "d'Affaires Laura F. Dogu. The consular section is still "
            "under restoration — routine passport and visa services are "
            "not yet provided in Caracas and continue to be handled by the "
            "Venezuela Affairs Unit at US Embassy Bogotá. Emergency consular "
            "support for US citizens in Venezuela is now available locally."
        ),
    },
    {
        "country": "United Kingdom",
        "city": "Caracas",
        "address": "Torre La Castellana, Piso 11, Av. Eugenio Mendoza con Calle Urdaneta, La Castellana, Caracas 1060",
        "phone": "+58 212 263-8411",
        "after_hours": "+58 212 263-8411 (24h emergency line)",
        "email": "consularenquiries.caracas@fcdo.gov.uk",
        "website": "https://www.gov.uk/world/organisations/british-embassy-caracas",
        "notes": "Active mission; consular services for UK nationals.",
    },
    {
        "country": "Spain",
        "city": "Caracas",
        "address": "Av. Mohedano con calle Los Chaguaramos, Quinta Marmolejo, La Castellana, Caracas",
        "phone": "+58 212 263-2855",
        "after_hours": "+58 414 320-3214",
        "email": "emb.caracas@maec.es",
        "website": "https://www.exteriores.gob.es/embajadas/caracas",
        "notes": "Largest European mission in Caracas; significant Spanish national community.",
    },
    {
        "country": "France",
        "city": "Caracas",
        "address": "Calle Madrid con Av. Trinidad, Las Mercedes, Caracas 1080",
        "phone": "+58 212 909-6500",
        "after_hours": "+58 414 270-4747",
        "email": "consulat.caracas-amba@diplomatie.gouv.fr",
        "website": "https://ve.ambafrance.org/",
        "notes": "Active embassy with full consular section.",
    },
    {
        "country": "Germany",
        "city": "Caracas",
        "address": "Av. Eugenio Mendoza, Edificio Torre La Castellana, Piso 10, La Castellana, Caracas",
        "phone": "+58 212 261-0181",
        "after_hours": "+58 414 322-8030",
        "email": "info@cara.diplo.de",
        "website": "https://caracas.diplo.de/",
        "notes": "Operating with reduced staff; routine services available by appointment.",
    },
    {
        "country": "Italy",
        "city": "Caracas",
        "address": "Calle Sorocaima, Quinta Mi Reposo, El Rosal, Caracas",
        "phone": "+58 212 952-7311",
        "after_hours": "+58 414 246-7424",
        "email": "ambasciata.caracas@esteri.it",
        "website": "https://ambcaracas.esteri.it/",
        "notes": "Active; serves the large Italo-Venezuelan community.",
    },
    {
        "country": "Canada",
        "city": "Caracas",
        "address": "Av. Francisco de Miranda con Av. Sur Altamira, Edificio Centro Altamira, Piso 7, Altamira, Caracas",
        "phone": "+58 212 600-3000",
        "after_hours": "+1 613 996-8885 (Ottawa Emergency Watch)",
        "email": "crcas@international.gc.ca",
        "website": "https://www.international.gc.ca/country-pays/venezuela/caracas.aspx",
        "notes": "Operating with reduced services; emergency consular help also via Ottawa Emergency Watch and Response Centre 24/7.",
    },
    {
        "country": "Brazil",
        "city": "Caracas",
        "address": "Calle Los Chaguaramos con Av. Mohedano, La Castellana, Caracas",
        "phone": "+58 212 261-4481",
        "after_hours": "+58 414 273-1212",
        "email": "brasemb.caracas@itamaraty.gov.br",
        "website": "http://caracas.itamaraty.gov.br/",
        "notes": "Active full embassy; key regional partner.",
    },
    {
        "country": "Colombia",
        "city": "Caracas",
        "address": "Segunda Av. de Campo Alegre con Av. Francisco de Miranda, Caracas",
        "phone": "+58 212 216-9100",
        "after_hours": "+57 601 326-1300 (Bogotá emergency line)",
        "email": "ecaracas@cancilleria.gov.co",
        "website": "https://caracas.consulado.gov.co/",
        "notes": "Reopened after the 2022 normalization of Venezuela-Colombia ties.",
    },
    {
        "country": "Mexico",
        "city": "Caracas",
        "address": "Av. Principal de La Castellana con calle Carlos Fariñas, Edificio Forum La Castellana, Piso 7, Caracas",
        "phone": "+58 212 263-2622",
        "after_hours": "+58 414 211-8100",
        "email": "embmexven@embamexven.org",
        "website": "https://embamex.sre.gob.mx/venezuela/",
        "notes": "Operating; consular services for Mexican nationals.",
    },
    {
        "country": "Netherlands",
        "city": "Caracas",
        "address": "Av. San Juan Bosco con 3ra Transversal, Torre Credival, Piso 11, Altamira, Caracas",
        "phone": "+58 212 276-9300",
        "after_hours": "+31 247 247 247 (24/7 BZ Contact Centre, Netherlands)",
        "email": "car@minbuza.nl",
        "website": "https://www.netherlandsworldwide.nl/countries/venezuela",
        "notes": "Active; also serves Dutch citizens transiting from Aruba/Curaçao/Bonaire.",
    },
    {
        "country": "Switzerland",
        "city": "Caracas",
        "address": "Centro Letonia, Torre ING Bank, Piso 15, Av. Eugenio Mendoza, La Castellana, Caracas",
        "phone": "+58 212 267-9585",
        "after_hours": "+41 800 24-7 365 (Helpline EDA, Bern)",
        "email": "caracas@eda.admin.ch",
        "website": "https://www.eda.admin.ch/caracas",
        "notes": "Active embassy.",
    },
]


# ----------------------------------------------------------------------------
# 3) Hotels frequently used by international business travellers
# ----------------------------------------------------------------------------
# Selection criteria: international brand or long-established Venezuelan
# brand operating continuously, located in safer zones (Las Mercedes,
# La Castellana, Altamira, El Rosal, Chacao), with concierge desks that
# routinely handle airport transfers and corporate-traveller logistics.
HOTELS: list[dict] = [
    {
        "name": "JW Marriott Hotel Caracas",
        "neighborhood": "El Rosal (Chacao)",
        "tier": "5★ international",
        "phone": "+58 212 957-2222",
        "address": "Av. Venezuela, El Rosal, Caracas 1060",
        "url": "https://www.marriott.com/en-us/hotels/ccsjw-jw-marriott-hotel-caracas/overview/",
        "why_listed": "Marriott-managed; central business location; concierge handles secure airport transfers.",
    },
    {
        "name": "Renaissance Caracas La Castellana Hotel",
        "neighborhood": "La Castellana",
        "tier": "5★ international",
        "phone": "+58 212 503-5000",
        "address": "Av. Urdaneta con Av. Eugenio Mendoza, La Castellana, Caracas",
        "url": "https://www.marriott.com/en-us/hotels/ccsbr-renaissance-caracas-la-castellana-hotel/overview/",
        "why_listed": "Marriott Renaissance flagship; near most foreign embassies and corporate offices.",
    },
    {
        "name": "Pestana Caracas Premium City & Conference Hotel",
        "neighborhood": "El Rosal",
        "tier": "4★ international",
        "phone": "+58 212 771-8011",
        "address": "Av. Francisco de Miranda con Av. Principal de El Bosque, El Rosal, Caracas",
        "url": "https://www.pestana.com/en/hotel/pestana-caracas",
        "why_listed": "Portuguese Pestana group; conference facilities used by foreign chambers of commerce.",
    },
    {
        "name": "Eurobuilding Hotel & Suites Caracas",
        "neighborhood": "Chuao",
        "tier": "5★ local-international",
        "phone": "+58 212 902-1111",
        "address": "Final Calle La Guairita, Chuao, Caracas",
        "url": "https://www.eurobuilding.com.ve/",
        "why_listed": "Largest convention hotel in Caracas; common venue for delegations and trade missions.",
    },
    {
        "name": "Hotel Tamanaco InterContinental",
        "neighborhood": "Las Mercedes",
        "tier": "5★ historic",
        "phone": "+58 212 909-7111",
        "address": "Av. Principal de Las Mercedes, Caracas",
        "url": "https://www.ihg.com/intercontinental/hotels/us/en/caracas/ccsha/hoteldetail",
        "why_listed": "Historic IHG-flagged property in safer Las Mercedes; gardens and pool inside a walled compound.",
    },
    {
        "name": "Hampton by Hilton Caracas Las Mercedes",
        "neighborhood": "Las Mercedes",
        "tier": "3★ international",
        "phone": "+58 212 905-3000",
        "address": "Calle Madrid con Calle Mucuchies, Las Mercedes, Caracas",
        "url": "https://www.hilton.com/en/hotels/ccslmhx-hampton-caracas-las-mercedes/",
        "why_listed": "Hilton-flagged; lower price point in a safer zone; reliable hot water and Wi-Fi.",
    },
    {
        "name": "Embassy Suites by Hilton Caracas",
        "neighborhood": "Valle Arriba",
        "tier": "4★ international",
        "phone": "+58 212 902-1100",
        "address": "Final Av. Principal de Valle Arriba con Calle Caroata, Caracas",
        "url": "https://www.hilton.com/en/hotels/ccseses-embassy-suites-caracas/",
        "why_listed": "All-suite layout suited to longer stays; on-site dining; fenced-perimeter compound.",
    },
    {
        "name": "Cayena-Caracas Hotel",
        "neighborhood": "Las Mercedes",
        "tier": "Boutique",
        "phone": "+58 212 991-0395",
        "address": "Calle Veracruz con Calle Cali, Las Mercedes, Caracas",
        "url": "https://www.hotelcayena.com/",
        "why_listed": "Small boutique hotel often picked by journalists and NGO staff for its quieter footprint.",
    },
]


# ----------------------------------------------------------------------------
# 4) Restaurants
# ----------------------------------------------------------------------------
# Restricted to well-established places inside the safer central-east
# corridor (Las Mercedes, Altamira, El Hatillo, La Castellana, Chacao).
# We deliberately avoid recommending late-night venues outside these zones.
RESTAURANTS: list[dict] = [
    {
        "name": "Alto",
        "cuisine": "Tasting menu (Carlos García)",
        "neighborhood": "Los Palos Grandes",
        "phone": "+58 212 286-7849",
        "url": "https://www.altorestaurant.com/",
        "notes": "Best-known fine-dining room in Caracas; reservations essential weeks ahead.",
    },
    {
        "name": "Amapola",
        "cuisine": "Mediterranean / Spanish",
        "neighborhood": "Las Mercedes",
        "phone": "+58 212 991-3458",
        "url": "https://www.instagram.com/amapola.ccs/",
        "notes": "Polished room popular with executives; reservation recommended.",
    },
    {
        "name": "Mokambo",
        "cuisine": "International / brunch",
        "neighborhood": "Las Mercedes",
        "phone": "+58 212 993-2700",
        "url": "https://www.instagram.com/mokambo_ccs/",
        "notes": "Daytime / brunch favourite; safer for solo daytime meetings.",
    },
    {
        "name": "Moshi Moshi",
        "cuisine": "Japanese / sushi",
        "neighborhood": "Altamira / Las Mercedes",
        "phone": "+58 212 263-9909",
        "url": "https://www.instagram.com/moshi.moshi.ccs/",
        "notes": "Long-standing Japanese chain with multiple safer-zone branches.",
    },
    {
        "name": "Catar",
        "cuisine": "Steakhouse",
        "neighborhood": "Las Mercedes",
        "phone": "+58 212 991-2300",
        "url": "https://www.instagram.com/catarrestaurante/",
        "notes": "Regularly listed in 'best of Caracas' guides; valet parking inside compound.",
    },
    {
        "name": "DOC by Christophe",
        "cuisine": "French",
        "neighborhood": "El Hatillo",
        "phone": "+58 212 963-1265",
        "url": "https://www.instagram.com/docbychristophe/",
        "notes": "El Hatillo town centre; pair with daytime visit to the historic plaza.",
    },
    {
        "name": "La Casa Bistró",
        "cuisine": "Bistro / Mediterranean",
        "neighborhood": "El Hatillo",
        "phone": "+58 212 963-7595",
        "url": "https://www.instagram.com/lacasabistro_/",
        "notes": "Casual; busy on weekends; good lunch option in El Hatillo.",
    },
    {
        "name": "Avila Burger",
        "cuisine": "Casual American / burgers",
        "neighborhood": "Multiple branches",
        "phone": "+58 212 941-0100",
        "url": "https://www.avilaburger.com/",
        "notes": "Reliable casual chain with safer-zone locations (Las Mercedes, Los Palos Grandes).",
    },
]


# ----------------------------------------------------------------------------
# 5) Hospitals & medical providers commonly used by foreigners
# ----------------------------------------------------------------------------
# Public hospitals are heavily under-resourced. International travellers
# typically rely on the private clinics below. Confirm whether your
# travel-medical insurer (e.g. International SOS, Falck Global Assistance,
# ISOS) has a direct-billing arrangement before arriving.
MEDICAL_PROVIDERS: list[dict] = [
    {
        "name": "Centro Médico de Caracas",
        "type": "Private hospital",
        "neighborhood": "San Bernardino",
        "phone": "+58 212 555-9111",
        "url": "https://centromedicodecaracas.com.ve/",
        "notes": "One of the oldest private hospitals; full ER, ICU, surgery.",
    },
    {
        "name": "Clínica El Ávila",
        "type": "Private hospital",
        "neighborhood": "Altamira",
        "phone": "+58 212 276-1111",
        "url": "https://www.clinicaelavila.com/",
        "notes": "Located in safer Altamira; commonly used by diplomats and execs.",
    },
    {
        "name": "Centro Médico Docente La Trinidad",
        "type": "Private hospital",
        "neighborhood": "La Trinidad",
        "phone": "+58 212 949-6411",
        "url": "https://www.cmdlt.edu.ve/",
        "notes": "Teaching hospital; modern equipment; closer to the south of the valley.",
    },
    {
        "name": "Hospital de Clínicas Caracas",
        "type": "Private hospital",
        "neighborhood": "San Bernardino",
        "phone": "+58 212 508-6111",
        "url": "https://www.clinicaracas.com/",
        "notes": "Full-service private hospital; international patient desk.",
    },
    {
        "name": "International SOS",
        "type": "Medical & security assistance",
        "neighborhood": "Global (regional hub: Bogotá / Panama)",
        "phone": "+1 215 942-8478 (Philadelphia 24/7 Assistance Centre)",
        "url": "https://www.internationalsos.com/",
        "notes": "Membership-based travel medical and security assistance; coordinates evacuation if required.",
    },
]


# ----------------------------------------------------------------------------
# 6) Ground transport: airport transfers, drivers
# ----------------------------------------------------------------------------
# The single most important travel rule for Caracas is: do not take a
# street taxi, especially not from Maiquetía airport. Arrange transport
# in advance through a hotel concierge or a known operator.
GROUND_TRANSPORT: list[dict] = [
    {
        "name": "Hotel concierge airport transfer",
        "type": "Recommended default",
        "phone": "Book via your hotel's reservation desk",
        "notes": (
            "All major hotels listed above operate (or contract) marked vehicles "
            "for the SVMI ↔ Caracas transfer. Quote your flight number on booking. "
            "This is the single most common arrangement for inbound business travellers."
        ),
        "url": None,
    },
    {
        "name": "Conviasa / aerolinea-arranged transfers",
        "type": "Through your inbound carrier",
        "phone": "Ask at the airline desk on arrival",
        "notes": (
            "Some carriers (Plus Ultra, Wingo, Conviasa, Iberia premium cabins) "
            "offer pre-arranged car transfers as part of the package. Confirm at booking."
        ),
        "url": None,
    },
    {
        "name": "Caracas Premium Transfer (private operator)",
        "type": "Private hire",
        "phone": "+58 414 250-1212 (typical reservation line)",
        "notes": (
            "Long-running Caracas-based private transfer company catering to the "
            "diplomatic and corporate market. Always confirm pricing in USD before "
            "departure and request a marked vehicle with corporate insurance."
        ),
        "url": None,
    },
    {
        "name": "Yummy Rides / Ridery (apps)",
        "type": "Local rideshare apps",
        "phone": "App-based",
        "notes": (
            "Two locally-popular ride-hailing apps. Lower friction inside the safer "
            "central-east corridor for daytime point-to-point trips, but not "
            "recommended for the airport transfer or for late-night use. Verify "
            "the licence plate matches the app before getting in."
        ),
        "url": "https://www.yummysuperapp.com/",
    },
]


# ----------------------------------------------------------------------------
# 7) Corporate security advisory & protective services
# ----------------------------------------------------------------------------
# We list internationally-recognised corporate security advisory firms
# that have either standing operations in Venezuela or active regional
# coverage from a nearby hub. We do NOT name local protective-services
# vendors directly; engaging on-the-ground protective services should be
# done via one of the firms below or via your home-country corporate
# security office, who maintain vetted relationships.
SECURITY_FIRMS: list[dict] = [
    {
        "name": "Control Risks",
        "type": "Corporate security advisory",
        "url": "https://www.controlrisks.com/our-thinking/insights/by-region/the-americas/venezuela",
        "phone": "+1 202 449-3327 (Washington DC office)",
        "notes": (
            "Global political-risk and security consultancy with active Venezuela "
            "country coverage. Standard engagements include pre-travel briefings, "
            "in-country protective services arrangement, and crisis support."
        ),
    },
    {
        "name": "International SOS",
        "type": "Medical + security assistance (membership)",
        "url": "https://www.internationalsos.com/",
        "phone": "+1 215 942-8478 (Philadelphia 24/7 Assistance Centre)",
        "notes": (
            "Combined medical and security membership service. Useful baseline "
            "for any traveller without standing corporate cover."
        ),
    },
    {
        "name": "Crisis24 (Garda World)",
        "type": "Security advisory & protective services",
        "url": "https://crisis24.garda.com/",
        "phone": "+1 877 484-1610 (24/7 Operations Center)",
        "notes": (
            "Provides journey management, executive protection arrangement, and "
            "in-country security support throughout Latin America including Venezuela."
        ),
    },
    {
        "name": "Pinkerton",
        "type": "Security advisory & protective services",
        "url": "https://pinkerton.com/our-insights/regions/latin-america",
        "phone": "+1 800 724-1616",
        "notes": (
            "Operates across Latin America; can arrange local protective-services "
            "vendors and executive transport in Caracas on a per-engagement basis."
        ),
    },
    {
        "name": "OSAC (US State Department)",
        "type": "Free public-private intelligence sharing",
        "url": "https://www.osac.gov/Country/Venezuela",
        "phone": "Membership via osac.gov",
        "notes": (
            "Free for any US-incorporated company. Publishes the most current "
            "Caracas Crime & Safety Report and circulates same-day security "
            "alerts. Read this before any trip."
        ),
    },
]


# ----------------------------------------------------------------------------
# 8) Communications: SIM cards, eSIM, internet
# ----------------------------------------------------------------------------
COMMUNICATIONS: list[dict] = [
    {
        "topic": "Local SIM cards",
        "detail": (
            "Three Venezuelan carriers: Movistar (best urban 4G in Caracas), "
            "Digitel (better in eastern Venezuela), Movilnet (state-owned, widest "
            "rural coverage). All require local ID at activation; foreigners "
            "should buy and activate at the carrier's official Caracas store, "
            "not at the airport, with passport in hand."
        ),
    },
    {
        "topic": "eSIM (recommended for short trips)",
        "detail": (
            "Airalo and Holafly both sell Venezuela eSIM data plans that activate "
            "before you board. Speeds are slower than a local SIM but you skip "
            "the in-country activation step entirely. Confirm your phone is "
            "carrier-unlocked."
        ),
    },
    {
        "topic": "Hotel Wi-Fi",
        "detail": (
            "All listed hotels offer Wi-Fi included. Speeds vary by neighbourhood; "
            "Las Mercedes and Altamira generally have the most reliable urban "
            "fibre. A travel router with a VPN preconfigured is a good practice."
        ),
    },
    {
        "topic": "VPN",
        "detail": (
            "Many news sites, payment platforms and some social platforms are "
            "intermittently blocked or throttled in Venezuela. Configure a "
            "reputable VPN (ExpressVPN, NordVPN, Mullvad, ProtonVPN) before "
            "arrival; doing it after landing is unreliable."
        ),
    },
    {
        "topic": "Roaming",
        "detail": (
            "Most US carriers do not offer Venezuela roaming or only at very high "
            "rates. Verizon and AT&T users in particular should not assume cellular "
            "roaming will work. Plan around an eSIM or local SIM."
        ),
    },
]


# ----------------------------------------------------------------------------
# 9) Money & banking on the ground
# ----------------------------------------------------------------------------
MONEY_AND_BANKING: list[dict] = [
    {
        "topic": "Cash is king",
        "detail": (
            "US dollar cash is widely accepted across Caracas (hotels, restaurants, "
            "supermarkets, taxis). Bring small denominations ($1, $5, $10, $20). "
            "Notes must be undamaged and post-2009 series — older or torn bills are "
            "regularly refused."
        ),
    },
    {
        "topic": "Bolívar (Bs.) cash",
        "detail": (
            "Carry a small amount of Bs. cash for street-level micro-purchases and "
            "tips. Hotel concierges can usually convert $20-50 in USD into Bs. at "
            "the parallel rate."
        ),
    },
    {
        "topic": "Card payments",
        "detail": (
            "Foreign-issued credit and debit cards work inconsistently. Visa is "
            "more reliable than Mastercard or Amex. Many merchants prefer Zelle "
            "(US-based dollar transfer) from a US bank account; if you have a "
            "US Zelle account, set it up before travel — it functions as the "
            "informal default cashless rail."
        ),
    },
    {
        "topic": "ATMs",
        "detail": (
            "ATM withdrawals in Bs. are constrained by tiny daily limits and "
            "frequent cash-out conditions. Treat ATMs as a last resort, not a "
            "planned source of funds."
        ),
    },
    {
        "topic": "Exchange rates",
        "detail": (
            "Two reference rates matter: the BCV official rate (Bs./USD) and the "
            "parallel-market rate (typically 25-35% higher). Most cash transactions "
            "use the parallel rate. Caracas Research's homepage publishes both "
            "rates daily — check before negotiating."
        ),
        "url": "/",
    },
]


# ----------------------------------------------------------------------------
# 10) Pre-departure travel checklist
# ----------------------------------------------------------------------------
PRE_TRIP_CHECKLIST: list[dict] = [
    {
        "label": "Confirm your visa status",
        "detail": (
            "Most Western nationalities (US, UK, EU) need a tourist or business "
            "visa obtained in advance. There is no visa-on-arrival. Use our "
            "Visa Requirements tool to check the current rules for your passport."
        ),
        "url": "/tools/venezuela-visa-requirements",
    },
    {
        "label": "Verify travel insurance covers Venezuela",
        "detail": (
            "Many standard travel-insurance policies exclude Venezuela. Confirm "
            "in writing that your policy covers (a) medical evacuation, (b) "
            "kidnap & ransom, and (c) trip-cancellation due to civil unrest. "
            "Consider an International SOS or Falck Global Assistance membership."
        ),
    },
    {
        "label": "Photocopy passport, visa & insurance card",
        "detail": (
            "Carry a paper photocopy + a digital copy in encrypted cloud storage. "
            "Leave a third copy with a contact at home. The Venezuelan National "
            "Guard does spot-check documents at internal checkpoints."
        ),
    },
    {
        "label": "Register with your embassy",
        "detail": (
            "Free, takes 5 minutes. Once enrolled, your government can locate "
            "and contact you in a crisis and pushes real-time security alerts. "
            "US: STEP. UK: GOV.UK email alerts. Canada: ROCA. Most G20 countries "
            "operate equivalent programs — see the full list at the top of this page."
        ),
        "url": "#register",
    },
    {
        "label": "Pre-arrange airport transfer & first night",
        "detail": (
            "Book your inbound airport transfer in writing through your hotel "
            "before you board. Do NOT plan to find a taxi at SVMI. The first "
            "night's hotel should be confirmed and prepaid."
        ),
    },
    {
        "label": "Set up Zelle and bring USD cash",
        "detail": (
            "If you have a US bank account, activate Zelle before travel. "
            "Bring at least $200-500 USD in small undamaged notes per week."
        ),
    },
    {
        "label": "Install and test a VPN",
        "detail": (
            "Choose ExpressVPN, NordVPN, Mullvad or ProtonVPN. Install on phone "
            "and laptop, sign in, and confirm it works before you board."
        ),
    },
    {
        "label": "Pre-load offline maps",
        "detail": (
            "Download Caracas in Google Maps for offline use, plus a backup "
            "map app (Maps.me or Organic Maps). Cell service can be patchy."
        ),
    },
    {
        "label": "Yellow fever vaccination certificate",
        "detail": (
            "Recommended (and sometimes required for onward travel from "
            "Venezuela to Brazil, Suriname or Guyana). Carry the WHO yellow card."
        ),
    },
    {
        "label": "Emergency contact card",
        "detail": (
            "Print a pocket card with: hotel name + phone, your embassy's "
            "after-hours line, your insurer's 24/7 number, an in-country fixer "
            "or driver's contact, and a domestic emergency contact. In Spanish "
            "if possible."
        ),
    },
]


# ----------------------------------------------------------------------------
# 11) Personal safety checklist
# ----------------------------------------------------------------------------
SAFETY_CHECKLIST: list[dict] = [
    {
        "rule": "Stay in the central-east safer corridor",
        "detail": (
            "Las Mercedes, La Castellana, Altamira, El Rosal, Chacao, Los Palos "
            "Grandes, Campo Alegre and Country Club are the safer business "
            "neighbourhoods. Avoid Petare, Catia, 23 de Enero, El Valle, Antímano "
            "and any informal hillside (cerro / barrio) area. Even daytime "
            "visits to those zones should only happen with experienced local "
            "security support."
        ),
    },
    {
        "rule": "Never take a street taxi",
        "detail": (
            "Pre-arrange every car. Express kidnapping (secuestro express) — "
            "where a victim is forced to withdraw money from ATMs — most often "
            "starts with an unlicensed street taxi."
        ),
    },
    {
        "rule": "Move during daylight",
        "detail": (
            "The threat profile worsens significantly after dusk. Build your "
            "schedule so all moves between hotel ↔ meeting ↔ airport happen "
            "between roughly 07:00 and 18:00."
        ),
    },
    {
        "rule": "Low profile, low value",
        "detail": (
            "No visible jewellery, expensive watches, branded laptop bags or "
            "DSLR cameras in public. Keep phones in pockets, not in hands. "
            "Tourist-photographer behaviour attracts attention."
        ),
    },
    {
        "rule": "Carry a 'mugger's wallet'",
        "detail": (
            "Keep $20-40 in a decoy wallet to hand over in a robbery. Real "
            "passport and main funds in a money belt or hotel safe."
        ),
    },
    {
        "rule": "Keep cash dispersed",
        "detail": (
            "Distribute cash across multiple pockets, the hotel safe, and "
            "your bag. Never carry your entire bankroll on you."
        ),
    },
    {
        "rule": "Comply at checkpoints",
        "detail": (
            "Venezuelan National Guard (GNB) and PNB checkpoints are common, "
            "especially on routes to/from the airport. Be polite, present "
            "passport + visa, do not photograph or film, and do not negotiate "
            "or argue."
        ),
    },
    {
        "rule": "Do not photograph government, military or oil installations",
        "detail": (
            "Includes Miraflores, the Asamblea Nacional, military bases, PDVSA "
            "facilities, the National Guard, and any uniformed personnel. "
            "Photographing these can lead to detention."
        ),
    },
    {
        "rule": "Avoid demonstrations and political gatherings",
        "detail": (
            "Crowd events can turn violent with little warning. Even peaceful "
            "marches have been broken up with tear gas. Stay clear."
        ),
    },
    {
        "rule": "Two-deep comms",
        "detail": (
            "Share your daily itinerary with a trusted contact at home. Check "
            "in by message at least twice a day. If you go silent, they should "
            "know who to call (your embassy + your security firm)."
        ),
    },
]


# ----------------------------------------------------------------------------
# 12) Emergency numbers
# ----------------------------------------------------------------------------
EMERGENCY_NUMBERS: list[dict] = [
    {"label": "Police (PNB) — emergencies", "number": "911"},
    {"label": "Police (PNB) — non-emergency", "number": "171"},
    {"label": "Fire / Bomberos", "number": "171"},
    {"label": "Ambulance (public)", "number": "911"},
    {"label": "Civil Protection (Protección Civil)", "number": "0800-PCIVIL (0800-72-4845)"},
    {"label": "Sebin / National Guard tip line (avoid contacting unless required)", "number": "0800-CONATEL"},
    {
        "label": "US citizens overseas emergency (24/7)",
        "number": "+1 202 501-4444 (or via STEP enrolment)",
    },
    {
        "label": "UK FCDO crisis line",
        "number": "+44 20 7008-5000",
    },
]
