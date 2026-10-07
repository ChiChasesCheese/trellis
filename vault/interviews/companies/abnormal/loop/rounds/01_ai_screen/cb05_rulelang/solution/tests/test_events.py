"""Loader, config, store and pipeline."""
from __future__ import annotations

import json

import pytest

from rulelang import metrics
from rulelang.config import load_settings
from rulelang.errors import BadRecord, ConfigError
from rulelang.events import load_events, parse_row
from rulelang.store import connect, migrate


def test_parse_email_normalises_addresses_and_timestamps():
    ev = parse_row(
        {"id": "x1", "tenant": "acme", "ts": "2026-09-01T10:00:00+02:00", "kind": "email",
         "from": "Dana <Dana@Acme.Example>", "to": ["ERIN@acme.example"], "subject": "s", "links": ["http://a.example/"]}
    )
    assert ev.actor == "dana@acme.example" and ev.recipients == ("erin@acme.example",)
    assert ev.ts.hour == 8 and ev.ts.tzinfo is not None


@pytest.mark.parametrize(
    "row,reason",
    [
        ({"tenant": "acme", "ts": "2026-09-01T10:00:00Z", "kind": "email", "from": "a@b.c", "to": ["d@e.f"]}, "missing_field"),
        ({"id": "1", "tenant": "acme", "ts": "soon", "kind": "email", "from": "a@b.c", "to": ["d@e.f"]}, "bad_ts"),
        ({"id": "1", "tenant": "acme", "ts": "2026-09-01T10:00:00Z", "kind": "fax"}, "unknown_kind"),
    ],
)
def test_parse_row_rejects_bad_rows(row, reason):
    with pytest.raises(BadRecord) as exc:
        parse_row(row)
    assert exc.value.reason == reason


def test_load_events_counts_bad_records_and_foreign_tenants(events_dir):
    events = list(load_events(events_dir, "acme"))
    assert len(events) == 23
    assert metrics.get("loader.bad_record", reason="bad_ts") == 1
    assert metrics.get("loader.bad_record", reason="bad_json") == 1
    assert metrics.get("loader.bad_record", reason="missing_field") == 1
    assert metrics.total("loader.other_tenant") == 4


def test_tenant_config_overrides_default():
    assert load_settings("acme").detectors.params["mass_mailing"]["recipient_threshold"] == 10
    assert load_settings("globex").detectors.disabled == ("mass_mailing",)
    assert load_settings("globex").org.internal_domains == ("globex.example", "globex-eu.example")


def test_unknown_config_keys_are_errors(tmp_path):
    cfg = tmp_path / "config"
    (cfg / "tenants").mkdir(parents=True)
    default = (load_settings.__globals__["CONFIG_DIR"] / "default.toml").read_text()
    (cfg / "default.toml").write_text(default)
    (cfg / "tenants" / "acme.toml").write_text('[widgets]\nsize = 3\n')
    with pytest.raises(ConfigError, match="unknown config sections: widgets"):
        load_settings("acme", cfg)


def test_migrations_are_idempotent():
    conn = connect()
    assert migrate(conn) == ["0001_init"]
    assert migrate(conn) == []


def test_reingest_does_not_duplicate_stored_signals(app, events_dir):
    first = app.pipeline.ingest_dir(events_dir, "acme")
    second = app.pipeline.ingest_dir(events_dir, "acme")
    # The graph already knows every sender on the second pass, so the first-contact signals do not recur.
    assert len(first) == 10 and len(second) == 5
    assert len(app.pipeline.signals.list("acme", limit=500)) == 10


def test_ingest_unknown_tenant_name_is_rejected(app, tmp_path):
    (tmp_path / "e.jsonl").write_text(json.dumps({"id": "1"}) + "\n")
    with pytest.raises(ConfigError):
        app.pipeline.ingest_dir(tmp_path, "../etc")
