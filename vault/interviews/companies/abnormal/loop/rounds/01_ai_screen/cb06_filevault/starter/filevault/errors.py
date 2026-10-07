"""Domain errors. The API layer translates these into HTTP responses (``api/app.py``)."""
from __future__ import annotations


class FileVaultError(Exception):
    """Base class for errors raised by the service layer."""


class ConfigError(FileVaultError):
    """Bad configuration; raised at startup."""


class InvalidInput(FileVaultError):
    """A caller-supplied value is unusable. ``field`` names the offending input."""

    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


class FileNotFound(FileVaultError):
    """No such file *for this user* (other users' files look exactly like missing ones)."""


class BlobNotFound(FileVaultError):
    """A blob store has nothing at the requested path."""


class FileTooLarge(FileVaultError):
    def __init__(self, size: int, limit: int):
        super().__init__(f"file is {size} bytes; the limit is {limit}")
        self.size = size
        self.limit = limit
