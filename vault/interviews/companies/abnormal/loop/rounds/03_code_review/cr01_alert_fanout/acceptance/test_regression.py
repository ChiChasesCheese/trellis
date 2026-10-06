"""Behaviour that must keep working after the fixes."""
import pytest
from fanout_helpers import Recorder, Rig, alert_body, webhook

from fanout.models import Channel

pytestmark = pytest.mark.regression


def test_alert_reaches_every_channel_and_is_acked():
    hook, mail = Recorder(), Recorder()
    rig = Rig([webhook(), Channel("acme", "email", "secops@example.com")], {"webhook": hook, "email": mail})
    rig.queue.send(alert_body())
    assert rig.worker.run_once() == 1
    assert len(hook.sent) == 1 and len(mail.sent) == 1
    assert rig.queue.stats()["total"] == 0
    rig.close()


def test_low_severity_is_dropped_and_acked():
    rec = Recorder()
    rig = Rig([webhook()], {"webhook": rec})
    rig.queue.send(alert_body(severity=2))
    rig.worker.run_once()
    assert rec.sent == [] and rig.queue.stats()["total"] == 0
    rig.close()


def test_sequential_duplicate_is_sent_once():
    rec = Recorder()
    rig = Rig([webhook()], {"webhook": rec})
    rig.queue.send(alert_body())
    rig.worker.run_once()
    rig.queue.send(alert_body())
    rig.worker.run_once()
    assert len(rec.sent) == 1
    rig.close()


def test_stale_alert_is_not_sent():
    rec = Recorder()
    rig = Rig([webhook()], {"webhook": rec})
    rig.queue.send(alert_body(age_s=7200))
    rig.worker.run_once()
    assert rec.sent == [] and rig.queue.stats()["total"] == 0
    rig.close()


def test_channel_min_severity_is_respected():
    rec = Recorder()
    rig = Rig([Channel("acme", "webhook", "https://hooks.example.com/acme", min_severity=5)], {"webhook": rec})
    rig.queue.send(alert_body(severity=4))
    rig.worker.run_once()
    assert rec.sent == []
    rig.close()
