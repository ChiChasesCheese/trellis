"""Per-tenant notification channel configuration (sqlite)."""
from __future__ import annotations

import sqlite3

from .models import Channel


class ConfigStore:
    def __init__(self, path: str = ":memory:"):
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS channels ("
            " tenant_id TEXT NOT NULL, kind TEXT NOT NULL, target TEXT NOT NULL,"
            " secret TEXT NOT NULL DEFAULT '', min_severity INTEGER NOT NULL DEFAULT 1,"
            " enabled INTEGER NOT NULL DEFAULT 1)"
        )
        self._db.commit()

    def add_channel(self, ch: Channel, enabled: bool = True) -> None:
        self._db.execute(
            "INSERT INTO channels (tenant_id, kind, target, secret, min_severity, enabled) VALUES (?,?,?,?,?,?)",
            (ch.tenant_id, ch.kind, ch.target, ch.secret, ch.min_severity, int(enabled)),
        )
        self._db.commit()

    def channels_for(self, tenant_id: str) -> list[Channel]:
        sql = (
            "SELECT tenant_id, kind, target, secret, min_severity FROM channels "
            f"WHERE tenant_id = '{tenant_id}' AND enabled = 1 ORDER BY rowid"
        )
        return [Channel(*row) for row in self._db.execute(sql).fetchall()]
