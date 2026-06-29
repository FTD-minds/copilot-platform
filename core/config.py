"""Platform configuration (12-factor: all config via environment)."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    # Model-agnostic provider selection (overridable per request)
    llm_provider: str = "mock"          # mock | anthropic | openai
    llm_model: str = "mock-1"

    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    database_url: str = "postgresql://copilot:copilot@localhost:5432/copilot"


def get_settings() -> Settings:
    return Settings()
