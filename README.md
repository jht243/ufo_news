# The UAP Index

Daily UAP news and source-intelligence portal. The app scrapes official records, UAP-specific research sources, witness databases, and Google News; labels every item by source type and evidence level; generates a static daily homepage; and provides tools for checking claims, resolving cases, finding documents, and grading public evidence.

## Architecture

- `run_daily.py`: scrape -> analyze -> create briefings -> generate `output/report.html`.
- `server.py`: Flask app serving the generated homepage plus tools, cases, documents, timeline, sources, explainers, and briefings.
- `src/scraper/uap_sources.py`: AARO, NARA, NASA, Congress, Federal Register, NUFORC, The Black Vault, The Debrief, Liberation Times, and Google News scrapers.
- `src/data/uap_cases.py`: seeded case files used by `/cases` and the tools.
- Supabase Storage can bridge cron and web via `SUPABASE_REPORT_OBJECT_KEY=uap-index-report.html`.

## Local Development

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_daily.py --report-only
python server.py
```

The default local database is `sqlite:///./uap_index.db`.
