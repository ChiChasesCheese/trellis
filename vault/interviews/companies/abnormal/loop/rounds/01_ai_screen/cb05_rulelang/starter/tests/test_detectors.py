"""Detectors, the runner and the pipeline's use of them."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from rulelang import metrics
from rulelang.detectors import DETECTORS, Detector, register_detector
from rulelang.errors import ConfigError
from rulelang.models import Event, Severity


def _names(signals):
    return sorted(s.detector for s in signals)


def _login(ts, lat, lon, country, id):
    return Event(id=id, tenant_id="acme", kind="login", ts=ts, actor="dana@acme.example",
                 attrs={"lat": lat, "lon": lon, "country": country, "ip": "198.51.100.1"})


def test_registry_has_the_six_builtin_detectors():
    assert sorted(DETECTORS) == [
        "impossible_travel", "mailbox_forwarding_rule", "mass_mailing",
        "new_sender", "suspicious_link", "vendor_lookalike",
    ]


def test_new_sender_fires_once_then_never_for_a_known_contact(app, make_email):
    first = make_email(actor="bob@fresh-supplier.example", id="e1")
    again = make_email(actor="bob@fresh-supplier.example", id="e2", ts=first.ts + timedelta(hours=1))
    assert _names(app.pipeline.process(first)) == ["new_sender"]
    assert app.pipeline.process(again) == []


def test_internal_sender_is_never_a_new_sender(app, make_email):
    assert app.pipeline.process(make_email(actor="zed@acme.example")) == []


def test_suspicious_link_flags_bad_and_punycode_hosts(app, make_email):
    bad = make_email(links=("https://login-secure.evil-payments.example/x",))
    puny = make_email(links=("https://xn--pypal-4ve.example/",))
    assert [s.severity for s in app.pipeline.process(bad)] == [Severity.HIGH]
    assert [s.severity for s in app.pipeline.process(puny)] == [Severity.MEDIUM]


def test_vendor_lookalike_needs_a_first_contact_and_a_near_miss(app, make_email):
    ev = make_email(actor="billing@acme-vend0r.example")
    assert _names(app.pipeline.process(ev)) == ["new_sender", "vendor_lookalike"]
    real = make_email(actor="billing@acme-vendor.example")
    assert _names(app.pipeline.process(real)) == ["new_sender"]


def test_impossible_travel_uses_the_previous_login(app):
    t0 = datetime(2026, 9, 1, 8, 0, tzinfo=timezone.utc)
    assert app.pipeline.process(_login(t0, 40.71, -74.01, "US", "l1")) == []
    near = app.pipeline.process(_login(t0 + timedelta(hours=1), 40.8, -74.0, "US", "l2"))
    far = app.pipeline.process(_login(t0 + timedelta(hours=2), 6.52, 3.38, "NG", "l3"))
    assert near == [] and _names(far) == ["impossible_travel"]


def test_mailbox_rule_only_external_forwarding_counts(app):
    def rule(id, target):
        return Event(id=id, tenant_id="acme", kind="mailbox_rule_created",
                     ts=datetime(2026, 9, 1, tzinfo=timezone.utc), actor="erin@acme.example",
                     attrs={"rule_name": "r", "forward_to": target})

    assert app.pipeline.process(rule("r1", "ivy@acme.example")) == []
    assert _names(app.pipeline.process(rule("r2", "x@mailbox-drop.example"))) == ["mailbox_forwarding_rule"]


def test_mass_mailing_threshold_is_per_tenant(app, make_email):
    twelve = tuple(f"u{i}@acme.example" for i in range(12))
    assert _names(app.pipeline.process(make_email(recipients=twelve))) == ["mass_mailing"]  # acme: 10
    globex = make_email(tenant_id="globex", actor="news@globex.example", recipients=tuple(f"u{i}@globex.example" for i in range(20)))
    assert app.pipeline.process(globex) == []  # globex switched it off


def test_a_crashing_detector_is_counted_and_does_not_stop_the_others(app, make_email, monkeypatch):
    class Boom(Detector):
        name = "boom"
        kinds = ("email",)

        def evaluate(self, event, ctx):
            raise RuntimeError("kaboom")

    monkeypatch.setitem(DETECTORS, "boom", Boom)
    signals = app.pipeline.process(make_email(actor="bob@fresh-supplier.example"))
    assert _names(signals) == ["new_sender"]
    assert metrics.get("detector.error", detector="boom") == 1


def test_unknown_disabled_detector_is_a_config_error(tmp_path):
    import shutil

    from rulelang.app import create_app
    from rulelang.config import CONFIG_DIR, FIXTURES_DIR

    cfg = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, cfg)
    (cfg / "tenants" / "acme.toml").write_text('[detectors]\ndisabled = ["nope"]\n')
    app = create_app(config_dir=cfg, fixtures_dir=FIXTURES_DIR)
    with pytest.raises(ConfigError, match="nope"):
        app.pipeline.ingest_dir(FIXTURES_DIR / "events", "acme")


def test_register_detector_rejects_duplicates():
    with pytest.raises(ValueError):
        register_detector(DETECTORS["new_sender"])


def test_fixture_run_finds_every_planted_signal(app, events_dir):
    signals = app.pipeline.ingest_dir(events_dir, "acme")
    by_event = {}
    for s in signals:
        by_event.setdefault(s.event_id, set()).add(s.detector)
    assert by_event["a-010"] == {"new_sender", "suspicious_link"}
    assert by_event["a-011"] == {"new_sender", "vendor_lookalike"}
    assert by_event["a-012"] == {"mass_mailing"}
    assert by_event["a-021"] == {"impossible_travel"}
    assert by_event["a-030"] == {"mailbox_forwarding_rule"}
