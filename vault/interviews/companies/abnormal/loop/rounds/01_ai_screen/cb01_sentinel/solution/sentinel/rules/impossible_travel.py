from __future__ import annotations

from sentinel.enrichment.geo_ip import haversine_km
from sentinel.models import RuleHit, SecurityEvent, ThreatLevel
from sentinel.rules.base import Rule, RuleContext, register_rule
from sentinel.timeutil import parse_ts


@register_rule
class ImpossibleTravel(Rule):
    id = "impossible_travel"
    title = "Impossible travel"

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        if event.kind != "login_success":
            return None
        geo = self.enrichment(event, "geo")
        last = self.enrichment(event, "history").get("last_login")
        if not geo or not last:
            return None
        km = haversine_km(last["lat"], last["lon"], geo["lat"], geo["lon"])
        if km < self.param("min_distance_km", 100):
            return None
        hours = max((event.ts - parse_ts(last["ts"])).total_seconds() / 3600, 1 / 60)
        speed = km / hours
        if speed <= self.param("max_speed_kmh", 900):
            return None
        return RuleHit(
            rule_id=self.id,
            severity=ThreatLevel.HIGH,
            reason=f"{event.user} moved {km:.0f} km in {hours * 60:.0f} min ({last['country']} -> {geo['country']})",
            evidence={"distance_km": round(km), "speed_kmh": round(speed), "from": last["country"], "to": geo["country"]},
        )
