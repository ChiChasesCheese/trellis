"""Exception types shared across the package."""
from __future__ import annotations


class QuarantineError(Exception):
    """Base class for errors raised on purpose by Quarantine code."""


class ConfigError(QuarantineError):
    """Invalid or inconsistent configuration (default.toml or a tenant override)."""


class MailboxError(QuarantineError):
    """The mail provider refused or failed a call."""


class LookupUnavailable(QuarantineError):
    """An intel lookup could not be answered (provider down, timeout)."""


class ValidationError(QuarantineError):
    """A report payload is missing a field or has a field of the wrong shape."""


class DuplicateReport(QuarantineError):
    """A report for this (tenant, message id) already exists."""
