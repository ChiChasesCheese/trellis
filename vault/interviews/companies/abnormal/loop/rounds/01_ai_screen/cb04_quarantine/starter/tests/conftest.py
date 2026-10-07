from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quarantine import metrics  # noqa: E402
from quarantine.actions import FakeMailbox  # noqa: E402
from quarantine.api.testing import TestClient  # noqa: E402
from quarantine.app import create_app  # noqa: E402
from quarantine.config import FIXTURES_DIR  # noqa: E402

NOW = datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _reset_metrics():
    metrics.reset()


@pytest.fixture
def mailbox() -> FakeMailbox:
    return FakeMailbox()


@pytest.fixture
def app(mailbox):
    return create_app(clock=lambda: NOW, mailbox=mailbox)


@pytest.fixture
def acme(app):
    return TestClient(app.wsgi, token="tok-acme-analyst")


@pytest.fixture
def globex(app):
    return TestClient(app.wsgi, token="tok-globex-analyst")


@pytest.fixture
def reports_dir() -> Path:
    return FIXTURES_DIR / "reports"


@pytest.fixture
def make_payload():
    counter = iter(range(1, 10_000))

    def _make(**kw) -> dict:
        n = next(counter)
        payload = {
            "message_id": f"<msg-{n}@mail.example>",
            "reporter": "bob@acme.test",
            "headers": {
                "From": "Digest <digest@newsletter.example>",
                "Date": "Tue, 15 Sep 2026 08:00:00 +0000",
                "Subject": "hello",
            },
            "links": [],
            "attachments": [],
        }
        headers = kw.pop("headers", None)
        payload.update(kw)
        if headers:
            payload["headers"] = {**payload["headers"], **headers}
        return payload

    return _make
