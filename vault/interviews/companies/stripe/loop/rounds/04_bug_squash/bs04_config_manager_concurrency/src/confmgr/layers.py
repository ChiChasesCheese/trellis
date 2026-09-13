"""Loaders for the two "external" configuration layers: a JSON file on disk, and a slice of
`os.environ` selected by prefix. Both are plain functions that take a source (a path, a prefix)
and return a flat `dict[str, object]` -- no caching, no state, nothing async or threaded. Higher
layers (env, runtime overrides) are meant to take precedence over lower ones (defaults, file);
that ordering is `manager.py`'s job, not this module's.
"""

from __future__ import annotations

import json
import os
from pathlib import Path


def load_file_layer(path: str) -> dict:
    """Read a JSON object from `path` and return it as a flat dict.

    A missing file is treated as "no overrides from this layer yet" and returns `{}` rather than
    raising -- config files are often optional (e.g. a machine that hasn't been provisioned with
    one yet should still start up on defaults). A file that parses to something other than a JSON
    object (a list, a number, ...) is a real error and raises `ValueError`.
    """
    p = Path(path)
    if not p.exists():
        return {}
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"config file {path!r} must contain a JSON object at the top level")
    return data


def load_env_layer(prefix: str) -> dict:
    """Collect every `os.environ` entry whose key starts with `prefix` into a dict, stripping the
    prefix off each key. E.g. with prefix "MYAPP_", `MYAPP_TIMEOUT=30` becomes `{"TIMEOUT": "30"}`.
    Values are always strings (environment variables have no other type); callers that need an
    int/bool must convert themselves.
    """
    out = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            out[key[len(prefix) :]] = value
    return out
