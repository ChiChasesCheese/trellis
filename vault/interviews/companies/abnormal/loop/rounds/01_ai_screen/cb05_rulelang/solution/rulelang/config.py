"""Typed settings, loaded from ``config/default.toml`` with ``config/tenants/<tenant>.toml`` merged over it.

Also home of the well-known repository paths. Unknown sections or keys are errors on purpose:
a typo in a tenant file must not silently turn a detector off.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rulelang.errors import ConfigError
from rulelang.rules import CompiledRule, compile_rule

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
FIXTURES_DIR = REPO_ROOT / "fixtures"
DEFAULT_DB = REPO_ROOT / "var" / "rulelang.db"


@dataclass(frozen=True)
class OrgSettings:
    """Who counts as "inside" for this tenant."""

    internal_domains: tuple[str, ...] = ()


@dataclass(frozen=True)
class IntelSettings:
    bad_hosts: Path
    domains: Path
    vendors: Path


@dataclass(frozen=True)
class DetectorSettings:
    # Detector names the tenant switched off.
    disabled: tuple[str, ...] = ()
    # Per-detector parameters, keyed by detector name: {"mass_mailing": {"recipient_threshold": 10}}
    params: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass(frozen=True)
class BlastRadiusSettings:
    max_hops: int = 2


@dataclass(frozen=True)
class Settings:
    tenant: str
    org: OrgSettings
    intel: IntelSettings
    detectors: DetectorSettings
    blast_radius: BlastRadiusSettings = BlastRadiusSettings()
    # Customer-written rules, compiled (and therefore validated) when the config is loaded.
    rules: tuple[CompiledRule, ...] = ()


_TENANT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")

_ALLOWED: dict[str, set[str]] = {
    "tenant": {"internal_domains"},
    "intel": {"bad_hosts", "domains", "vendors"},
    "blast_radius": {"max_hops"},
}

_RULE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


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


def _string_list(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ConfigError(f"{where} must be a list of strings")
    return tuple(value)


def build_settings(tenant: str, raw: dict[str, Any], fixtures_dir: Path) -> Settings:
    unknown = set(raw) - set(_ALLOWED) - {"detectors", "rules"}
    if unknown:
        raise ConfigError(f"unknown config sections: {', '.join(sorted(unknown))}")

    org = _section(raw, "tenant")
    intel = _section(raw, "intel")
    blast = _section(raw, "blast_radius")
    max_hops = blast.get("max_hops", 2)
    if not isinstance(max_hops, int) or isinstance(max_hops, bool) or not 1 <= max_hops <= 10:
        raise ConfigError("[blast_radius] max_hops must be an integer between 1 and 10")

    rules_raw = raw.get("rules", {})
    if not isinstance(rules_raw, dict):
        raise ConfigError("[rules] must be a table of <name> = \"<expression>\"")
    rules = []
    for name, source in rules_raw.items():
        if not _RULE_NAME_RE.match(name) or not isinstance(source, str):
            raise ConfigError(f"[rules] {name!r}: names are lower_snake_case and values are expression strings")
        rules.append(compile_rule(name, source))

    det = dict(raw.get("detectors", {}))
    disabled = _string_list(det.pop("disabled", []), "[detectors] disabled")
    for name, params in det.items():
        if not isinstance(params, dict):
            raise ConfigError(f"[detectors.{name}] must be a table")

    try:
        return Settings(
            tenant=tenant,
            org=OrgSettings(
                internal_domains=_string_list(org.get("internal_domains", []), "[tenant] internal_domains")
            ),
            intel=IntelSettings(
                bad_hosts=fixtures_dir / intel["bad_hosts"],
                domains=fixtures_dir / intel["domains"],
                vendors=fixtures_dir / intel["vendors"],
            ),
            detectors=DetectorSettings(disabled=disabled, params=det),
            blast_radius=BlastRadiusSettings(max_hops=max_hops),
            rules=tuple(rules),
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
