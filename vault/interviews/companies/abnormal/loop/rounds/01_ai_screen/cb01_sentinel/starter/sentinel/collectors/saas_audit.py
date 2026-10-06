"""Administrative actions from SaaS audit logs."""
from __future__ import annotations

from typing import Any

from sentinel.collectors.base import Collector, register_collector
from sentinel.models import SecurityEvent
from sentinel.timeutil import parse_ts

ADMIN_ACTIONS = frozenset(
    {"role.grant", "role.revoke", "mfa.disable", "sso.config.change", "api_key.create", "user.delete"}
)


@register_collector
class SaasAuditCollector(Collector):
    source = "saas_audit"

    def normalize(self, record: dict[str, Any]) -> SecurityEvent | None:
        if record["org"] != self.tenant_id:
            return None
        action = record["action"]
        return SecurityEvent(
            id=str(record["uid"]),
            tenant_id=self.tenant_id,
            ts=parse_ts(record["timestamp"]),
            source=self.source,
            kind="admin_action" if action in ADMIN_ACTIONS else "audit",
            user=record["actor"].lower(),
            src_ip=record.get("ip"),
            attrs={"action": action, "target": record.get("target"), "app": record.get("app")},
        )
