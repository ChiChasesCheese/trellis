"""P1/P2 findings: fail on the starter, pass on the fixed repo (not required for a v1 review pass)."""
import io
import logging
import os
import threading
import time
import urllib.request

import pytest
from fanout_helpers import Recorder, Rig, alert_body, webhook

from fanout.errors import SendError
from fanout.models import Alert, Channel
from fanout.queue import Queue
from fanout.senders import EmailSender, SlackSender, WebhookSender

pytestmark = pytest.mark.stretch
ALERT = Alert("acme", "a1", "r", 4, "T", "ann@example.com", "2026-10-01T12:00:00Z")


def test_cr05_concurrent_duplicates_send_once():
    """CR-05: two copies of one alert handled at the same time must not both pass the dedup check."""
    started, release = threading.Event(), threading.Event()

    class Slow:
        calls = 0

        def send(self, channel, alert):
            Slow.calls += 1
            started.set()
            release.wait(2)

    rig = Rig([webhook()], {"webhook": Slow()})
    rig.queue.send(alert_body())
    rig.queue.send(alert_body())
    m1, m2 = rig.queue.receive(2, 30)
    a = threading.Thread(target=rig.worker.process_message, args=(m1,))
    a.start()
    assert started.wait(2)
    b = threading.Thread(target=rig.worker.process_message, args=(m2,))
    b.start()
    for _ in range(40):
        if Slow.calls >= 2:
            break
        time.sleep(0.01)
    release.set()
    a.join(5)
    b.join(5)
    assert Slow.calls == 1
    rig.close()


def test_cr05_redelivery_after_partial_failure_does_not_resend_to_the_channel_that_worked():
    from fanout_helpers import Failing, Stop

    ok = Recorder()
    rig = Rig([Channel("acme", "email", "secops@example.com"), webhook()], {"email": ok, "webhook": Failing(limit=10_000)})
    rig.queue.send(alert_body())
    try:
        for _ in range(3):
            rig.worker.run_once()
            rig.clock.advance(120)  # past the redelivery backoff, well inside the dedup TTL
    except Stop:
        pass
    assert len(ok.sent) == 1
    rig.close()


def _capture_urlopen(monkeypatch):
    seen = {}

    class Resp(io.BytesIO):
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake(req, *args, **kwargs):
        seen["args"], seen["kwargs"] = args, kwargs
        return Resp()

    monkeypatch.setattr(urllib.request, "urlopen", fake)
    return seen


def test_cr06_webhook_has_a_timeout(monkeypatch):
    seen = _capture_urlopen(monkeypatch)
    WebhookSender().send(webhook(), ALERT)
    timeout = seen["kwargs"].get("timeout", seen["args"][1] if len(seen["args"]) > 1 else None)
    assert timeout is not None and 0 < timeout <= 30


def test_cr07_webhook_secret_is_not_logged(monkeypatch, caplog):
    _capture_urlopen(monkeypatch)
    caplog.set_level(logging.DEBUG)
    WebhookSender().send(webhook(secret="s3cr3t-token"), ALERT)
    assert "s3cr3t-token" not in caplog.text


def test_cr08_slack_failure_is_reported_not_swallowed():
    def boom(channel, text):
        raise ConnectionError("slack down")

    with pytest.raises(SendError):
        SlackSender(transport=boom).send(Channel("acme", "slack", "#sec"), ALERT)


def test_cr08_email_failure_is_reported_not_swallowed():
    def boom(to, subject, body):
        raise ConnectionError("smtp down")

    with pytest.raises(SendError):
        EmailSender(transport=boom).send(Channel("acme", "email", "a@example.com"), ALERT)


def test_cr08_failed_slack_send_keeps_the_message():
    def boom(channel, text):
        raise ConnectionError("slack down")

    rig = Rig([Channel("acme", "slack", "#sec")], {"slack": SlackSender(transport=boom)})
    rig.queue.send(alert_body())
    rig.worker.run_once()
    assert rig.queue.stats()["total"] == 1
    rig.close()


def test_cr09_message_text_does_not_leak_between_alerts():
    bodies = []
    sender = EmailSender(transport=lambda to, subj, body: bodies.append(body))
    sender.send(Channel("acme", "email", "a@example.com"), Alert("acme", "1", "r", 4, "T", "ann@acme.example.com", "2026-10-01T12:00:00Z"))
    sender.send(Channel("globex", "email", "g@example.com"), Alert("globex", "2", "r", 4, "T", "bob@globex.example.com", "2026-10-01T12:00:00Z"))
    assert "ann@acme.example.com" not in bodies[1]
    assert bodies[1].count("severity=") == 1


def test_cr10_stale_receipt_cannot_delete_a_redelivered_message():
    from fanout_helpers import Clock

    clock = Clock()
    q = Queue(clock=clock)
    q.send("m")
    (first,) = q.receive(1, 10)
    clock.advance(11)
    (second,) = q.receive(1, 10)
    assert second.receive_count == 2
    assert q.delete(first.receipt) is False
    assert q.stats()["total"] == 1
    assert q.delete(second.receipt) is True


@pytest.mark.skipif(not hasattr(time, "tzset"), reason="needs time.tzset")
def test_cr11_staleness_check_is_timezone_independent():
    old = os.environ.get("TZ")
    os.environ["TZ"] = "Asia/Shanghai"
    time.tzset()
    try:
        rec = Recorder()
        rig = Rig([webhook()], {"webhook": rec})
        rig.queue.send(alert_body(age_s=5))
        rig.worker.run_once()
        assert len(rec.sent) == 1
        rig.close()
    finally:
        if old is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old
        time.tzset()


def test_cr12_channel_config_is_fetched_once_per_tenant_per_batch():
    from fanout.config_store import ConfigStore

    class Counting(ConfigStore):
        calls = 0

        def channels_for(self, tenant_id):
            Counting.calls += 1
            return super().channels_for(tenant_id)

    rig = Rig([webhook()], {"webhook": Recorder()}, store_cls=Counting)
    for i in range(8):
        rig.queue.send(alert_body(alert_id=f"n{i}"))
    rig.worker.run_once()
    assert Counting.calls <= 1
    rig.close()
