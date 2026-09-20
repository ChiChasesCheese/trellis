import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class ManualClock:
    """可控的假时钟：测试自己推进时间，不依赖真实的 sleep。"""

    def __init__(self, t: float = 0.0) -> None:
        self.t = t

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


# ---------------------------------------------------------------------------
# 第 1 关：固定容量、O(1) get/put、LRU 淘汰
# ---------------------------------------------------------------------------


def test_capacity_must_be_positive() -> None:
    with pytest.raises(ValueError):
        impl.Cache(0)
    with pytest.raises(ValueError):
        impl.Cache(-1)


def test_basic_put_get_roundtrip() -> None:
    cache = impl.Cache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1


def test_get_missing_key_raises_keyerror() -> None:
    cache = impl.Cache(2)
    with pytest.raises(KeyError):
        cache.get("missing")


def test_put_updates_existing_value_without_eviction() -> None:
    cache = impl.Cache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 99)  # 更新已有 key，不应触发淘汰
    assert cache.get("a") == 99
    assert cache.get("b") == 2
    assert len(cache) == 2


def test_lru_eviction_order() -> None:
    cache = impl.Cache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # 容量已满，a 最久未用，被淘汰
    assert "a" not in cache
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    assert len(cache) == 2


def test_get_marks_recently_used_and_protects_from_eviction() -> None:
    cache = impl.Cache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")       # a 变为最近使用
    cache.put("c", 3)    # 该淘汰 b 了，不是 a
    assert "a" in cache
    assert "b" not in cache
    assert "c" in cache


def test_contains_does_not_affect_recency() -> None:
    cache = impl.Cache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert "a" in cache  # 只是探测，不算一次使用
    cache.put("c", 3)    # a 仍然是最久未用的，该被淘汰
    assert "a" not in cache
    assert "b" in cache
    assert "c" in cache


def test_len_reflects_current_size() -> None:
    cache = impl.Cache(3)
    assert len(cache) == 0
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache) == 2


def test_dunder_getitem_setitem_delitem() -> None:
    cache = impl.Cache(2)
    cache["a"] = 1
    assert cache["a"] == 1
    del cache["a"]
    assert "a" not in cache
    with pytest.raises(KeyError):
        cache["a"]


def test_discard_missing_key_raises_keyerror() -> None:
    cache = impl.Cache(2)
    with pytest.raises(KeyError):
        cache.discard("nope")


def test_generic_over_arbitrary_hashable_keys_and_values() -> None:
    cache: impl.Cache = impl.Cache(2)
    cache.put((1, "x"), {"n": 1})
    assert cache.get((1, "x")) == {"n": 1}


# ---------------------------------------------------------------------------
# 第 2 关：淘汰策略可插拔——LFU
# ---------------------------------------------------------------------------


def test_lfu_evicts_least_frequently_used() -> None:
    cache = impl.Cache(2, policy=impl.LFUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.get("a")  # a 的频率现在是 3（插入算 1 次），b 是 1
    cache.put("c", 3)  # b 频率最低，被淘汰
    assert "b" not in cache
    assert "a" in cache
    assert "c" in cache


def test_lfu_ties_broken_by_least_recently_used_within_frequency() -> None:
    cache = impl.Cache(2, policy=impl.LFUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)  # a、b 频率都为 1
    cache.get("a")     # a 频率变 2；b 仍是 1（同时也是最小频率里最久未用的）
    cache.put("c", 3)  # 最小频率桶里只有 b，淘汰 b
    assert "b" not in cache
    assert "a" in cache
    assert "c" in cache


def test_policy_is_pluggable_without_changing_cache_class() -> None:
    lru = impl.Cache(2, policy=impl.LRUPolicy())
    lfu = impl.Cache(2, policy=impl.LFUPolicy())
    assert type(lru) is type(lfu) is impl.Cache
    for c in (lru, lfu):
        c.put("a", 1)
        c.put("b", 2)
        assert c.get("a") == 1


def test_lfu_bucket_count_matches_number_of_distinct_live_frequencies() -> None:
    policy = impl.LFUPolicy()
    policy.record_insert("a")
    policy.record_insert("b")
    policy.record_insert("c")   # a、b、c 都是频率 1 -> 只有 1 个桶
    assert policy.bucket_count == 1
    policy.record_access("a")
    policy.record_access("a")   # a 频率变 3
    policy.record_access("b")   # b 频率变 2
    # c 频率 1，b 频率 2，a 频率 3 -> 三个不同的活跃频率
    assert policy.bucket_count == 3


def test_lfu_bucket_count_does_not_leak_on_repeated_access_of_one_key() -> None:
    """一个 key 被反复访问一千次，旧频率的桶必须每次都被回收，不能在内存里堆积空桶。"""
    policy = impl.LFUPolicy()
    policy.record_insert("a")
    for _ in range(1000):
        policy.record_access("a")
    assert policy.bucket_count == 1


def test_lfu_evict_repeatedly_until_empty_returns_lfu_then_lru_order() -> None:
    policy = impl.LFUPolicy()
    for key in ("a", "b", "c", "d"):
        policy.record_insert(key)          # 全部频率 1，插入顺序 a, b, c, d
    policy.record_access("c")              # c 频率变 2
    policy.record_access("d")
    policy.record_access("d")              # d 频率变 3
    # 频率：a=1, b=1（a 比 b 先插入，同频率里 a 更久未用），c=2，d=3
    assert policy.evict() == "a"
    assert policy.evict() == "b"
    assert policy.evict() == "c"
    assert policy.evict() == "d"
    assert len(policy) == 0
    assert policy.bucket_count == 0


def test_lfu_evict_twice_without_insert_between_recomputes_min_freq() -> None:
    """两次 evict 中间不插入新 key，且第一次刚好掏空 min_freq 所在的桶：
    修复前会在空桶上 pop_front 抛 IndexError，修复后 min_freq 必须正确前移到下一个非空频率。
    """
    policy = impl.LFUPolicy()
    policy.record_insert("a")
    policy.record_insert("b")
    policy.record_access("b")  # b 频率变 2，a 仍是频率 1（唯一的最小频率 key）
    assert policy.evict() == "a"   # 掏空频率 1 的桶
    assert policy.evict() == "b"   # 不应该抛异常，min_freq 已经前移到 2


def test_lfu_remove_only_min_frequency_key_then_evict_returns_next() -> None:
    policy = impl.LFUPolicy()
    policy.record_insert("a")
    policy.record_insert("b")
    policy.record_access("b")  # b 频率变 2，a 是最小频率桶里唯一的 key
    policy.remove("a")         # 主动移除最小频率桶里唯一的 key
    assert policy.bucket_count == 1
    assert policy.evict() == "b"   # min_freq 必须已经从 1 重新算成 2


# ---------------------------------------------------------------------------
# 第 3 关：线程安全
# ---------------------------------------------------------------------------


def test_synchronized_cache_never_exceeds_capacity_under_contention() -> None:
    capacity = 4
    n_threads = 20
    cache = impl.SynchronizedCache(impl.Cache(capacity))
    barrier = threading.Barrier(n_threads)

    def worker(i: int) -> None:
        barrier.wait()
        for j in range(50):
            cache.put(f"k{i}-{j}", i * 1000 + j)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(cache) <= capacity  # 不变量：并发下 size 永不超过 capacity


def test_synchronized_cache_no_lost_entries_when_capacity_fits_all() -> None:
    n_threads = 16
    cache = impl.SynchronizedCache(impl.Cache(capacity=n_threads))
    barrier = threading.Barrier(n_threads)
    results: dict[int, bool] = {}
    lock = threading.Lock()

    def worker(i: int) -> None:
        barrier.wait()
        cache.put(f"k{i}", i)
        with lock:
            results[i] = True

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == n_threads  # 不变量：容量足够放下所有 key 时，一条都不能丢
    assert len(cache) == n_threads
    for i in range(n_threads):
        assert cache.get(f"k{i}") == i


# ---------------------------------------------------------------------------
# 第 4 关：按 key 的 TTL，可注入时钟
# ---------------------------------------------------------------------------


def test_expiring_cache_returns_value_before_ttl() -> None:
    clock = ManualClock(t=0.0)
    cache = impl.ExpiringCache(impl.Cache(2), ttl_seconds=10.0, clock=clock)
    cache.put("a", 1)
    clock.advance(9.0)
    assert cache.get("a") == 1
    assert "a" in cache


def test_expiring_cache_entry_expires_after_ttl() -> None:
    clock = ManualClock(t=0.0)
    cache = impl.ExpiringCache(impl.Cache(2), ttl_seconds=10.0, clock=clock)
    cache.put("a", 1)
    clock.advance(10.0)
    assert "a" not in cache
    with pytest.raises(KeyError):
        cache.get("a")
    assert len(cache) == 0  # 过期项被顺手清理，不再占用底层缓存的容量


def test_expiring_cache_put_refreshes_ttl() -> None:
    clock = ManualClock(t=0.0)
    cache = impl.ExpiringCache(impl.Cache(2), ttl_seconds=10.0, clock=clock)
    cache.put("a", 1)
    clock.advance(9.0)
    cache.put("a", 2)   # 重新 put，ttl 从这一刻重新计时
    clock.advance(9.0)  # 距首次 put 已 18s，但距第二次 put 只有 9s
    assert cache.get("a") == 2
