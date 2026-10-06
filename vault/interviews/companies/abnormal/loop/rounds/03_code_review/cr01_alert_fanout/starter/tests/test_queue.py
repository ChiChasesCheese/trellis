from fanout.queue import Queue


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def test_received_message_is_hidden_until_timeout():
    clock = Clock()
    q = Queue(clock=clock)
    q.send("hello")
    assert [m.body for m in q.receive(10, 30)] == ["hello"]
    assert q.receive(10, 30) == []
    clock.t += 31
    again = q.receive(10, 30)
    assert [m.body for m in again] == ["hello"]
    assert again[0].receive_count == 2


def test_delete_removes_message():
    q = Queue()
    q.send("x")
    (m,) = q.receive(1, 30)
    assert q.delete(m.receipt) is True
    assert q.stats()["total"] == 0


def test_change_visibility_extends_hiding():
    clock = Clock()
    q = Queue(clock=clock)
    q.send("x")
    (m,) = q.receive(1, 5)
    q.change_visibility(m.receipt, 100)
    clock.t += 50
    assert q.receive(1, 5) == []
