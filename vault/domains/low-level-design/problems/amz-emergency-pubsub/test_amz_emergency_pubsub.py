"""应急事件发布订阅的验收测试：路由与过滤、失败隔离、重试与死信、异步优先级与背压、并发不变量。

只用公开 API（`publish`、`subscribe`、`flush`、`dead_letters`、`stats`、`pending`、`subscriber_count`），
不碰下划线属性。慢订阅者用 `threading.Event` 卡住而不是 `sleep`，所以断言的是顺序与计数，不是时间。
"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import datetime, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def fixed_clock():
    return datetime(2026, 1, 1, tzinfo=timezone.utc)


class Recorder:
    def __init__(self) -> None:
        self.events: list = []

    def __call__(self, event) -> None:
        self.events.append(event)

    @property
    def seqs(self) -> list[int]:
        return [e.seq for e in self.events]


def bus_with(**kwargs):
    return impl.EmergencyBus(clock=fixed_clock, **kwargs)


# ---- 第 1 关：发布 / 订阅


def test_publish_reaches_every_subscriber_and_event_is_a_snapshot() -> None:
    bus = bus_with()
    a, b = Recorder(), Recorder()
    bus.subscribe(a)
    bus.subscribe(b)
    event = bus.publish("fire", impl.Severity.CRITICAL, "三号楼起火", "B3")
    assert a.events == [event] and b.events == [event]
    assert (event.seq, event.topic, event.location) == (1, "fire", "B3")
    assert event.published_at == fixed_clock()
    with pytest.raises(Exception):
        event.message = "改掉"           # 冻结的事件


def test_sequence_numbers_increase_and_no_subscriber_is_fine() -> None:
    bus = bus_with()
    assert bus.publish("flood", impl.Severity.INFO, "x").seq == 1
    assert bus.publish("flood", impl.Severity.INFO, "y").seq == 2


def test_unsubscribe_stops_delivery_and_reports_whether_it_was_subscribed() -> None:
    bus = bus_with()
    rec = Recorder()
    sub = bus.subscribe(rec)
    bus.publish("fire", impl.Severity.INFO, "1")
    assert bus.unsubscribe(sub) is True
    assert bus.unsubscribe(sub) is False
    bus.publish("fire", impl.Severity.INFO, "2")
    assert len(rec.events) == 1 and bus.subscriber_count == 0


def test_invalid_arguments() -> None:
    bus = bus_with()
    with pytest.raises(ValueError):
        bus.publish("", impl.Severity.INFO, "x")
    with pytest.raises(ValueError):
        bus.subscribe(Recorder(), max_attempts=0)
    with pytest.raises(ValueError):
        bus.subscribe(Recorder(), queue_size=0)


# ---- 第 2 关：过滤与失败隔离


def test_topic_and_severity_filters_combine() -> None:
    bus = bus_with()
    fire_only, serious, both = Recorder(), Recorder(), Recorder()
    bus.subscribe(fire_only, topics={"fire"})
    bus.subscribe(serious, min_severity=impl.Severity.WARNING)
    bus.subscribe(both, topics=["fire", "flood"], min_severity=impl.Severity.CRITICAL)
    bus.publish("fire", impl.Severity.INFO, "a")
    bus.publish("flood", impl.Severity.CRITICAL, "b")
    bus.publish("quake", impl.Severity.WARNING, "c")
    assert [e.message for e in fire_only.events] == ["a"]
    assert [e.message for e in serious.events] == ["b", "c"]
    assert [e.message for e in both.events] == ["b"]


def test_a_raising_subscriber_does_not_stop_the_others() -> None:
    bus = bus_with()
    before, after = Recorder(), Recorder()

    def boom(event) -> None:
        raise RuntimeError("handler bug")

    bus.subscribe(before, name="before")
    bad = bus.subscribe(boom, name="bad")
    bus.subscribe(after, name="after")
    event = bus.publish("fire", impl.Severity.CRITICAL, "起火")      # 不抛异常
    assert before.events == [event] and after.events == [event]      # 出错者前后的订阅者都收到
    (dead,) = bus.dead_letters
    assert (dead.subscriber, dead.reason, dead.event.seq) == ("bad", impl.DeadReason.HANDLER_FAILED, 1)
    assert "RuntimeError" in dead.error and "handler bug" in dead.error
    assert bad.stats == impl.SubscriptionStats(delivered=0, failed=1, dropped=0)


def test_retry_succeeds_on_a_later_attempt_without_dead_letter() -> None:
    bus = bus_with()
    calls: list[int] = []

    def flaky(event) -> None:
        calls.append(event.seq)
        if len(calls) < 3:
            raise IOError("pager offline")

    sub = bus.subscribe(flaky, max_attempts=3)
    bus.publish("fire", impl.Severity.INFO, "x")
    assert len(calls) == 3 and bus.dead_letters == ()
    assert sub.stats.delivered == 1 and sub.stats.failed == 0


def test_retries_exhausted_goes_to_dead_letter_with_attempt_count() -> None:
    bus = bus_with()
    sub = bus.subscribe(lambda e: 1 / 0, max_attempts=2, name="z")
    bus.publish("fire", impl.Severity.INFO, "x")
    (dead,) = bus.dead_letters
    assert dead.attempts == 2 and "ZeroDivisionError" in dead.error
    assert sub.stats.failed == 1


def test_dead_letters_are_bounded_and_returned_as_a_snapshot() -> None:
    bus = bus_with(dead_letter_limit=3)
    bus.subscribe(lambda e: 1 / 0)
    for i in range(5):
        bus.publish("fire", impl.Severity.INFO, str(i))
    snap = bus.dead_letters
    assert [d.event.seq for d in snap] == [3, 4, 5]                  # 只留最近 3 条
    bus.publish("fire", impl.Severity.INFO, "6")
    assert len(snap) == 3                                            # 旧快照不会被改动


def test_handler_may_publish_and_unsubscribe_reentrantly() -> None:
    bus = bus_with()
    rec = Recorder()
    holder = {}

    def escalate(event) -> None:
        if event.topic == "fire":
            bus.publish("evacuate", impl.Severity.CRITICAL, "疏散")   # 处理函数里再发布
            bus.unsubscribe(holder["self"])                           # 并且退订自己

    holder["self"] = bus.subscribe(escalate, name="escalator")
    bus.subscribe(rec)
    bus.publish("fire", impl.Severity.WARNING, "起火")
    assert [e.topic for e in rec.events] == ["evacuate", "fire"]      # 嵌套的先送完
    assert bus.subscriber_count == 1


def test_base_exceptions_are_not_swallowed() -> None:
    bus = bus_with()

    def stop(event) -> None:
        raise KeyboardInterrupt

    bus.subscribe(stop)
    with pytest.raises(KeyboardInterrupt):
        bus.publish("fire", impl.Severity.INFO, "x")


# ---- 第 3 关：异步、优先级、背压


def test_slow_async_subscriber_does_not_block_publisher_or_others() -> None:
    bus = bus_with()
    gate = threading.Event()
    slow_seen: list[int] = []
    fast = Recorder()
    bus.subscribe(lambda e: (gate.wait(5), slow_seen.append(e.seq)), queue_size=10, name="slow")
    bus.subscribe(fast, name="fast")
    bus.publish("fire", impl.Severity.INFO, "1")      # 慢的卡在 gate 上，publish 仍然立刻返回
    bus.publish("fire", impl.Severity.INFO, "2")
    assert fast.seqs == [1, 2] and slow_seen == []
    gate.set()
    assert bus.flush(5)
    assert slow_seen == [1, 2]
    bus.close()


def test_async_mailbox_delivers_higher_severity_first_then_fifo() -> None:
    bus = bus_with()
    gate, started = threading.Event(), threading.Event()
    seen: list[str] = []

    def handler(event) -> None:
        started.set()
        gate.wait(5)
        seen.append(event.message)

    bus.subscribe(handler, queue_size=10)
    bus.publish("x", impl.Severity.INFO, "blocker")
    assert started.wait(5)                            # 工作线程已经卡在第一条上，后面的都在排队
    bus.publish("x", impl.Severity.INFO, "i1")
    bus.publish("x", impl.Severity.CRITICAL, "c1")
    bus.publish("x", impl.Severity.WARNING, "w1")
    bus.publish("x", impl.Severity.CRITICAL, "c2")
    bus.publish("x", impl.Severity.INFO, "i2")
    gate.set()
    assert bus.flush(5)
    assert seen == ["blocker", "c1", "c2", "w1", "i1", "i2"]
    bus.close()


def test_full_mailbox_drops_the_least_important_oldest_event() -> None:
    bus = bus_with()
    gate, started = threading.Event(), threading.Event()
    seen: list[str] = []

    def handler(event) -> None:
        started.set()
        gate.wait(5)
        seen.append(event.message)

    sub = bus.subscribe(handler, queue_size=2, name="slow")
    bus.publish("x", impl.Severity.INFO, "blocker")
    assert started.wait(5)
    bus.publish("x", impl.Severity.INFO, "i1")
    bus.publish("x", impl.Severity.WARNING, "w1")                    # 信箱满：[w1, i1]
    bus.publish("x", impl.Severity.CRITICAL, "c1")                   # 挤掉最不重要的 i1
    bus.publish("x", impl.Severity.INFO, "i2")                       # 比信箱里所有都不重要：自己被丢
    gate.set()
    assert bus.flush(5)
    assert seen == ["blocker", "c1", "w1"]
    assert sub.stats.dropped == 2
    assert sorted(d.event.message for d in bus.dead_letters if d.reason == impl.DeadReason.QUEUE_FULL) == ["i1", "i2"]
    bus.close()


def test_async_failure_is_isolated_and_dead_lettered() -> None:
    bus = bus_with()
    ok = Recorder()
    bus.subscribe(lambda e: 1 / 0, queue_size=5, name="bad", max_attempts=2)
    bus.subscribe(ok, queue_size=5, name="ok")
    for i in range(3):
        bus.publish("fire", impl.Severity.INFO, str(i))
    assert bus.flush(5)
    assert ok.seqs == [1, 2, 3]
    assert [d.subscriber for d in bus.dead_letters] == ["bad"] * 3
    bus.close()


def test_unsubscribe_discards_pending_and_close_rejects_new_work() -> None:
    bus = bus_with()
    gate, started, done = threading.Event(), threading.Event(), threading.Event()
    seen: list[int] = []

    def handler(event) -> None:
        started.set()
        gate.wait(5)
        seen.append(event.seq)
        done.set()

    sub = bus.subscribe(handler, queue_size=10)
    bus.publish("x", impl.Severity.INFO, "1")
    assert started.wait(5)
    bus.publish("x", impl.Severity.INFO, "2")
    bus.publish("x", impl.Severity.INFO, "3")
    assert bus.unsubscribe(sub) is True                              # 排队的 2、3 被丢弃，且不会卡在慢处理上
    gate.set()
    assert done.wait(5)
    assert seen == [1]                                               # 正在处理的那条送完，排队的不再送
    bus.close()
    with pytest.raises(impl.BusClosedError):
        bus.publish("x", impl.Severity.INFO, "late")
    with pytest.raises(impl.BusClosedError):
        bus.subscribe(Recorder())
    bus.close()                                                      # 可重复关闭


def test_close_with_drain_delivers_everything_queued() -> None:
    bus = bus_with()
    rec = Recorder()
    bus.subscribe(rec, queue_size=100)
    for i in range(20):
        bus.publish("x", impl.Severity.INFO, str(i))
    bus.close(drain=True)
    assert rec.seqs == list(range(1, 21))


# ---- 第 4 关：并发


def test_concurrent_publishers_every_subscriber_sees_every_event_once() -> None:
    bus = bus_with()
    sync_rec, async_rec = Recorder(), Recorder()
    lock = threading.Lock()

    def sync_handler(event) -> None:
        with lock:
            sync_rec(event)

    bus.subscribe(sync_handler)
    bus.subscribe(async_rec, queue_size=1000)
    barrier = threading.Barrier(8)

    def publisher() -> None:
        barrier.wait()
        for i in range(50):
            bus.publish("fire", impl.Severity.INFO, str(i))

    threads = [threading.Thread(target=publisher) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert bus.flush(10)
    assert sorted(sync_rec.seqs) == list(range(1, 401))              # 编号唯一、连续，一条不丢不重
    assert sorted(async_rec.seqs) == list(range(1, 401))
    bus.close()
