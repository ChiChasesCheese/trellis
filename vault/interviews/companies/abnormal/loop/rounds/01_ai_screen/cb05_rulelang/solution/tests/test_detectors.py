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


# ---------------------------------------------------------------- dependency order

@pytest.fixture
def clean_registry():
    saved = dict(DETECTORS)
    yield
    DETECTORS.clear()
    DETECTORS.update(saved)


def _detector(name, requires=(), fire=True, boom=False):
    class _D(Detector):
        kinds = ("email",)

        def evaluate(self, event, ctx):
            if boom:
                raise RuntimeError("boom")
            if requires and not all(r in ctx.signals for r in requires):
                return self.signal(event, Severity.LOW, "ran without its inputs")
            return self.signal(event, Severity.LOW, "ok") if fire else None

    _D.name, _D.requires = name, tuple(requires)
    return register_detector(_D)


def test_registration_order_does_not_change_results(clean_registry, make_email):
    from rulelang.app import create_app

    ev = make_email(actor="billing@acme-vend0r.example")
    baseline = _names(create_app().pipeline.process(ev))
    reordered = dict(reversed(list(DETECTORS.items())))
    DETECTORS.clear()
    DETECTORS.update(reordered)
    assert _names(create_app().pipeline.process(ev)) == baseline == ["new_sender", "vendor_lookalike"]


def test_detectors_run_after_what_they_require(clean_registry, app, make_email):
    _detector("zz_child", requires=("zz_parent",))
    _detector("zz_parent")
    signals = app.pipeline.process(make_email())
    assert {s.detector: s.summary for s in signals} == {"zz_child": "ok", "zz_parent": "ok"}


def test_cycle_is_reported_at_startup_with_its_members(clean_registry, app, make_email):
    _detector("cyc_a", requires=("cyc_b",))
    _detector("cyc_b", requires=("cyc_c",))
    _detector("cyc_c", requires=("cyc_a",))
    with pytest.raises(ConfigError, match=r"cycle: cyc_a -> cyc_b -> cyc_c -> cyc_a"):
        app.pipeline.process(make_email())


def test_unknown_requirement_is_a_config_error(clean_registry, app, make_email):
    _detector("orphan", requires=("ghost",))
    with pytest.raises(ConfigError, match="requires unknown detector 'ghost'"):
        app.pipeline.process(make_email())


def test_downstream_is_skipped_and_counted_when_upstream_crashes(clean_registry, app, make_email):
    _detector("up", boom=True)
    _detector("down", requires=("up",))
    _detector("down2", requires=("down",))
    assert _names(app.pipeline.process(make_email(actor="ivy@acme.example"))) == []
    assert metrics.get("detector.error", detector="up") == 1
    assert metrics.get("detector.skipped", detector="down", missing="up") == 1
    assert metrics.get("detector.skipped", detector="down2", missing="down") == 1


def test_upstream_not_firing_is_not_a_failure(clean_registry, app, make_email):
    _detector("quiet", fire=False)
    _detector("after_quiet", requires=("quiet",))
    signals = app.pipeline.process(make_email())
    assert [(s.detector, s.summary) for s in signals] == [("after_quiet", "ran without its inputs")]
    assert metrics.total("detector.skipped") == 0


def test_tenant_disabling_an_upstream_skips_its_dependants(tmp_path, make_email):
    import shutil

    from rulelang.app import create_app
    from rulelang.config import CONFIG_DIR, FIXTURES_DIR

    cfg = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, cfg)
    (cfg / "tenants" / "acme.toml").write_text(
        '[tenant]\ninternal_domains = ["acme.example"]\n[detectors]\ndisabled = ["new_sender"]\n'
    )
    app = create_app(config_dir=cfg, fixtures_dir=FIXTURES_DIR)
    assert app.pipeline.process(make_email(actor="billing@acme-vend0r.example")) == []
    assert metrics.get("detector.skipped", detector="vendor_lookalike", missing="new_sender") == 1
