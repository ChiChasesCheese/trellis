"""Typed settings. Built by ``sentinel.config.loader`` from default.toml + a tenant override."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EnrichmentSettings:
    geoip: Path
    bad_ips: Path


@dataclass(frozen=True)
class ThreatSettings:
    # Number of distinct rules that must fire on one event before the level is bumped by one.
    escalate_at: int = 3


@dataclass(frozen=True)
class RankingSettings:
    half_life_hours: float = 72.0
    weights: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class AlertSettings:
    assets: Path


@dataclass(frozen=True)
class Settings:
    tenant: str
    enrichment: EnrichmentSettings
    threat: ThreatSettings
    ranking: RankingSettings
    alerts: AlertSettings
    # Per-rule parameters, keyed by rule id: {"brute_force": {"threshold": 5}, ...}
    rules: dict[str, dict[str, Any]] = field(default_factory=dict)
