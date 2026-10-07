"""Tenant enricher plugins: every ``*.py`` in a plugin directory may define ``Enricher`` subclasses."""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import sys
from collections.abc import Sequence
from pathlib import Path

from sentinel.enrichment.base import ENRICHERS, Enricher
from sentinel.errors import ConfigError


def _load_module(path: Path):
    name = f"sentinel_plugin_{hashlib.sha1(str(path.resolve()).encode()).hexdigest()[:8]}_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # a broken plugin file is a configuration problem, reported at startup
        sys.modules.pop(name, None)
        raise ConfigError(f"enrichment plugin {path} failed to import: {exc}") from exc
    return module


def discover(plugin_dirs: Sequence[Path]) -> dict[str, type[Enricher]]:
    """Find concrete Enricher subclasses in ``plugin_dirs``, keyed by their ``name``."""
    found: dict[str, type[Enricher]] = {}
    for directory in plugin_dirs:
        if not directory.is_dir():
            raise ConfigError(f"enrichment plugin_dirs entry is not a directory: {directory}")
        for path in sorted(directory.glob("*.py")):
            if path.name.startswith("_"):
                continue
            module = _load_module(path)
            for obj in vars(module).values():
                if not (isinstance(obj, type) and issubclass(obj, Enricher) and obj is not Enricher):
                    continue
                if obj.__module__ != module.__name__ or inspect.isabstract(obj):
                    continue  # imported from elsewhere, or still abstract
                name = getattr(obj, "name", None)
                if not isinstance(name, str) or not name:
                    raise ConfigError(f"plugin {path.name}: {obj.__name__} has no `name`")
                if name in found or name in ENRICHERS:
                    raise ConfigError(f"plugin {path.name}: enricher name {name!r} is already taken")
                found[name] = obj
    return found
