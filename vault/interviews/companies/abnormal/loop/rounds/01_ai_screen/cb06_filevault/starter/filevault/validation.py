"""Input validation shared by the service (and so by the API and the CLI)."""
from __future__ import annotations

import re

from filevault.errors import InvalidInput

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
