"""Acceptance-test target selection (copy verbatim into cbNN_*/acceptance/conftest.py, set PACKAGE).

Which copy of the codebase is under test:
  CODEBASE=/abs/path   your practice copy (loop/ai_screen.py check sets this)
  IMPL=starter         the untouched starter (must fail every `core` test)
  (default)            the reference solution
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

PACKAGE = "rulelang"  # top-level package name of the codebase
HERE = Path(__file__).resolve().parent


def codebase_root() -> Path:
    if os.environ.get("CODEBASE"):
        return Path(os.environ["CODEBASE"]).resolve()
    return (HERE.parent / ("starter" if os.environ.get("IMPL") == "starter" else "solution")).resolve()


ROOT = codebase_root()
for name in [m for m in sys.modules if m == PACKAGE or m.startswith(PACKAGE + ".")]:
    del sys.modules[name]
sys.path.insert(0, str(ROOT))


def pytest_configure(config):
    for m in ("core", "stretch", "regression"):
        config.addinivalue_line("markers", f"{m}: acceptance tier")
    for t in ("t1", "t2", "t3"):
        config.addinivalue_line("markers", f"{t}: ticket")


@pytest.fixture
def codebase_root_path() -> Path:
    return ROOT
