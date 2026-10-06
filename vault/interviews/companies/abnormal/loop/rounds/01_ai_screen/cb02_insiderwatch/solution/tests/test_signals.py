from datetime import date

from insiderwatch.events import Action
from insiderwatch.signals import SignalContext, all_signals, signal_names
from insiderwatch.signals.base import Signal

from conftest import history, make_event


def ctx_for(baselines, roster, config, day):
    return SignalContext(day=day, baselines=baselines, roster=roster, config=config)


def findings(name, ctx, user, events):
    sig = next(s for s in all_signals() if s.name == name)
    return list(sig.evaluate(ctx, user, events))


def test_registry_names():
    assert {"volume_spike", "off_hours_activity", "unusual_login_location"} <= set(signal_names())
    assert all(isinstance(s, Signal) for s in all_signals())


def test_volume_spike_fires_on_outlier_day(baselines, roster, config):
    baselines.update(history("ann@acme.example", "2026-09-01", 20, nbytes=1_000_000))
    today = [make_event(day="2026-09-21", nbytes=500_000_000)]
    out = findings("volume_spike", ctx_for(baselines, roster, config, date(2026, 9, 21)), "ann@acme.example", today)
    assert len(out) == 1 and out[0].strength == 1.0


def test_volume_spike_quiet_on_normal_day_and_cold_start(baselines, roster, config):
    ctx = ctx_for(baselines, roster, config, date(2026, 9, 21))
    big = [make_event(day="2026-09-21", nbytes=500_000_000)]
    assert findings("volume_spike", ctx, "ann@acme.example", big) == []  # no history: cold start
    baselines.update(history("ann@acme.example", "2026-09-01", 20))
    normal = [make_event(day="2026-09-21") for _ in range(4)]
    assert findings("volume_spike", ctx, "ann@acme.example", normal) == []


def test_off_hours_uses_roster_timezone(baselines, roster, config):
    ctx = ctx_for(baselines, roster, config, date(2026, 9, 1))
    evening_utc = make_event(day="2026-09-01", hour=22)  # 18:00 in New York, 22:00 UTC
    assert len(findings("off_hours_activity", ctx, "ann@acme.example", [evening_utc])) == 1
    midday_ny = make_event(day="2026-09-01", hour=15)
    assert findings("off_hours_activity", ctx, "ann@acme.example", [midday_ny]) == []


def test_off_hours_ignores_logins(baselines, roster, config):
    ctx = ctx_for(baselines, roster, config, date(2026, 9, 6))
    assert findings("off_hours_activity", ctx, "lee@acme.example",
                    [make_event(user="lee@acme.example", day="2026-09-06", hour=3, action=Action.LOGIN)]) == []


def test_unusual_location_needs_history_and_a_new_country(baselines, roster, config):
    ctx = ctx_for(baselines, roster, config, date(2026, 9, 21))
    new = [make_event(day="2026-09-21", action=Action.LOGIN, country="BR")]
    assert findings("unusual_login_location", ctx, "ann@acme.example", new) == []
    baselines.update(history("ann@acme.example", "2026-09-01", 20, per_day=1, country="US")
                     + [make_event(day="2026-09-02", action=Action.LOGIN, country="US")])
    assert len(findings("unusual_login_location", ctx, "ann@acme.example", new)) == 1
    home = [make_event(day="2026-09-21", action=Action.LOGIN, country="US")]
    assert findings("unusual_login_location", ctx, "ann@acme.example", home) == []
