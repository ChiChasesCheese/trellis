"""Customer-managed suppression of rule hits.

A suppression mutes one rule for one tenant, optionally only when the event matches every
condition in ``match``. Conditions are dotted paths into the event as the rules see it:
``user``, ``src_ip``, ``kind``, ``source``, ``attrs.<key>`` and ``<enricher name>.<key>``
(e.g. ``geo.country``). A value is compared for equality, a list means any-of, and a
``src_ip`` value containing ``/`` is a CIDR block.

Suppressions are applied between rule evaluation and alert creation, so rules stay unaware of them.
"""
from __future__ import annotations

import ipaddress
import json
import logging
import sqlite3
import uuid
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from sentinel import metrics
from sentinel.models import RuleHit, SecurityEvent
from sentinel.timeutil import iso, parse_ts, utcnow

log = logging.getLogger(__name__)


@dataclass
class Suppression:
    id: str
    tenant_id: str
    rule_id: str
    created_at: datetime
    match: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "match": self.match,
            "created_at": iso(self.created_at),
        }


class SuppressionRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add(self, s: Suppression) -> None:
        self.conn.execute(
            "INSERT INTO suppressions (id, tenant_id, rule_id, match, created_at) VALUES (?, ?, ?, ?, ?)",
            (s.id, s.tenant_id, s.rule_id, json.dumps(s.match, sort_keys=True), iso(s.created_at)),
        )
        self.conn.commit()

    def list(self, tenant_id: str, rule_id: str | None = None) -> list[Suppression]:
        sql, args = "SELECT * FROM suppressions WHERE tenant_id = ?", [tenant_id]
        if rule_id:
            sql += " AND rule_id = ?"
            args.append(rule_id)
        rows = self.conn.execute(sql + " ORDER BY created_at, id", args).fetchall()
        return [self._row(r) for r in rows]

    def delete(self, tenant_id: str, suppression_id: str) -> bool:
        cur = self.conn.execute(
            "DELETE FROM suppressions WHERE tenant_id = ? AND id = ?", (tenant_id, suppression_id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def record_hit(self, s: Suppression, event: SecurityEvent, at: datetime) -> None:
        self.conn.execute(
            "INSERT INTO suppressed_hits (tenant_id, suppression_id, rule_id, event_id, suppressed_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (s.tenant_id, s.id, s.rule_id, event.id, iso(at)),
        )
        self.conn.commit()

    @staticmethod
    def _row(row: sqlite3.Row) -> Suppression:
        return Suppression(
            id=row["id"],
            tenant_id=row["tenant_id"],
            rule_id=row["rule_id"],
            match=json.loads(row["match"]),
            created_at=parse_ts(row["created_at"]),
        )


def new_suppression(tenant_id: str, rule_id: str, match: dict[str, Any], now: datetime) -> Suppression:
    return Suppression(id=f"sup_{uuid.uuid4().hex[:10]}", tenant_id=tenant_id, rule_id=rule_id, match=match, created_at=now)


def _lookup(event: SecurityEvent, path: str) -> Any:
    """Resolve a dotted path against the event, enrichment results included."""
    root, _, rest = path.partition(".")
    if root in ("user", "src_ip", "kind", "source"):
        return getattr(event, root) if not rest else None
    node: Any = {"attrs": event.attrs, **event.enrichment}.get(root)
    for part in rest.split(".") if rest else []:
        node = node.get(part) if isinstance(node, dict) else None
    return node


def _value_matches(path: str, expected: Any, actual: Any) -> bool:
    if actual is None:
        return False
    if isinstance(expected, list):
        return any(_value_matches(path, e, actual) for e in expected)
    if path == "src_ip" and isinstance(expected, str) and "/" in expected:
        try:
            return ipaddress.ip_address(actual) in ipaddress.ip_network(expected, strict=False)
        except ValueError:
            return False
    return str(expected) == str(actual)


def matches(s: Suppression, event: SecurityEvent) -> bool:
    return all(_value_matches(p, v, _lookup(event, p)) for p, v in s.match.items())


class SuppressionService:
    def __init__(self, repo: SuppressionRepository, clock: Callable[[], datetime] = utcnow):
        self.repo = repo
        self.clock = clock

    def apply(self, event: SecurityEvent, hits: Sequence[RuleHit]) -> list[RuleHit]:
        """Drop the hits this tenant has suppressed; every dropped hit is counted and audited."""
        if not hits:
            return []
        active = self.repo.list(event.tenant_id)
        kept: list[RuleHit] = []
        for hit in hits:
            hit_by = next((s for s in active if s.rule_id == hit.rule_id and matches(s, event)), None)
            if hit_by is None:
                kept.append(hit)
                continue
            log.info("suppressed %s on event %s (suppression %s)", hit.rule_id, event.id, hit_by.id)
            metrics.incr("suppression.applied", rule=hit.rule_id)
            self.repo.record_hit(hit_by, event, self.clock())
        return kept
