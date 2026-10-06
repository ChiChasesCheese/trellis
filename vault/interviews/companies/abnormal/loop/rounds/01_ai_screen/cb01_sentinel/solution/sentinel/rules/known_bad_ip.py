from __future__ import annotations

from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.rules.base import Rule, RuleContext, register_rule


@register_rule
class KnownBadIp(Rule):
    id = "known_bad_ip"
    title = "Activity from a listed IP"

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        intel = self.enrichment(event, "threat_intel")
        if not intel.get("listed"):
            return None
        critical = intel["confidence"] >= self.param("critical_confidence", 0.9)
        return RuleHit(
            rule_id=self.id,
            severity=ThreatLevel.CRITICAL if critical else ThreatLevel.HIGH,
            reason=f"{event.src_ip} is listed on {intel['feed']} (confidence {intel['confidence']:.2f})",
            evidence={"feed": intel["feed"], "confidence": intel["confidence"]},
        )
