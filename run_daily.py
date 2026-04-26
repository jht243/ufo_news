#!/usr/bin/env python3
from __future__ import annotations
import logging, sys, time
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.config import settings
console = Console()
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO), format="%(asctime)s %(name)-28s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("run_daily")
@click.command()
@click.option("--skip-scrape", is_flag=True)
@click.option("--skip-email", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--report-only", is_flag=True)
def main(skip_scrape: bool, skip_email: bool, dry_run: bool, report_only: bool):
    console.print(Panel("[bold]The UAP Index - Daily Pipeline[/bold]", style="blue"))
    started = time.time(); results = {}
    if report_only:
        skip_scrape = True; skip_email = True
    if not skip_scrape:
        try:
            from src.pipeline import run_daily_scrape
            results["scrape"] = run_daily_scrape()
        except Exception as exc:
            logger.exception("Scrape failed"); results["scrape"] = {"error": str(exc)}
    if not report_only:
        try:
            from src.analyzer import run_analysis
            results["analysis"] = run_analysis()
        except Exception as exc:
            logger.exception("Analysis failed"); results["analysis"] = {"error": str(exc)}
        try:
            from src.blog_generator import run_blog_generation
            results["blog_generation"] = run_blog_generation()
        except Exception as exc:
            logger.exception("Blog generation failed"); results["blog_generation"] = {"error": str(exc)}
    try:
        from src.report_generator import generate_report
        path = generate_report(); results["report"] = {"path": str(path)}
    except Exception as exc:
        logger.exception("Report generation failed"); results["report"] = {"error": str(exc)}; sys.exit(1)
    table = Table(title="Pipeline Summary"); table.add_column("Phase"); table.add_column("Result")
    for k, v in results.items(): table.add_row(k, str(v))
    table.add_row("duration", f"{time.time() - started:.1f}s"); console.print(table)
if __name__ == "__main__": main()
