from __future__ import annotations

from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.rules.base import Rule, RuleContext, register_rule


@register_rule
class RareAdminAction(Rule):
    id = "rare_admin_action"
    title = "Rare administrative action"

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        if event.kind != "admin_action":
            return None
        action = event.attrs.get("action")
        if action not in self.param("actions", []):
            return None
        return RuleHit(
            rule_id=self.id,
            severity=ThreatLevel.MEDIUM,
            reason=f"{event.user} performed {action} on {event.attrs.get('target')}",
            evidence={"action": action, "target": event.attrs.get("target")},
        )
