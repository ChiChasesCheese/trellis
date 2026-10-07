"""DEPRECATED. An md5 duplicate finder from the prototype; never finished, never wired in.

It only indexes in memory, forgets everything on restart, and md5 is not collision-safe for
content addressing. Kept for reference until the prototype notes are archived. Do not extend it.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict


class HashIndex:
    def __init__(self) -> None:
        self._by_digest: dict[str, list[str]] = defaultdict(list)

    @staticmethod
    def digest(data: bytes) -> str:
        return hashlib.md5(data).hexdigest()  # noqa: S324

    def add(self, path: str, data: bytes) -> str:
        digest = self.digest(data)
        self._by_digest[digest].append(path)
        return digest

    def find_duplicates(self) -> dict[str, list[str]]:
        return {d: paths for d, paths in self._by_digest.items() if len(paths) > 1}

    def remove(self, path: str) -> None:
        for digest, paths in list(self._by_digest.items()):
            if path in paths:
                paths.remove(path)
            if not paths:
                del self._by_digest[digest]

    # TODO: persist the index and consult it on upload
    def lookup(self, data: bytes) -> list[str]:
        return list(self._by_digest.get(self.digest(data), []))
