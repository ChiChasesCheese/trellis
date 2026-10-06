"""Scoring: combine rule hits into a ThreatLevel, and rank alerts by severity x asset criticality x recency."""
from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

from sentinel.models import RuleHit, ThreatLevel


def combine(hits: Sequence[RuleHit], escalate_at: int = 3) -> ThreatLevel:
    """Highest severity wins; ``escalate_at`` distinct rules bump it up one level (capped at CRITICAL)."""
    if not hits:
        raise ValueError("cannot compute a threat level without hits")
    level = max(h.severity for h in hits)
    if len({h.rule_id for h in hits}) >= escalate_at and level < ThreatLevel.CRITICAL:
        level = ThreatLevel(level + 1)
    return level


class AssetCatalog:
    """Per-tenant criticality of users and hosts, from fixtures/assets.json (1.0 = ordinary)."""

    def __init__(self, path: Path):
        raw = json.loads(Path(path).read_text())
        self._default = float(raw.get("default", 1.0))
        self._tenants = raw.get("tenants", {})

    def criticality(self, tenant_id: str, user: str | None, host: str | None = None) -> float:
        tenant = self._tenants.get(tenant_id, {})
        values = [
            tenant.get("users", {}).get(user or ""),
            tenant.get("hosts", {}).get(host or ""),
        ]
        known = [float(v) for v in values if v is not None]
        return max(known) if known else self._default


def score(
    level: ThreatLevel,
    weights: dict[str, float],
    criticality: float,
    age_hours: float,
    half_life_hours: float,
) -> float:
    decay = 0.5 ** (max(age_hours, 0.0) / half_life_hours)
    return float(f"{weights[level.name] * criticality * decay:.6g}")
