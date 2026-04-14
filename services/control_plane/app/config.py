from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HardSecNet Control Plane"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./runtime/control_plane.db"
    secret_key: str = "hardsecnet-dev-secret-change-me-2026"
    access_token_expire_minutes: int = 720
    artifacts_dir: Path = Path("./runtime/control_plane_artifacts")
    cors_origins: str = "http://127.0.0.1:4173,http://localhost:4173,http://127.0.0.1:5173,http://localhost:5173"

    model_config = SettingsConfigDict(
        env_prefix="HARDSECNET_CP_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
