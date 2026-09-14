import random

import pytest

A, D = "ALLOW", "DENY"


def run(impl, part, lines):
    return impl.process(lines, part)


# ---------------------------------------------------------------- Part 1: global sliding window
@pytest.mark.part1
def test_example_global_window(impl):
    out = run(impl, 1, ["LIMIT 5 2000"] + [str(t) for t in (0, 1, 2, 3, 4, 5, 1999, 2000, 2001, 2002)])
    assert out == [A, A, A, A, A, D, D, A, A, A]


@pytest.mark.part1
@pytest.mark.edge
def test_window_boundary_left_open_right_closed(impl):
    w = impl.SlidingWindow(1, 1000)
    assert w.allow(0) is True
    assert w.allow(999) is False   # 0 is inside (-1, 999]
    assert w.allow(1000) is True   # 0 is NOT inside (0, 1000]
    assert w.allow(1000) is False  # same timestamp, second request
    assert w.allow(2000) is True


@pytest.mark.part1
@pytest.mark.edge
def test_denied_requests_are_not_recorded(impl):
    w = impl.SlidingWindow(2, 100)
    assert [w.allow(t) for t in (0, 0, 50, 60, 70)] == [A == A, True, False, False, False]
    # the denials at 50/60/70 must not extend the lockout: at 100 the window (0,100] is empty
    assert w.allow(100) is True
    assert w.allow(100) is True
    assert w.allow(100) is False


@pytest.mark.part1
@pytest.mark.edge
def test_limit_one_and_zero_and_same_timestamp_burst(impl):
    w = impl.SlidingWindow(3, 10)
    assert [w.allow(5) for _ in range(5)] == [True, True, True, False, False]
    assert impl.SlidingWindow(0, 10).allow(0) is False
    assert run(impl, 1, ["LIMIT 5 2000"]) == []  # no requests
    # default config when the LIMIT header is absent: 5 per 2000 ms
    assert run(impl, 1, ["0", "0", "0", "0", "0", "0"]) == [A, A, A, A, A, D]


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_order_timestamp_rejected(impl):
    w = impl.SlidingWindow(5, 2000)
    assert w.allow(10) is True
    with pytest.raises(ValueError, match="out-of-order"):
        w.allow(9)
    assert w.allow(10) is True  # equal timestamp is fine
    assert run(impl, 1, ["LIMIT 5 2000", "10", "9", "10"]) == [A, "ERROR", A]


# ---------------------------------------------------------------- Part 2: per client
@pytest.mark.part2
def test_example_per_client(impl):
    out = run(impl, 2, ["LIMIT 2 1000", "0 a", "0 b", "1 a", "2 a", "2 b", "1000 a", "1001 a"])
    assert out == [A, A, A, D, A, A, A]


@pytest.mark.part2
@pytest.mark.edge
def test_clients_are_independent_and_many_small_clients(impl):
    rl = impl.RateLimiter(5, 2000)
    assert all(rl.allow("big", 0) for _ in range(5))
    assert rl.allow("big", 1) is False
    # 1000 other clients each make 5 requests inside the same window: all allowed
    assert all(rl.allow(f"c{i}", 1) for i in range(1000) for _ in range(5))
    assert rl.allow("c7", 2) is False
    assert rl.allow("big", 2000) is True


@pytest.mark.part2
@pytest.mark.edge
def test_part1_stdin_ignores_client_but_part2_keys_on_it(impl):
    lines = ["LIMIT 1 1000", "0 a", "0 b"]
    assert run(impl, 1, lines) == [A, D]
    assert run(impl, 2, lines) == [A, A]
    # out-of-order is per client: b at 5 after a at 10 is fine, a at 9 is not
    assert run(impl, 2, ["LIMIT 5 1000", "10 a", "5 b", "9 a"]) == [A, A, "ERROR"]


@pytest.mark.part2
@pytest.mark.edge
def test_rate_limiter_cleanup(impl):
    rl = impl.RateLimiter(5, 2000)
    rl.allow("a", 0)
    rl.allow("b", 5000)
    rl.allow("c", 9000)
    # at 10000 with idle 5000: a (last 0) and b (last 5000) are idle >= 5000 -> evicted; c is not
    assert rl.cleanup(10_000, 5000) == 2
    assert set(rl.windows) == {"c"}
    # a client whose window still holds events is never evicted
    rl.allow("d", 10_000)
    # c (last 9000) is idle and its window (9000,11000] is empty -> evicted;
    # d: last 10000 <= 10000 counts as idle, but its window (9000,11000] still holds the event
    assert rl.cleanup(11_000, 1000) == 1
    assert set(rl.windows) == {"d"}
    assert rl.cleanup(12_000, 1000) == 1  # now (10000,12000] is empty -> evicted


# ---------------------------------------------------------------- Part 3: weights
@pytest.mark.part3
def test_example_weighted(impl):
    out = run(impl, 3, ["LIMIT 5 2000", "0 a 3", "1 a 2", "2 a 1", "3 a 6", "2000 a 3", "2001 a 3"])
    assert out == [A, A, D, D, A, D]


@pytest.mark.part3
@pytest.mark.edge
def test_weight_boundary_exact_fill(impl):
    rl = impl.RateLimiter(10, 1000)
    assert rl.allow("a", 0, 4) is True
    assert rl.allow("a", 1, 6) is True    # 4 + 6 == 10 -> allowed (non-strict)
    assert rl.allow("a", 2, 1) is False   # 11 > 10
    assert rl.allow("a", 1000, 4) is True  # 4 at t=0 left the window; 6 + 4 == 10
    assert rl.allow("a", 1001, 1) is True  # 6 left: 4 + 1
    with pytest.raises(ValueError):
        rl.allow("a", 1001, 0)
    with pytest.raises(ValueError):
        rl.allow("a", 1001, -2)


@pytest.mark.part3
@pytest.mark.edge
def test_overweight_request_never_recorded_and_parts_1_2_ignore_weight_column(impl):
    rl = impl.RateLimiter(5, 1000)
    assert rl.allow("a", 0, 6) is False
    assert rl.allow("a", 0, 5) is True  # the denied 6 did not consume anything
    # Parts 1-2 read `ts client weight` lines but treat every request as weight 1
    assert run(impl, 2, ["LIMIT 5 1000", "0 a 5", "1 a 5"]) == [A, A]
    assert run(impl, 3, ["LIMIT 5 1000", "0 a 5", "1 a 5"]) == [A, D]


# ---------------------------------------------------------------- Part 4: token bucket
@pytest.mark.part4
def test_example_token_bucket(impl):
    out = run(impl, 4, ["BUCKET 5 2"] + ["0 a"] * 6 + ["500 a", "600 a", "5000 a", "CLEANUP 20000 10000", "20000 a"])
    assert out == [A, A, A, A, A, D, A, D, A, "EVICTED 1", A]


@pytest.mark.part4
@pytest.mark.edge
def test_fractional_refill_accumulates_exactly(impl):
    tb = impl.TokenBucket(5, 2)
    assert all(tb.allow("a", 0) for _ in range(5))
    assert tb.allow("a", 100) is False   # 0.2 tokens
    assert tb.allow("a", 200) is False   # 0.4
    assert tb.allow("a", 499) is False   # 0.998
    assert tb.allow("a", 500) is True    # 1.0 exactly -> allowed, now 0
    assert tb.allow("a", 1100) is True   # +1.2 -> 1.2 -> allowed, 0.2 left
    assert tb.allow("a", 1500) is True   # +0.8 -> 1.0
    assert tb.allow("a", 1500) is False


@pytest.mark.part4
@pytest.mark.edge
def test_bucket_cap_cost_and_new_client_full(impl):
    tb = impl.TokenBucket(3, 1)
    assert tb.allow("a", 0, 3) is True       # new client starts full; cost 3 drains it
    assert tb.allow("a", 86_400_000, 4) is False  # a day later: capped at 3, cost 4 too big
    assert tb.allow("a", 86_400_000, 3) is True
    assert tb.allow("a", 86_400_000, 1) is False
    with pytest.raises(ValueError, match="out-of-order"):
        tb.allow("a", 1)
    assert tb.allow("b", 1, 1) is True       # other clients unaffected
    with pytest.raises(ValueError):
        tb.allow("b", 1, 0)


@pytest.mark.part4
@pytest.mark.edge
def test_cleanup_boundary_and_return_count(impl):
    tb = impl.TokenBucket(5, 2)
    tb.allow("a", 0)
    tb.allow("b", 1000)
    tb.allow("c", 1001)
    assert tb.cleanup(6000, 5000) == 2       # a (idle 6000) and b (idle exactly 5000) evicted; c idle 4999 stays
    assert set(tb.buckets) == {"c"}
    assert tb.cleanup(6000, 5000) == 0
    assert tb.allow("a", 6000, 5) is True    # comes back with a full bucket
    assert run(impl, 4, ["BUCKET 5 2", "0 a", "CLEANUP 0 0"]) == [A, "EVICTED 1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 4\nBUCKET 5 2\n" + "0 a\n" * 6 + "500 a\n600 a\n5000 a\nCLEANUP 20000 10000\n20000 a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ALLOW\n" * 5 + "DENY\nALLOW\nDENY\nALLOW\nEVICTED 1\nALLOW\n"
    r = run_script("PART 3\nLIMIT 5 2000\n0 a 3\n1 a 2\n2 a 1\n3 a 6\n2000 a 3\n2001 a 3\n")
    assert r.stdout == "ALLOW\nALLOW\nDENY\nDENY\nALLOW\nDENY\n"
    r = run_script("PART 1\nLIMIT 5 2000\n10\n9\n")
    assert r.stdout == "ALLOW\nERROR\n"
    assert run_script("").stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_one_million_requests(run_script):
    rng = random.Random(0)
    lines = ["PART 3", "LIMIT 5 2000"]
    t = 0
    for _ in range(1_000_000):
        t += rng.randrange(0, 3)
        lines.append(f"{t} c{rng.randrange(2000)} {rng.randrange(1, 4)}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 1_000_000 and "ERROR" not in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
