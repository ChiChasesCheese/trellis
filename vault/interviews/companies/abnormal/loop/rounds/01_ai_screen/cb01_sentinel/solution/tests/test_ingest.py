"""Ingestion side: collectors, enrichment, config, db, pipeline and CLI."""
import io
import json
from datetime import datetime, timedelta, timezone

import pytest

from sentinel import metrics
from sentinel.cli import main
from sentinel.collectors import COLLECTORS, collect_all
from sentinel.config import FIXTURES_DIR, ConfigError, SettingsProvider, load_settings
from sentinel.db import EventRepository, connect, migrate
from sentinel.enrichment import EnrichmentContext, EnrichmentService
from sentinel.enrichment.geo_ip import GeoIpEnricher
from sentinel.enrichment.history import HistoryEnricher
from sentinel.enrichment.threat_intel import ThreatIntelEnricher
from sentinel.timeutil import iso, parse_ts, sliding_window


def test_all_sources_registered():
    assert set(COLLECTORS) == {"auth_log", "endpoint", "saas_audit"}


def test_collect_all_is_tenant_scoped_and_sorted(events_dir):
    events = collect_all(events_dir, "acme")
    assert events and all(e.tenant_id == "acme" for e in events)
    assert [e.ts for e in events] == sorted(e.ts for e in events)
    assert {e.source for e in events} == {"auth_log", "endpoint", "saas_audit"}


def test_bad_records_are_counted_and_skipped(events_dir):
    collect_all(events_dir, "acme")
    assert metrics.get("collector.bad_record", source="auth_log") == 2
    assert metrics.get("collector.bad_record", source="endpoint") == 1


def test_auth_log_normalization(tmp_path):
    d = tmp_path / "auth_log"
    d.mkdir()
    (d / "x.jsonl").write_text(
        json.dumps({"id": "1", "tenant": "t", "time": "2026-09-01T10:00:00+02:00", "user": "A@T.test", "ip": "1.2.3.4", "ua": "ua", "result": "failure"})
        + "\n"
    )
    (event,) = collect_all(tmp_path, "t")
    assert event.kind == "login_failure"
    assert event.user == "a@t.test"
    assert event.ts.hour == 8 and event.ts.utcoffset().total_seconds() == 0


def test_saas_audit_marks_admin_actions(events_dir):
    kinds = {e.id: e.kind for e in collect_all(events_dir, "acme") if e.source == "saas_audit"}
    assert kinds["s-1"] == "admin_action"
    assert kinds["s-2"] == "audit"


def _ctx():
    conn = connect()
    migrate(conn)
    settings = load_settings("acme")
    return settings, EnrichmentContext(settings, EventRepository(conn))


def test_geo_longest_prefix_wins(make_event):
    settings, ctx = _ctx()
    geo = GeoIpEnricher(settings)
    assert geo.enrich(make_event(src_ip="203.0.113.10"), ctx)["country"] == "DE"
    assert geo.enrich(make_event(src_ip="203.0.113.200"), ctx)["country"] == "RU"
    assert geo.enrich(make_event(src_ip="10.0.0.1"), ctx) == {}
    assert geo.enrich(make_event(src_ip=None), ctx) == {}


def test_threat_intel_exact_and_cidr(make_event):
    settings, ctx = _ctx()
    ti = ThreatIntelEnricher(settings)
    assert ti.enrich(make_event(src_ip="203.0.113.250"), ctx)["feed"] == "botnet-c2"
    assert ti.enrich(make_event(src_ip="198.18.200.9"), ctx)["feed"] == "scanner-farm"
    assert ti.enrich(make_event(src_ip="198.51.100.7"), ctx) == {}


def test_history_sees_only_earlier_events(make_event):
    settings, ctx = _ctx()
    service = EnrichmentService(settings, ctx.events)
    first = service.enrich(make_event(id="h1"))
    assert first.enrichment["history"]["known_user"] is False
    ctx.events.add(first)
    later = service.enrich(make_event(id="h2", ts=first.ts + timedelta(hours=1), src_ip="203.0.113.10"))
    hist = later.enrichment["history"]
    assert hist["known_user"] is True
    assert hist["seen_countries"] == ["US"]
    assert hist["new_country"] is True
    assert hist["last_login"]["country"] == "US"


def test_history_depends_on_geo(make_event):
    assert HistoryEnricher.requires == ("geo",)


def test_migrate_is_idempotent():
    conn = connect()
    applied = migrate(conn)
    assert applied[0] == "0001_init" and applied == sorted(applied)
    assert migrate(conn) == []


def test_events_are_keyed_per_tenant(make_event):
    conn = connect()
    migrate(conn)
    repo = EventRepository(conn)
    repo.add(make_event(id="same", tenant_id="acme"))
    repo.add(make_event(id="same", tenant_id="globex"))
    assert repo.count("acme") == 1 and repo.count("globex") == 1
    assert repo.get("acme", "same").tenant_id == "acme"


def test_tenant_override_merges_over_default():
    acme = load_settings("acme")
    assert acme.rules["brute_force"] == {"threshold": 4, "window_minutes": 10}
    assert load_settings("unknown-tenant").rules["brute_force"]["threshold"] == 5
    assert load_settings("globex").rules["new_country_login"]["enabled"] is False


def test_unknown_keys_and_sections_are_errors(tmp_path):
    (tmp_path / "tenants").mkdir()
    default = (load_settings.__globals__["CONFIG_DIR"] / "default.toml").read_text()
    (tmp_path / "default.toml").write_text(default)
    (tmp_path / "tenants" / "bad.toml").write_text("[enrichment]\nnonsense = 1\n")
    with pytest.raises(ConfigError, match="unknown keys"):
        load_settings("bad", config_dir=tmp_path)
    (tmp_path / "tenants" / "bad.toml").write_text("[mystery]\nx = 1\n")
    with pytest.raises(ConfigError, match="unknown config sections"):
        load_settings("bad", config_dir=tmp_path)


def test_tenant_names_are_validated():
    with pytest.raises(ConfigError):
        load_settings("../etc")


def test_provider_caches():
    p = SettingsProvider()
    assert p.for_tenant("acme") is p.for_tenant("acme")


T0 = datetime(2026, 9, 1, tzinfo=timezone.utc)


def test_parse_ts_variants():
    assert parse_ts("2026-09-01T00:00:00Z") == T0
    assert parse_ts("2026-08-31T17:00:00-07:00") == T0
    assert parse_ts(T0.timestamp()) == T0
    assert iso(T0) == "2026-09-01T00:00:00Z"


def test_parse_ts_rejects_naive():
    with pytest.raises(ValueError):
        parse_ts("2026-09-01T00:00:00")


def test_sliding_window_counts_densest_span():
    stamps = [T0 + timedelta(minutes=m) for m in (0, 1, 2, 30, 31)]
    assert sliding_window(stamps, timedelta(minutes=5)) == 3
    assert sliding_window(stamps, timedelta(hours=1)) == 5
    assert sliding_window([], timedelta(minutes=5)) == 0


def test_fixture_run_produces_expected_alerts(app, events_dir):
    alerts = app.pipeline.ingest_dir(events_dir, "acme")
    by_rule = {}
    for a in alerts:
        for rid in a.rule_ids:
            by_rule.setdefault(rid, []).append(a)
    assert len(by_rule["impossible_travel"]) == 1
    assert len(by_rule["new_country_login"]) == 3  # alice -> SG, carol -> DE, bob -> DE
    assert len(by_rule["brute_force"]) == 5  # attempts 4..8 at acme's threshold of 4
    assert len(by_rule["rare_admin_action"]) == 2
    assert max(a.threat_level for a in alerts).name == "CRITICAL"


def test_events_are_stored_with_enrichment(app, events_dir):
    app.pipeline.ingest_dir(events_dir, "acme")
    assert app.pipeline.events.get("acme", "a-003").enrichment["geo"]["city"] == "Singapore"
    assert app.pipeline.events.get("globex", "a-003") is None


def test_ingest_counts_events(app, events_dir):
    app.pipeline.ingest_dir(events_dir, "globex")
    assert metrics.get("pipeline.events") == 5


def test_ingest_then_alerts(tmp_path):
    db = tmp_path / "s.db"
    out = io.StringIO()
    assert main(["ingest", str(FIXTURES_DIR / "events"), "--tenant", "acme", "--db", str(db)], out) == 0
    assert "alerts" in out.getvalue()
    out = io.StringIO()
    assert main(["alerts", "--tenant", "acme", "--db", str(db), "--limit", "3"], out) == 0
    lines = out.getvalue().strip().splitlines()
    assert len(lines) == 3 and lines[0].split()[1] == "CRITICAL"


def test_rules_command():
    out = io.StringIO()
    assert main(["rules"], out) == 0
    assert "impossible_travel" in out.getvalue()


def test_config_error_exits_2(tmp_path, capsys):
    assert main(["ingest", str(tmp_path), "--tenant", "Bad Name", "--db", str(tmp_path / "x.db")]) == 2
    assert "invalid tenant" in capsys.readouterr().err
