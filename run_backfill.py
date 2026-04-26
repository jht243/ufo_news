#!/usr/bin/env python3
from __future__ import annotations
from datetime import date, datetime, timedelta
import click
from rich.console import Console
from rich.panel import Panel
from src.analyzer import run_analysis
from src.blog_generator import run_blog_generation
from src.pipeline import run_daily_scrape
from src.report_generator import generate_report
console = Console()
def _parse(s): return datetime.strptime(s, "%Y-%m-%d").date()
@click.command()
@click.option("--start-date", default="2026-01-01")
@click.option("--end-date", default=None)
@click.option("--skip-analyze", is_flag=True)
@click.option("--skip-report", is_flag=True)
def main(start_date, end_date, skip_analyze, skip_report):
    start = _parse(start_date); end = _parse(end_date) if end_date else date.today()
    console.print(Panel(f"The UAP Index backfill {start} -> {end}", style="blue"))
    cur = start; total = {"articles_found": 0, "articles_new": 0, "errors": []}
    while cur <= end:
        res = run_daily_scrape(cur); total["articles_found"] += res.get("articles_found", 0); total["articles_new"] += res.get("articles_new", 0); total["errors"].extend(res.get("errors", [])); cur += timedelta(days=1)
    if not skip_analyze: total["analysis"] = run_analysis(); total["blog_generation"] = run_blog_generation()
    if not skip_report: total["report"] = str(generate_report())
    console.print(total)
if __name__ == "__main__": main()
