from __future__ import annotations

from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.rules.base import Rule, RuleContext, register_rule


@register_rule
class NewCountryLogin(Rule):
    id = "new_country_login"
    title = "Login from a new country"

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        if event.kind != "login_success":
            return None
        if not self.enrichment(event, "history").get("new_country"):
            return None
        country = self.enrichment(event, "geo")["country"]
        return RuleHit(
            rule_id=self.id,
            severity=ThreatLevel.MEDIUM,
            reason=f"{event.user} logged in from {country} for the first time",
            evidence={"country": country},
        )
