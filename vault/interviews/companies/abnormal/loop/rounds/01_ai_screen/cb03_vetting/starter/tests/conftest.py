from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vetting.api.app import create_app
from vetting.api.testing import TestClient
from vetting.lookups import build_lookups
from vetting.models import Identity, Kind, Observation
from vetting.pipeline import Pipeline
from vetting.settings import DEFAULT_CONFIG_DIR, DEFAULT_INTEL_DIR, PROJECT_ROOT, load_settings
from vetting.signals import SignalContext
from vetting.store import Store

FIXTURES = PROJECT_ROOT / "fixtures"
T0 = datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def store() -> Store:
    s = Store.open(":memory:")
    yield s
    s.close()


@pytest.fixture
def settings():
    return load_settings("globex", DEFAULT_CONFIG_DIR)


@pytest.fixture
def lookups():
    return build_lookups(DEFAULT_INTEL_DIR)


@pytest.fixture
def make_ctx(settings, lookups, store):
    """Build a SignalContext from ``(kind, value)`` pairs for one made-up identity."""

    def build(*pairs: tuple[Kind, str], identity_id: str = "greenhouse:1", name: str = "Test Person") -> SignalContext:
        identity = Identity(identity_id, "globex", "greenhouse", identity_id.split(":")[1], name, T0)
        observations = [
            Observation(identity_id, "globex", kind, value, "greenhouse", T0, f"{identity_id}#t{i}")
            for i, (kind, value) in enumerate(pairs)
        ]
        return SignalContext(identity, observations, lookups, settings, store)

    return build


@pytest.fixture
def db_path(tmp_path) -> Path:
    return tmp_path / "vetting.db"


@pytest.fixture
def ingested(db_path):
    """Fixtures ingested for tenant acme; returns the db path."""
    store = Store.open(db_path)
    Pipeline.for_tenant("acme", store).ingest(FIXTURES)
    store.close()
    return db_path


@pytest.fixture
def client(ingested) -> TestClient:
    return TestClient(create_app(ingested), token="tok-acme-reviewer")


def write_json(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return path
