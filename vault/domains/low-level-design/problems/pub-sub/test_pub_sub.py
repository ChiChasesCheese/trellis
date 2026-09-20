"""进程内 Pub-Sub 的验收测试：四关的行为、失败路径，以及并发下"顺序不乱、一条不丢"的不变量。

所有断言都只看公开 API（`size`、`oldest_seq`、`cursor_count`、`lagged_count`、`delivered_count`、
`failed_count`、`next_seq`），不碰任何下划线属性——学习者换一套内部表示也应该照样通过。
并发测试用真线程加栅栏，断言的是不变量（总数对得上、位点单调递增），不是时间。
"""

from __future__ import annotations

import importlib
import os
import threading
import time
from datetime import datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FrozenClock:
    """固定时钟，测试自己推进；消息时间因此完全可预测。"""

    def __init__(self) -> None:
        self._base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._delta = timedelta()

    def __call__(self) -> datetime:
        return self._base + self._delta

    def advance(self, seconds: float) -> None:
        self._delta += timedelta(seconds=seconds)


class Collector:
    """一个记录收到了什么的订阅处理器。`fail_times` 让它先失败若干次再成功。"""

    def __init__(self, fail_times: int = 0, always_fail: bool = False) -> None:
        self.messages: list = []
        self.calls = 0
        self._fail_times = fail_times
        self._always_fail = always_fail
        self._lock = threading.Lock()

    def __call__(self, message) -> None:
        with self._lock:
            self.calls += 1
            if self._always_fail or self.calls <= self._fail_times:
                raise RuntimeError(f"boom on call {self.calls}")
            self.messages.append(message)

    @property
    def payloads(self) -> list:
        with self._lock:
            return [m.payload for m in self.messages]


def wait_until(predicate, timeout: float = 3.0) -> bool:
    """等一个不变量成立。只用于"异步的东西迟早会发生"，断言本身不依赖具体时长。"""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return predicate()


# ---------------------------------------------------------------------------
# 第 1 关：主题、发布者、订阅者、订阅生命周期
# ---------------------------------------------------------------------------


def test_push_subscriber_receives_messages_of_its_topic_in_order() -> None:
    broker = impl.Broker(clock=FrozenClock())
    sink = Collector()
    broker.subscribe("orders.created", sink, name="billing")
    for i in range(5):
        broker.publish("orders.created", i)
    broker.close()
    assert sink.payloads == [0, 1, 2, 3, 4]
    assert [m.seq for m in sink.messages] == [0, 1, 2, 3, 4]


def test_a_subscriber_does_not_see_other_topics() -> None:
    broker = impl.Broker()
    orders, users = Collector(), Collector()
    broker.subscribe("orders.created", orders)
    broker.subscribe("users.created", users)
    broker.publish("orders.created", "o1")
    broker.publish("users.created", "u1")
    broker.close()
    assert orders.payloads == ["o1"]
    assert users.payloads == ["u1"]


def test_unsubscribe_stops_delivery_and_releases_the_cursor() -> None:
    broker = impl.Broker()
    sink = Collector()
    subscription = broker.subscribe("orders.created", sink)
    broker.publish("orders.created", "before")
    assert wait_until(lambda: sink.payloads == ["before"])
    topic = broker.topic("orders.created")
    assert topic.cursor_count == 1
    broker.unsubscribe(subscription)
    assert topic.cursor_count == 0          # 游标必须被摘掉，否则 BLOCK 策略会被幽灵游标卡死
    assert broker.subscription_count == 0
    broker.publish("orders.created", "after")
    time.sleep(0.05)
    assert sink.payloads == ["before"]
    broker.close()


def test_one_failing_subscriber_does_not_stop_the_others() -> None:
    broker = impl.Broker()
    good, bad = Collector(), Collector(always_fail=True)
    broker.subscribe("alerts", good, name="good")
    bad_sub = broker.subscribe("alerts", bad, name="bad")
    for i in range(3):
        broker.publish("alerts", i)
    broker.close()
    assert good.payloads == [0, 1, 2]
    assert bad.calls == 3                   # 坏订阅者每条都试过，也每条都炸了
    assert bad_sub.failed_count == 3
    assert bad_sub.delivered_count == 0


def test_a_failing_handler_does_not_block_its_own_later_messages() -> None:
    broker = impl.Broker()
    sink = Collector(fail_times=1)
    subscription = broker.subscribe("alerts", sink)
    broker.publish("alerts", "first")
    broker.publish("alerts", "second")
    broker.close()
    assert sink.payloads == ["second"]      # 第一条炸了，游标照样前进
    assert subscription.failed_count == 1
    assert subscription.delivered_count == 1


def test_publishing_to_an_unknown_topic_without_auto_create_raises() -> None:
    broker = impl.Broker(auto_create=False)
    with pytest.raises(impl.TopicNotFoundError):
        broker.publish("nope", 1)
    with pytest.raises(impl.TopicNotFoundError):
        broker.subscribe("nope")
    broker.close()


def test_publishing_after_close_is_refused() -> None:
    broker = impl.Broker()
    broker.publish("orders.created", 1)
    broker.close()
    broker.close()                          # 关闭幂等
    with pytest.raises(impl.BrokerClosedError):
        broker.publish("orders.created", 2)


# ---------------------------------------------------------------------------
# 第 2 关：投递模型——拉 + 每订阅者游标，重放与慢订阅者隔离
# ---------------------------------------------------------------------------


def test_two_pull_subscribers_have_independent_cursors() -> None:
    broker = impl.Broker()
    fast = broker.subscribe("metrics", name="fast")
    slow = broker.subscribe("metrics", name="slow")
    for i in range(4):
        broker.publish("metrics", i)
    assert [m.payload for m in fast.poll(max_items=10)] == [0, 1, 2, 3]
    assert fast.poll(max_items=10) == ()                     # 追平了就是空
    assert [m.payload for m in slow.poll(max_items=2)] == [0, 1]
    assert [m.payload for m in slow.poll(max_items=10)] == [2, 3]
    broker.close()


def test_from_beginning_replays_the_retained_log() -> None:
    broker = impl.Broker(capacity=16)
    for i in range(3):
        broker.publish("metrics", i)
    late = broker.subscribe("metrics", from_beginning=True, name="late")
    assert [m.payload for m in late.poll(max_items=10)] == [0, 1, 2]
    broker.close()


def test_a_late_subscriber_without_from_beginning_only_sees_new_messages() -> None:
    broker = impl.Broker(capacity=16)
    broker.publish("metrics", "old")
    late = broker.subscribe("metrics", name="late")
    assert late.poll(max_items=10) == ()
    broker.publish("metrics", "new")
    assert [m.payload for m in late.poll(max_items=10)] == ["new"]
    broker.close()


def test_seek_replays_from_an_offset() -> None:
    broker = impl.Broker(capacity=16)
    puller = broker.subscribe("metrics", name="reader")
    for i in range(5):
        broker.publish("metrics", i)
    assert [m.payload for m in puller.poll(max_items=10)] == [0, 1, 2, 3, 4]
    assert puller.seek("metrics", 2) == 2
    assert [m.payload for m in puller.poll(max_items=10)] == [2, 3, 4]   # 重放，推模型给不了
    assert puller.seek("metrics", 999) == 5                              # 夹到保留窗口内
    broker.close()


def test_poll_on_a_push_subscription_is_refused() -> None:
    broker = impl.Broker()
    subscription = broker.subscribe("orders.created", Collector())
    with pytest.raises(impl.PubSubError):
        subscription.poll()
    broker.close()


def test_poll_with_timeout_returns_empty_instead_of_hanging() -> None:
    broker = impl.Broker()
    puller = broker.subscribe("metrics", name="reader")
    started = time.monotonic()
    assert puller.poll(max_items=1, timeout=0.05) == ()
    assert time.monotonic() - started < 2.0
    broker.close()


# ---------------------------------------------------------------------------
# 第 3 关：有界日志、溢出策略、真线程下的顺序与不丢
# ---------------------------------------------------------------------------


def test_drop_oldest_bounds_the_log_and_counts_what_the_slow_subscriber_lost() -> None:
    broker = impl.Broker(capacity=3, policy=impl.OverflowPolicy.DROP_OLDEST)
    slow = broker.subscribe("metrics", name="slow")
    for i in range(6):
        broker.publish("metrics", i)
    topic = broker.topic("metrics")
    assert topic.size == 3                  # 有界就是有界
    assert topic.next_seq == 6
    assert topic.oldest_seq == 3
    assert topic.evicted_count == 3
    assert [m.payload for m in slow.poll(max_items=10)] == [3, 4, 5]
    assert slow.lagged_count == 3           # 丢弃必须可观测，否则就是静默丢数据
    broker.close()


def test_reject_policy_raises_backpressure_instead_of_dropping() -> None:
    broker = impl.Broker(capacity=2, policy=impl.OverflowPolicy.REJECT)
    reader = broker.subscribe("metrics", name="reader")
    broker.publish("metrics", 0)
    broker.publish("metrics", 1)
    with pytest.raises(impl.BackpressureError):
        broker.publish("metrics", 2)
    assert broker.topic("metrics").next_seq == 2
    assert [m.payload for m in reader.poll(max_items=10)] == [0, 1]
    broker.publish("metrics", 2)            # 读走之后又放得下了
    broker.close()


def test_block_policy_makes_the_publisher_wait_for_the_slowest_cursor() -> None:
    broker = impl.Broker(capacity=2, policy=impl.OverflowPolicy.BLOCK)
    reader = broker.subscribe("metrics", name="reader")
    broker.publish("metrics", 0)
    broker.publish("metrics", 1)
    done = threading.Event()

    def publish_third() -> None:
        broker.publish("metrics", 2, timeout=5.0)
        done.set()

    publisher = threading.Thread(target=publish_third)
    publisher.start()
    assert not done.wait(0.15)                              # 队头还没人读过，发布者被反压住
    assert [m.payload for m in reader.poll(max_items=1)] == [0]
    assert done.wait(3.0)                                   # 队头被读过，腾位置合法了
    publisher.join(3.0)
    assert broker.topic("metrics").next_seq == 3
    assert reader.lagged_count == 0                         # BLOCK 的承诺：一条都不丢
    broker.close()


def test_block_policy_gives_up_at_the_timeout() -> None:
    broker = impl.Broker(capacity=1, policy=impl.OverflowPolicy.BLOCK)
    broker.subscribe("metrics", name="reader")
    broker.publish("metrics", 0, timeout=1.0)
    with pytest.raises(impl.BackpressureError):
        broker.publish("metrics", 1, timeout=0.05)
    broker.close()


def test_unsubscribing_the_slow_reader_unblocks_the_publisher() -> None:
    broker = impl.Broker(capacity=1, policy=impl.OverflowPolicy.BLOCK)
    reader = broker.subscribe("metrics", name="reader")
    broker.publish("metrics", 0, timeout=1.0)
    done = threading.Event()

    def publish_second() -> None:
        broker.publish("metrics", 1, timeout=5.0)
        done.set()

    publisher = threading.Thread(target=publish_second)
    publisher.start()
    assert not done.wait(0.1)
    broker.unsubscribe(reader)                              # 走掉的读者不许继续挡着发布者
    assert done.wait(3.0)
    publisher.join(3.0)
    broker.close()


def test_order_is_per_topic_per_subscriber_and_nothing_is_lost() -> None:
    broker = impl.Broker(capacity=4096)
    sink = Collector()
    broker.subscribe("orders.created", sink, name="audit")
    publishers, per_thread = 4, 50
    barrier = threading.Barrier(publishers)

    def publish(tag: int) -> None:
        barrier.wait()
        for i in range(per_thread):
            broker.publish("orders.created", (tag, i), key=str(tag))

    threads = [threading.Thread(target=publish, args=(t,)) for t in range(publishers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(10.0)
    broker.close()                                          # 关闭前发布的，一条都不能少
    assert len(sink.messages) == publishers * per_thread
    seqs = [m.seq for m in sink.messages]
    assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs)   # 主题内位点严格递增
    for tag in range(publishers):
        own = [i for (t, i) in sink.payloads if t == tag]
        assert own == list(range(per_thread))               # 单个发布者自己的顺序也保住了
    assert broker.topic("orders.created").next_seq == publishers * per_thread


def test_concurrent_pull_subscribers_each_see_every_message() -> None:
    broker = impl.Broker(capacity=1024)
    readers = [broker.subscribe("metrics", name=f"r{i}") for i in range(3)]
    for i in range(100):
        broker.publish("metrics", i)
    seen: dict[str, list] = {}

    def drain(subscription) -> None:
        got: list = []
        while len(got) < 100:
            batch = subscription.poll(max_items=7, timeout=0.05)
            if not batch:
                break
            got.extend(m.payload for m in batch)
        seen[subscription.id] = got

    threads = [threading.Thread(target=drain, args=(r,)) for r in readers]
    for t in threads:
        t.start()
    for t in threads:
        t.join(10.0)
    for reader in readers:
        assert seen[reader.id] == list(range(100))          # 广播：每人都拿到全量
        assert reader.lagged_count == 0
    broker.close()


# ---------------------------------------------------------------------------
# 第 4 关：通配订阅与死信——不碰投递路径
# ---------------------------------------------------------------------------


def test_star_matches_exactly_one_segment_and_hash_matches_the_rest() -> None:
    star = impl.TopicPattern("orders.*")
    assert star.matches("orders.created")
    assert not star.matches("orders.created.eu")
    assert not star.matches("orders")
    hashed = impl.TopicPattern("orders.#")
    assert hashed.matches("orders.created")
    assert hashed.matches("orders.created.eu")
    assert not hashed.matches("users.created")
    exact = impl.TopicPattern("orders.created")
    assert exact.matches("orders.created") and not exact.is_wildcard


def test_an_invalid_pattern_is_rejected_at_construction() -> None:
    with pytest.raises(impl.InvalidPatternError):
        impl.TopicPattern("orders.#.eu")
    with pytest.raises(impl.InvalidPatternError):
        impl.TopicPattern("orders..created")


def test_a_wildcard_subscription_picks_up_topics_created_later() -> None:
    broker = impl.Broker()
    sink = Collector()
    subscription = broker.subscribe("orders.#", sink, name="audit")
    broker.publish("orders.created", "a")                   # 主题此刻才被建出来
    broker.publish("orders.shipped.eu", "b")
    broker.publish("users.created", "c")
    assert set(subscription.topic_names) == {"orders.created", "orders.shipped.eu"}
    broker.close()
    assert sorted(sink.payloads) == ["a", "b"]


def test_wildcards_never_match_the_internal_dead_letter_topic() -> None:
    broker = impl.Broker()
    sink = Collector()
    subscription = broker.subscribe("#", sink, name="everything")
    broker.publish(broker.dead_letter_topic, "internal")
    broker.publish("orders.created", "normal")
    assert subscription.topic_names == ("orders.created",)
    broker.close()
    assert sink.payloads == ["normal"]                      # 否则失败一次就成死循环


def test_dead_letter_carries_the_failed_message_and_its_origin() -> None:
    broker = impl.Broker()
    bad = Collector(always_fail=True)
    subscription = broker.subscribe("orders.created", bad, max_attempts=2, dead_letter=True, name="risky")
    broker.publish("orders.created", "payload")
    assert wait_until(lambda: subscription.failed_count == 1)
    assert bad.calls == 2                                   # 重试次数就是 max_attempts
    dlq = broker.topic(broker.dead_letter_topic)
    assert wait_until(lambda: dlq.next_seq == 1)
    dlq.register("probe", from_beginning=True)
    messages, lost = dlq.read("probe", 10)
    assert lost == 0 and len(messages) == 1
    assert messages[0].payload == "payload"
    assert messages[0].headers["origin_topic"] == "orders.created"
    assert messages[0].headers["origin_seq"] == 0
    assert messages[0].headers["subscription"] == "risky"
    broker.close()


def test_a_transient_failure_is_retried_and_then_counted_as_delivered() -> None:
    broker = impl.Broker()
    flaky = Collector(fail_times=2)
    subscription = broker.subscribe("orders.created", flaky, max_attempts=3, name="flaky")
    broker.publish("orders.created", "once")
    broker.close()
    assert flaky.calls == 3
    assert flaky.payloads == ["once"]
    assert subscription.delivered_count == 1                # 重试成功只算投递一次
    assert subscription.failed_count == 0


def test_messages_carry_the_injected_clock_and_their_topic() -> None:
    clock = FrozenClock()
    broker = impl.Broker(clock=clock)
    first = broker.publish("metrics", 1)
    clock.advance(60)
    second = broker.publish("metrics", 2)
    assert first.topic == "metrics" and first.seq == 0
    assert (second.published_at - first.published_at).total_seconds() == 60
    with pytest.raises(Exception):
        first.seq = 7                                       # 冻结：事件对象谁都改不了
    broker.close()


def test_reading_with_an_unknown_subscription_id_is_refused() -> None:
    broker = impl.Broker()
    topic = broker.create_topic("metrics")
    with pytest.raises(impl.UnknownSubscriptionError):
        topic.read("ghost", 1)
    with pytest.raises(impl.UnknownSubscriptionError):
        topic.seek("ghost", 0)
    broker.close()
