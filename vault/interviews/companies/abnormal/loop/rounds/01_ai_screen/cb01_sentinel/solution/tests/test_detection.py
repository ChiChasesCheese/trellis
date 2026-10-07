"""Detection side: rules, threat levels, ranking and alerts."""
import json
from datetime import datetime, timedelta, timezone

import pytest

from sentinel import metrics
from sentinel.alerts import AlertRepository, AlertService, AlertStatus
from sentinel.config import ConfigError, load_settings
from sentinel.db import EventRepository, connect, migrate
from sentinel.enrichment import EnrichmentService
from sentinel.models import RuleHit, ThreatLevel
from sentinel.rules import RULES, RuleContext, RuleEngine, rule_ids
from sentinel.scoring import AssetCatalog, combine, score

NOW = datetime(2026, 9, 20, tzinfo=timezone.utc)


@pytest.fixture
def harness():
    conn = connect()
    migrate(conn)
    repo = EventRepository(conn)
    settings = load_settings("acme")
    enrich = EnrichmentService(settings, repo)
    engine = RuleEngine(settings)

    def feed(event):
        enrich.enrich(event)
        hits = engine.evaluate(event, RuleContext(repo))
        repo.add(event)
        return hits

    return feed


def test_registry_lists_builtin_rules():
    assert rule_ids() == [
        "brute_force", "impossible_travel", "known_bad_ip", "new_country_login", "rare_admin_action",
    ]
    assert all(cls.id == rid for rid, cls in RULES.items())


def test_impossible_travel_and_new_country(harness, make_event):
    assert harness(make_event()) == []
    hits = harness(make_event(ts=make_event().ts + timedelta(minutes=30), src_ip="198.18.5.5"))
    assert {h.rule_id for h in hits} == {"impossible_travel", "new_country_login"}
    travel = next(h for h in hits if h.rule_id == "impossible_travel")
    assert travel.severity is ThreatLevel.HIGH and travel.evidence["to"] == "SG"


def test_slow_travel_is_fine(harness, make_event):
    harness(make_event())
    hits = harness(make_event(ts=make_event().ts + timedelta(days=2), src_ip="198.18.5.5"))
    assert {h.rule_id for h in hits} == {"new_country_login"}


def test_known_bad_ip_severity_follows_confidence(harness, make_event):
    (c2,) = harness(make_event(src_ip="203.0.113.250", user="u1@acme.test"))
    (tor,) = harness(make_event(src_ip="203.0.113.140", user="u2@acme.test"))
    assert c2.severity is ThreatLevel.CRITICAL
    assert tor.severity is ThreatLevel.HIGH


def test_brute_force_fires_from_threshold(harness, make_event):
    base = make_event().ts
    results = [
        harness(make_event(kind="login_failure", src_ip="198.51.100.99", user="v@acme.test", ts=base + timedelta(seconds=20 * i)))
        for i in range(6)
    ]
    assert [bool(r) for r in results] == [False, False, False, True, True, True]  # acme threshold is 4


def test_rare_admin_action(harness, make_event):
    hits = harness(make_event(source="saas_audit", kind="admin_action", attrs={"action": "mfa.disable", "target": "x"}))
    assert [h.rule_id for h in hits] == ["rare_admin_action"]
    assert harness(make_event(source="saas_audit", kind="admin_action", attrs={"action": "user.delete"})) == []


def test_broken_rule_is_counted_not_raised(make_event):
    conn = connect()
    migrate(conn)
    engine = RuleEngine(load_settings("acme"))
    event = make_event(kind="login_success", enrichment={"history": {"last_login": {"ts": "bogus"}}, "geo": {"lat": 1, "lon": 1, "country": "X"}})
    assert engine.evaluate(event, RuleContext(EventRepository(conn))) == []
    assert metrics.get("rules.error", rule="impossible_travel") == 1


def test_unknown_rule_in_config_is_rejected():
    settings = load_settings("acme")
    bad = type(settings)(**{**settings.__dict__, "rules": {"nope": {}}})
    with pytest.raises(ConfigError):
        RuleEngine(bad)


W = {"LOW": 1, "MEDIUM": 3, "HIGH": 7, "CRITICAL": 15}


def hit(rule_id, level):
    return RuleHit(rule_id, level, "r")


def test_combine_takes_max_and_escalates():
    assert combine([hit("a", ThreatLevel.LOW), hit("b", ThreatLevel.MEDIUM)]) is ThreatLevel.MEDIUM
    three = [hit("a", ThreatLevel.LOW), hit("b", ThreatLevel.LOW), hit("c", ThreatLevel.LOW)]
    assert combine(three) is ThreatLevel.MEDIUM
    assert combine([hit(x, ThreatLevel.CRITICAL) for x in "abc"]) is ThreatLevel.CRITICAL


def test_combine_requires_hits():
    with pytest.raises(ValueError):
        combine([])


def test_score_decays_by_half_life():
    fresh = score(ThreatLevel.HIGH, W, 2.0, 0, 72)
    assert fresh == 14.0
    assert score(ThreatLevel.HIGH, W, 2.0, 72, 72) == 7.0


def test_asset_catalog(tmp_path):
    p = tmp_path / "a.json"
    p.write_text(json.dumps({"default": 1.0, "tenants": {"t": {"users": {"u": 3.0}, "hosts": {"h": 2.0}}}}))
    cat = AssetCatalog(p)
    assert cat.criticality("t", "u", "h") == 3.0
    assert cat.criticality("t", "other", "h") == 2.0
    assert cat.criticality("t", "other") == 1.0
    assert cat.criticality("zzz", "u") == 1.0


def _service():
    conn = connect()
    migrate(conn)
    settings = load_settings("acme")
    repo = AlertRepository(conn)
    return AlertService(settings, repo, AssetCatalog(settings.alerts.assets), lambda: NOW), repo


def test_create_from_scores_and_stores(make_event):
    service, repo = _service()
    event = make_event(user="carol@acme.test", ts=NOW)
    alert = service.create_from(event, [RuleHit("known_bad_ip", ThreatLevel.CRITICAL, "bad")])
    assert alert.threat_level is ThreatLevel.CRITICAL
    assert alert.score == 45.0  # 15 x criticality 3.0, no decay at age 0
    assert repo.get("acme", alert.id).event_ids == [event.id]


def test_repository_is_tenant_scoped(make_event):
    service, repo = _service()
    alert = service.create_from(make_event(), [RuleHit("r", ThreatLevel.LOW, "x")])
    assert repo.get("globex", alert.id) is None
    assert repo.list("globex") == []
    assert repo.set_status("globex", alert.id, AlertStatus.ACKED) is False
    assert repo.set_status("acme", alert.id, AlertStatus.ACKED) is True
    assert repo.count("acme", AlertStatus.OPEN) == 0


# ---------------------------------------------------------------- suppressions


def _suppress_harness():
    from sentinel.suppressions import SuppressionRepository, SuppressionService, new_suppression

    conn = connect()
    migrate(conn)
    repo = SuppressionRepository(conn)
    return repo, SuppressionService(repo, lambda: NOW), new_suppression


def test_match_paths_cover_event_fields_and_enrichment(make_event):
    from sentinel.suppressions import matches, new_suppression

    event = make_event(user="a@acme.test", src_ip="10.1.2.3", enrichment={"geo": {"country": "DE"}})
    mk = lambda m: new_suppression("acme", "brute_force", m, NOW)  # noqa: E731
    assert matches(mk({}), event)
    assert matches(mk({"geo.country": "DE", "user": "a@acme.test"}), event)
    assert matches(mk({"src_ip": "10.0.0.0/8"}), event)
    assert matches(mk({"geo.country": ["FR", "DE"]}), event)
    assert not matches(mk({"geo.country": "FR"}), event)
    assert not matches(mk({"history.new_country": True}), event)  # absent enrichment never matches


def test_apply_drops_and_audits(make_event):
    repo, service, new = _suppress_harness()
    repo.add(new("acme", "known_bad_ip", {}, NOW))
    hits = [RuleHit("known_bad_ip", ThreatLevel.HIGH, "x"), RuleHit("brute_force", ThreatLevel.MEDIUM, "y")]
    kept = service.apply(make_event(), hits)
    assert [h.rule_id for h in kept] == ["brute_force"]
    assert metrics.get("suppression.applied", rule="known_bad_ip") == 1
    assert service.apply(make_event(tenant_id="globex"), hits) == hits


# ---------------------------------------------------------------- alert dedup


def _dedup_service(window=60):
    from dataclasses import replace

    conn = connect()
    migrate(conn)
    settings = load_settings("acme")
    settings = replace(settings, alerts=replace(settings.alerts, dedup_window_minutes=window))
    repo = AlertRepository(conn)
    return AlertService(settings, repo, AssetCatalog(settings.alerts.assets), lambda: NOW), repo


HIT = [RuleHit("brute_force", ThreatLevel.MEDIUM, "spray")]


def test_repeats_inside_the_window_merge(make_event):
    service, repo = _dedup_service()
    base = make_event(ts=NOW)
    first = service.create_from(base, HIT)
    second = service.create_from(make_event(ts=NOW + timedelta(minutes=50)), [RuleHit("brute_force", ThreatLevel.HIGH, "spray")])
    third = service.create_from(make_event(ts=NOW + timedelta(minutes=100)), HIT)  # 50 min after the last one
    assert first.id == second.id == third.id
    stored = repo.get("acme", first.id)
    assert stored.event_count == 3 and len(stored.event_ids) == 3
    assert stored.threat_level is ThreatLevel.HIGH  # the highest level seen wins
    assert repo.count("acme") == 1


def test_different_source_or_window_opens_a_new_alert(make_event):
    service, repo = _dedup_service(window=30)
    first = service.create_from(make_event(ts=NOW), HIT)
    assert service.create_from(make_event(ts=NOW, user="bob@acme.test"), HIT).id != first.id
    assert service.create_from(make_event(ts=NOW + timedelta(minutes=31)), HIT).id != first.id
    assert repo.count("acme") == 3


def test_acked_alert_is_not_reopened_by_new_events(make_event):
    service, repo = _dedup_service()
    first = service.create_from(make_event(ts=NOW), HIT)
    repo.set_status("acme", first.id, AlertStatus.ACKED)
    second = service.create_from(make_event(ts=NOW + timedelta(minutes=1)), HIT)
    assert second.id != first.id and repo.get("acme", first.id).event_count == 1


def test_window_zero_disables_dedup(make_event):
    service, repo = _dedup_service(window=0)
    service.create_from(make_event(ts=NOW), HIT)
    service.create_from(make_event(ts=NOW), HIT)
    assert repo.count("acme") == 2


def test_event_count_raises_the_score(make_event):
    service, _ = _dedup_service()
    one = service.create_from(make_event(ts=NOW, user="x@acme.test"), HIT)
    score_one = one.score
    again = service.create_from(make_event(ts=NOW, user="x@acme.test"), HIT)
    assert again.score > score_one
