"""Opaque keyset cursors over ``(created_at, id)``, newest first."""
from __future__ import annotations

import base64
import binascii
import json
from dataclasses import dataclass

from filevault.errors import InvalidInput


@dataclass(frozen=True)
class Page:
    """Where to resume (``after`` is the last ``(created_at, id)`` already seen) and how much."""

    after: tuple[str, str] | None
    limit: int


def encode_cursor(created_at: str, file_id: str) -> str:
    raw = json.dumps([created_at, file_id]).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def paginate(cursor: str | None, limit: int, max_limit: int = 200) -> Page:
    """Validate ``limit`` and decode ``cursor``; bad input is an ``InvalidInput``."""
    if not 1 <= limit <= max_limit:
        raise InvalidInput("limit", f"limit must be between 1 and {max_limit}")
    if not cursor:
        return Page(None, limit)
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        created_at, file_id = json.loads(base64.urlsafe_b64decode(padded))
        if not (isinstance(created_at, str) and isinstance(file_id, str)):
            raise ValueError
    except (binascii.Error, ValueError, TypeError):
        raise InvalidInput("cursor", "cursor is not valid") from None
    return Page((created_at, file_id), limit)
