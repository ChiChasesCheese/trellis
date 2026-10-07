from __future__ import annotations

from datetime import timedelta

from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.rules.base import Rule, RuleContext, register_rule
from sentinel.timeutil import sliding_window


@register_rule
class BruteForce(Rule):
    """Fires on every failed login that brings one source address to the threshold within the window."""

    id = "brute_force"
    title = "Brute-force login attempts"

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        if event.kind != "login_failure" or not event.src_ip:
            return None
        window = timedelta(minutes=self.param("window_minutes", 10))
        threshold = self.param("threshold", 5)
        earlier = ctx.events.failed_logins_from_ip(
            event.tenant_id, event.src_ip, event.ts - window, event.ts
        )
        attempts = sliding_window([*earlier, event.ts], window)
        if attempts < threshold:
            return None
        return RuleHit(
            rule_id=self.id,
            severity=ThreatLevel.MEDIUM,
            reason=f"{attempts} failed logins from {event.src_ip} within {window.seconds // 60} min",
            evidence={"attempts": attempts, "src_ip": event.src_ip},
        )
