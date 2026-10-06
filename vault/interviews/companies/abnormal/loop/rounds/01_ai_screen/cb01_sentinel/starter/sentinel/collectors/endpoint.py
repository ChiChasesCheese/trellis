"""Process and file events from endpoint agents (epoch-second timestamps)."""
from __future__ import annotations

from typing import Any

from sentinel.collectors.base import Collector
from sentinel.collectors.registry import register_collector
from sentinel.errors import CollectorError
from sentinel.models import SecurityEvent
from sentinel.timeutil import parse_ts

_KINDS = {"process_start", "file_write", "usb_mount"}


@register_collector
class EndpointCollector(Collector):
    source = "endpoint"

    def normalize(self, record: dict[str, Any]) -> SecurityEvent | None:
        if record["tenant_id"] != self.tenant_id:
            return None
        kind = record["type"]
        if kind not in _KINDS:
            raise CollectorError(f"unknown endpoint event type: {kind!r}")
        return SecurityEvent(
            id=str(record["event_id"]),
            tenant_id=self.tenant_id,
            ts=parse_ts(record["ts"]),
            source=self.source,
            kind=kind,
            user=(record.get("user") or "").lower() or None,
            attrs={k: record[k] for k in ("host", "process", "path") if k in record},
        )
