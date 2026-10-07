from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rulelang import metrics  # noqa: E402
from rulelang.api.testing import TestClient  # noqa: E402
from rulelang.app import create_app  # noqa: E402
from rulelang.config import FIXTURES_DIR  # noqa: E402
from rulelang.models import Event  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_metrics():
    metrics.reset()


@pytest.fixture
def app():
    return create_app()


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
def make_email():
    counter = iter(range(1, 10_000))

    def _make(**kw) -> Event:
        defaults = dict(
            id=f"em-{next(counter)}",
            tenant_id="acme",
            ts=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
            kind="email",
            actor="erin@acme.example",
            recipients=("ivy@acme.example",),
            subject="hello",
            links=(),
        )
        defaults.update(kw)
        return Event(**defaults)

    return _make
