"""Who has emailed whom. A directed, per-tenant graph persisted in ``comm_edges``.

One edge per ordered (sender, recipient) pair, holding the first and the most recent contact and a
message count. Edges are recorded *after* an event has been evaluated, so a detector asking
``first_contact`` about an event never sees that event's own edges.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime

from rulelang.models import Event
from rulelang.timeutil import iso, parse_ts


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    first_ts: datetime
    last_ts: datetime
    count: int


def _edge(row: sqlite3.Row) -> Edge:
    return Edge(
        src=row["src"],
        dst=row["dst"],
        first_ts=parse_ts(row["first_ts"]),
        last_ts=parse_ts(row["last_ts"]),
        count=row["count"],
    )


class CommGraph:
    def __init__(self, conn: sqlite3.Connection, tenant_id: str):
        self.conn = conn
        self.tenant_id = tenant_id

    def record(self, event: Event) -> None:
        """Add the edges an email creates (sender -> each recipient). Other event kinds are ignored."""
        if event.kind != "email":
            return
        ts = iso(event.ts)
        for dst in sorted(set(event.recipients)):
            self.conn.execute(
                "INSERT INTO comm_edges (tenant_id, src, dst, first_ts, last_ts, count) VALUES (?,?,?,?,?,1)"
                " ON CONFLICT (tenant_id, src, dst) DO UPDATE SET"
                " first_ts = MIN(first_ts, excluded.first_ts), last_ts = MAX(last_ts, excluded.last_ts),"
                " count = count + 1",
                (self.tenant_id, event.actor, dst, ts, ts),
            )
        self.conn.commit()

    def neighbors(self, addr: str) -> list[Edge]:
        """Outgoing edges of ``addr``: everyone it has emailed, oldest relationship first."""
        rows = self.conn.execute(
            "SELECT * FROM comm_edges WHERE tenant_id = ? AND src = ? ORDER BY first_ts, dst",
            (self.tenant_id, addr),
        ).fetchall()
        return [_edge(r) for r in rows]

    def first_contact(self, a: str, b: str) -> datetime | None:
        """When ``a`` first emailed ``b``; ``None`` if it never has."""
        row = self.conn.execute(
            "SELECT first_ts FROM comm_edges WHERE tenant_id = ? AND src = ? AND dst = ?",
            (self.tenant_id, a, b),
        ).fetchone()
        return parse_ts(row["first_ts"]) if row else None
