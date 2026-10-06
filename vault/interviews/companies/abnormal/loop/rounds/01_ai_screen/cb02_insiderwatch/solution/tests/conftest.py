from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from insiderwatch.baselines import BaselineStore  # noqa: E402
from insiderwatch.config import Config  # noqa: E402
from insiderwatch.db import open_db  # noqa: E402
from insiderwatch.events import Action, Event  # noqa: E402
from insiderwatch.hr import Employee, Roster  # noqa: E402


@pytest.fixture
def fixtures_dir() -> Path:
    return ROOT / "fixtures"


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture
def conn(tmp_path):
    connection = open_db(tmp_path / "iw.db")
    yield connection
    connection.close()


@pytest.fixture
def baselines(conn, config) -> BaselineStore:
    return BaselineStore(conn, config)


@pytest.fixture
def roster() -> Roster:
    return Roster([
        Employee("ann@acme.example", "Ann", "Eng", timezone="America/New_York"),
        Employee("lee@acme.example", "Lee", "Eng", timezone="UTC",
                 resignation_submitted=None, termination_date=None),
    ])


def make_event(user="ann@acme.example", day="2026-09-01", hour=15, action=Action.FILE_DOWNLOAD,
               nbytes=1_000_000, **attrs) -> Event:
    ts = datetime.fromisoformat(day).replace(hour=hour, tzinfo=timezone.utc)
    return Event(user=user, ts=ts, action=action, bytes=nbytes, source="test", attrs=attrs)


def history(user: str, start: str, days: int, per_day: int = 4, nbytes: int = 1_000_000, **attrs):
    """Weekday-agnostic synthetic history: `per_day` downloads every day from `start`."""
    first = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    out = []
    for i in range(days):
        day = (first + timedelta(days=i)).date().isoformat()
        out.extend(make_event(user, day, 14 + k % 3, nbytes=nbytes, **attrs) for k in range(per_day))
    return out
