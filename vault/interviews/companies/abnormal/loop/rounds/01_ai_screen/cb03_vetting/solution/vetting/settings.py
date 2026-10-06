"""Settings: ``config/default.toml`` with ``config/tenants/<tenant>.toml`` laid over it.

Unknown sections or keys are a ConfigError on purpose: a typo in a tenant file must not silently
fall back to the default.
"""
from __future__ import annotations

import re
import tomllib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vetting.errors import ConfigError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_INTEL_DIR = PROJECT_ROOT / "fixtures" / "intel"
DEFAULT_TOKENS = PROJECT_ROOT / "fixtures" / "tokens.json"
DEFAULT_DB = PROJECT_ROOT / "var" / "vetting.db"

_TENANT_ID = re.compile(r"^[a-z][a-z0-9_-]{1,31}$")
_SECTIONS = {"scoring", "weights", "lookups", "correlation", "feedback"}


@dataclass(frozen=True)
class CorrelationSettings:
    phone_prefix_digits: int = 9
    min_overlap_kinds: int = 2
    allowlist_cidrs: tuple[str, ...] = ()


@dataclass(frozen=True)
class FeedbackSettings:
    weak_signal_max_weight: int = 30
    cleared_weight_factor: float = 0.25


@dataclass(frozen=True)
class Settings:
    tenant_id: str
    weights: Mapping[str, int]
    highly_recommended_at: int
    recommended_at: int
    cache_ttl_seconds: int
    correlation: CorrelationSettings = field(default_factory=CorrelationSettings)
    feedback: FeedbackSettings = field(default_factory=FeedbackSettings)

    def weight(self, signal: str) -> int:
        try:
            return self.weights[signal]
        except KeyError:
            raise ConfigError(f"no weight configured for signal {signal!r} (see config/default.toml)") from None

    def require_weights(self, signals: Iterable[str]) -> None:
        for name in signals:
            self.weight(name)


def check_tenant_id(tenant_id: str) -> str:
    if not _TENANT_ID.match(tenant_id):
        raise ConfigError(f"invalid tenant id {tenant_id!r}")
    return tenant_id


def _merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def _read(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except FileNotFoundError:
        return {}
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path}: {exc}") from exc


def load_settings(tenant_id: str, config_dir: Path = DEFAULT_CONFIG_DIR) -> Settings:
    check_tenant_id(tenant_id)
    raw = _merge(_read(config_dir / "default.toml"), _read(config_dir / "tenants" / f"{tenant_id}.toml"))
    unknown = set(raw) - _SECTIONS
    if unknown:
        raise ConfigError(f"unknown config section(s): {sorted(unknown)}")
    try:
        scoring, lookups = raw["scoring"], raw["lookups"]
        corr, feedback = raw.get("correlation", {}), raw.get("feedback", {})
        weights = {name: int(value) for name, value in raw["weights"].items()}
        settings = Settings(
            tenant_id=tenant_id,
            weights=weights,
            highly_recommended_at=int(scoring["highly_recommended_at"]),
            recommended_at=int(scoring["recommended_at"]),
            cache_ttl_seconds=int(lookups["cache_ttl_seconds"]),
            correlation=CorrelationSettings(
                phone_prefix_digits=int(corr.get("phone_prefix_digits", 9)),
                min_overlap_kinds=int(corr.get("min_overlap_kinds", 2)),
                allowlist_cidrs=tuple(corr.get("allowlist_cidrs", ())),
            ),
            feedback=FeedbackSettings(
                weak_signal_max_weight=int(feedback.get("weak_signal_max_weight", 30)),
                cleared_weight_factor=float(feedback.get("cleared_weight_factor", 0.25)),
            ),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ConfigError(f"incomplete or malformed config for tenant {tenant_id!r}: {exc!r}") from exc
    if settings.recommended_at > settings.highly_recommended_at:
        raise ConfigError("scoring.recommended_at must not exceed scoring.highly_recommended_at")
    if any(value < 0 for value in weights.values()):
        raise ConfigError("weights must be non-negative")
    return settings
