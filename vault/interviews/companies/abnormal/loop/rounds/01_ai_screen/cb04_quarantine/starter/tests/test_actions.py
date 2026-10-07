from __future__ import annotations

from quarantine.actions import FakeMailbox
from quarantine.errors import MailboxError
from quarantine.models import ReportStatus

import pytest


def _quarantined(app, make_payload):
    return app.intake.submit("acme", make_payload(links=["https://login-micros0ft.example/a"])).report


def test_fake_mailbox_records_calls():
    mb = FakeMailbox()
    mb.quarantine("acme", "<m1>")
    mb.release("acme", "<m1>")
    assert mb.calls == [("quarantine", "acme", "<m1>"), ("release", "acme", "<m1>")]


def test_fake_mailbox_can_fail_receipts():
    mb = FakeMailbox(fail_receipts=True)
    with pytest.raises(MailboxError):
        mb.send_receipt("acme", "bob@acme.test", "rpt_1", "RELEASE")


def test_quarantine_is_logged(app, make_payload):
    report = _quarantined(app, make_payload)
    assert app.action_log.count("acme", report.id, "quarantine") == 1


def test_release_calls_mailbox_and_marks_released(app, make_payload):
    report = _quarantined(app, make_payload)
    app.actions.release(report)
    assert app.mailbox.calls_of("release") == [("release", "acme", report.message_id)]
    assert app.reports.get("acme", report.id).status is ReportStatus.RELEASED
    assert [a["action"] for a in app.action_log.for_report("acme", report.id)] == ["quarantine", "release"]
