"""t3_burst_scale: thousands of reports of one message become one incident with a reporter count."""
from __future__ import annotations

import time

import pytest

from cb04_support import BAD_LINK, build_env, payload
from quarantine import metrics

pytestmark = pytest.mark.t3

ANALYZERS = ("attachment_type", "display_name_spoof", "link_reputation", "sender_reputation")


@pytest.fixture
def env(tmp_path):
    return build_env(tmp_path)


def _report_many(env, message_id: str, n: int, tenant: str = "acme", **kw):
    last = None
    for i in range(n):
        last = env.post(tenant, payload(message_id, reporter=f"user{i}@acme.test", **kw))
        assert last.status_code in (200, 201), last.json
    return last


@pytest.mark.core
def test_a_first_report_has_a_reporter_count_of_one(env):
    resp = env.post("acme", payload("<a@m>", links=(BAD_LINK,)))
    assert resp.json["reporter_count"] == 1
    assert env.get("acme", resp.json["id"]).json["reporter_count"] == 1


@pytest.mark.core
def test_three_reporters_make_a_count_of_three(env):
    _report_many(env, "<a@m>", 3, links=(BAD_LINK,))
    items = env.listing("acme")["items"]
    assert len(items) == 1
    assert items[0]["reporter_count"] == 3
    assert env.get("acme", items[0]["id"]).json["reporter_count"] == 3


@pytest.mark.core
def test_analyzers_run_once_however_many_people_report(env):
    _report_many(env, "<a@m>", 50, links=(BAD_LINK,))
    for name in ANALYZERS:
        assert metrics.get("analyzer.run", analyzer=name) == 1, name


@pytest.mark.core
def test_a_burst_of_two_thousand_is_one_incident_and_fast(env):
    started = time.perf_counter()
    last = _report_many(env, "<campaign@m>", 2000, links=(BAD_LINK,))
    elapsed = time.perf_counter() - started
    assert last.json["reporter_count"] == 2000
    assert elapsed < 2.0, f"{elapsed:.2f}s"
    assert env.listing("acme")["total"] == 1
    assert len(env.mailbox.calls_of("quarantine")) == 1
    assert metrics.get("analyzer.run", analyzer="link_reputation") == 1


@pytest.mark.core
def test_the_listing_shows_a_count_per_incident(env):
    _report_many(env, "<a@m>", 4, links=(BAD_LINK,))
    _report_many(env, "<b@m>", 2)
    counts = {i["message_id"]: i["reporter_count"] for i in env.listing("acme")["items"]}
    assert counts == {"<a@m>": 4, "<b@m>": 2}


@pytest.mark.stretch
def test_the_same_person_reporting_twice_counts_once(env):
    for _ in range(3):
        env.post("acme", payload("<a@m>", reporter="bob@acme.test"))
    env.post("acme", payload("<a@m>", reporter="carol@acme.test"))
    assert env.listing("acme")["items"][0]["reporter_count"] == 2


@pytest.mark.stretch
def test_the_response_to_a_repeat_report_carries_the_running_count(env):
    _report_many(env, "<a@m>", 2)
    resp = env.post("acme", payload("<a@m>", reporter="third@acme.test"))
    assert resp.status_code == 200
    assert resp.json["reporter_count"] == 3


@pytest.mark.regression
def test_different_messages_are_not_merged(env):
    for i in range(3):
        env.post("acme", payload(f"<m{i}@m>", links=(BAD_LINK,)))
    assert env.listing("acme")["total"] == 3
    assert metrics.get("analyzer.run", analyzer="link_reputation") == 3
    assert len(env.mailbox.calls_of("quarantine")) == 3


@pytest.mark.regression
def test_the_same_message_in_another_tenant_is_its_own_incident(env):
    _report_many(env, "<a@m>", 3)
    resp = env.post("globex", payload("<a@m>", reporter="x@globex.test"))
    assert resp.status_code == 201
    assert env.listing("globex")["total"] == 1
    assert env.listing("acme")["total"] == 1


@pytest.mark.regression
def test_every_reporter_still_gets_a_receipt(tmp_path):
    env = build_env(tmp_path, file_db=True)
    _report_many(env, "<a@m>", 25, links=(BAD_LINK,))
    env.settle()
    assert {r["reporter"] for r in env.mailbox.receipts} == {f"user{i}@acme.test" for i in range(25)}
    assert len(env.mailbox.receipts) == 25
