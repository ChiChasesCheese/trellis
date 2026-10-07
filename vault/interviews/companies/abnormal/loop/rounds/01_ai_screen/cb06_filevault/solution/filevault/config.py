"""Typed settings: ``config/default.toml`` first, then ``FILEVAULT_<KEY>`` environment overrides."""
from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

from filevault.errors import ConfigError

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "default.toml"
ENV_PREFIX = "FILEVAULT_"


@dataclass(frozen=True)
class Settings:
    quota_bytes_per_user: int
    rate_limit_per_sec: float
    max_upload_bytes: int
    admin_users: tuple[str, ...]
    default_page_size: int
    max_page_size: int
    data_dir: Path


_KINDS: dict[str, type] = {
    "quota_bytes_per_user": int,
    "rate_limit_per_sec": float,
    "max_upload_bytes": int,
    "admin_users": tuple,
    "default_page_size": int,
    "max_page_size": int,
    "data_dir": Path,
}


def _coerce(name: str, value: Any) -> Any:
    kind = _KINDS[name]
    try:
        if kind is tuple:
            items = value.split(",") if isinstance(value, str) else value
            return tuple(str(item).strip() for item in items if str(item).strip())
        return kind(value)
    except (TypeError, ValueError):
        raise ConfigError(f"{name}: cannot read {value!r} as {kind.__name__}") from None


def load_settings(env: Mapping[str, str] | None = None, path: Path = DEFAULT_CONFIG) -> Settings:
    """Read ``path``, apply environment overrides (``os.environ`` unless ``env`` is given)."""
    raw: dict[str, Any] = tomllib.loads(path.read_text())
    unknown = sorted(set(raw) - set(_KINDS))
    if unknown:
        raise ConfigError(f"unknown config keys: {', '.join(unknown)}")
    env = os.environ if env is None else env
    for f in fields(Settings):
        override = env.get(ENV_PREFIX + f.name.upper())
        if override is not None:
            raw[f.name] = override
    missing = sorted(set(_KINDS) - set(raw))
    if missing:
        raise ConfigError(f"missing config keys: {', '.join(missing)}")
    settings = Settings(**{name: _coerce(name, raw[name]) for name in _KINDS})
    _validate(settings)
    return settings


def _validate(s: Settings) -> None:
    for name in ("quota_bytes_per_user", "max_upload_bytes", "default_page_size", "max_page_size"):
        if getattr(s, name) <= 0:
            raise ConfigError(f"{name} must be positive")
    if s.rate_limit_per_sec <= 0:
        raise ConfigError("rate_limit_per_sec must be positive")
    if s.default_page_size > s.max_page_size:
        raise ConfigError("default_page_size cannot exceed max_page_size")
