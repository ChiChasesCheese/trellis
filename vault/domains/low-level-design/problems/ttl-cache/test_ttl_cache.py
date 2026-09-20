"""TTL 缓存的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。

时钟一律注入，没有任何 `sleep`；并发测试用屏障对齐起跑线，断言的是不变量（容量没被撑破、
回源只发生一次）而不是时序。所有断言只用公开方法和只读属性，换一种内部表示照样能过。
"""

from __future__ import annotations

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FakeClock:
    """可控时钟：`advance` 推进，调用它返回当前秒数。"""

    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


# ---------- 第 1 关：get/put 与按条过期 ----------


def test_put_and_get_round_trip() -> None:
    cache = impl.TTLCache(capacity=4, clock=FakeClock())
    cache.put("a", 1)
    cache["b"] = 2
    assert cache.get("a") == 1 and cache["b"] == 2
    with pytest.raises(KeyError):
        cache.get("missing")


def test_an_entry_dies_on_its_own_deadline() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=4, default_ttl=10.0, clock=clock)
    cache.put("a", 1)
    cache.put("b", 2, ttl=2.0)          # 每条数据可以有自己的存活时间
    clock.advance(1.9)
    assert cache.get("a") == 1 and cache.get("b") == 2
    clock.advance(0.2)
    assert cache.get("a") == 1
    with pytest.raises(KeyError):
        cache.get("b")


def test_a_never_read_expired_entry_is_still_reclaimed() -> None:
    """纯惰性过期的死穴：没人再读的 key 永远不会被发现已经死了。索引驱动的清理必须替它收尸。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=100, clock=clock)
    cache.put("cold", 1, ttl=1.0)       # 写进去之后再也没人读它
    cache.put("hot", 2, ttl=100.0)
    clock.advance(2.0)
    assert cache.get("hot") == 2        # 只碰了另一个 key
    assert len(cache) == 1 and cache.keys() == ("hot",)


def test_len_and_keys_never_show_an_expired_entry() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=10, default_ttl=5.0, clock=clock)
    for name in ("a", "b", "c"):
        cache.put(name, 1)
    assert len(cache) == 3
    clock.advance(6.0)
    assert len(cache) == 0 and cache.keys() == () and list(cache) == []
    assert "a" not in cache


def test_an_expired_entry_does_not_hold_capacity() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=2, default_ttl=5.0, clock=clock)
    cache.put("a", 1)
    cache.put("b", 2)
    clock.advance(6.0)
    cache.put("c", 3)                   # 两条都死了，写第三条不该淘汰任何活着的数据
    assert cache.get("c") == 3
    assert cache.stats.evictions == 0 and cache.stats.expirations == 2


def test_delete_and_invalid_configuration() -> None:
    cache = impl.TTLCache(capacity=2, clock=FakeClock())
    cache.put("a", 1)
    del cache["a"]
    with pytest.raises(KeyError):
        cache.delete("a")
    with pytest.raises(impl.InvalidConfiguration):
        impl.TTLCache(capacity=0, clock=FakeClock())
    with pytest.raises(impl.InvalidConfiguration):
        impl.TTLCache(capacity=2, default_ttl=0.0, clock=FakeClock())
    with pytest.raises(impl.InvalidConfiguration):
        cache.put("b", 1, ttl=-1.0)


# ---------- 第 2 关：淘汰策略与 TTL 的组合 ----------


def test_lru_evicts_the_least_recently_used() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=2, clock=clock)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")                      # a 变成最近使用
    cache.put("c", 3)
    assert sorted(cache.keys()) == ["a", "c"]
    assert cache.stats.evictions == 1


def test_overwriting_a_key_is_not_an_eviction() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=2, clock=clock)
    seen: list[tuple[str, str]] = []
    cache.add_listener(lambda event: seen.append((event.key, event.reason.value)))
    cache.put("a", 1)
    cache.put("a", 2)
    assert cache.get("a") == 2 and len(cache) == 1
    assert cache.stats.evictions == 0
    assert seen == [("a", "replaced")]


def test_nearest_deadline_policy_sacrifices_the_soonest_to_die() -> None:
    """同一条接缝的另一种实现：容量满时先赶走马上就要过期的那条，损失的未来命中最少。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=2, clock=clock, policy=impl.NearestDeadlinePolicy())
    cache.put("short", 1, ttl=5.0)
    cache.put("long", 2, ttl=500.0)
    cache.get("short")                  # 最近用过，但它仍然是最先要死的那个
    cache.put("new", 3, ttl=50.0)
    assert sorted(cache.keys()) == ["long", "new"]


def test_swapping_the_policy_does_not_change_the_ttl_behaviour() -> None:
    clock = FakeClock()
    for policy in (impl.LRUPolicy(), impl.NearestDeadlinePolicy()):
        cache = impl.TTLCache(capacity=5, default_ttl=10.0, clock=clock, policy=policy)
        cache.put("a", 1)
        assert cache.get("a") == 1
        clock.advance(11.0)
        assert len(cache) == 0
        clock.advance(-11.0)


# ---------- 第 3 关：线程安全、续命、单飞 ----------


def test_fixed_lifetime_does_not_extend_on_read() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=4, default_ttl=10.0, clock=clock)
    cache.put("a", 1)
    for _ in range(9):
        clock.advance(1.0)
        assert cache.get("a") == 1      # 反复读也不续命
    clock.advance(1.0)
    with pytest.raises(KeyError):
        cache.get("a")


def test_refresh_on_access_extends_the_life() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=4, default_ttl=10.0, clock=clock, refresh_on_access=True)
    cache.put("a", 1)
    for _ in range(9):
        clock.advance(9.0)
        assert cache.get("a") == 1      # 每读一次就重新开始计时
    clock.advance(11.0)
    with pytest.raises(KeyError):
        cache.get("a")


def test_threads_never_exceed_capacity() -> None:
    """100 个线程各写 20 个不同的 key，容量 50：任何时刻都不许超过 50 条。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=50, clock=clock)
    barrier = threading.Barrier(100)

    def worker(base: int) -> None:
        barrier.wait()
        for i in range(20):
            cache.put(base * 20 + i, i)

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(cache) == 50
    assert cache.stats.evictions == 2000 - 50


def test_single_flight_loads_a_hot_key_only_once() -> None:
    """一百个线程同时缓存未命中，回源必须只发生一次——否则就是缓存踩踏。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=10, default_ttl=100.0, clock=clock)
    calls = []
    guard = threading.Lock()
    barrier = threading.Barrier(100)
    ready = threading.Event()

    def loader() -> str:
        with guard:
            calls.append(1)
        ready.wait(timeout=5)           # 拖住领跑者，逼所有后来者去排队
        return "value"

    results: list[str] = []

    def worker() -> None:
        barrier.wait()
        value = cache.get_or_load("hot", loader)
        with guard:
            results.append(value)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(100)]
    for thread in threads:
        thread.start()
    ready.set()
    for thread in threads:
        thread.join(timeout=10)
    assert len(calls) == 1
    assert results == ["value"] * 100
    assert cache.stats.loads == 1
    assert cache.inflight_count == 0


def test_a_failing_loader_releases_the_key() -> None:
    """回源抛异常时也必须把在途标记摘掉，否则后来者会永远等下去。"""
    cache = impl.TTLCache(capacity=4, clock=FakeClock())

    def boom() -> int:
        raise RuntimeError("backend down")

    with pytest.raises(RuntimeError):
        cache.get_or_load("k", boom)
    assert cache.inflight_count == 0
    assert cache.get_or_load("k", lambda: 7) == 7


# ---------- 第 4 关：统计与淘汰回调 ----------


def test_stats_count_hits_misses_expirations_and_evictions() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=2, default_ttl=5.0, clock=clock)
    cache.put("a", 1)
    cache.get("a")
    with pytest.raises(KeyError):
        cache.get("nope")
    cache.put("b", 2)
    cache.put("c", 3)                   # 容量满，淘汰一条
    clock.advance(6.0)
    cache.purge_expired()
    stats = cache.stats
    assert (stats.hits, stats.misses, stats.evictions, stats.expirations) == (1, 1, 1, 2)
    assert stats.hit_rate == pytest.approx(0.5)


def test_listener_receives_the_value_and_the_reason() -> None:
    clock = FakeClock()
    cache = impl.TTLCache(capacity=1, clock=clock)
    events: list[tuple[str, int, str]] = []
    cache.add_listener(lambda e: events.append((e.key, e.value, e.reason.value)))
    cache.put("a", 1, ttl=5.0)
    clock.advance(6.0)
    cache.purge_expired()
    cache.put("b", 2)
    cache.put("c", 3)                   # 容量 1，b 被淘汰
    cache.delete("c")
    assert events == [("a", 1, "expired"), ("b", 2, "capacity"), ("c", 3, "removed")]


def test_listener_runs_outside_the_lock() -> None:
    """回调在锁外执行：监听者可以回头访问缓存而不会把自己锁死。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=1, clock=clock)
    seen: list[int] = []
    cache.add_listener(lambda e: seen.append(len(cache)))
    cache.put("a", 1)
    worker = threading.Thread(target=lambda: cache.put("b", 2), daemon=True)
    worker.start()
    worker.join(timeout=5)
    assert not worker.is_alive()        # 持锁回调会在这里挂住
    assert seen == [1]


# ---------- 容器必须会缩 ----------


def test_a_million_expired_entries_do_not_stay_in_memory() -> None:
    """一百万条写进来就没人再读的数据：存活条数和到期索引都必须随时间回落。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=1_000_000, default_ttl=1.0, clock=clock)
    peak_size = peak_heap = 0
    for i in range(1_000_000):
        cache.put(i, i)
        clock.advance(1e-4)             # 每个存活窗口里大约写进一万条
        if i % 10_000 == 0:
            peak_size = max(peak_size, len(cache))
            peak_heap = max(peak_heap, cache.expiry_heap_size)
    assert peak_size < 25_000 and peak_heap < 25_000
    clock.advance(10.0)
    assert cache.purge_expired() > 0
    assert len(cache) == 0 and cache.expiry_heap_size == 0


def test_overwriting_one_key_does_not_pile_up_tombstones() -> None:
    """改期在小顶堆里只能靠墓碑实现——墓碑必须被压实掉，否则一个热 key 就撑爆内存。"""
    clock = FakeClock()
    cache = impl.TTLCache(capacity=10, default_ttl=100.0, clock=clock)
    for i in range(200_000):
        cache.put("hot", i)             # 每次写入都要给同一个 key 改一次期
        clock.advance(1e-3)
    assert len(cache) == 1 and cache.get("hot") == 199_999
    assert cache.expiry_heap_size < 100
