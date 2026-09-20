"""限流器的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。

时钟一律注入，没有任何 `sleep`；并发测试用屏障对齐起跑线，断言的是"没有超卖"这条
不变量，而不是某个时序。所有断言只用公开方法和只读属性，换一种内部表示照样能过。
"""

from __future__ import annotations

import importlib
import math
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


ALGORITHMS = ["fixed", "bucket", "log", "counter"]


def make_algorithm(kind: str, limit: int = 5, window: float = 10.0):
    """按名字造一份限流状态——共享契约的测试对四种算法各跑一遍。"""
    if kind == "fixed":
        return impl.FixedWindowCounter(limit, window)
    if kind == "bucket":
        return impl.TokenBucket(limit, window, burst=limit)
    if kind == "log":
        return impl.SlidingWindowLog(limit, window)
    return impl.SlidingWindowCounter(limit, window)


# ---------- 第 1 关：一个 key、一个固定窗口 ----------


def test_fixed_window_allows_exactly_the_limit() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.FixedWindowCounter(3, 10.0), clock=clock)
    assert [bool(limiter.allow("alice")) for _ in range(5)] == [True, True, True, False, False]


def test_fixed_window_boundary_burst_is_twice_the_limit() -> None:
    """限额 5／10 秒，却在 0.2 秒内放行 10 次——这正是固定窗口该被换掉的理由。"""
    clock = FakeClock(9.9)
    limiter = impl.RateLimiter(lambda: impl.FixedWindowCounter(5, 10.0), clock=clock)
    passed = sum(bool(limiter.allow("alice")) for _ in range(5))
    clock.advance(0.2)
    passed += sum(bool(limiter.allow("alice")) for _ in range(5))
    assert passed == 10


def test_sliding_window_counter_kills_the_boundary_burst() -> None:
    clock = FakeClock(9.9)
    limiter = impl.RateLimiter(lambda: impl.SlidingWindowCounter(5, 10.0), clock=clock)
    passed = sum(bool(limiter.allow("alice")) for _ in range(5))
    clock.advance(0.2)
    passed += sum(bool(limiter.allow("alice")) for _ in range(5))
    assert passed == 5


def test_decision_is_truthy_and_carries_retry_after() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.FixedWindowCounter(1, 10.0), clock=clock)
    granted = limiter.allow("alice")
    assert granted and granted.remaining == 0 and granted.retry_after == 0.0
    denied = limiter.allow("alice")
    assert not denied and denied.retry_after == pytest.approx(10.0)


# ---------- 第 2 关：算法成为可替换的接缝 ----------


@pytest.mark.parametrize("kind", ALGORITHMS)
def test_denied_request_consumes_nothing(kind: str) -> None:
    """被拒的请求既不扣额度，也不把恢复时间往后推——否则客户端重试即永久饿死。"""
    state = make_algorithm(kind, limit=2)
    state.try_acquire(0.0)
    state.try_acquire(0.0)
    first = state.try_acquire(0.0)
    for _ in range(50):
        state.try_acquire(0.0)
    second = state.try_acquire(0.0)
    assert not first and not second
    assert second.retry_after == pytest.approx(first.retry_after)


@pytest.mark.parametrize("kind", ALGORITHMS)
def test_retry_after_is_honest(kind: str) -> None:
    """等满 retry_after 之后必须真的能过——否则这个字段就是在骗调用方。"""
    state = make_algorithm(kind, limit=3, window=10.0)
    for _ in range(3):
        assert state.try_acquire(0.0)
    denied = state.try_acquire(0.0)
    assert not denied and denied.retry_after > 0
    assert state.try_acquire(denied.retry_after + 1e-6)


@pytest.mark.parametrize("kind", ALGORITHMS)
def test_cost_above_the_limit_can_never_pass(kind: str) -> None:
    state = make_algorithm(kind, limit=5)
    decision = state.try_acquire(0.0, cost=6)
    assert not decision and decision.retry_after == math.inf


@pytest.mark.parametrize("kind", ALGORITHMS)
def test_non_positive_cost_is_a_configuration_error(kind: str) -> None:
    state = make_algorithm(kind)
    with pytest.raises(impl.InvalidConfiguration):
        state.check(0.0, cost=0)


def test_token_bucket_refills_lazily_and_never_overflows() -> None:
    """没有后台线程：令牌是用"距上次记账过了多久"现算出来的，而且封顶在容量。"""
    bucket = impl.TokenBucket(60, 60.0, burst=5)
    assert bucket.refill_rate == pytest.approx(1.0)
    for _ in range(5):
        assert bucket.try_acquire(0.0)
    assert not bucket.try_acquire(0.0)
    assert bucket.try_acquire(1.0)          # 1 秒补 1 个令牌
    assert not bucket.try_acquire(1.0)
    for _ in range(5):                      # 闲置很久也只补到容量，不会攒成 3600 个
        assert bucket.try_acquire(3600.0)
    assert not bucket.try_acquire(3600.0)


def test_token_bucket_ignores_a_clock_that_goes_backwards() -> None:
    bucket = impl.TokenBucket(10, 10.0)
    for _ in range(10):
        assert bucket.try_acquire(100.0)
    assert not bucket.try_acquire(99.0)     # 时钟倒退不该凭空造出令牌


def test_sliding_window_log_is_exact_and_its_memory_shrinks() -> None:
    log = impl.SlidingWindowLog(4, 10.0)
    for i in range(4):
        assert log.try_acquire(float(i))
    assert not log.try_acquire(4.0)
    assert log.logged == 4
    assert log.try_acquire(10.5)            # t=0 那条正好滑出窗口
    assert log.logged == 4                  # 旧记录被清掉，内存不随时间累积


def test_sliding_window_counter_errs_strict_not_lax() -> None:
    """近似算法假设上一格均匀分布：流量堆在格子开头时它会提前拒绝，而不是放行超额。"""
    counter = impl.SlidingWindowCounter(10, 10.0)
    for _ in range(10):
        assert counter.try_acquire(0.5)     # 10 次全挤在上一格的开头
    exact = impl.SlidingWindowLog(10, 10.0)
    for _ in range(10):
        exact.try_acquire(0.5)
    assert exact.check(10.6).allowed        # 精确算法知道那 10 次已经滑出窗口
    assert not counter.check(10.6).allowed  # 近似算法仍按 94% 的重叠比例记着它们


def test_swapping_the_algorithm_does_not_touch_the_limiter() -> None:
    """同一个 `RateLimiter` 换一个工厂就换了算法，隔离、加锁、回收的代码一行不改。"""
    clock = FakeClock()
    for factory in (lambda: impl.FixedWindowCounter(2, 10.0),
                    lambda: impl.TokenBucket(2, 10.0),
                    lambda: impl.SlidingWindowLog(2, 10.0),
                    lambda: impl.SlidingWindowCounter(2, 10.0)):
        limiter = impl.RateLimiter(factory, clock=clock)
        assert [bool(limiter.allow("k")) for _ in range(3)] == [True, True, False]


# ---------- 第 3 关：按 key 隔离、状态回收、线程安全 ----------


def test_keys_are_isolated() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.TokenBucket(2, 10.0), clock=clock)
    assert limiter.allow("alice") and limiter.allow("alice")
    assert not limiter.allow("alice")
    assert limiter.allow("bob")             # bob 的额度不受 alice 影响


def test_peek_does_not_consume_and_reset_clears() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.FixedWindowCounter(1, 10.0), clock=clock)
    assert limiter.peek("alice") and limiter.peek("alice")
    assert limiter.allow("alice")
    assert not limiter.peek("alice")
    limiter.reset("alice")
    assert limiter.allow("alice")
    limiter.reset("nobody")                 # 不存在的 key 不报错


def test_sweep_reclaims_only_states_that_are_equivalent_to_new() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.TokenBucket(10, 100.0), clock=clock)  # 每 10 秒补 1 个
    limiter.allow("busy")
    limiter.allow("idle")
    assert limiter.tracked_keys == 2
    assert limiter.sweep() == 0             # 两个 key 都还欠着令牌，一个都不能丢
    clock.advance(5.0)
    limiter.allow("busy")                   # busy 又花掉一个令牌
    clock.advance(10.0)                     # idle 的桶已经补满，busy 的还差半个
    assert limiter.sweep() == 1
    assert limiter.tracked_keys == 1


def test_a_million_keys_do_not_leak() -> None:
    """一百万个只来过一次的 key：占用的内存必须随窗口滑过去而回落，不能单调增长。"""
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.FixedWindowCounter(5, 1.0), clock=clock)
    peak = 0
    for i in range(1_000_000):
        limiter.allow(i)
        clock.advance(1e-4)                 # 每个窗口里大约来一万个不同的 key
        if i % 10_000 == 0:
            peak = max(peak, limiter.tracked_keys)
    assert peak < 25_000                    # 远低于一百万：闲置状态被持续回收
    clock.advance(10.0)
    limiter.sweep()
    assert limiter.tracked_keys == 0


def test_threads_never_oversell_one_key() -> None:
    """200 个线程同时冲同一个 key，限额 50：放行数必须精确等于 50，不多不少。"""
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.TokenBucket(50, 10.0), clock=clock)
    barrier = threading.Barrier(200)
    granted: list[bool] = []
    guard = threading.Lock()

    def worker() -> None:
        barrier.wait()
        decision = limiter.allow("hot")
        with guard:
            granted.append(bool(decision))

    threads = [threading.Thread(target=worker) for _ in range(200)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sum(granted) == 50
    assert len(granted) == 200


def test_threads_on_many_keys_keep_every_budget_separate() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.SlidingWindowLog(10, 10.0), clock=clock, shards=4)
    barrier = threading.Barrier(40)
    results: dict[int, int] = {}
    guard = threading.Lock()

    def worker(key: int) -> None:
        barrier.wait()
        passed = sum(bool(limiter.allow(key)) for _ in range(10))
        with guard:
            results[key] = results.get(key, 0) + passed

    threads = [threading.Thread(target=worker, args=(i % 8,)) for i in range(40)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert set(results) == set(range(8))
    assert all(count == 10 for count in results.values())


# ---------- 第 4 关：组合规则与按次开销 ----------


def test_cost_lets_a_heavy_call_consume_more() -> None:
    clock = FakeClock()
    limiter = impl.RateLimiter(lambda: impl.TokenBucket(10, 10.0), clock=clock)
    assert limiter.allow("alice", cost=7)
    assert not limiter.allow("alice", cost=5)
    assert limiter.allow("alice", cost=3)


def test_composite_denies_if_any_rule_denies() -> None:
    clock = FakeClock()
    per_user = impl.RateLimiter(lambda: impl.TokenBucket(10, 10.0), clock=clock, name="user")
    per_endpoint = impl.RateLimiter(lambda: impl.TokenBucket(2, 10.0), clock=clock, name="endpoint")
    composite = impl.CompositeLimiter([
        impl.Rule("user", per_user, lambda req: req[0]),
        impl.Rule("endpoint", per_endpoint, lambda req: req[1]),
    ], clock=clock)
    assert composite.rule_names == ("user", "endpoint")
    assert composite.allow(("alice", "/search"))
    assert composite.allow(("bob", "/search"))
    denied = composite.allow(("carol", "/search"))
    assert not denied and denied.rule == "endpoint"


def test_composite_does_not_consume_when_a_later_rule_denies() -> None:
    """两阶段判定：被接口规则拒掉的请求，不许扣掉用户自己的额度。"""
    clock = FakeClock()
    per_user = impl.RateLimiter(lambda: impl.TokenBucket(10, 10.0), clock=clock, name="user")
    per_endpoint = impl.RateLimiter(lambda: impl.TokenBucket(1, 10.0), clock=clock, name="endpoint")
    composite = impl.CompositeLimiter([
        impl.Rule("user", per_user, lambda req: req[0]),
        impl.Rule("endpoint", per_endpoint, lambda req: req[1]),
    ], clock=clock)
    assert composite.allow(("alice", "/a"))
    for _ in range(5):
        assert not composite.allow(("alice", "/a"))
    # 换成没被接口规则卡住的路径：alice 还能过 9 次，说明那 5 次拒绝一份额度都没扣。
    assert sum(bool(composite.allow(("alice", f"/b{i}"))) for i in range(12)) == 9


def test_composite_refuses_a_shared_limiter() -> None:
    clock = FakeClock()
    shared = impl.RateLimiter(lambda: impl.TokenBucket(5, 10.0), clock=clock)
    with pytest.raises(impl.InvalidConfiguration):
        impl.CompositeLimiter([impl.Rule("a", shared, lambda r: r),
                               impl.Rule("b", shared, lambda r: r)], clock=clock)
    with pytest.raises(impl.InvalidConfiguration):
        impl.CompositeLimiter([], clock=clock)


@pytest.mark.parametrize("limit,window", [(0, 10.0), (-1, 10.0), (5, 0.0), (5, -1.0)])
def test_invalid_algorithm_configuration_is_rejected(limit: int, window: float) -> None:
    with pytest.raises(impl.InvalidConfiguration):
        impl.TokenBucket(limit, window)
