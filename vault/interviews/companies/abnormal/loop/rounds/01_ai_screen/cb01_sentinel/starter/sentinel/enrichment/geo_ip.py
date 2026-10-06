from __future__ import annotations

from typing import Any

from sentinel.enrichment.base import Enricher, EnrichmentContext
from sentinel.geo import load_geo_db
from sentinel.models import SecurityEvent


class GeoIpEnricher(Enricher):
    name = "geo"

    def enrich(self, event: SecurityEvent, ctx: EnrichmentContext) -> dict[str, Any]:
        if not event.src_ip:
            return {}
        rec = load_geo_db(self.settings.enrichment.geoip).lookup(event.src_ip)
        if rec is None:
            return {}
        return {
            "country": rec.country,
            "city": rec.city,
            "lat": rec.lat,
            "lon": rec.lon,
            "asn": rec.asn,
        }
