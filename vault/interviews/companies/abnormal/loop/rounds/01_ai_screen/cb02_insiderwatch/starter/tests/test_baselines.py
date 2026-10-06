from datetime import date

from insiderwatch.events import Action
from insiderwatch.baselines.stats import mean, pstdev, percentile

from conftest import history, make_event


def test_stats_helpers():
    assert mean([1, 2, 3]) == 2
    assert pstdev([2, 2, 2]) == 0
    assert percentile([0, 10], 0.95) == 9.5
    assert percentile([], 0.5) == 0.0


def test_cold_start_returns_none(baselines):
    baselines.update(history("ann@acme.example", "2026-09-01", 5))
    assert baselines.get("ann@acme.example", Action.FILE_DOWNLOAD, date(2026, 9, 6)) is None
    assert baselines.get("nobody@acme.example", Action.FILE_DOWNLOAD, date(2026, 9, 6)) is None


def test_baseline_after_min_days(baselines, config):
    baselines.update(history("ann@acme.example", "2026-09-01", 20, per_day=4, nbytes=1_000_000))
    b = baselines.get("ann@acme.example", Action.FILE_DOWNLOAD, date(2026, 9, 21))
    assert b.days_observed == 20
    assert b.mean_count == 4 and b.std_count == 0
    assert b.mean_bytes == 4_000_000


def test_get_excludes_the_day_itself(baselines):
    baselines.update(history("ann@acme.example", "2026-09-01", 20))
    baselines.update([make_event(day="2026-09-21", nbytes=900_000_000)])
    b = baselines.get("ann@acme.example", Action.FILE_DOWNLOAD, date(2026, 9, 21))
    assert b.mean_bytes == 4_000_000


def test_never_seen_action_is_a_real_zero(baselines):
    baselines.update(history("ann@acme.example", "2026-09-01", 20))
    b = baselines.get("ann@acme.example", Action.FILE_SHARE_EXTERNAL, date(2026, 9, 21))
    assert b is not None and b.mean_count == 0 and b.p95_count == 0


def test_window_is_capped(baselines, config):
    baselines.update(history("ann@acme.example", "2026-07-01", 80))
    b = baselines.get("ann@acme.example", Action.FILE_DOWNLOAD, date(2026, 9, 20))
    assert b.days_observed == config.baseline_window_days


def test_update_is_additive_within_a_day(baselines):
    baselines.update([make_event(day="2026-09-01")])
    baselines.update([make_event(day="2026-09-01")])
    row = baselines._conn.execute("SELECT count FROM daily_totals").fetchone()
    assert row["count"] == 2


def test_known_countries_from_logins(baselines):
    baselines.update([make_event(action=Action.LOGIN, country="US"), make_event(action=Action.LOGIN, country="DE")])
    assert baselines.known_countries("ann@acme.example") == {"US", "DE"}
