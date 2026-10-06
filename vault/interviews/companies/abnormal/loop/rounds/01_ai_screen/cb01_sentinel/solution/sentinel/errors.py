"""Exception types shared across the package."""
from __future__ import annotations


class SentinelError(Exception):
    """Base class for errors raised on purpose by Sentinel code."""


class ConfigError(SentinelError):
    """Invalid or inconsistent configuration (default.toml or a tenant override)."""


class CollectorError(SentinelError):
    """A raw record could not be turned into a SecurityEvent."""
