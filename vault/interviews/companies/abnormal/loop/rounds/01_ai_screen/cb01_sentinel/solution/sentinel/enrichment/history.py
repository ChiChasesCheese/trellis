from __future__ import annotations

from typing import Any

from sentinel.enrichment.base import Enricher, EnrichmentContext, register_enricher
from sentinel.models import SecurityEvent
from sentinel.timeutil import iso


@register_enricher
class HistoryEnricher(Enricher):
    """What we already know about this user. Reads the stored geo of past events and the
    current event's geo (so it must run after GeoIpEnricher)."""

    name = "history"
    requires = ("geo",)

    def enrich(self, event: SecurityEvent, ctx: EnrichmentContext) -> dict[str, Any]:
        if not event.user:
            return {}
        past = ctx.events.history_for_user(event.tenant_id, event.user, event.ts)
        logins = [e for e in past if e.kind == "login_success"]
        countries = sorted({e.enrichment.get("geo", {}).get("country") for e in logins} - {None})
        last_login = None
        for prior in logins:  # newest first
            geo = prior.enrichment.get("geo", {})
            if "lat" in geo:
                last_login = {
                    "ts": iso(prior.ts),
                    "ip": prior.src_ip,
                    "country": geo["country"],
                    "lat": geo["lat"],
                    "lon": geo["lon"],
                }
                break
        country = event.enrichment.get("geo", {}).get("country")
        return {
            "known_user": bool(past),
            "first_seen": iso(past[-1].ts) if past else None,
            "seen_countries": countries,
            "seen_ips": sorted({e.src_ip for e in logins if e.src_ip}),
            "seen_devices": sorted({e.attrs["device"] for e in logins if "device" in e.attrs}),
            "last_login": last_login,
            "new_country": bool(country and countries and country not in countries),
        }
