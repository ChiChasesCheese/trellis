import importlib
import os
import threading

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FakeClock:
    """整数纳秒的假时钟：测试自己决定时间怎么走，不用 sleep。"""

    def __init__(self) -> None:
        self.ns = 0

    def __call__(self) -> int:
        return self.ns

    def advance_ms(self, ms: float) -> None:
        self.ns += round(ms * 1_000_000)


def make(strategy):
    clock = FakeClock()
    return impl.RateLimiter(strategy, clock=clock), clock


def a(limiter, client="alice", endpoint="/v1/chat", limit=2, window_ms=10_000):
    return limiter.check(client, endpoint, limit, window_ms, 0, 0.0)


def b(limiter, client="alice", endpoint="/v1/chat", capacity=3, rate=0.5):
    return limiter.check(client, endpoint, 0, 0, capacity, rate)


# ---- 策略 A ----

def test_a_exact_limit_then_reject_with_exact_resets():
    limiter, clock = make("policy_a")
    assert a(limiter) == (True, 1, 10_000)
    clock.advance_ms(3000)
    assert a(limiter) == (True, 0, 7000)
    clock.advance_ms(500)
    assert a(limiter) == (False, 0, 6500)


def test_a_recovery_after_expiry_counts_only_the_new_request():
    limiter, clock = make("policy_a")
    a(limiter, window_ms=120)
    a(limiter, window_ms=120)
    clock.advance_ms(140)
    assert a(limiter, window_ms=120) == (True, 1, 120)


def test_a_request_exactly_one_window_old_no_longer_counts():
    limiter, clock = make("policy_a")
    a(limiter, limit=1, window_ms=100)
    clock.advance_ms(99)
    assert a(limiter, limit=1, window_ms=100)[0] is False
    clock.advance_ms(1)  # 恰好 100 ms
    assert a(limiter, limit=1, window_ms=100) == (True, 0, 100)


def test_a_rejected_requests_leave_no_trace():
    limiter, clock = make("policy_a")
    a(limiter, limit=1, window_ms=100)
    for _ in range(5):
        clock.advance_ms(10)
        assert a(limiter, limit=1, window_ms=100)[0] is False
    # 若被拒的请求也记了账，最后一次拒绝发生在 t=50，窗口要到 t=150 才空出来
    clock.advance_ms(50)
    assert a(limiter, limit=1, window_ms=100) == (True, 0, 100)


def test_a_reset_truncates_toward_zero():
    limiter, clock = make("policy_a")
    a(limiter, limit=1, window_ms=10)
    clock.ns += 2_500_000  # 2.5 ms
    allowed, remaining, reset = a(limiter, limit=1, window_ms=10)
    assert (allowed, remaining, reset) == (False, 0, 7)  # 7.5 → 7
    assert type(reset) is int


# ---- 策略 B ----

def test_b_initial_burst_then_reject():
    limiter, _ = make("policy_b")
    assert [b(limiter) for _ in range(3)] == [(True, 2, 0), (True, 1, 0), (True, 0, 0)]
    assert b(limiter) == (False, 0, 2000)


def test_b_partial_refill_reports_time_to_one_full_token():
    limiter, clock = make("policy_b")
    for _ in range(3):
        b(limiter, rate=0.25)
    clock.advance_ms(2000)  # 0.25 × 2 s = 0.5 个令牌
    assert b(limiter, rate=0.25) == (False, 0, 2000)  # 还差 0.5，要 2 s


def test_b_fraction_is_kept_between_rejections():
    limiter, clock = make("policy_b")
    for _ in range(3):
        b(limiter, rate=0.25)
    clock.advance_ms(2000)
    assert b(limiter, rate=0.25)[0] is False
    clock.advance_ms(2000)  # 0.5 + 0.5 = 1.0：被拒的那次不能把 0.5 清零或取整
    assert b(limiter, rate=0.25) == (True, 0, 0)


def test_b_budget_never_exceeds_capacity():
    limiter, clock = make("policy_b")
    b(limiter)
    clock.advance_ms(3_600_000)
    assert [b(limiter) for _ in range(3)] == [(True, 2, 0), (True, 1, 0), (True, 0, 0)]
    assert b(limiter)[0] is False


def test_b_remaining_is_whole_tokens_left_after_this_request():
    limiter, clock = make("policy_b")
    for _ in range(3):
        b(limiter)
    clock.advance_ms(3000)  # 1.5 个令牌
    assert b(limiter) == (True, 0, 0)  # 还剩 0.5，向下取整为 0
    assert b(limiter) == (False, 0, 1000)


def test_b_reset_truncates_toward_zero():
    limiter, _ = make("policy_b")
    for _ in range(3):
        b(limiter, rate=3.0)
    assert b(limiter, rate=3.0) == (False, 0, 333)  # 1/3 s = 333.33 ms


def test_b_zero_refill_rate_never_recovers():
    limiter, clock = make("policy_b")
    b(limiter, capacity=1, rate=0.0)
    clock.advance_ms(10_000_000)
    allowed, remaining, reset = b(limiter, capacity=1, rate=0.0)
    assert (allowed, remaining) == (False, 0)
    assert type(reset) is int and reset >= 0


def test_b_clock_running_backwards_never_mints_tokens():
    limiter, clock = make("policy_b")
    clock.advance_ms(5000)
    for _ in range(3):
        b(limiter)
    clock.advance_ms(-4000)
    assert b(limiter)[0] is False


# ---- 两种策略共有 ----

def test_state_is_isolated_per_client_and_endpoint():
    for strategy, call in (("policy_a", lambda lim, **kw: a(lim, limit=1, **kw)),
                           ("policy_b", lambda lim, **kw: b(lim, capacity=1, **kw))):
        limiter, _ = make(strategy)
        assert call(limiter)[0] is True
        assert call(limiter)[0] is False
        assert call(limiter, client="bob")[0] is True
        assert call(limiter, endpoint="/v1/complete")[0] is True


def test_stats_count_decisions_and_keys_for_both_policies():
    for strategy, call in (("policy_a", lambda lim, **kw: a(lim, limit=2, **kw)),
                           ("policy_b", lambda lim, **kw: b(lim, capacity=2, rate=0.0, **kw))):
        limiter, _ = make(strategy)
        assert limiter.stats() == {"strategy": strategy, "total_allowed": 0, "total_rejected": 0, "active_keys": 0}
        for _ in range(3):
            call(limiter)
        call(limiter, client="bob")
        assert limiter.stats() == {"strategy": strategy, "total_allowed": 3, "total_rejected": 1, "active_keys": 2}


def test_stats_returns_a_fresh_dict():
    limiter, _ = make("policy_a")
    a(limiter)
    snapshot = limiter.stats()
    snapshot["total_allowed"] = 999
    assert limiter.stats()["total_allowed"] == 1


def test_unknown_strategy_and_bad_parameters_are_refused_without_a_trace():
    try:
        impl.RateLimiter("policy_c")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    limiter, _ = make("policy_a")
    for bad in ((0, 100), (1, 0)):
        try:
            limiter.check("alice", "/v1/chat", bad[0], bad[1], 0, 0.0)
            raise AssertionError("expected ValueError")
        except ValueError:
            pass
    limiter_b, _ = make("policy_b")
    for bad in ((0, 1.0), (1, -0.5)):
        try:
            limiter_b.check("alice", "/v1/chat", 0, 0, bad[0], bad[1])
            raise AssertionError("expected ValueError")
        except ValueError:
            pass
    assert limiter.stats()["active_keys"] == 0 and limiter_b.stats()["active_keys"] == 0


def test_unused_policy_parameters_may_hold_anything():
    limiter, _ = make("policy_a")
    assert limiter.check("alice", "/v1/chat", 2, 500, -7, float("nan"))[0] is True
    limiter_b, _ = make("policy_b")
    assert limiter_b.check("alice", "/v1/chat", -1, -1, 2, 1.0)[0] is True


def test_default_clock_is_real_and_returns_plain_ints():
    limiter = impl.RateLimiter("policy_a")
    allowed, remaining, reset = limiter.check("alice", "/v1/chat", 1, 60_000, 0, 0.0)
    assert (allowed, remaining) == (True, 0)
    assert type(reset) is int and 59_000 <= reset <= 60_000


def test_idle_keys_are_reclaimed_so_memory_stays_bounded():
    # 每毫秒来一个新 key，窗口 10 ms：任一时刻最多 10 个 key 还有效。
    # 整理在字典长到固定下限（参考实现 4096）时触发，所以 10 万个 key 之后常驻远小于 10 万；
    # 只要下限不超过 10000，就满足下面的上界。
    limiter, clock = make("policy_a")
    for i in range(100_000):
        a(limiter, client=f"c{i}", limit=1, window_ms=10)
        clock.advance_ms(1)
    assert limiter.stats()["active_keys"] <= 10_000


def test_reclaiming_never_changes_a_decision():
    limiter, clock = make("policy_b")
    for i in range(20_000):
        b(limiter, client=f"c{i}", capacity=1, rate=1000.0)
        clock.advance_ms(1)
    # c0 的桶早已补满；不管它是否被整理掉，结果都必须和全新的 key 一样
    assert b(limiter, client="c0", capacity=1, rate=1000.0) == (True, 0, 0)


# ---- 并发（真线程 + 屏障；断言不变量，不断言时序）----

def hammer(limiter, call, threads=200):
    barrier = threading.Barrier(threads)
    results = []

    def worker():
        barrier.wait()
        results.append(call(limiter))

    pool = [threading.Thread(target=worker) for _ in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    return results


def test_concurrent_checks_never_oversell_policy_a():
    limiter, _ = make("policy_a")
    results = hammer(limiter, lambda lim: a(lim, limit=50, window_ms=60_000))
    assert sum(1 for r in results if r[0]) == 50
    assert limiter.stats() == {"strategy": "policy_a", "total_allowed": 50, "total_rejected": 150, "active_keys": 1}


def test_concurrent_checks_never_oversell_policy_b():
    limiter, _ = make("policy_b")
    results = hammer(limiter, lambda lim: b(lim, capacity=50, rate=0.0))
    assert sum(1 for r in results if r[0]) == 50
    assert sorted(r[1] for r in results if r[0]) == list(range(50))  # 剩余额度 49…0 各出现一次


def test_stats_snapshots_stay_consistent_while_checks_run():
    limiter, _ = make("policy_a")
    stop = threading.Event()
    seen = []

    def reader():
        while not stop.wait(0.0002):
            s = limiter.stats()
            seen.append((s["total_allowed"], s["total_rejected"]))

    t = threading.Thread(target=reader)
    t.start()
    hammer(limiter, lambda lim: a(lim, limit=50, window_ms=60_000))
    stop.set()
    t.join()
    assert all(allowed <= 50 for allowed, _ in seen)
    assert all(allowed + rejected <= 200 for allowed, rejected in seen)
    assert limiter.stats()["total_allowed"] + limiter.stats()["total_rejected"] == 200


def test_reclaiming_judges_each_key_by_its_own_parameters():
    # 一个长窗口的 key 被别的 key 用短窗口参数触发整理时，不能被当成闲置删掉，否则它的额度会被清零
    limiter, clock = make("policy_a")
    assert a(limiter, client="long", limit=1, window_ms=60_000)[0] is True
    for i in range(5_000):
        a(limiter, client=f"c{i}", limit=1, window_ms=1)
        clock.advance_ms(2)
    assert a(limiter, client="long", limit=1, window_ms=60_000)[0] is False
