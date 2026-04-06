from __future__ import annotations

from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine

from .config import settings


def _normalize_sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///./"):
        absolute = Path.cwd() / url.removeprefix("sqlite:///./")
        absolute.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{absolute.as_posix()}"
    return url


DATABASE_URL = _normalize_sqlite_url(settings.database_url)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
