from __future__ import annotations

import ipaddress
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from sentinel.enrichment.base import Enricher, EnrichmentContext, register_enricher
from sentinel.models import SecurityEvent


@lru_cache(maxsize=8)
def _load(path: Path) -> tuple[dict[str, dict], list[tuple[ipaddress._BaseNetwork, dict]]]:
    raw = json.loads(Path(path).read_text())
    nets = [(ipaddress.ip_network(c), meta) for c, meta in raw.get("cidrs", {}).items()]
    return dict(raw.get("ips", {})), nets


@register_enricher
class ThreatIntelEnricher(Enricher):
    name = "threat_intel"

    def enrich(self, event: SecurityEvent, ctx: EnrichmentContext) -> dict[str, Any]:
        if not event.src_ip:
            return {}
        ips, nets = _load(self.settings.enrichment.bad_ips)
        meta = ips.get(event.src_ip)
        if meta is None:
            try:
                addr = ipaddress.ip_address(event.src_ip)
            except ValueError:
                return {}
            meta = next((m for net, m in nets if addr in net), None)
        if meta is None:
            return {}
        return {"listed": True, "feed": meta["feed"], "confidence": float(meta["confidence"])}
