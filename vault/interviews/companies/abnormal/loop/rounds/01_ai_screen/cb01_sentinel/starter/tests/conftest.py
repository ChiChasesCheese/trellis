from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentinel import metrics  # noqa: E402
from sentinel.api.testing import TestClient  # noqa: E402
from sentinel.app import create_app  # noqa: E402
from sentinel.models import SecurityEvent  # noqa: E402
from sentinel.config import FIXTURES_DIR  # noqa: E402

NOW = datetime(2026, 9, 20, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _reset_metrics():
    metrics.reset()


@pytest.fixture
def app():
    return create_app(clock=lambda: NOW)


@pytest.fixture
def acme(app):
    return TestClient(app.wsgi, token="tok-acme-analyst")


@pytest.fixture
def globex(app):
    return TestClient(app.wsgi, token="tok-globex-analyst")


@pytest.fixture
def events_dir() -> Path:
    return FIXTURES_DIR / "events"


@pytest.fixture
def make_event():
    counter = iter(range(1, 10_000))

    def _make(**kw) -> SecurityEvent:
        defaults = dict(
            id=f"ev-{next(counter)}",
            tenant_id="acme",
            ts=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
            source="auth_log",
            kind="login_success",
            user="alice@acme.test",
            src_ip="198.51.100.7",
            attrs={"device": "d1"},
        )
        defaults.update(kw)
        return SecurityEvent(**defaults)

    return _make
