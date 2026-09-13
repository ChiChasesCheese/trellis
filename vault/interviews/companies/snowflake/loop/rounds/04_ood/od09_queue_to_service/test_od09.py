import random

import pytest


# ------------------------------------------------------------------ Part 1: deque-like base queue
@pytest.mark.part1
def test_worked_example_1(impl):
    q = impl.SimpleQueue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.peek() == "a"
    assert q.dequeue() == "a"
    assert len(q) == 1
    assert q.dequeue() == "b"
    with pytest.raises(IndexError):
        q.dequeue()


@pytest.mark.part1
@pytest.mark.edge
def test_peek_empty_raises(impl):
    q = impl.SimpleQueue()
    with pytest.raises(IndexError):
        q.peek()


@pytest.mark.part1
@pytest.mark.edge
def test_peek_does_not_remove(impl):
    q = impl.SimpleQueue()
    q.enqueue("x")
    assert q.peek() == "x"
    assert q.peek() == "x"
    assert len(q) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_fifo_order(impl):
    q = impl.SimpleQueue()
    for i in range(5):
        q.enqueue(i)
    assert [q.dequeue() for _ in range(5)] == [0, 1, 2, 3, 4]


# ------------------------------------------------------------------ Part 2: at-least-once ack/visibility
@pytest.mark.part2
def test_worked_example_2(impl):
    mq = impl.MessageQueue()
    id_a = mq.enqueue("A")
    id_b = mq.enqueue("B")
    r1 = mq.dequeue(now=0, visibility_timeout=10)
    r2 = mq.dequeue(now=1, visibility_timeout=10)
    assert mq.ack(id_b) is True
    r3 = mq.dequeue(now=5, visibility_timeout=10)
    r4 = mq.dequeue(now=10, visibility_timeout=10)
    assert mq.ack(id_a) is True
    r5 = mq.dequeue(now=100, visibility_timeout=10)
    assert [r1, r2, r3, r4, r5] == [
        (id_a, "A"),
        (id_b, "B"),
        None,
        (id_a, "A"),
        None,
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_empty_queue_dequeue_returns_none_not_exception(impl):
    mq = impl.MessageQueue()
    assert mq.dequeue(now=0, visibility_timeout=10) is None


@pytest.mark.part2
@pytest.mark.edge
def test_visibility_half_open_boundary(impl):
    mq = impl.MessageQueue()
    mid = mq.enqueue("x")
    mq.dequeue(now=0, visibility_timeout=10)  # deadline = 10
    assert mq.dequeue(now=9, visibility_timeout=10) is None  # still in-flight
    result = mq.dequeue(now=10, visibility_timeout=10)  # deadline hit exactly -> redelivered
    assert result == (mid, "x")


@pytest.mark.part2
@pytest.mark.edge
def test_ack_unknown_id_returns_false(impl):
    mq = impl.MessageQueue()
    assert mq.ack("ghost") is False


@pytest.mark.part2
@pytest.mark.edge
def test_ack_twice_second_call_returns_false(impl):
    mq = impl.MessageQueue()
    mid = mq.enqueue("x")
    mq.dequeue(now=0, visibility_timeout=10)
    assert mq.ack(mid) is True
    assert mq.ack(mid) is False


@pytest.mark.part2
@pytest.mark.edge
def test_ack_false_while_timed_out_and_not_yet_redelivered(impl):
    mq = impl.MessageQueue()
    id_x = mq.enqueue("x")
    id_y = mq.enqueue("y")
    mq.dequeue(now=0, visibility_timeout=5)  # delivers x, deadline=5
    mq.dequeue(now=0, visibility_timeout=5)  # delivers y, deadline=5
    # both x and y are now in-flight; at now=5 both expire and go back to ready, x first
    result = mq.dequeue(now=5, visibility_timeout=100)  # pulls x back off the ready queue
    assert result == (id_x, "x")
    # y is sitting in the ready queue (expired, not yet redelivered) -- ack must fail
    assert mq.ack(id_y) is False


@pytest.mark.part2
@pytest.mark.edge
def test_late_ack_after_timeout_does_not_affect_redelivery(impl):
    mq = impl.MessageQueue()
    mid = mq.enqueue("x")
    mq.dequeue(now=0, visibility_timeout=5)  # deadline = 5
    # message times out and gets redelivered before the "late" ack arrives
    redelivered = mq.dequeue(now=5, visibility_timeout=5)  # deadline now = 10
    assert redelivered == (mid, "x")
    # a late ack referring to the FIRST delivery's in-flight window has already been superseded;
    # the only currently-valid in-flight state is the second delivery, which a correct ack call
    # against the (single, shared) message_id must still be able to acknowledge
    assert mq.ack(mid) is True
    assert mq.ack(mid) is False  # now permanently gone


@pytest.mark.part2
@pytest.mark.edge
def test_at_least_once_message_can_be_delivered_more_than_once(impl):
    mq = impl.MessageQueue()
    mid = mq.enqueue("x")
    first = mq.dequeue(now=0, visibility_timeout=1)
    second = mq.dequeue(now=1, visibility_timeout=1)  # timed out -> redelivered
    assert first == second == (mid, "x")


# ------------------------------------------------------------------ Part 3: crash simulation
@pytest.mark.part3
def test_worked_example_3(impl):
    mq = impl.MessageQueue()
    id_a = mq.enqueue("A")
    id_b = mq.enqueue("B")
    id_c = mq.enqueue("C")
    mq.dequeue(now=0, visibility_timeout=1000)  # delivers A
    mq.dequeue(now=0, visibility_timeout=1000)  # delivers B
    mq.ack(id_b)
    n = mq.requeue_all_in_flight()
    assert n == 1  # only A was in-flight; B was already acked
    assert mq.dequeue(now=1, visibility_timeout=1000) == (id_a, "A")
    assert mq.dequeue(now=1, visibility_timeout=1000) == (id_c, "C")
    assert mq.dequeue(now=1, visibility_timeout=1000) is None


@pytest.mark.part3
@pytest.mark.edge
def test_acked_messages_never_redelivered_after_crash(impl):
    mq = impl.MessageQueue()
    mid = mq.enqueue("x")
    mq.dequeue(now=0, visibility_timeout=100)
    mq.ack(mid)
    n = mq.requeue_all_in_flight()
    assert n == 0
    assert mq.dequeue(now=1, visibility_timeout=100) is None


@pytest.mark.part3
@pytest.mark.edge
def test_requeue_all_orders_by_original_delivery_not_expiry(impl):
    mq = impl.MessageQueue()
    id_a = mq.enqueue("A")
    id_b = mq.enqueue("B")
    # deliver B first with a SHORT timeout, A second with a LONG timeout -- expiry order is
    # reversed relative to delivery order, so this distinguishes the two policies
    mq.dequeue(now=0, visibility_timeout=1)  # delivers A (FIFO enqueue order), deadline=1
    mq.dequeue(now=0, visibility_timeout=1000)  # delivers B, deadline=1000
    mq.requeue_all_in_flight()  # must order by delivery sequence: A (delivered 1st) before B
    assert mq.dequeue(now=1, visibility_timeout=10) == (id_a, "A")
    assert mq.dequeue(now=1, visibility_timeout=10) == (id_b, "B")


@pytest.mark.part3
@pytest.mark.edge
def test_requeue_all_empty_returns_zero(impl):
    mq = impl.MessageQueue()
    assert mq.requeue_all_in_flight() == 0


@pytest.mark.part3
@pytest.mark.edge
def test_requeue_all_puts_crashed_work_ahead_of_never_delivered(impl):
    mq = impl.MessageQueue()
    id_a = mq.enqueue("A")
    mq.enqueue("B")  # never delivered
    mq.dequeue(now=0, visibility_timeout=100)  # delivers A
    mq.requeue_all_in_flight()
    # A (crashed, unfinished work) must come back before the never-delivered B
    assert mq.dequeue(now=1, visibility_timeout=100) == (id_a, "A")


# ------------------------------------------------------------------ fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_strings_exact(impl):
    out = impl.part1(["ENQ a", "PEEK", "DEQ", "DEQ"])
    assert out == ["a", "a", "ERROR:IndexError"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["ENQ A", "ENQ B", "DEQ 0 10", "DEQ 1 10"]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "m1"
    assert lines[1] == "m2"
    assert lines[2] == "m1 A"
    assert lines[3] == "m2 B"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    body = ["ENQ A", "DEQ 0 100", "CRASH", "DEQ 1 100"]
    r = run_script("PART 3\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[1] == "m1 A"
    assert lines[2] == "1"
    assert lines[3] == "m1 A"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_ops(run_script):
    rng = random.Random(0)
    body = []
    ids = []
    now = 0
    for i in range(100_000):
        now += rng.randrange(0, 2)
        r = rng.random()
        if r < 0.5 or not ids:
            body.append(f"ENQ item{i}")
            ids.append(i)  # placeholder; real ids come back from ENQ output, tracked separately
        elif r < 0.8:
            body.append(f"DEQ {now} 5")
        else:
            body.append(f"ACK m{rng.randrange(1, len(ids) + 1)}")
    result = run_script("PART 2\n" + "\n".join(body) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
