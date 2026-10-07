"""Domain errors. The API layer maps these to HTTP errors (see vetting/api/errors.py)."""


class VettingError(Exception):
    """Base class for every error this package raises on purpose."""


class ConfigError(VettingError):
    """Bad or missing configuration."""


class ValidationError(VettingError):
    """Caller-supplied data is not acceptable."""


class NotFoundError(VettingError):
    """The requested record does not exist for this tenant."""
