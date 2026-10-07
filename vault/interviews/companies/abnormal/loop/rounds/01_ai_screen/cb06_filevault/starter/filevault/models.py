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

    def to_dict(self) -> dict[str, Any]:
        """The public representation. ``owner`` and ``blob_path`` are internal."""
        return {
            "id": self.id,
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size,
            "created_at": to_iso(self.created_at),
        }
