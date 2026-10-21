"""可配置缓存的验收测试：四关的行为、"策略与后端不一致"的失败路径，以及并发下的不变量。

只用公开 API（`len(cache)`、`store_size`、`stats`、`LfuPolicy.bucket_count`），不碰下划线属性。
时钟是注入的假时钟，线程测试断言不变量（容量不超、两边 key 数一致），不断言时间。
"""

from __future__ import annotations

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class FlakyStore:
    """包一层内存后端，可以按需让 put 失败、让指定 key 删不掉，用来制造"两边不一致"的现场。"""

    def __init__(self) -> None:
        self.inner = impl.MemoryStore()
        self.fail_put = False
        self.undeletable: set[str] = set()

    def __len__(self) -> int:
        return len(self.inner)

    def get(self, key):
        return self.inner.get(key)

    def put(self, key, value) -> None:
        if self.fail_put:
            raise impl.StoreError("disk full")
        self.inner.put(key, value)

    def delete(self, key) -> None:
        if key in self.undeletable:
            raise impl.StoreError("cannot delete")
        self.inner.delete(key)


def make(capacity=2, eviction="lru", backend="memory", path=None, clock=None, ttl=None):
    cfg = impl.CacheConfig(capacity=capacity, eviction=eviction, backend=backend, path=path, default_ttl=ttl)
    return impl.create_cache(cfg, clock) if clock else impl.create_cache(cfg)


def assert_consistent(cache) -> None:
    assert len(cache) == cache.store_size


# ---- 第 1 关：get / put / 淘汰


def test_put_then_get_and_default_on_miss() -> None:
    cache = make()
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("zzz") is None
    assert cache.get("zzz", default=-1) == -1


def test_lru_evicts_least_recently_used() -> None:
    cache = make(capacity=2, eviction="lru")
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")                      # a 变新，b 成了最久没用的
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1 and cache.get("c") == 3
    assert_consistent(cache)


def test_overwrite_does_not_evict_and_refreshes_recency() -> None:
    cache = make(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)                  # 覆盖：不涨容量，a 变新
    assert len(cache) == 2
    cache.put("c", 3)
    assert cache.get("b") is None and cache.get("a") == 10


def test_delete_returns_whether_it_existed() -> None:
    cache = make()
    cache.put("a", 1)
    assert cache.delete("a") is True
    assert cache.delete("a") is False
    assert cache.get("a") is None
    assert_consistent(cache)


# ---- 第 2 关：换策略（LFU）


def test_lfu_evicts_least_frequently_used_with_lru_tiebreak() -> None:
    cache = make(capacity=2, eviction="lfu")
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)                   # a 用过 2 次，b 只有 1 次 -> 淘汰 b
    assert cache.get("b") is None and cache.get("a") == 1
    cache.put("d", 4)                   # c 频率 1，a 频率 3 -> 淘汰 c，而不是刚插入的 d
    assert cache.get("c") is None and cache.get("d") == 4


def test_lfu_new_key_is_not_evicted_immediately() -> None:
    cache = make(capacity=1, eviction="lfu")
    cache.put("a", 1)
    cache.get("a")
    cache.put("b", 2)                   # 新 key 频率最低，但它自己不能成为受害者
    assert cache.get("b") == 2 and cache.get("a") is None


def test_lfu_frequency_ties_go_to_oldest() -> None:
    policy = impl.LfuPolicy()
    for key in ("x", "y", "z"):
        policy.on_insert(key)
    assert policy.victim() == "x"
    policy.on_access("x")
    assert policy.victim() == "y"


def test_lfu_empty_buckets_are_reclaimed() -> None:
    policy = impl.LfuPolicy()
    policy.on_insert("a")
    for _ in range(50):
        policy.on_access("a")           # 频率 1..51，每升一级留下的空桶都必须被回收
    assert policy.bucket_count == 1
    policy.on_insert("b")
    policy.on_remove("a")
    assert policy.bucket_count == 1 and policy.victim() == "b"
    policy.on_remove("b")
    assert policy.bucket_count == 0 and len(policy) == 0
    with pytest.raises(impl.EmptyPolicyError):
        policy.victim()


def test_lfu_min_pointer_after_removing_middle_key() -> None:
    policy = impl.LfuPolicy()
    policy.on_insert("a")
    policy.on_insert("b")
    policy.on_access("b")
    policy.on_access("b")               # a:1  b:3
    policy.on_remove("a")               # 最小桶被删空，最小频率必须重新找到 b 的 3
    assert policy.victim() == "b"


# ---- 第 3 关：换后端（文件）


def test_file_backend_roundtrip_and_eviction_removes_files(tmp_path) -> None:
    cache = make(capacity=2, backend="file", path=tmp_path)
    cache.put("a", {"n": 1})
    cache.put("b", [1, 2])
    assert cache.get("a") == {"n": 1}
    cache.put("c", "x")                 # 淘汰 b
    assert cache.get("b") is None
    assert len(list(tmp_path.glob("*.json"))) == 2
    assert_consistent(cache)


@pytest.mark.parametrize("eviction", ["lru", "lfu"])
@pytest.mark.parametrize("backend", ["memory", "file"])
def test_every_policy_works_with_every_backend(tmp_path, eviction, backend) -> None:
    cache = make(capacity=3, eviction=eviction, backend=backend, path=tmp_path)
    for i in range(10):
        cache.put(f"k{i}", i)
        assert len(cache) <= 3
        assert_consistent(cache)
    assert cache.stats.evictions == 7


def test_file_backend_keys_cannot_escape_the_directory(tmp_path) -> None:
    inner = tmp_path / "cache"
    cache = make(backend="file", path=inner)
    cache.put("../../evil", 1)
    assert cache.get("../../evil") == 1
    assert not (tmp_path / "evil.json").exists()
    assert len(list(inner.glob("*.json"))) == 1


def test_config_errors(tmp_path) -> None:
    with pytest.raises(impl.ConfigError):
        make(eviction="fifo")
    with pytest.raises(impl.ConfigError):
        make(backend="redis")
    with pytest.raises(impl.ConfigError):
        make(backend="file")            # 没给目录
    with pytest.raises(impl.ConfigError):
        make(capacity=0)
    (tmp_path / "old.json").write_text('{"key": "old", "value": 1}')
    with pytest.raises(impl.ConfigError):
        make(backend="file", path=tmp_path)   # 目录里已有缓存不认识的数据


# ---- 失败路径：策略与后端不一致


def test_failed_put_leaves_cache_unchanged(tmp_path) -> None:
    cache = make(capacity=2, backend="file", path=tmp_path)
    cache.put("a", 1)
    cache.put("b", 2)
    with pytest.raises(impl.StoreError):
        cache.put("c", {1, 2})          # set 不能序列化：磁盘还没动就失败
    assert len(cache) == 2 and cache.stats.evictions == 0
    assert cache.get("a") == 1 and cache.get("b") == 2   # 没有人因为一次失败的写入被淘汰
    assert_consistent(cache)


def test_failed_overwrite_keeps_old_value() -> None:
    store = FlakyStore()
    cache = impl.Cache(2, impl.LruPolicy(), store)
    cache.put("a", 1)
    store.fail_put = True
    with pytest.raises(impl.StoreError):
        cache.put("a", 2)
    store.fail_put = False
    assert cache.get("a") == 1
    assert_consistent(cache)


def test_failed_eviction_rolls_back_the_new_value() -> None:
    store = FlakyStore()
    cache = impl.Cache(1, impl.LruPolicy(), store)
    cache.put("a", 1)
    store.undeletable = {"a"}
    with pytest.raises(impl.StoreError):
        cache.put("b", 2)               # 要淘汰 a 但删不掉
    store.undeletable = set()
    assert cache.get("a") == 1 and cache.get("b") is None
    assert len(cache) == 1 and cache.store_size == 1
    cache.put("b", 2)                   # 故障恢复后一切照常
    assert cache.get("b") == 2 and cache.get("a") is None


def test_corrupt_file_raises_store_error(tmp_path) -> None:
    store = impl.FileStore(tmp_path)
    store.put("a", 1)
    next(tmp_path.glob("*.json")).write_text("{not json")
    with pytest.raises(impl.StoreError):
        store.get("a")
    with pytest.raises(KeyError):
        store.get("missing")


# ---- 过期与统计


def test_ttl_expiry_counts_and_frees_the_slot() -> None:
    clock = FakeClock()
    cache = make(capacity=2, clock=clock)
    cache.put("a", 1, ttl=10)
    cache.put("b", 2)
    clock.now += 10
    assert cache.get("a") is None       # 到点即过期（>=）
    assert len(cache) == 1 and cache.stats.expirations == 1
    cache.put("c", 3)
    assert cache.get("b") == 2          # 过期腾出了位置，所以 b 没被淘汰
    assert cache.stats.evictions == 0


def test_default_ttl_and_overwrite_resets_deadline() -> None:
    clock = FakeClock()
    cache = make(clock=clock, ttl=10)
    cache.put("a", 1)
    clock.now += 6
    cache.put("a", 2)                   # 覆盖重新计时
    clock.now += 6
    assert cache.get("a") == 2
    cache.put("a", 3, ttl=1)
    clock.now += 1
    assert cache.get("a") is None


def test_stats_are_a_snapshot() -> None:
    cache = make()
    cache.put("a", 1)
    cache.get("a")
    cache.get("b")
    snap = cache.stats
    assert (snap.hits, snap.misses) == (1, 1) and snap.hit_rate == 0.5
    cache.get("a")
    assert snap.hits == 1 and cache.stats.hits == 2
    assert impl.CacheStats().hit_rate == 0.0


# ---- 第 4 关：线程安全


@pytest.mark.parametrize("eviction", ["lru", "lfu"])
def test_concurrent_writers_keep_invariants(tmp_path, eviction) -> None:
    cache = make(capacity=8, eviction=eviction, backend="file", path=tmp_path)
    barrier = threading.Barrier(6)
    errors: list[BaseException] = []

    def worker(seed: int) -> None:
        try:
            barrier.wait()
            for i in range(60):
                key = f"k{(seed * 7 + i) % 20}"
                cache.put(key, i)
                cache.get(key)
                if i % 5 == 0:
                    cache.delete(key)
        except BaseException as exc:    # noqa: BLE001 - 线程里的任何异常都算失败
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(s,)) for s in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert len(cache) <= 8
    assert_consistent(cache)
    assert len(list(tmp_path.glob("*.json"))) == len(cache)
