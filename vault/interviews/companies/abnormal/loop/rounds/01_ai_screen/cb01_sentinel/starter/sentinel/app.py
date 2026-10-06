"""Composition root: wires db, settings, pipeline and the HTTP API together."""
from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sentinel.api import ApiApp, ApiContext, TokenStore
from sentinel.config import SettingsProvider
from sentinel.db import connect, migrate
from sentinel.pipeline import Pipeline
from sentinel.timeutil import utcnow


@dataclass
class App:
    conn: sqlite3.Connection
    settings: SettingsProvider
    pipeline: Pipeline
    wsgi: ApiApp


def create_app(
    *,
    db_path: str | Path = ":memory:",
    config_dir: Path | None = None,
    fixtures_dir: Path | None = None,
    clock: Callable[[], datetime] = utcnow,
) -> App:
    """Open the database (migrating it), and build the pipeline and API around it."""
    conn = connect(db_path)
    migrate(conn)
    settings = SettingsProvider(config_dir, fixtures_dir)
    tokens = TokenStore(settings.fixtures_dir / "tokens.json")
    return App(
        conn=conn,
        settings=settings,
        pipeline=Pipeline(conn, settings, clock),
        wsgi=ApiApp(ApiContext.build(conn, settings), tokens),
    )
