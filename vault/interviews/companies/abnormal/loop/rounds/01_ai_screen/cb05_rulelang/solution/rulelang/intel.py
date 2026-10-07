"""Threat-intel lookups backed by the JSON feeds under ``fixtures/intel/``.

Detectors read intel through ``ctx.intel`` and never open the feed files themselves.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rulelang.config import IntelSettings
from rulelang.errors import ConfigError


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read intel feed {path.name}: {exc}") from exc


class IntelStore:
    def __init__(self, settings: IntelSettings):
        self._settings = settings
        self._bad_hosts: frozenset[str] | None = None
        self._domains: dict[str, dict[str, Any]] | None = None
        self._vendors: tuple[str, ...] | None = None

    @property
    def bad_hosts(self) -> frozenset[str]:
        if self._bad_hosts is None:
            self._bad_hosts = frozenset(h.lower() for h in _load(self._settings.bad_hosts))
        return self._bad_hosts

    @property
    def vendors(self) -> tuple[str, ...]:
        """Domains of vendors the tenant's business really deals with."""
        if self._vendors is None:
            self._vendors = tuple(v.lower() for v in _load(self._settings.vendors))
        return self._vendors

    def domain_age_days(self, domain: str) -> int | None:
        """Registered age of ``domain`` in days; ``None`` when the feed has no record of it."""
        if self._domains is None:
            self._domains = _load(self._settings.domains)
        record = self._domains.get(domain.lower())
        return int(record["age_days"]) if record else None
