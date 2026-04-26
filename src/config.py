from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"extra": "ignore"}

    database_url: str = "sqlite:///./uap_index.db"
    storage_dir: Path = Path("./storage")
    output_dir: Path = Path("./output")
    log_level: str = "INFO"

    scraper_timeout_seconds: int = 30
    scraper_max_retries: int = 3
    scraper_retry_delay_seconds: int = 60
    scraper_lookback_days: int = 30

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_premium_model: str = "gpt-5.2"
    analysis_min_relevance: int = 4
    report_lookback_days: int = 120
    llm_call_budget_per_run: int = 80
    llm_input_price_per_mtok: float = 2.50
    llm_output_price_per_mtok: float = 10.00

    newsletter_provider: str = "console"
    newsletter_from_email: str = "briefing@uapindex.com"
    newsletter_api_key: str = ""
    buttondown_api_key: str = ""
    subscriber_list_path: str = "subscribers.json"

    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_report_bucket: str = "reports"
    supabase_report_object_key: str = "uap-index-report.html"

    server_port: int = 8080
    admin_token: str = ""

    site_url: str = "https://uapindex.com"
    site_name: str = "The UAP Index"
    site_owner_org: str = "The UAP Index"
    site_locale: str = "en_US"

    blog_gen_budget_per_run: int = 8
    blog_gen_min_relevance: int = 5
    blog_gen_lookback_days: int = 14
    blog_gen_max_words: int = 900
    google_news_daily_cap: int = 12

    indexnow_key: str = "0b2fff2a4cb56ba2c10382745f51cdd8"
    google_indexing_sa_json: str = ""
    google_indexing_sa_file: str = ""
    google_indexing_lookback_days: int = 7
    google_indexing_max_per_run: int = 50
    internet_archive_access_key: str = ""
    internet_archive_secret_key: str = ""
    internet_archive_collection: str = "opensource"
    internet_archive_max_per_run: int = 5
    zenodo_access_token: str = ""
    zenodo_use_sandbox: bool = False
    zenodo_community: str = ""
    zenodo_max_per_run: int = 3
    osf_access_token: str = ""
    osf_project_node_id: str = ""
    osf_preprint_provider: str = "osf"
    osf_subject_id: str = "584240da54be81056cecaab4"
    osf_license_name: str = "CC-By Attribution 4.0 International"
    osf_max_per_run: int = 3
    bluesky_handle: str = ""
    bluesky_app_password: str = ""


settings = Settings()
