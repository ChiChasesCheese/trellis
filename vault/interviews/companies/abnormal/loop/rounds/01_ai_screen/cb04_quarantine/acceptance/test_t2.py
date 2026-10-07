"""t2_production_ready: validation, idempotent release, receipts off the request path, no PII in logs."""
from __future__ import annotations

import io
import logging

import pytest

from cb04_support import BAD_LINK, build_env, payload
from quarantine.actions import FakeMailbox

pytestmark = pytest.mark.t2


@pytest.fixture
def env(tmp_path):
    return build_env(tmp_path, file_db=True)


def _drain(env, mailbox) -> int:
    from quarantine.cli import main

    return main(["drain-outbox", "--db", str(env.db_path)], out=io.StringIO(), mailbox=mailbox)


# ---------------------------------------------------------------- input validation


@pytest.mark.core
def test_missing_message_id_is_a_400_with_the_standard_error(env):
    body = payload("<x@m>")
    del body["message_id"]
    resp = env.post("acme", body)
    assert resp.status_code == 400
    assert resp.json["error"]["code"] == "bad_request"


@pytest.mark.core
def test_missing_reporter_is_a_400(env):
    body = payload("<x@m>")
    del body["reporter"]
    assert env.post("acme", body).status_code == 400


@pytest.mark.core
def test_links_must_be_a_list(env):
    body = payload("<x@m>")
    body["links"] = "https://login-micros0ft.example/a"
    assert env.post("acme", body).status_code == 400


@pytest.mark.core
def test_attachment_without_a_filename_is_a_400(env):
    body = payload("<x@m>")
    body["attachments"] = [{"size": 10}]
    assert env.post("acme", body).status_code == 400


@pytest.mark.regression
def test_invalid_reports_leave_nothing_behind(env):
    env.post("acme", {"reporter": "bob@acme.test"})
    assert env.listing("acme")["total"] == 0


@pytest.mark.regression
def test_minimal_valid_payload_is_accepted(env):
    resp = env.post("acme", {"message_id": "<min@m>", "reporter": "bob@acme.test"})
    assert resp.status_code == 201
    assert resp.json["status"] == "CLEARED"


# ---------------------------------------------------------------- release


@pytest.mark.core
def test_releasing_twice_calls_the_mailbox_once(env):
    report = env.post("acme", payload("<a@m>", links=(BAD_LINK,))).json
    first = env.client("acme").post(f"/reports/{report['id']}/release")
    second = env.client("acme").post(f"/reports/{report['id']}/release")
    assert (first.status_code, second.status_code) == (200, 200)
    assert second.json["status"] == "RELEASED"
    assert len(env.mailbox.calls_of("release")) == 1


@pytest.mark.regression
def test_release_puts_the_message_back_once(env):
    report = env.post("acme", payload("<a@m>", links=(BAD_LINK,))).json
    resp = env.client("acme").post(f"/reports/{report['id']}/release")
    assert resp.json["status"] == "RELEASED"
    assert env.mailbox.calls_of("release") == [("release", "acme", "<a@m>")]
    assert env.get("acme", report["id"]).json["status"] == "RELEASED"


# ---------------------------------------------------------------- receipts


@pytest.mark.core
def test_a_failing_mail_provider_does_not_fail_the_report(tmp_path):
    env = build_env(tmp_path, file_db=True, mailbox=FakeMailbox(fail_receipts=True))
    resp = env.post("acme", payload("<a@m>", links=(BAD_LINK,)))
    assert resp.status_code == 201
    assert resp.json["status"] == "QUARANTINED"
    assert env.get("acme", resp.json["id"]).status_code == 200


@pytest.mark.core
def test_drain_outbox_delivers_the_receipt_once_the_provider_recovers(tmp_path):
    mailbox = FakeMailbox(fail_receipts=True)
    env = build_env(tmp_path, file_db=True, mailbox=mailbox)
    report = env.post("acme", payload("<a@m>", reporter="bob@acme.test", links=(BAD_LINK,))).json
    mailbox.fail_receipts = False
    assert _drain(env, mailbox) == 0
    assert [(r["reporter"], r["report_id"]) for r in mailbox.receipts] == [("bob@acme.test", report["id"])]
    assert mailbox.receipts[0]["disposition"] == "QUARANTINE"


@pytest.mark.stretch
def test_a_second_drain_sends_nothing_new(tmp_path):
    mailbox = FakeMailbox(fail_receipts=True)
    env = build_env(tmp_path, file_db=True, mailbox=mailbox)
    env.post("acme", payload("<a@m>"))
    mailbox.fail_receipts = False
    _drain(env, mailbox)
    _drain(env, mailbox)
    assert len(mailbox.receipts) == 1


@pytest.mark.stretch
def test_a_failed_drain_keeps_the_receipt_for_the_next_one(tmp_path):
    mailbox = FakeMailbox(fail_receipts=True)
    env = build_env(tmp_path, file_db=True, mailbox=mailbox)
    env.post("acme", payload("<a@m>"))
    _drain(env, mailbox)  # provider still down
    assert mailbox.receipts == []
    mailbox.fail_receipts = False
    _drain(env, mailbox)
    assert len(mailbox.receipts) == 1


@pytest.mark.regression
def test_the_reporter_gets_a_receipt_for_every_report(env):
    env.post("acme", payload("<a@m>", reporter="bob@acme.test"))
    env.post("acme", payload("<a@m>", reporter="carol@acme.test"))
    env.settle()
    assert sorted(r["reporter"] for r in env.mailbox.receipts) == ["bob@acme.test", "carol@acme.test"]


# ---------------------------------------------------------------- logs


@pytest.mark.stretch
def test_logs_do_not_carry_the_reporters_address(env, caplog):
    caplog.set_level(logging.DEBUG)
    env.post("acme", payload("<a@m>", reporter="pii.person@acme.test", links=(BAD_LINK,)))
    env.settle()
    assert "pii.person@acme.test" not in caplog.text
