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


def test_release_twice_touches_the_mailbox_once(app, make_payload):
    report = _quarantined(app, make_payload)
    assert app.actions.release(report) is True
    assert app.actions.release(app.reports.get("acme", report.id)) is False
    assert len(app.mailbox.calls_of("release")) == 1
    assert app.action_log.count("acme", report.id, "release") == 1


def test_failed_release_leaves_the_report_quarantined(app, make_payload):
    report = _quarantined(app, make_payload)

    def boom(tenant_id, message_id):
        raise MailboxError("provider down")

    app.mailbox.release = boom
    with pytest.raises(MailboxError):
        app.actions.release(report)
    assert app.reports.get("acme", report.id).status is ReportStatus.QUARANTINED


def test_drain_delivers_pending_receipts_once(app, make_payload):
    from quarantine.actions import drain

    app.intake.submit("acme", make_payload())
    assert drain(app.outbox, app.mailbox, "acme").delivered == 1
    assert drain(app.outbox, app.mailbox, "acme").delivered == 0
    assert app.outbox.count("acme", "SENT") == 1


def test_drain_keeps_failed_receipts_for_the_next_run(app, make_payload):
    from quarantine.actions import drain

    app.intake.submit("acme", make_payload())
    app.mailbox.fail_receipts = True
    result = drain(app.outbox, app.mailbox, "acme")
    assert (result.delivered, result.failed) == (0, 1)
    app.mailbox.fail_receipts = False
    assert drain(app.outbox, app.mailbox, "acme").delivered == 1


def test_drain_only_touches_its_own_tenant(app, make_payload):
    from quarantine.actions import drain

    app.intake.submit("globex", make_payload())
    assert drain(app.outbox, app.mailbox, "acme").delivered == 0
    assert app.outbox.count("globex", "PENDING") == 1
