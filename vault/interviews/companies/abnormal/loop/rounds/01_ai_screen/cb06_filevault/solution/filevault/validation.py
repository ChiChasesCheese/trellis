"""Input validation shared by the service (and so by the API and the CLI)."""
from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime

from filevault.errors import InvalidInput
from filevault.models import FileFilters
from filevault.timeutil import parse_iso

MAX_FILENAME = 255
_CONTENT_TYPE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+(\s*;.*)?$")
DEFAULT_CONTENT_TYPE = "application/octet-stream"


def clean_filename(raw: str) -> str:
    """Trimmed filename, 1-255 characters, no path separators or NULs."""
    name = raw.strip()
    if not name or len(name) > MAX_FILENAME or "/" in name or "\\" in name or "\x00" in name:
        raise InvalidInput("filename", "filename must be 1-255 characters without slashes")
    return name


def clean_content_type(raw: str | None) -> str:
    """A ``type/subtype`` media type; empty means the generic binary type."""
    if not raw or not raw.strip():
        return DEFAULT_CONTENT_TYPE
    value = raw.strip()
    if not _CONTENT_TYPE.match(value):
        raise InvalidInput("content_type", f"not a media type: {value!r}")
    return value


def _size(raw: Mapping[str, str | None], name: str) -> int | None:
    value = raw.get(name)
    if value is None or value == "":
        return None
    try:
        size = int(value)
    except ValueError:
        raise InvalidInput(name, f"{name} must be a whole number of bytes") from None
    if size < 0:
        raise InvalidInput(name, f"{name} cannot be negative")
    return size


def _moment(raw: Mapping[str, str | None], name: str) -> datetime | None:
    value = raw.get(name)
    if value is None or value == "":
        return None
    try:
        return parse_iso(value)
    except ValueError:
        raise InvalidInput(name, f"{name} must be an ISO-8601 date or datetime") from None


def parse_filters(raw: Mapping[str, str | None]) -> FileFilters:
    """Build ``FileFilters`` from query-string values; anything unusable names its parameter."""
    filters = FileFilters(
        q=(raw.get("q") or "").strip() or None,
        content_type=(raw.get("type") or "").strip() or None,
        min_size=_size(raw, "min_size"),
        max_size=_size(raw, "max_size"),
        created_from=_moment(raw, "from"),
        created_to=_moment(raw, "to"),
    )
    if None not in (filters.min_size, filters.max_size) and filters.min_size > filters.max_size:
        raise InvalidInput("min_size", "min_size cannot exceed max_size")
    if None not in (filters.created_from, filters.created_to) and filters.created_from > filters.created_to:
        raise InvalidInput("from", "from cannot be after to")
    return filters
