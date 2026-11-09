"""Database connection and table creation (SQLite)."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Engine, event
from sqlmodel import SQLModel, create_engine

DEFAULT_DB_PATH = "data/jobs.db"


def get_db_path() -> Path:
    """Return the database file path.

    Reads `JOBS_DB_PATH` from the environment or the `.env` file.
    Falls back to `data/jobs.db`.
    """
    load_dotenv()
    return Path(os.environ.get("JOBS_DB_PATH", DEFAULT_DB_PATH))


def get_engine(url: str | None = None) -> Engine:
    """Create a database engine.

    Pass a `url` such as "sqlite://" for an in-memory database (used by tests).
    Without a url, the engine uses the file from `get_db_path()`.
    """
    engine = create_engine(url or f"sqlite:///{get_db_path().as_posix()}")

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _record) -> None:
        # SQLite ignores foreign keys unless this is switched on for each connection.
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def init_db(engine: Engine) -> None:
    """Create all tables that do not exist yet."""
    from job_hunter import models  # noqa: F401  (loading the models registers the tables)

    SQLModel.metadata.create_all(engine)
