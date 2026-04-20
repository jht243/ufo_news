"""
Pre-canned SEC EDGAR full-text search presets for Venezuela / PDVSA /
impairment / contingent-liability research.

These power /tools/sec-edgar-venezuela-impairment-search. The tool's
job is to take a question that an analyst would otherwise spend 15 min
crafting in EDGAR's awkward Lucene-flavoured search UI and turn it into
a single click that opens a pre-built efts.sec.gov query.

Why this is its own module:
  - The presets are content. Every preset is a Venezuela-research
    research question phrased the way a sell-side analyst would phrase
    it ("companies that took an impairment on Venezuelan operations
    last cycle"), and we want to be able to add / remove them without
    touching server.py.
  - The query strings need to be reviewed by anyone who knows EDGAR's
    quirks. Co-locating with `src/analysis/edgar_search.py` would
    suggest they're shared with the runtime EDGAR fetcher; they're
    not — these are deeplinks into EDGAR's user-facing UI.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from urllib.parse import urlencode


# Public-facing EDGAR full-text search base URL. The user-facing UI
# at https://efts.sec.gov/LATEST/search-index/?q=… renders results in
# the browser; we deeplink into it (the JSON API in
# `src/analysis/edgar_search.py` is a different surface used server-side
# for our own EDGAR scans).
EDGAR_SEARCH_UI = "https://efts.sec.gov/LATEST/search-index"


@dataclass(frozen=True)
class EdgarPreset:
    slug: str            # short identifier for the preset card
    title: str           # human label rendered on the card
    question: str        # the research question this answers
    query: str           # raw EDGAR search "q" string (Lucene-ish)
    forms: tuple[str, ...]  # SEC forms to constrain the search to
    lookback_days: int = 730  # default 2-year window; covers ~2 cycles of 10-K filings
    why: str = ""        # one-sentence rationale explaining the preset

    def url(self) -> str:
        """Return a deeplink to EDGAR's user-facing search UI."""
        end = date.today()
        start = end - timedelta(days=self.lookback_days)
        params = {
            "q": self.query,
            "dateRange": "custom",
            "startdt": start.isoformat(),
            "enddt": end.isoformat(),
            "forms": ",".join(self.forms),
        }
        return f"{EDGAR_SEARCH_UI}?{urlencode(params)}"


# ────────────────────────────────────────────────────────────────────
# Preset catalogue
# ────────────────────────────────────────────────────────────────────
#
# Ordering matters — the first preset is the SERP / page hero. Pick the
# one most analysts will click first (the "everything" search) and put
# it at the top.

PRESETS: tuple[EdgarPreset, ...] = (
    EdgarPreset(
        slug="any-venezuela-mention",
        title="Any Venezuela / PDVSA / CITGO mention (10-K, 20-F, 10-Q)",
        question=(
            "Which public companies disclosed Venezuela, PDVSA, or CITGO "
            "in their most recent annual or quarterly reports?"
        ),
        query='"Venezuela" OR "PdVSA" OR "PDVSA" OR "CITGO" OR "Caracas"',
        forms=("10-K", "20-F", "10-Q"),
        why=(
            "The widest possible Venezuela disclosure net. Use this as the "
            "starting point — every company that mentions Venezuela in an "
            "annual or quarterly will appear here."
        ),
    ),
    EdgarPreset(
        slug="venezuela-impairment",
        title="Venezuela impairment / write-down disclosures",
        question=(
            "Which companies have booked an impairment, write-down, or "
            "deconsolidation tied to their Venezuelan operations?"
        ),
        query='("Venezuela" OR "Venezuelan") AND ("impairment" OR "write-down" OR "writedown" OR "deconsolidat*")',
        forms=("10-K", "20-F", "10-Q", "8-K"),
        why=(
            "The historical-exposure question. Most multinationals exited "
            "Venezuela between 2015 and 2020 via impairment charges or "
            "deconsolidation — this surfaces those filings."
        ),
    ),
    EdgarPreset(
        slug="pdvsa-counterparty",
        title="PDVSA / CITGO counterparty exposure",
        question=(
            "Which companies disclose PDVSA or CITGO as a customer, "
            "supplier, joint-venture partner, or off-take counterparty?"
        ),
        query='("PdVSA" OR "PDVSA" OR "Petroleos de Venezuela" OR "CITGO") AND ("joint venture" OR "counterparty" OR "off-take" OR "offtake" OR "supply agreement")',
        forms=("10-K", "20-F", "10-Q", "8-K"),
        why=(
            "PDVSA's commercial counterparties have to disclose the "
            "relationship under both materiality and OFAC-compliance rules. "
            "This is the cleanest way to enumerate them."
        ),
    ),
    EdgarPreset(
        slug="venezuela-contingent-liability",
        title="Venezuela contingent liabilities / arbitration disclosures",
        question=(
            "Which companies disclose ongoing arbitration, expropriation "
            "claims, or contingent liabilities tied to Venezuela?"
        ),
        query='("Venezuela" OR "Venezuelan") AND ("arbitration" OR "ICSID" OR "expropriation" OR "contingent liabilit*" OR "nationalization")',
        forms=("10-K", "20-F", "10-Q", "8-K"),
        why=(
            "Decades of expropriation claims (ConocoPhillips, ExxonMobil, "
            "Crystallex, etc.) are still working through ICSID and US "
            "courts. This preset surfaces who is still litigating."
        ),
    ),
    EdgarPreset(
        slug="venezuela-ofac-sanctions",
        title="Venezuela OFAC sanctions compliance disclosures",
        question=(
            "Which companies disclose OFAC Venezuela sanctions, general "
            "licenses, or sanctions-compliance risks in their filings?"
        ),
        query='("Venezuela" OR "Venezuelan") AND ("OFAC" OR "sanctions" OR "general license" OR "Office of Foreign Assets Control")',
        forms=("10-K", "20-F", "10-Q", "8-K"),
        why=(
            "Most companies that discuss OFAC Venezuela sanctions in a "
            "10-K do so because they have, or had, exposure they need to "
            "ring-fence. Useful for the compliance-officer-as-investor."
        ),
    ),
    EdgarPreset(
        slug="venezuela-bond-debt",
        title="Venezuelan sovereign / PDVSA bond exposure",
        question=(
            "Which funds or insurers hold (or held) Venezuelan sovereign "
            "or PDVSA debt and disclosed it in their reports?"
        ),
        query='("Venezuelan sovereign" OR "Republic of Venezuela bonds" OR "PdVSA bonds" OR "PDVSA bonds")',
        forms=("10-K", "20-F", "N-CSR", "N-Q"),
        why=(
            "Distressed-debt funds, EM bond funds, and insurers held "
            "Venezuela paper through default. N-CSR and N-Q forms expose "
            "fund-level holdings."
        ),
    ),
    EdgarPreset(
        slug="venezuela-citgo-collateral",
        title="CITGO / PDV Holding share-pledge & collateral disclosures",
        question=(
            "Which creditors have disclosed CITGO / PDV Holding shares as "
            "collateral, security, or judgment satisfaction?"
        ),
        query='("CITGO" OR "PDV Holding" OR "PDVH") AND ("collateral" OR "pledge*" OR "judgment" OR "Crystallex")',
        forms=("10-K", "20-F", "10-Q", "8-K"),
        why=(
            "CITGO's parent (PDVH) is the asset behind the Crystallex "
            "Delaware auction. Bondholders, judgment creditors, and "
            "advisers all touch it in their filings."
        ),
    ),
)


def list_presets() -> list[EdgarPreset]:
    return list(PRESETS)


def get_preset(slug: str) -> EdgarPreset | None:
    for p in PRESETS:
        if p.slug == slug:
            return p
    return None


# ────────────────────────────────────────────────────────────────────
# Curated "known disclosers" — the S&P 500 tickers most commonly named
# in Venezuela-related SEC filings. Used to render a quick-link table
# so visitors can jump straight to a company's EDGAR Venezuela history.
#
# Source: the curated_venezuela_exposure map (which we already maintain
# by hand). This avoids hardcoding the same fact in two places.
# ────────────────────────────────────────────────────────────────────


def _build_company_edgar_url(*, cik: str | None, company_name: str) -> str:
    """Pre-canned EDGAR search for ANY Venezuela mention in this
    company's recent filings."""
    end = date.today()
    start = end - timedelta(days=730)
    params = {
        "q": '"Venezuela" OR "PdVSA" OR "PDVSA" OR "CITGO"',
        "dateRange": "custom",
        "startdt": start.isoformat(),
        "enddt": end.isoformat(),
        "forms": "10-K,10-Q,8-K,20-F,6-K",
    }
    if cik:
        cik_clean = str(cik).strip().lstrip("0") or "0"
        params["ciks"] = cik_clean.zfill(10)
    else:
        params["company"] = company_name
    return f"{EDGAR_SEARCH_UI}?{urlencode(params)}"


@dataclass(frozen=True)
class CuratedDiscloser:
    ticker: str
    short_name: str
    exposure_level: str
    one_line: str
    profile_url: str  # /companies/<slug>/venezuela-exposure
    edgar_search_url: str  # deeplink into EDGAR for this company


def list_curated_disclosers(*, max_n: int = 30) -> list[CuratedDiscloser]:
    """Return the curated S&P 500 companies that have any non-'none'
    exposure level, sorted by exposure-level severity then ticker."""
    try:
        from src.data.curated_venezuela_exposure import _CURATED  # type: ignore
        from src.data.sp500_companies import find_company
    except Exception:
        return []

    severity = {"direct": 0, "indirect": 1, "historical": 2, "none": 9}
    rows: list[CuratedDiscloser] = []
    for ticker, entry in _CURATED.items():
        if entry.exposure_level == "none":
            continue
        company = find_company(ticker)
        if company is None:
            continue
        # Trim summary to one line for the table view; the full version
        # lives on the per-company landing page.
        first_sentence = entry.summary.split(". ")[0].rstrip(".") + "."
        rows.append(CuratedDiscloser(
            ticker=ticker,
            short_name=company.short_name,
            exposure_level=entry.exposure_level,
            one_line=first_sentence,
            profile_url=f"/companies/{company.slug}/venezuela-exposure",
            edgar_search_url=_build_company_edgar_url(
                cik=company.cik, company_name=company.short_name
            ),
        ))

    rows.sort(key=lambda r: (severity.get(r.exposure_level, 9), r.ticker))
    return rows[:max_n]
