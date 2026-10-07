"""Two logins by one user that are too far apart for the time between them."""
from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(a))


@register_detector
class ImpossibleTravel(Detector):
    name = "impossible_travel"
    kinds = ("login",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        if "lat" not in event.attrs or "lon" not in event.attrs:
            return None
        prev = ctx.events.last_login(event.tenant_id, event.actor, event.ts)
        if prev is None or "lat" not in prev.attrs:
            return None
        km = haversine_km(prev.attrs["lat"], prev.attrs["lon"], event.attrs["lat"], event.attrs["lon"])
        hours = max((event.ts - prev.ts).total_seconds() / 3600, 1 / 3600)
        speed = km / hours
        if km < self.param("min_distance_km", 100) or speed <= self.param("max_speed_kmh", 900):
            return None
        return self.signal(
            event,
            Severity.HIGH,
            f"{event.actor} moved {km:.0f} km in {hours * 60:.0f} min",
            from_country=prev.attrs.get("country"),
            to_country=event.attrs.get("country"),
            distance_km=round(km),
            speed_kmh=round(speed),
        )
