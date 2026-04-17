"""
Generate or regenerate evergreen landing pages (pillar + sectors).

These pages use the premium model (settings.openai_premium_model) so
each generation costs more than a daily blog post — but they're
generated weekly at most, not per-request.

Usage:
    python scripts/generate_landing_pages.py --pillar
    python scripts/generate_landing_pages.py --sector mining
    python scripts/generate_landing_pages.py --all-sectors
    python scripts/generate_landing_pages.py --pillar --force
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


EXPLAINERS = [
    {
        "slug": "what-are-ofac-sanctions-on-venezuela",
        "title": "What Are OFAC Sanctions on Venezuela? A Plain-English Guide",
        "intent": "what are OFAC sanctions on Venezuela / how do US sanctions on Venezuela work",
    },
    {
        "slug": "what-is-the-banco-central-de-venezuela",
        "title": "What Is the Banco Central de Venezuela (BCV)? A 2026 Guide",
        "intent": "what is the BCV / Banco Central de Venezuela explained",
    },
    {
        "slug": "venezuelan-bolivar-explained",
        "title": "The Venezuelan Bolívar Explained: History, Devaluations, and Today's Rate",
        "intent": "what is the bolivar / why has the bolivar devalued",
    },
    {
        "slug": "how-to-buy-venezuelan-bonds",
        "title": "How to Buy Venezuelan Sovereign and PDVSA Bonds in 2026",
        "intent": "how to buy Venezuelan bonds / PDVSA bond investing",
    },
    {
        "slug": "doing-business-in-caracas",
        "title": "Doing Business in Caracas: An Operating Manual for Foreign Investors",
        "intent": "doing business in Caracas / Caracas business etiquette / how to set up a company in Venezuela",
    },
]


DEFAULT_SECTORS = [
    "mining",
    "diplomatic",
    "governance",
    "sanctions",
    "legal",
    "real-estate",
    "energy",
    "oil-gas",
    "banking",
    "economic",
    "agriculture",
    "telecom",
    "tourism",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pillar", action="store_true", help="Generate the /invest-in-venezuela pillar page")
    parser.add_argument("--sector", type=str, default=None, help="Generate one /sectors/{slug} page")
    parser.add_argument("--all-sectors", action="store_true", help="Generate all sector pages")
    parser.add_argument("--explainer", type=str, default=None, help="Generate one /explainers/{slug} page")
    parser.add_argument("--all-explainers", action="store_true", help="Generate all evergreen explainers")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if recently updated")
    args = parser.parse_args()

    if not (args.pillar or args.sector or args.all_sectors or args.explainer or args.all_explainers):
        parser.error("must pass at least one of --pillar / --sector / --all-sectors / --explainer / --all-explainers")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
    )
    log = logging.getLogger("generate_landing_pages")

    from src.landing_generator import generate_explainer, generate_pillar_page, generate_sector_page

    total_cost = 0.0

    if args.pillar:
        log.info("generating pillar page (premium model)")
        page = generate_pillar_page(force=args.force)
        log.info("pillar -> %s (%d words, $%.4f)", page.canonical_path, page.word_count or 0, page.llm_cost_usd or 0.0)
        total_cost += page.llm_cost_usd or 0.0

    sectors_to_generate: list[str] = []
    if args.sector:
        sectors_to_generate.append(args.sector)
    if args.all_sectors:
        sectors_to_generate.extend(DEFAULT_SECTORS)

    for slug in sectors_to_generate:
        log.info("generating sector page: %s (premium model)", slug)
        page = generate_sector_page(slug, force=args.force)
        log.info("sector %s -> %s (%d words, $%.4f)", slug, page.canonical_path, page.word_count or 0, page.llm_cost_usd or 0.0)
        total_cost += page.llm_cost_usd or 0.0

    explainers_to_run: list[dict] = []
    if args.explainer:
        match = next((e for e in EXPLAINERS if e["slug"] == args.explainer), None)
        if not match:
            parser.error(f"unknown explainer slug: {args.explainer}. Known: {[e['slug'] for e in EXPLAINERS]}")
        explainers_to_run.append(match)
    if args.all_explainers:
        explainers_to_run.extend(EXPLAINERS)

    for ex in explainers_to_run:
        log.info("generating explainer: %s (premium model)", ex["slug"])
        page = generate_explainer(ex["slug"], topic_title=ex["title"], search_intent=ex["intent"], force=args.force)
        log.info("explainer %s -> %s (%d words, $%.4f)", ex["slug"], page.canonical_path, page.word_count or 0, page.llm_cost_usd or 0.0)
        total_cost += page.llm_cost_usd or 0.0

    log.info("done. total cost: $%.4f", total_cost)


if __name__ == "__main__":
    main()
