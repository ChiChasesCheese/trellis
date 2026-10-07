"""Read ``*.jsonl`` event files into ``Event`` objects.

Row shapes (``tenant``, ``id``, ``ts``, ``kind`` always present):

    email                  from, to[], subject, links[]
    login                  user, ip, country, lat, lon
    mailbox_rule_created   user, rule_name, forward_to

A bad row is counted (``loader.bad_record``) and skipped; one bad line never loses a file.
"""
from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from rulelang import metrics
from rulelang.addresses import normalize_address
from rulelang.errors import BadRecord
from rulelang.models import EVENT_KINDS, Event
from rulelang.timeutil import parse_ts

log = logging.getLogger(__name__)


def _need(row: dict[str, Any], *keys: str) -> None:
    missing = [k for k in keys if not row.get(k)]
    if missing:
        raise BadRecord("missing_field", f"missing {', '.join(missing)}")


def parse_row(row: dict[str, Any]) -> Event:
    """Build an ``Event`` from one decoded row; raises ``BadRecord``."""
    _need(row, "id", "tenant", "ts", "kind")
    kind = row["kind"]
    if kind not in EVENT_KINDS:
        raise BadRecord("unknown_kind", f"unknown kind {kind!r}")
    try:
        ts = parse_ts(row["ts"])
    except (ValueError, TypeError) as exc:
        raise BadRecord("bad_ts", f"bad timestamp {row['ts']!r}") from exc

    common = dict(id=str(row["id"]), tenant_id=row["tenant"], kind=kind, ts=ts)
    if kind == "email":
        _need(row, "from", "to")
        return Event(
            **common,
            actor=normalize_address(row["from"]),
            recipients=tuple(normalize_address(r) for r in row["to"]),
            subject=row.get("subject", ""),
            links=tuple(row.get("links", [])),
        )
    _need(row, "user")
    actor = normalize_address(row["user"])
    if kind == "login":
        attrs = {k: row[k] for k in ("ip", "country", "lat", "lon") if k in row}
    else:
        _need(row, "forward_to")
        attrs = {"rule_name": row.get("rule_name", ""), "forward_to": normalize_address(row["forward_to"])}
    return Event(**common, actor=actor, attrs=attrs)


def load_events(root: Path, tenant_id: str) -> Iterator[Event]:
    """Yield the tenant's events from every ``*.jsonl`` file under ``root`` (rows of other tenants are skipped)."""
    for path in sorted(Path(root).glob("*.jsonl")):
        with path.open() as fh:
            for lineno, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise BadRecord("not_object", "row is not an object")
                    if row.get("tenant") != tenant_id:
                        metrics.incr("loader.other_tenant")
                        continue
                    yield parse_row(row)
                except (BadRecord, json.JSONDecodeError) as exc:
                    reason = exc.reason if isinstance(exc, BadRecord) else "bad_json"
                    metrics.incr("loader.bad_record", reason=reason)
                    log.warning("%s:%d skipped: %s", path.name, lineno, exc)
