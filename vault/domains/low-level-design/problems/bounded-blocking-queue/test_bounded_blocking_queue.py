"""有界阻塞队列参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。

并发测试一律靠 `wait_until` 轮询 `waiting_putters`／`waiting_takers` 来确认一个线程真的
阻塞了，再靠 `Thread.join(timeout=...)` 兜底防止真死锁挂起测试——两者都不是"断言用时"，
用时只用来给一个必然会发生的状态变化留出等待窗口，通过条件永远是状态本身。
"""

import importlib
import os
import threading
import time

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def wait_until(predicate, timeout=2.0, interval=0.01) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


# ---- 第 1 关：满则 put 阻塞，空则 take 阻塞 ----------------------------------


def test_fifo_order_of_a_single_producer_consumer():
    q = impl.BoundedBlockingQueue(capacity=5)
    for i in range(5):
        q.put(i)
    assert [q.take() for _ in range(5)] == [0, 1, 2, 3, 4]


def test_put_blocks_when_full_until_a_slot_is_freed():
    q = impl.BoundedBlockingQueue(capacity=2)
    q.put(1)
    q.put(2)
    blocked = threading.Thread(target=q.put, args=(3,))
    blocked.start()
    assert wait_until(lambda: q.waiting_putters == 1)
    assert q.take() == 1
    blocked.join(timeout=2)
    assert not blocked.is_alive()
    assert q.drain() == [2, 3]


def test_take_blocks_when_empty_until_an_item_is_put():
    q = impl.BoundedBlockingQueue(capacity=2)
    result = {}

    def taker():
        result["item"] = q.take()

    t = threading.Thread(target=taker)
    t.start()
    assert wait_until(lambda: q.waiting_takers == 1)
    q.put("x")
    t.join(timeout=2)
    assert not t.is_alive()
    assert result["item"] == "x"


def test_full_empty_len_and_repr_reflect_state():
    q = impl.BoundedBlockingQueue(capacity=2)
    assert q.empty and not q.full and len(q) == 0
    q.put(1)
    q.put(2)
    assert q.full and not q.empty and len(q) == 2
    assert "size=2" in repr(q)


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        impl.BoundedBlockingQueue(capacity=0)


# ---- 第 2 关：两个条件变量、while 循环下的正确性 ------------------------------


def test_only_one_racing_putter_gets_the_freed_slot_when_capacity_is_one():
    """两个线程同时等一个即将腾出的唯一空位：谁醒来必须重新用 while 检查，不能靠
    "被 notify 就等于轮到我了" 这种假设——否则会有两个线程同时把队列塞成 2/1。"""
    q = impl.BoundedBlockingQueue(capacity=1)
    q.put("seed")
    put_by, guard = [], threading.Lock()
    barrier = threading.Barrier(2)

    def putter(label):
        barrier.wait()
        q.put(label)
        with guard:
            put_by.append(label)

    threads = [threading.Thread(target=putter, args=(label,)) for label in ("A", "B")]
    for t in threads:
        t.start()
    assert wait_until(lambda: q.waiting_putters == 2)

    assert q.take() == "seed"
    assert wait_until(lambda: q.size == 1)             # 恰好一个 putter 挤进去了
    assert wait_until(lambda: q.waiting_putters == 1)  # 另一个仍然卡着

    second = q.take()
    for t in threads:
        t.join(timeout=2)
    assert not any(t.is_alive() for t in threads)
    third = q.take()
    assert sorted(put_by) == ["A", "B"]
    assert {second, third} == {"A", "B"}
    assert q.size == 0


def test_nothing_is_lost_or_duplicated_under_many_producers_and_consumers():
    q = impl.BoundedBlockingQueue(capacity=4)
    n_producers, per_producer = 5, 40
    produced = [(p, i) for p in range(n_producers) for i in range(per_producer)]
    total = len(produced)
    collected, guard = [], threading.Lock()
    barrier = threading.Barrier(n_producers + 2)

    def produce(p):
        barrier.wait()
        for i in range(per_producer):
            q.put((p, i))

    def consume(n):
        barrier.wait()
        for _ in range(n):
            item = q.take()
            with guard:
                collected.append(item)

    half = total // 2
    producers = [threading.Thread(target=produce, args=(p,)) for p in range(n_producers)]
    consumers = [threading.Thread(target=consume, args=(half,)),
                 threading.Thread(target=consume, args=(total - half,))]
    for t in producers + consumers:
        t.start()
    for t in producers + consumers:
        t.join(timeout=15)
    assert not any(t.is_alive() for t in producers + consumers)
    assert sorted(collected) == sorted(produced)
    assert q.size == 0


def test_waiting_counts_report_zero_when_nobody_is_blocked():
    q = impl.BoundedBlockingQueue(capacity=2)
    assert q.waiting_putters == 0
    assert q.waiting_takers == 0
    q.put(1)
    assert q.waiting_putters == 0
    assert q.waiting_takers == 0


# ---- 第 3 关：超时与 close() -------------------------------------------------


def test_put_timeout_raises_and_leaves_the_queue_unchanged():
    q = impl.BoundedBlockingQueue(capacity=1)
    q.put("full")
    with pytest.raises(impl.QueueTimeout):
        q.put("x", timeout=0.05)
    assert q.size == 1
    assert q.take() == "full"


def test_take_timeout_raises_when_the_queue_stays_empty():
    q = impl.BoundedBlockingQueue(capacity=1)
    with pytest.raises(impl.QueueTimeout):
        q.take(timeout=0.05)


def test_put_nowait_and_take_nowait_never_block():
    q = impl.BoundedBlockingQueue(capacity=1)
    q.put_nowait("x")
    with pytest.raises(impl.QueueTimeout):
        q.put_nowait("y")
    assert q.take_nowait() == "x"
    with pytest.raises(impl.QueueTimeout):
        q.take_nowait()


def test_close_wakes_every_blocked_putter_with_queue_closed():
    q = impl.BoundedBlockingQueue(capacity=1)
    q.put("full")
    errors, guard = [], threading.Lock()

    def putter():
        try:
            q.put("x")
        except impl.QueueClosed as exc:
            with guard:
                errors.append(exc)

    threads = [threading.Thread(target=putter) for _ in range(2)]
    for t in threads:
        t.start()
    assert wait_until(lambda: q.waiting_putters == 2)
    q.close()
    for t in threads:
        t.join(timeout=2)
    assert not any(t.is_alive() for t in threads)
    assert len(errors) == 2


def test_close_wakes_every_blocked_taker_with_queue_closed():
    q = impl.BoundedBlockingQueue(capacity=1)
    errors, guard = [], threading.Lock()

    def taker():
        try:
            q.take()
        except impl.QueueClosed as exc:
            with guard:
                errors.append(exc)

    threads = [threading.Thread(target=taker) for _ in range(3)]
    for t in threads:
        t.start()
    assert wait_until(lambda: q.waiting_takers == 3)
    q.close()
    for t in threads:
        t.join(timeout=2)
    assert not any(t.is_alive() for t in threads)
    assert len(errors) == 3


def test_close_lets_takers_drain_what_is_left_before_failing():
    q = impl.BoundedBlockingQueue(capacity=5)
    for i in range(3):
        q.put(i)
    q.close()
    assert [q.take() for _ in range(3)] == [0, 1, 2]
    with pytest.raises(impl.QueueClosed):
        q.take()


def test_put_after_close_fails_immediately_even_with_room():
    q = impl.BoundedBlockingQueue(capacity=5)
    q.close()
    with pytest.raises(impl.QueueClosed):
        q.put("x")
    assert q.size == 0


# ---- 第 4 关：drain / take_batch ---------------------------------------------


def test_drain_returns_everything_currently_in_the_queue():
    q = impl.BoundedBlockingQueue(capacity=10)
    for i in range(5):
        q.put(i)
    assert q.drain() == [0, 1, 2, 3, 4]
    assert q.size == 0


def test_drain_caps_at_max_items_and_leaves_the_rest():
    q = impl.BoundedBlockingQueue(capacity=10)
    for i in range(5):
        q.put(i)
    assert q.drain(max_items=3) == [0, 1, 2]
    assert q.size == 2


def test_drain_returns_only_what_is_available_without_waiting_to_fill_max_items():
    q = impl.BoundedBlockingQueue(capacity=10)
    result = {}

    def drainer():
        result["batch"] = q.drain(max_items=5)

    t = threading.Thread(target=drainer)
    t.start()
    assert wait_until(lambda: q.waiting_takers == 1)
    q.put("only-one")
    t.join(timeout=2)
    assert not t.is_alive()
    assert result["batch"] == ["only-one"]


def test_drain_on_a_closed_and_drained_queue_raises_queue_closed():
    q = impl.BoundedBlockingQueue(capacity=2)
    q.close()
    with pytest.raises(impl.QueueClosed):
        q.drain()
