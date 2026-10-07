"""Blobs as files under one root directory (``data/blobs`` by default)."""
from __future__ import annotations

import os
import uuid
from pathlib import Path

from filevault.errors import BlobNotFound
from filevault.storage.base import BlobStore


class LocalDiskStore(BlobStore):
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, path: str) -> Path:
        target = (self.root / path).resolve()
        if self.root not in target.parents:
            raise ValueError(f"path escapes the store root: {path!r}")
        return target

    def put(self, path: str, data: bytes) -> None:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        scratch = target.with_name(f"{target.name}.{uuid.uuid4().hex}.part")
        scratch.write_bytes(data)
        os.replace(scratch, target)  # readers see the old bytes or the new, never half

    def get(self, path: str) -> bytes:
        try:
            return self._resolve(path).read_bytes()
        except FileNotFoundError:
            raise BlobNotFound(path) from None

    def delete(self, path: str) -> None:
        self._resolve(path).unlink(missing_ok=True)

    def exists(self, path: str) -> bool:
        return self._resolve(path).is_file()

    def paths(self) -> list[str]:
        return sorted(
            p.relative_to(self.root).as_posix()
            for p in self.root.rglob("*")
            if p.is_file() and not p.name.endswith(".part")
        )
