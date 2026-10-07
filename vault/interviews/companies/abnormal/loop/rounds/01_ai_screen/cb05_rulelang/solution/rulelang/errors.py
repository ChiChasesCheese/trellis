"""Exception types. The CLI turns any ``RulelangError`` into ``error: ...`` and exit code 2."""
from __future__ import annotations


class RulelangError(Exception):
    """Base class for errors the operator can act on."""


class ConfigError(RulelangError):
    """Bad or missing configuration (tenant config, intel files, detector wiring)."""


class BadRecord(RulelangError):
    """One input record could not be parsed; the loader counts it and moves on."""

    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason
