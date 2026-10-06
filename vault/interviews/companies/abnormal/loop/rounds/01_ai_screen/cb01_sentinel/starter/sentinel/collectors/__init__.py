"""Collectors turn raw source files into SecurityEvents. Importing this package registers them all."""
from __future__ import annotations

from pathlib import Path

from sentinel.collectors import auth_log, endpoint, saas_audit  # noqa: F401  (registration side effect)
from sentinel.collectors.base import Collector
from sentinel.collectors.registry import COLLECTORS, register_collector
from sentinel.models import SecurityEvent


def collect_all(root: Path, tenant_id: str) -> list[SecurityEvent]:
    """Run every registered collector over ``root`` and return the tenant's events, oldest first."""
    events: list[SecurityEvent] = []
    for cls in COLLECTORS.values():
        events.extend(cls(root, tenant_id).collect())
    events.sort(key=lambda e: (e.ts, e.id))
    return events


__all__ = ["COLLECTORS", "Collector", "collect_all", "register_collector"]
