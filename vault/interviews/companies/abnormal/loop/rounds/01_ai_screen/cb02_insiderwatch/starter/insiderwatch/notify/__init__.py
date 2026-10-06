"""Notifiers: how an alert reaches a human. Add one by registering it in NOTIFIERS."""
from __future__ import annotations

import sqlite3
import sys
from typing import Protocol

from ..alerts.models import Alert
from ..config import Config
from ..errors import ConfigError


class Notifier(Protocol):
    def notify(self, alert: Alert) -> None: ...


def build_notifier(name: str, conn: sqlite3.Connection, config: Config) -> Notifier:
    from .console import ConsoleNotifier
    from .slack_webhook import SlackWebhookNotifier

    if name == "console":
        return ConsoleNotifier(config, stream=sys.stderr)
    if name == "slack":
        return SlackWebhookNotifier(conn, config)
    raise ConfigError(f"unknown notifier {name!r} (expected console or slack)")


__all__ = ["Notifier", "build_notifier"]
