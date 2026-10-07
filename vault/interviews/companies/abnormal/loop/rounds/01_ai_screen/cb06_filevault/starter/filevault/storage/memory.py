"""A dict-backed store for tests."""
from __future__ import annotations

import threading

from filevault.errors import BlobNotFound
from filevault.storage.base import BlobStore


class InMemoryStore(BlobStore):
    def __init__(self) -> None:
        self._blobs: dict[str, bytes] = {}
        self._lock = threading.Lock()

    def put(self, path: str, data: bytes) -> None:
        with self._lock:
            self._blobs[path] = bytes(data)

    def get(self, path: str) -> bytes:
        with self._lock:
            try:
                return self._blobs[path]
            except KeyError:
                raise BlobNotFound(path) from None

    def delete(self, path: str) -> None:
        with self._lock:
            self._blobs.pop(path, None)

    def exists(self, path: str) -> bool:
        with self._lock:
            return path in self._blobs

    def paths(self) -> list[str]:
        with self._lock:
            return sorted(self._blobs)
