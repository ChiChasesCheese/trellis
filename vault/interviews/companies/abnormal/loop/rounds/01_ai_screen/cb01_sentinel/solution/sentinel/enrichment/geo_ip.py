"""Geo-IP enrichment: CIDR -> country/city/lat/lon/asn, plus great-circle distance."""
from __future__ import annotations

import ipaddress
import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from sentinel.enrichment.base import Enricher, EnrichmentContext, register_enricher
from sentinel.models import SecurityEvent

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlam / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


@dataclass(frozen=True)
class GeoRecord:
    cidr: ipaddress.IPv4Network | ipaddress.IPv6Network
    country: str
    city: str
    lat: float
    lon: float
    asn: int


class GeoDb:
    def __init__(self, records: list[GeoRecord]):
        # Longest prefix first so the most specific network wins.
        self._records = sorted(records, key=lambda r: r.cidr.prefixlen, reverse=True)

    def lookup(self, ip: str) -> GeoRecord | None:
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return None
        for rec in self._records:
            if addr.version == rec.cidr.version and addr in rec.cidr:
                return rec
        return None


@lru_cache(maxsize=8)
def load_geo_db(path: Path) -> GeoDb:
    raw = json.loads(Path(path).read_text())
    return GeoDb(
        [
            GeoRecord(
                cidr=ipaddress.ip_network(n["cidr"]),
                country=n["country"],
                city=n["city"],
                lat=float(n["lat"]),
                lon=float(n["lon"]),
                asn=int(n["asn"]),
            )
            for n in raw["networks"]
        ]
    )


@register_enricher
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
