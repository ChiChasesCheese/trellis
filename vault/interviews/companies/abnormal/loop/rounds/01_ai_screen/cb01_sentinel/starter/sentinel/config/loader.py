"""Load ``config/default.toml`` and deep-merge ``config/tenants/<tenant>.toml`` over it."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from sentinel.config.settings import (
    AlertSettings,
    EnrichmentSettings,
    RankingSettings,
    Settings,
    ThreatSettings,
)
from sentinel.errors import ConfigError
from sentinel.paths import CONFIG_DIR, FIXTURES_DIR

_TENANT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")

_ALLOWED: dict[str, set[str]] = {
    "enrichment": {"geoip", "bad_ips"},
    "threat": {"escalate_at"},
    "ranking": {"half_life_hours", "weights"},
    "alerts": {"assets"},
}


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
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path.name}: {exc}") from exc


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
    data = raw.get(name, {})
    if not isinstance(data, dict):
        raise ConfigError(f"[{name}] must be a table")
    unknown = set(data) - _ALLOWED[name]
    if unknown:
        raise ConfigError(f"[{name}] unknown keys: {', '.join(sorted(unknown))}")
    return data


def build_settings(tenant: str, raw: dict[str, Any], fixtures_dir: Path) -> Settings:
    unknown = set(raw) - set(_ALLOWED) - {"rules"}
    if unknown:
        raise ConfigError(f"unknown config sections: {', '.join(sorted(unknown))}")

    enr = _section(raw, "enrichment")
    thr = _section(raw, "threat")
    rank = _section(raw, "ranking")
    alerts = _section(raw, "alerts")
    rules = raw.get("rules", {})
    if not isinstance(rules, dict) or not all(isinstance(v, dict) for v in rules.values()):
        raise ConfigError("[rules.*] entries must be tables")

    escalate_at = thr.get("escalate_at", 3)
    if not isinstance(escalate_at, int) or escalate_at < 2:
        raise ConfigError("[threat] escalate_at must be an integer >= 2")
    half_life = rank.get("half_life_hours", 72.0)
    if not isinstance(half_life, (int, float)) or half_life <= 0:
        raise ConfigError("[ranking] half_life_hours must be > 0")

    try:
        return Settings(
            tenant=tenant,
            enrichment=EnrichmentSettings(
                geoip=fixtures_dir / enr["geoip"], bad_ips=fixtures_dir / enr["bad_ips"]
            ),
            threat=ThreatSettings(escalate_at=escalate_at),
            ranking=RankingSettings(
                half_life_hours=float(half_life), weights=dict(rank.get("weights", {}))
            ),
            alerts=AlertSettings(assets=fixtures_dir / alerts["assets"]),
            rules=rules,
        )
    except KeyError as exc:
        raise ConfigError(f"missing required config key: {exc.args[0]}") from exc


def load_settings(
    tenant: str, config_dir: Path = CONFIG_DIR, fixtures_dir: Path = FIXTURES_DIR
) -> Settings:
    if not _TENANT_RE.match(tenant):
        raise ConfigError(f"invalid tenant name: {tenant!r}")
    raw = _read(config_dir / "default.toml")
    override = config_dir / "tenants" / f"{tenant}.toml"
    if override.exists():
        raw = _merge(raw, _read(override))
    return build_settings(tenant, raw, fixtures_dir)


class SettingsProvider:
    """Hands out (and caches) per-tenant settings."""

    def __init__(self, config_dir: Path | None = None, fixtures_dir: Path | None = None):
        self.config_dir = Path(config_dir) if config_dir else CONFIG_DIR
        self.fixtures_dir = Path(fixtures_dir) if fixtures_dir else FIXTURES_DIR
        self._cache: dict[str, Settings] = {}

    def for_tenant(self, tenant: str) -> Settings:
        if tenant not in self._cache:
            self._cache[tenant] = load_settings(tenant, self.config_dir, self.fixtures_dir)
        return self._cache[tenant]
