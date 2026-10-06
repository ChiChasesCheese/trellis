"""P0 findings: each test fails on the starter and passes on the fixed repo."""
import pytest
from fanout_helpers import Crash, Failing, Recorder, Rig, Stop, alert_body, webhook

from fanout.models import Channel

pytestmark = pytest.mark.core


def test_cr01_message_is_still_in_queue_while_it_is_being_sent():
    """CR-01: ack must come after the work. At send time the message must still exist (in flight)."""
    seen = []
    rig = Rig([webhook()], {"webhook": Recorder(observe=lambda: seen.append(rig.queue.stats()))})
    rig.queue.send(alert_body())
    rig.worker.run_once()
    assert seen and seen[0]["total"] == 1 and seen[0]["in_flight"] == 1
    assert rig.queue.stats()["total"] == 0  # and it is acked once the send succeeded
    rig.close()


def test_cr01_crash_mid_send_does_not_lose_the_alert():
    class Dies:
        def send(self, channel, alert):
            raise Crash()

    rig = Rig([webhook()], {"webhook": Dies()})
    rig.queue.send(alert_body())
    with pytest.raises(Crash):
        rig.worker.run_once()
    rig.clock.advance(3600)  # visibility timeout passes, as it would after a pod restart
    assert rig.queue.stats()["visible"] == 1
    rig.close()


def test_cr02_same_alert_id_in_two_tenants_notifies_both():
    """CR-02: alert ids are only unique per tenant; the dedup identity must include the tenant."""
    rec = Recorder()
    rig = Rig([webhook("acme", "https://hooks.example.com/acme"), webhook("globex", "https://hooks.example.com/globex")], {"webhook": rec})
    rig.queue.send(alert_body(tenant="acme", alert_id="1001"))
    rig.worker.run_once()  # one batch at a time: the cache must remember acme's alert...
    rig.queue.send(alert_body(tenant="globex", alert_id="1001"))
    rig.worker.run_once()  # ...without it swallowing globex's
    assert sorted(s[1] for s in rec.sent) == ["https://hooks.example.com/acme", "https://hooks.example.com/globex"]
    rig.close()


def test_cr03_failing_downstream_is_bounded_and_dead_lettered():
    """CR-03: retries are bounded, and a message that keeps failing ends up in the DLQ, not in a hot loop."""
    sender = Failing()
    rig = Rig([webhook()], {"webhook": sender})
    rig.queue.send(alert_body())
    try:
        for _ in range(12):
            rig.worker.run_once()
            rig.clock.advance(3600)
    except Stop:
        pass
    assert sender.calls <= 30, f"{sender.calls} send attempts for one message"
    assert rig.queue.stats()["total"] == 0
    assert rig.dlq.stats()["total"] == 1
    assert "a1" in rig.dlq.bodies()[0]
    rig.close()


def test_cr03_failed_message_backs_off_instead_of_being_redelivered_immediately():
    rig = Rig([webhook()], {"webhook": Failing()})
    rig.queue.send(alert_body())
    try:
        rig.worker.run_once()
    except Stop:
        pytest.fail("worker spun on a failing send")
    assert rig.queue.stats()["total"] == 1  # not acked
    assert rig.queue.receive(1, 30) == []  # and not instantly visible again
    rig.close()


def test_cr03_malformed_message_goes_to_dlq_instead_of_vanishing():
    rig = Rig([webhook()], {"webhook": Recorder()})
    rig.queue.send("{not json")
    rig.worker.run_once()
    assert rig.queue.stats()["total"] == 0
    assert rig.dlq.stats()["total"] == 1
    rig.close()


def test_cr04_tenant_id_is_data_not_sql():
    """CR-04: a tenant id that looks like SQL must not return other tenants' channels."""
    rec = Recorder()
    rig = Rig([webhook("acme", "https://hooks.example.com/acme")], {"webhook": rec})
    rig.queue.send(alert_body(tenant="x' OR '1'='1", alert_id="evil"))
    rig.worker.run_once()
    assert rec.sent == []
    rig.close()


def test_cr04_tenant_id_with_a_quote_does_not_break_lookup():
    rig = Rig([Channel("o'brien", "webhook", "https://hooks.example.com/ob")], {"webhook": Recorder()})
    assert [c.target for c in rig.store.channels_for("o'brien")] == ["https://hooks.example.com/ob"]
    rig.close()
