"""TTLCache unit tests: basic get/set/expiry/invalidate/clear, plus one concurrency test that
pins down how `get_or_compute` behaves when two threads race a cache miss for the same key.
"""

import threading
import time

from confmgr.cache import TTLCache


# ---------------------------------------------------------------- basic get/set/expiry
def test_get_on_empty_cache_returns_none():
    cache = TTLCache(ttl_seconds=60)
    assert cache.get("missing") is None


def test_set_then_get_returns_the_stored_value():
    cache = TTLCache(ttl_seconds=60)
    cache.set("k", "v")
    assert cache.get("k") == "v"


def test_entry_expires_after_its_ttl():
    cache = TTLCache(ttl_seconds=0.05)
    cache.set("k", "v")
    assert cache.get("k") == "v"
    time.sleep(0.1)
    assert cache.get("k") is None


def test_invalidate_removes_only_the_given_key():
    cache = TTLCache(ttl_seconds=60)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.invalidate("a")
    assert cache.get("a") is None
    assert cache.get("b") == 2


def test_invalidate_missing_key_is_a_no_op():
    cache = TTLCache(ttl_seconds=60)
    cache.invalidate("nope")  # must not raise


def test_clear_removes_every_entry():
    cache = TTLCache(ttl_seconds=60)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None


# ---------------------------------------------------------------- get_or_compute, single-threaded
def test_get_or_compute_calls_factory_on_a_miss():
    cache = TTLCache(ttl_seconds=60)
    assert cache.get_or_compute("k", lambda: "fresh") == "fresh"
    assert cache.get("k") == "fresh"


def test_get_or_compute_skips_factory_on_a_hit():
    cache = TTLCache(ttl_seconds=60)
    cache.set("k", "cached")
    calls = []

    def factory():
        calls.append(1)
        return "should-not-be-used"

    assert cache.get_or_compute("k", factory) == "cached"
    assert calls == []


# ---------------------------------------------------------------- concurrency: cache-stampede guard
def test_get_or_compute_calls_factory_at_most_once_under_concurrent_misses():
    """Two threads call get_or_compute for the same, not-yet-cached key at (as close to) the same
    moment as threading.Barrier can arrange. factory() sleeps long enough that -- if the check
    and the write aren't one atomic operation -- both threads are guaranteed to observe a miss
    before either of them stores a value, so this reproduces the same way on every run rather
    than depending on how the OS happens to schedule the two threads."""
    cache = TTLCache(ttl_seconds=60)
    calls = []
    calls_lock = threading.Lock()
    start_barrier = threading.Barrier(2)
    results = []

    def factory():
        with calls_lock:
            calls.append(1)
        time.sleep(0.2)  # stands in for an expensive layer-merge computation
        return "computed-value"

    def worker():
        start_barrier.wait()
        results.append(cache.get_or_compute("shared-key", factory))

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert len(calls) == 1, f"factory should run exactly once per miss, ran {len(calls)} time(s)"
    assert results == ["computed-value", "computed-value"]
