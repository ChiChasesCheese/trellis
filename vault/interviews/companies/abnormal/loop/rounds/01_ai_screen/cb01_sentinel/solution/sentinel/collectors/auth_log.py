"""Login events from the identity provider."""
from __future__ import annotations

import hashlib
from typing import Any

from sentinel.collectors.base import Collector, register_collector
from sentinel.errors import CollectorError
from sentinel.models import SecurityEvent
from sentinel.timeutil import parse_ts


@register_collector
class AuthLogCollector(Collector):
    source = "auth_log"

    def normalize(self, record: dict[str, Any]) -> SecurityEvent | None:
        if record["tenant"] != self.tenant_id:
            return None
        result = record["result"]
        if result not in ("success", "failure"):
            raise CollectorError(f"unknown login result: {result!r}")
        ua = record.get("ua") or ""
        return SecurityEvent(
            id=str(record["id"]),
            tenant_id=self.tenant_id,
            ts=parse_ts(record["time"]),
            source=self.source,
            kind=f"login_{result}",
            user=record["user"].lower(),
            src_ip=record["ip"],
            attrs={"user_agent": ua, "device": hashlib.sha1(ua.encode()).hexdigest()[:8]},
        )
