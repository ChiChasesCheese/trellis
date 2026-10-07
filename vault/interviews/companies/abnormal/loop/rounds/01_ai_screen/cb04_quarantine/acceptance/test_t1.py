"""t1_planted_bugs: reports leak across tenants, a failed lookup clears phishing, duplicates race."""
from __future__ import annotations

import pytest

from cb04_support import BAD_LINK, FLAKY_LINK, BrokenLookup, build_env, payload

pytestmark = pytest.mark.t1


@pytest.fixture
def env(tmp_path):
    return build_env(tmp_path)


def _filed(env, message_id="<a@m>", **kw) -> dict:
    resp = env.post("acme", payload(message_id, **kw))
    assert resp.status_code in (200, 201), resp.json
    return resp.json


# ---------------------------------------------------------------- tenant isolation


@pytest.mark.core
def test_another_tenant_cannot_read_a_report(env):
    report = _filed(env, links=(BAD_LINK,))
    assert env.get("globex", report["id"]).status_code == 404


@pytest.mark.core
def test_cross_tenant_lookup_uses_the_standard_error_and_leaks_nothing(env):
    report = _filed(env, "<secret-subject@m>", subject="Q3 layoffs", links=(BAD_LINK,))
    resp = env.get("globex", report["id"])
    assert resp.json["error"]["code"] == "not_found"
    assert "layoffs" not in str(resp.json) and "secret-subject" not in str(resp.json)


@pytest.mark.core
def test_another_tenant_cannot_release_a_report(env):
    report = _filed(env, links=(BAD_LINK,))
    assert env.client("globex").post(f"/reports/{report['id']}/release").status_code == 404
    assert env.mailbox.calls_of("release") == []
    assert env.get("acme", report["id"]).json["status"] == "QUARANTINED"


# ---------------------------------------------------------------- failed lookups


@pytest.mark.core
def test_provider_outage_never_clears_a_message(env):
    resp = env.post("acme", payload("<a@m>", links=(FLAKY_LINK,)))
    assert resp.status_code == 201
    assert resp.json["disposition"] == "NEEDS_REVIEW"
    assert resp.json["status"] == "NEEDS_REVIEW"


@pytest.mark.core
def test_unexpected_lookup_error_never_clears_a_message(tmp_path):
    env = build_env(tmp_path, url_lookup=BrokenLookup())
    resp = env.post("acme", payload("<a@m>", links=(BAD_LINK,)))
    assert resp.status_code == 201
    assert resp.json["disposition"] == "NEEDS_REVIEW"


@pytest.mark.regression
def test_outage_does_not_downgrade_a_message_another_signal_condemns(env):
    resp = env.post("acme", payload("<a@m>", sender="Pay <p@payroll-update.example>", links=(FLAKY_LINK,)))
    assert resp.json["disposition"] == "QUARANTINE"


@pytest.mark.regression
def test_working_lookup_still_quarantines_and_clean_still_clears(env):
    assert env.post("acme", payload("<bad@m>", links=(BAD_LINK,))).json["status"] == "QUARANTINED"
    assert env.post("acme", payload("<ok@m>")).json["status"] == "CLEARED"
    assert len(env.mailbox.calls_of("quarantine")) == 1


# ---------------------------------------------------------------- duplicate reports


@pytest.mark.core
def test_simultaneous_reports_of_one_message_make_one_report(tmp_path):
    env = build_env(tmp_path, slow=0.15)
    bodies = [payload("<same@m>", reporter=f"u{i}@acme.test", links=(BAD_LINK,)) for i in range(2)]
    responses = env.post_concurrently("acme", bodies)
    assert all(r.status_code in (200, 201) for r in responses), [r.json for r in responses]
    assert len({r.json["id"] for r in responses}) == 1
    assert env.listing("acme")["total"] == 1


@pytest.mark.core
def test_simultaneous_reports_quarantine_the_message_once(tmp_path):
    env = build_env(tmp_path, slow=0.15)
    bodies = [payload("<same@m>", reporter=f"u{i}@acme.test", links=(BAD_LINK,)) for i in range(2)]
    env.post_concurrently("acme", bodies)
    assert len(env.mailbox.calls_of("quarantine")) == 1


@pytest.mark.stretch
def test_eight_simultaneous_reports_are_still_one(tmp_path):
    env = build_env(tmp_path, slow=0.1)
    bodies = [payload("<same@m>", reporter=f"u{i}@acme.test", links=(BAD_LINK,)) for i in range(8)]
    responses = env.post_concurrently("acme", bodies)
    assert all(r.status_code in (200, 201) for r in responses), [r.json for r in responses]
    assert len({r.json["id"] for r in responses}) == 1
    assert env.listing("acme")["total"] == 1
    assert len(env.mailbox.calls_of("quarantine")) == 1


@pytest.mark.regression
def test_sequential_duplicate_returns_the_same_report(env):
    first = env.post("acme", payload("<a@m>", links=(BAD_LINK,)))
    second = env.post("acme", payload("<a@m>", reporter="carol@acme.test", links=(BAD_LINK,)))
    assert (first.status_code, second.status_code) == (201, 200)
    assert first.json["id"] == second.json["id"]
    assert len(env.mailbox.calls_of("quarantine")) == 1


@pytest.mark.regression
def test_same_message_id_in_two_tenants_stays_two_reports(env):
    a = env.post("acme", payload("<a@m>"))
    g = env.post("globex", payload("<a@m>"))
    assert a.json["id"] != g.json["id"]
    assert env.get("acme", a.json["id"]).status_code == 200
    assert env.get("globex", g.json["id"]).status_code == 200


# ---------------------------------------------------------------- time zones


@pytest.mark.stretch
def test_repeat_sender_window_is_measured_in_utc(env):
    """Three reports from one sender, 10 and 9 hours apart in real time, with Date headers in other zones."""
    sender = "Promo <promo@bulk-unknown.example>"
    env.post("acme", payload("<p1@m>", sender=sender, date="Mon, 14 Sep 2026 20:00:00 -0800"))
    env.post("acme", payload("<p2@m>", sender=sender, date="Mon, 14 Sep 2026 21:00:00 -0800"))
    third = env.post("acme", payload("<p3@m>", sender=sender, date="Tue, 15 Sep 2026 23:00:00 +0900"))
    assert third.json["disposition"] == "QUARANTINE"
    assert any("earlier report" in r for v in third.json["verdicts"] for r in v["reasons"])


@pytest.mark.regression
def test_repeat_sender_in_one_zone_escalates(env):
    sender = "Promo <promo@bulk-unknown.example>"
    env.post("acme", payload("<p1@m>", sender=sender, date="Tue, 15 Sep 2026 06:00:00 +0000"))
    env.post("acme", payload("<p2@m>", sender=sender, date="Tue, 15 Sep 2026 07:00:00 +0000"))
    third = env.post("acme", payload("<p3@m>", sender=sender, date="Tue, 15 Sep 2026 08:00:00 +0000"))
    assert third.json["disposition"] == "QUARANTINE"
