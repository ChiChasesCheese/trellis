"""The blob-store seam. Everything that holds file bytes goes through this interface."""
from __future__ import annotations

from abc import ABC, abstractmethod


class BlobStore(ABC):
    """Stores opaque bytes under a relative, slash-separated path."""

    @abstractmethod
    def put(self, path: str, data: bytes) -> None:
        """Store ``data`` at ``path``, replacing anything there. Must be atomic for readers."""

    @abstractmethod
    def get(self, path: str) -> bytes:
        """Return the bytes at ``path`` or raise ``BlobNotFound``."""

    @abstractmethod
    def delete(self, path: str) -> None:
        """Remove ``path``. Removing something that is not there is not an error."""

    @abstractmethod
    def exists(self, path: str) -> bool: ...

    @abstractmethod
    def paths(self) -> list[str]:
        """Every stored path, sorted."""
