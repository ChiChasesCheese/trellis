"""Puts src/ on sys.path so `import fetchrace` works whether this repo is run in place or copied
elsewhere wholesale (loop/mock.py copies the whole problem dir, minus solution/ and REPORT.md,
into loop/work/<id>/ and runs pytest there -- this file must keep working after that copy)."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
for p in (SRC, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pytest  # noqa: E402

from support.server import make_server  # noqa: E402


@pytest.fixture()
def http_server():
    """Starts the local test HTTP server (see tests/support/server.py) for the duration of one
    test and shuts it down afterward. Yields the server's base URL."""
    base_url, server = make_server(fail_times=2)
    try:
        yield base_url
    finally:
        server.shutdown()
        server.server_close()
