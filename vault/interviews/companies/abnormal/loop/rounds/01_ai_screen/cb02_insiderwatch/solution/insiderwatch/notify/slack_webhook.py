"""Slack delivery. Stub: messages are written to the `outbox` table; a separate sender drains it."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from ..alerts.models import Alert
from ..config import Config
from .console import format_alert


# TODO(INSIDER-256): a sender process that drains `outbox` and POSTs to the webhook.
class SlackWebhookNotifier:
    def __init__(self, conn: sqlite3.Connection, config: Config) -> None:
        self._conn = conn
        self._config = config

    def notify(self, alert: Alert) -> None:
        payload = {"text": format_alert(alert, self._config), "alert_id": alert.id}
        with self._conn:
            self._conn.execute(
                "INSERT INTO outbox (channel, payload, created_at) VALUES (?,?,?)",
                (self._config.slack_webhook_url, json.dumps(payload), datetime.now(timezone.utc).isoformat()),
            )


def read_outbox(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT id, channel, payload, created_at FROM outbox ORDER BY id").fetchall()
    return [{"id": r["id"], "channel": r["channel"], "payload": json.loads(r["payload"]),
             "created_at": r["created_at"]} for r in rows]
