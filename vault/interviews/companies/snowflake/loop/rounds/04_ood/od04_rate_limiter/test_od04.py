import random
import threading

import pytest

EX1_TIMES = [1, 2, 3, 4, 7]
EX1_OUT = [True, True, True, False, True]

EX2_REQUESTS = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
EX2_RULES = [(2, 5)]
EX2_OUT = [0, 1, 5, 6, 10]

EX3_REQUESTS = [(0, 1), (1, 0), (2, 1)]
EX3_RULES = [(1, 5)]
EX3_OUT = [0, 5, 5]


# ------------------------------------------------------------------ Part 1: sliding window
@pytest.mark.part1
def test_worked_example_1_accept_requests(impl):
    assert impl.accept_requests(EX1_TIMES, limit=3, window_seconds=5) == EX1_OUT


@pytest.mark.part1
def test_worked_example_1_via_streaming_class(impl):
    limiter = impl.RateLimiter(limit=3, window_seconds=5)
    assert [limiter.allow(t) for t in EX1_TIMES] == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_rejected_request_never_occupies_a_slot(impl):
    limiter = impl.RateLimiter(limit=1, window_seconds=10)
    assert limiter.allow(0) is True
    assert limiter.allow(1) is False  # rejected -- must not occupy the one slot
    assert limiter.allow(2) is False  # still rejected: slot 0 hasn't aged out yet
    assert limiter.allow(10) is True  # (10-10, 10] excludes t=0 exactly


@pytest.mark.part1
@pytest.mark.edge
def test_window_boundary_is_half_open(impl):
    limiter = impl.RateLimiter(limit=1, window_seconds=5)
    assert limiter.allow(0) is True
    assert limiter.allow(4) is False  # 0 > 4-5=-1 -> still inside
    assert limiter.allow(5) is True  # 0 > 5-5=0 is False -> aged out exactly at the boundary


@pytest.mark.part1
@pytest.mark.edge
def test_limit_zero_always_rejects(impl):
    limiter = impl.RateLimiter(limit=0, window_seconds=100)
    assert limiter.allow(0) is False
    assert limiter.allow(1) is False


@pytest.mark.part1
@pytest.mark.edge
def test_empty_request_list(impl):
    assert impl.accept_requests([], limit=5, window_seconds=10) == []


# ------------------------------------------------------------------ Part 2: multi-rule FIFO simulation
@pytest.mark.part2
def test_worked_example_2(impl):
    assert impl.simulate_rate_limiter(EX2_REQUESTS, EX2_RULES) == EX2_OUT


@pytest.mark.part2
def test_worked_example_3_failed_waits_but_does_not_consume(impl):
    assert impl.simulate_rate_limiter(EX3_REQUESTS, EX3_RULES) == EX3_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_empty_requests(impl):
    assert impl.simulate_rate_limiter([], [(1, 5)]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_bottleneck_rule_dominates_result(impl):
    # a very permissive second rule must not change the result vs. the single-rule case
    requests = EX2_REQUESTS
    rules_with_slack = [(2, 5), (1000, 1)]
    assert impl.simulate_rate_limiter(requests, rules_with_slack) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_fifo_order_never_lets_a_later_arrival_jump_ahead(impl):
    # second request arrives later but its own rule would be satisfied immediately; it must
    # still not start before the first request's start time
    requests = [(0, 1), (0, 1)]
    rules = [(1, 100)]
    starts = impl.simulate_rate_limiter(requests, rules)
    assert starts[0] <= starts[1]
    assert starts == [0, 100]


# ------------------------------------------------------------------ Part 3: thread-safe try_acquire
@pytest.mark.part3
def test_try_acquire_matches_simulate_single_threaded(impl):
    limiter = impl.MultiRuleRateLimiter(EX2_RULES)
    starts = [limiter.try_acquire(arrival) for arrival, _flag in EX2_REQUESTS]
    assert starts == EX2_OUT


@pytest.mark.part3
def test_concurrent_try_acquire_never_exceeds_limit_in_any_window(impl):
    limit, window = 3, 10
    limiter = impl.MultiRuleRateLimiter([(limit, window)])
    n_threads, n_per_thread = 12, 15
    granted: list[int] = []
    lock = threading.Lock()

    def worker(base: int):
        rng = random.Random(base)
        for _ in range(n_per_thread):
            arrival = base + rng.randrange(0, 5)
            t = limiter.try_acquire(arrival)
            with lock:
                granted.append(t)

    threads = [threading.Thread(target=worker, args=(i * 3,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert len(granted) == n_threads * n_per_thread
    granted.sort()
    # invariant: in ANY window of `window` consecutive time units, at most `limit` grants
    for i in range(len(granted)):
        count = sum(1 for g in granted if granted[i] - window < g <= granted[i])
        assert count <= limit, f"window ending at {granted[i]} has {count} grants (> {limit})"


@pytest.mark.part3
@pytest.mark.edge
def test_concurrent_try_acquire_loses_no_calls(impl):
    limiter = impl.MultiRuleRateLimiter([(5, 3)])
    n = 100
    results: list[int] = []
    lock = threading.Lock()

    def worker(i: int):
        t = limiter.try_acquire(0)
        with lock:
            results.append(t)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)
    assert len(results) == n  # every call returned, none lost/deadlocked


# ------------------------------------------------------------------ fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_output_strings_exact(impl):
    out = impl.part1(["LIMIT 1", "WINDOW 5", "0", "1"])
    assert out == ["True", "False"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["RULES 2:5"] + [f"{t}:{f}" for t, f in EX2_REQUESTS]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(str(x) for x in EX2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["LIMIT 3", "WINDOW 5"] + [str(t) for t in EX1_TIMES]
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(str(x) for x in EX1_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_requests_single_rule(run_script):
    rng = random.Random(0)
    body = ["RULES 100:60"]
    t = 0
    for _ in range(100_000):
        t += rng.randrange(0, 2)
        flag = 1 if rng.random() < 0.8 else 0
        body.append(f"{t}:{flag}")
    result = run_script("PART 2\n" + "\n".join(body) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 100_000
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
