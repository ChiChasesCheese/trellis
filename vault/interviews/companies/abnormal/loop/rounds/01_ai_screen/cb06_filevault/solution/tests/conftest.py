from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from filevault import metrics
from filevault.app import create_app
from filevault.api.testing import TestClient

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
T0 = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)


class FakeClock:
    """A settable clock; ``tick`` moves it forward."""

    def __init__(self, now: datetime = T0):
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def tick(self, **delta: float) -> None:
        self.now += timedelta(**delta)


@pytest.fixture(autouse=True)
def _fresh_metrics():
    metrics.reset()
    yield
    metrics.reset()


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def app(tmp_path, clock):
    application = create_app(tmp_path / "data", clock=clock, env={})
    yield application
    application.close()


@pytest.fixture
def client(app):
    return TestClient(app.wsgi, user="alice")


def upload(client: TestClient, filename: str, data: bytes, content_type: str = "text/plain"):
    return client.post(
        "/files",
        {
            "filename": filename,
            "content_type": content_type,
            "content_base64": base64.b64encode(data).decode(),
        },
    )


def load_uploads() -> list[dict]:
    return json.loads((FIXTURES / "uploads.json").read_text())
