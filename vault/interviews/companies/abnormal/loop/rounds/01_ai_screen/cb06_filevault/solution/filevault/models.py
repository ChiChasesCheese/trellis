"""Plain data objects shared by the layers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from filevault.timeutil import to_iso


@dataclass(frozen=True)
class FileRecord:
    """One user's view of one uploaded file."""

    id: str
    owner: str
    filename: str
    content_type: str
    size: int
    created_at: datetime
    blob_path: str
    sha256: str | None = None  # None for files stored before deduplication

    def to_dict(self) -> dict[str, Any]:
        """The public representation. ``owner`` and ``blob_path`` are internal."""
        return {
            "id": self.id,
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size,
            "created_at": to_iso(self.created_at),
        }


@dataclass(frozen=True)
class FileFilters:
    """Optional narrowing of a listing. ``None`` means "do not filter on this"."""

    q: str | None = None  # case-insensitive substring of the filename
    content_type: str | None = None
    min_size: int | None = None  # inclusive
    max_size: int | None = None  # inclusive
    created_from: datetime | None = None  # inclusive
    created_to: datetime | None = None  # inclusive
