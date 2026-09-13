"""Fixtures for int02 (payments reconciliation) tests: a real `loop.mockserver.payments`
HTTP server on a random OS-assigned port, started/stopped per test via
`start_in_thread()`. Charge fixture data is deterministic given (seed, n) — see
data/ledger.csv's header comment / problem.md for exactly which (seed, n) it was
generated against."""

from __future__ import annotations

import pytest

from loop.mockserver import payments

API_KEY = "sk_test_123"
LEDGER_SEED = 7
LEDGER_N = 20


@pytest.fixture()
def payments_server():
    """Base URL of a freshly-started payments mockserver seeded to match
    data/ledger.csv (seed=7, n=20), generous rate limit (no 429s by default) and no
    injected 500s. Shuts down after the test."""
    server, thread = payments.start_in_thread(port=0, seed=LEDGER_SEED, n=LEDGER_N, rate=1000, fail_every=0)
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    yield base_url
    server.shutdown()
    server.server_close()
