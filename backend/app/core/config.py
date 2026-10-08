from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables
    or the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # Application
    # ==========================================================

    app_name: str = Field(
        default="AI E-Commerce Assistant"
    )

    app_version: str = Field(
        default="1.0.0"
    )

    environment: str = Field(
        default="development"
    )

    debug: bool = Field(
        default=True
    )

    # ==========================================================
    # Database
    # ==========================================================

    postgres_host: str

    postgres_port: int = 5432

    postgres_db: str

    postgres_user: str

    postgres_password: str

    database_url: str

    # ==========================================================
    # Google Gemini
    # ==========================================================

    google_api_key: str = Field(
        default=""
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash"
    )

    # ==========================================================
    # Pricing
    # ==========================================================

    tax_rate: float = Field(
        default=0.18
    )

    shipping_charge: float = Field(
        default=100.0
    )

    free_shipping_threshold: float = Field(
        default=1000.0
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()


settings = get_settings()