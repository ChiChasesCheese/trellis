"""One place that decides how log lines look."""
from __future__ import annotations

import logging
import os
import sys

FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"


def configure_logging(level: str | None = None) -> None:
    """Log to stderr at ``level`` (default: ``FILEVAULT_LOG_LEVEL`` or WARNING). Safe to call twice."""
    name = (level or os.environ.get("FILEVAULT_LOG_LEVEL") or "WARNING").upper()
    root = logging.getLogger("filevault")
    root.setLevel(getattr(logging, name, logging.WARNING))
    if not any(getattr(h, "_filevault", False) for h in root.handlers):
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(FORMAT))
        handler._filevault = True  # type: ignore[attr-defined]
        root.addHandler(handler)
