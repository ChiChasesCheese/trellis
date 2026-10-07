from conftest import alert_body


def test_alert_is_sent_to_every_channel(rig):
    queue, _store, rec, worker = rig
    queue.send(alert_body())
    assert worker.run_once() == 1
    assert [s[1] for s in rec["webhook"].sent] == ["https://hooks.example.com/acme"]
    assert [s[1] for s in rec["email"].sent] == ["secops@example.com"]
    assert queue.stats()["total"] == 0


def test_low_severity_is_not_sent(rig):
    queue, _store, rec, worker = rig
    queue.send(alert_body(severity=2))
    worker.run_once()
    assert rec["webhook"].sent == [] and rec["email"].sent == []


def test_same_alert_twice_is_sent_once(rig):
    queue, _store, rec, worker = rig
    queue.send(alert_body())
    worker.run_once()
    queue.send(alert_body())
    worker.run_once()
    assert len(rec["webhook"].sent) == 1


def test_malformed_message_does_not_crash_worker(rig):
    queue, _store, rec, worker = rig
    queue.send("not json")
    assert worker.run_once() == 1
