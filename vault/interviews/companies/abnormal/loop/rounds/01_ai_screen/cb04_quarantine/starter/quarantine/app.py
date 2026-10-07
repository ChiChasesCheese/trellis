"""Composition root: wires db, settings, analyzers, mailbox and the HTTP API together."""
from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from quarantine.actions import ActionService, FakeMailbox, Mailbox
from quarantine.analyzers import AnalysisContext, AnalyzerRunner
from quarantine.api import ApiApp, ApiContext, TokenStore
from quarantine.config import SettingsProvider
from quarantine.intake import IntakeService
from quarantine.lookups import FixtureUrlLookup, SenderIntel, UrlLookup
from quarantine.store import ActionLogRepository, ReportRepository, connect, migrate
from quarantine.timeutil import utcnow


@dataclass
class App:
    conn: sqlite3.Connection
    settings: SettingsProvider
    mailbox: Mailbox
    reports: ReportRepository
    action_log: ActionLogRepository
    actions: ActionService
    intake: IntakeService
    wsgi: ApiApp


def create_app(
    *,
    db_path: str | Path = ":memory:",
    config_dir: Path | None = None,
    fixtures_dir: Path | None = None,
    clock: Callable[[], datetime] = utcnow,
    mailbox: Mailbox | None = None,
    url_lookup: UrlLookup | None = None,
) -> App:
    """Open the database (migrating it), and build intake, actions and the API around it."""
    conn = connect(db_path)
    migrate(conn)
    settings = SettingsProvider(config_dir, fixtures_dir)
    mailbox = mailbox if mailbox is not None else FakeMailbox()
    reports = ReportRepository(conn)
    action_log = ActionLogRepository(conn)
    actions = ActionService(mailbox, reports, action_log, clock)
    intel = settings.fixtures_dir / "intel"
    ctx = AnalysisContext(
        settings=settings,
        reports=reports,
        url_lookup=url_lookup or FixtureUrlLookup(intel / "urls.json"),
        sender_intel=SenderIntel(intel / "senders.json"),
    )
    runner = AnalyzerRunner(ctx)
    intake = IntakeService(settings, reports, runner, actions, mailbox, clock)
    tokens = TokenStore(settings.fixtures_dir / "tokens.json")
    return App(
        conn=conn,
        settings=settings,
        mailbox=mailbox,
        reports=reports,
        action_log=action_log,
        actions=actions,
        intake=intake,
        wsgi=ApiApp(ApiContext(conn, settings, reports, intake, actions), tokens),
    )
