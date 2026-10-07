"""Typed settings, loaded from ``config/default.toml`` with ``config/tenants/<tenant>.toml`` merged over it.

Also home of the well-known repository paths.
"""
from __future__ import annotations

import dataclasses
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from quarantine.errors import ConfigError

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
FIXTURES_DIR = REPO_ROOT / "fixtures"
DEFAULT_DB = REPO_ROOT / "var" / "quarantine.db"


@dataclass(frozen=True)
class DecisionSettings:
    quarantine_at: int = 70
    review_at: int = 40


@dataclass(frozen=True)
class SenderSettings:
    unknown_score: int = 30
    repeat_window_hours: int = 24
    repeat_bonus: int = 25
    repeat_cap: int = 50


@dataclass(frozen=True)
class AttachmentSettings:
    risky_extensions: tuple[str, ...] = ()


@dataclass(frozen=True)
class DisplayNameSettings:
    protected: tuple[str, ...] = ()


@dataclass(frozen=True)
class IntakeSettings:
    max_links: int = 50


@dataclass(frozen=True)
class Settings:
    tenant: str
    domains: tuple[str, ...] = ()
    decision: DecisionSettings = field(default_factory=DecisionSettings)
    sender: SenderSettings = field(default_factory=SenderSettings)
    attachments: AttachmentSettings = field(default_factory=AttachmentSettings)
    display_name: DisplayNameSettings = field(default_factory=DisplayNameSettings)
    intake: IntakeSettings = field(default_factory=IntakeSettings)


_TENANT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")

_SECTIONS: dict[str, type] = {
    "decision": DecisionSettings,
    "sender": SenderSettings,
    "attachments": AttachmentSettings,
    "display_name": DisplayNameSettings,
    "intake": IntakeSettings,
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


def _section(cls: type, name: str, raw: dict[str, Any]) -> Any:
    known = {f.name for f in dataclasses.fields(cls)}
    unknown = sorted(set(raw) - known)
    if unknown:
        raise ConfigError(f"[{name}] unknown keys: {', '.join(unknown)}")
    return cls(**{k: tuple(v) if isinstance(v, list) else v for k, v in raw.items()})


def build_settings(tenant: str, raw: dict[str, Any]) -> Settings:
    unknown = sorted(set(raw) - set(_SECTIONS) - {"domains"})
    if unknown:
        raise ConfigError(f"unknown config keys: {', '.join(unknown)}")
    sections = {name: _section(cls, name, raw.get(name, {})) for name, cls in _SECTIONS.items()}
    decision: DecisionSettings = sections["decision"]
    if not 0 < decision.review_at < decision.quarantine_at <= 100:
        raise ConfigError("[decision] needs 0 < review_at < quarantine_at <= 100")
    return Settings(tenant=tenant, domains=tuple(raw.get("domains", ())), **sections)


class SettingsProvider:
    """Hands out validated per-tenant settings; a tenant needs a file in ``config/tenants/``."""

    def __init__(self, config_dir: Path | None = None, fixtures_dir: Path | None = None):
        self.config_dir = Path(config_dir or CONFIG_DIR)
        self.fixtures_dir = Path(fixtures_dir or FIXTURES_DIR)
        self._cache: dict[str, Settings] = {}

    def for_tenant(self, tenant: str) -> Settings:
        if tenant not in self._cache:
            if not _TENANT_RE.match(tenant):
                raise ConfigError(f"invalid tenant id {tenant!r}")
            path = self.config_dir / "tenants" / f"{tenant}.toml"
            if not path.exists():
                raise ConfigError(f"unknown tenant {tenant!r}")
            raw = _merge(_read(self.config_dir / "default.toml"), _read(path))
            self._cache[tenant] = build_settings(tenant, raw)
        return self._cache[tenant]

    def tenants(self) -> list[str]:
        return sorted(p.stem for p in (self.config_dir / "tenants").glob("*.toml"))
