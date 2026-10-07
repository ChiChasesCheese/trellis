import pytest
from conftest import alert_body

from fanout.errors import SendError


class Flaky:
    def __init__(self, fail_times):
        self.fail_times = fail_times
        self.calls = 0

    def send(self, channel, alert):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise SendError("503")


def test_transient_failure_is_retried_in_process(rig):
    queue, _store, rec, worker = rig
    worker.senders["webhook"] = Flaky(fail_times=2)
    queue.send(alert_body())
    worker.run_once()
    assert worker.senders["webhook"].calls == 3
    assert queue.stats()["total"] == 0


def test_persistent_failure_keeps_message_for_redelivery(rig):
    queue, _store, rec, worker = rig
    worker.senders["webhook"] = Flaky(fail_times=10_000)
    queue.send(alert_body())
    worker.run_once()
    assert worker.senders["webhook"].calls == worker.settings.max_attempts
    assert queue.stats()["total"] == 1


def test_tenant_id_is_not_interpreted_as_sql(rig):
    queue, store, rec, worker = rig
    assert store.channels_for("x' OR '1'='1") == []
