"""ConfigManager: merges four configuration layers -- defaults, a JSON file, matching
environment variables, and in-process runtime overrides -- into one `get(key)` lookup, with a
TTL cache in front so a hot key doesn't have to walk all four layers on every call.

Precedence (highest wins): runtime overrides > environment > file > defaults. `reload()` re-reads
the file and environment layers from their sources (defaults and overrides are already in this
process's memory and don't need "reading" again) -- this is the hot-reload half of the class,
meant to be called whenever the operator knows the on-disk file or the environment has changed,
without restarting the process.

Data flow for one `get(key)` call: ConfigManager.get -> TTLCache.get_or_compute -> (on a miss)
ConfigManager._resolve -> the four layer dicts, in precedence order.
"""

from __future__ import annotations

import threading

from .cache import TTLCache
from .layers import load_env_layer, load_file_layer

_MISSING = object()  # sentinel: distinguishes "key resolves to None" from "key not found anywhere"


class ConfigManager:
    def __init__(
        self,
        defaults: dict | None = None,
        file_path: str | None = None,
        env_prefix: str | None = None,
        cache_ttl: float = 5.0,
    ):
        self._defaults = dict(defaults or {})
        self._file_path = file_path
        self._env_prefix = env_prefix
        self._file_layer = load_file_layer(file_path) if file_path else {}
        self._env_layer = load_env_layer(env_prefix) if env_prefix else {}
        self._overrides: dict = {}
        self._overrides_lock = threading.Lock()
        self._cache = TTLCache(cache_ttl)

    def get(self, key: str, default=None):
        """Return the effective value of `key` across all four layers, or `default` if no layer
        defines it. Results are served from the TTL cache when available."""
        value = self._cache.get_or_compute(key, lambda: self._resolve(key))
        return default if value is _MISSING else value

    def set_override(self, key: str, value) -> None:
        """Set a runtime override for `key` -- takes precedence over every other layer until
        `clear_override()` is called or the process restarts."""
        with self._overrides_lock:
            self._overrides[key] = value
        self._cache.invalidate(key)

    def clear_override(self, key: str) -> None:
        """Remove a runtime override for `key`, if one was set, falling back to the next layer
        below it."""
        with self._overrides_lock:
            self._overrides.pop(key, None)
        self._cache.invalidate(key)

    def reload(self) -> None:
        """Re-read the file layer (if a `file_path` was given) and the environment layer (if an
        `env_prefix` was given) from their sources. Defaults and runtime overrides are untouched
        by a reload -- they don't come from an external, reloadable source."""
        if self._file_path:
            self._file_layer = load_file_layer(self._file_path)
        if self._env_prefix:
            self._env_layer = load_env_layer(self._env_prefix)

    def _resolve(self, key: str):
        """Look `key` up across all four layers in precedence order, returning `_MISSING` if none
        of them define it."""
        with self._overrides_lock:
            if key in self._overrides:
                return self._overrides[key]
        if key in self._env_layer:
            return self._env_layer[key]
        if key in self._file_layer:
            return self._file_layer[key]
        if key in self._defaults:
            return self._defaults[key]
        return _MISSING

    def get_int(self, key: str, default: int | None = None) -> int | None:
        """Like `get()`, but converts the resolved value to `int` (values that came from the
        environment layer are always strings, since `os.environ` has no other type). Raises
        `ValueError` if the resolved value can't be parsed as an int. Returns `default` unchanged
        if `key` isn't defined anywhere -- `default` is not itself converted."""
        value = self.get(key, default=_MISSING)
        if value is _MISSING:
            return default
        return int(value)

    _TRUE_STRINGS = {"1", "true", "yes", "on"}
    _FALSE_STRINGS = {"0", "false", "no", "off"}

    def get_bool(self, key: str, default: bool | None = None) -> bool | None:
        """Like `get()`, but converts the resolved value to `bool`. A native `bool` passes
        through unchanged; a string is matched case-insensitively against a small set of
        accepted spellings (see `_TRUE_STRINGS`/`_FALSE_STRINGS`). Raises `ValueError` for
        anything else. Returns `default` unchanged if `key` isn't defined anywhere."""
        value = self.get(key, default=_MISSING)
        if value is _MISSING:
            return default
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in self._TRUE_STRINGS:
            return True
        if text in self._FALSE_STRINGS:
            return False
        raise ValueError(f"cannot interpret {value!r} as a boolean for key {key!r}")

    def snapshot(self) -> dict:
        """Return the effective value of every key known to any layer, as one flat dict --
        handy for logging "here is the config this process actually started with" at startup.
        Each value goes through the same `get()`/cache path a normal lookup would."""
        with self._overrides_lock:
            override_keys = set(self._overrides)
        keys = override_keys | set(self._env_layer) | set(self._file_layer) | set(self._defaults)
        return {key: self.get(key) for key in keys}
