"""`insiderwatch check`: dry-run every registered connector over a raw directory.

Useful when onboarding a customer: shows how many records each source yields and why records
are being dropped, without touching the database.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import Config
from .pipeline import build_connectors


def check_raw_dir(raw_dir: Path, config: Config) -> dict[str, Any]:
    report: dict[str, Any] = {}
    for connector in build_connectors(raw_dir, config):
        events = list(connector.events())
        report[connector.source] = {
            "fetched": connector.stats.fetched,
            "emitted": connector.stats.emitted,
            "dropped": dict(connector.stats.dropped),
            "first": events[0].ts.isoformat() if events else None,
            "last": events[-1].ts.isoformat() if events else None,
            "users": len({e.user for e in events}),
        }
    return report


def unregistered_sources(raw_dir: Path, config: Config) -> list[str]:
    """Directories under raw_dir that no registered connector claims."""
    claimed = {c.source for c in build_connectors(raw_dir, config)}
    return sorted(p.name for p in Path(raw_dir).iterdir() if p.is_dir() and p.name not in claimed)
