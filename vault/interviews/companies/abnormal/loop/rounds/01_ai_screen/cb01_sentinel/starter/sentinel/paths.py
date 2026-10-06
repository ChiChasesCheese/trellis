"""Well-known locations, resolved relative to the repository checkout."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
FIXTURES_DIR = REPO_ROOT / "fixtures"
DEFAULT_DB = REPO_ROOT / "var" / "sentinel.db"
