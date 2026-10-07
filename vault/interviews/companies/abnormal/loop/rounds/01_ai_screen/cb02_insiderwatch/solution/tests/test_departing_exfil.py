from datetime import date

from insiderwatch.events import Action
from insiderwatch.hr import Employee, Roster
from insiderwatch.signals import SignalContext, all_signals

from conftest import history, make_event

USER = "ann@acme.example"


def run(baselines, config, employee, day, events):
    ctx = SignalContext(day=day, baselines=baselines, roster=Roster([employee]), config=config)
    sig = next(s for s in all_signals() if s.name == "departing_exfil")
    return list(sig.evaluate(ctx, USER, events))


def leaving(**kw):
    return Employee(USER, "Ann", "Eng", **kw)


def shares(day, n):
    return [make_event(day=day, hour=15, action=Action.FILE_SHARE_EXTERNAL, nbytes=0) for _ in range(n)]


def test_new_external_sharing_in_window_is_flagged(baselines, config):
    baselines.update(history(USER, "2026-09-01", 20))
    out = run(baselines, config, leaving(termination_date=date(2026, 9, 25)), date(2026, 9, 21), shares("2026-09-21", 3))
    assert len(out) == 1 and 0.4 < out[0].strength < 1.0


def test_same_behaviour_outside_window_or_for_stayers_is_ignored(baselines, config):
    baselines.update(history(USER, "2026-09-01", 20))
    today = shares("2026-09-21", 3)
    assert run(baselines, config, leaving(termination_date=date(2026, 11, 30)), date(2026, 9, 21), today) == []
    assert run(baselines, config, leaving(), date(2026, 9, 21), today) == []


def test_usual_volume_is_not_flagged_for_a_heavy_user(baselines, config):
    baselines.update(history(USER, "2026-09-01", 20, per_day=30, nbytes=20_000_000))
    normal = [make_event(day="2026-09-21", nbytes=20_000_000) for _ in range(30)]
    assert run(baselines, config, leaving(termination_date=date(2026, 9, 25)), date(2026, 9, 21), normal) == []


def test_resignation_without_last_day_uses_notice_period(baselines, config):
    baselines.update(history(USER, "2026-09-01", 20))
    emp = leaving(resignation_submitted=date(2026, 9, 20))
    assert len(run(baselines, config, emp, date(2026, 9, 25), shares("2026-09-25", 3))) == 1


def test_cold_start_flags_external_egress_but_not_downloads(baselines, config):
    emp = leaving(termination_date=date(2026, 9, 25))
    assert len(run(baselines, config, emp, date(2026, 9, 21), shares("2026-09-21", 1))) == 1
    assert run(baselines, config, emp, date(2026, 9, 21), [make_event(day="2026-09-21")]) == []


def test_any_activity_after_the_last_day_is_maximum_strength(baselines, config):
    baselines.update(history(USER, "2026-09-01", 20))
    out = run(baselines, config, leaving(termination_date=date(2026, 9, 18)), date(2026, 9, 22),
              [make_event(day="2026-09-22", nbytes=1)])
    assert len(out) == 1 and out[0].strength == 1.0 and out[0].evidence["post_departure"]
