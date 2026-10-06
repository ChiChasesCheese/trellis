"""t3 -- alert de-duplication. New name: `event_count` on alerts. Windows/keys are the candidate's design."""
from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb01_support import T0, US, build_env, burst, travel  # noqa: E402

pytestmark = pytest.mark.t3

SOURCE_IP = "198.51.100.99"  # a plain US address, not on any intel list
# acme alerts from the 4th failed login inside 10 minutes, so a 12-attempt burst trips the rule 9 times.
HITS_IN_12 = 9


@pytest.fixture
def env(codebase_root_path, tmp_path):
    return build_env(codebase_root_path, tmp_path)


@pytest.mark.regression
def test_below_threshold_failures_raise_no_alert(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 3))
    assert env.alerts("acme", status=None) == []


@pytest.mark.regression
def test_ack_still_works(env):
    env.ingest("acme", travel("acme", "alice@acme.test"))
    alert = env.alerts("acme")[0]
    assert env.client("acme").post(f"/alerts/{alert['id']}/ack").json["status"] == "ACKED"


@pytest.mark.core
def test_one_source_one_open_alert(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12))
    assert len(env.alerts("acme", rule="brute_force")) == 1


@pytest.mark.core
def test_event_count_covers_every_event_that_tripped_the_rule(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12))
    (alert,) = env.alerts("acme", rule="brute_force")
    assert alert["event_count"] == HITS_IN_12


@pytest.mark.core
def test_event_count_is_present_and_one_for_a_single_event_alert(env):
    env.ingest("acme", travel("acme", "alice@acme.test"))
    alerts = env.alerts("acme", rule="impossible_travel")
    assert len(alerts) == 1 and alerts[0]["event_count"] == 1


@pytest.mark.core
def test_different_users_and_sources_do_not_merge(env):
    env.ingest(
        "acme",
        burst("acme", "v1@acme.test", SOURCE_IP, 6, prefix="a"),
        burst("acme", "v2@acme.test", "198.51.100.98", 6, prefix="b"),
    )
    assert len(env.alerts("acme", rule="brute_force")) == 2


@pytest.mark.core
def test_a_burst_days_later_is_a_new_alert(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12, prefix="first"))
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12, start=T0 + timedelta(days=4), prefix="second"))
    alerts = env.alerts("acme", rule="brute_force")
    assert len(alerts) == 2
    assert sorted(a["event_count"] for a in alerts) == [HITS_IN_12, HITS_IN_12]


@pytest.mark.core
def test_events_after_an_ack_open_a_fresh_alert(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12, prefix="first"))
    (first,) = env.alerts("acme", rule="brute_force")
    assert env.client("acme").post(f"/alerts/{first['id']}/ack").status_code == 200

    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 6, start=T0 + timedelta(minutes=20), prefix="second"))
    fresh = env.alerts("acme", status="OPEN", rule="brute_force")
    assert len(fresh) == 1 and fresh[0]["id"] != first["id"]
    acked = env.client("acme").get(f"/alerts/{first['id']}").json
    assert acked["status"] == "ACKED" and acked["event_count"] == HITS_IN_12  # history was not rewritten


@pytest.mark.core
def test_tenants_dedup_independently(env):
    env.ingest("acme", burst("acme", "v@shared.test", SOURCE_IP, 12, prefix="a"))
    env.ingest("globex", burst("globex", "v@shared.test", SOURCE_IP, 12, prefix="g"))
    assert len(env.alerts("acme", rule="brute_force")) == 1
    assert len(env.alerts("globex", rule="brute_force")) == 1


@pytest.mark.stretch
def test_alert_detail_also_reports_event_count(env):
    env.ingest("acme", burst("acme", "v@acme.test", SOURCE_IP, 12))
    (alert,) = env.alerts("acme", rule="brute_force")
    assert env.client("acme").get(f"/alerts/{alert['id']}").json["event_count"] == HITS_IN_12


@pytest.mark.stretch
def test_a_bigger_flood_outranks_a_smaller_one_of_the_same_severity(env):
    # The big one is 30 minutes *older*, so recency alone would rank the small one first.
    env.ingest("acme", burst("acme", "big@acme.test", SOURCE_IP, 12, start=T0, prefix="big"))
    env.ingest("acme", burst("acme", "small@acme.test", "198.51.100.98", 5, start=T0 + timedelta(minutes=30), prefix="small"))
    order = [a["event_count"] for a in env.alerts("acme", rule="brute_force")]  # API order: highest score first
    assert order == sorted(order, reverse=True) and order[0] == HITS_IN_12
