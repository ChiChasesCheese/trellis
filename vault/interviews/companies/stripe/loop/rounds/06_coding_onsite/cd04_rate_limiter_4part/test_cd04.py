import random
import threading

import pytest


# ---------------------------------------------------------------- Part 1: the basics
@pytest.mark.part1
def test_worked_example_basics(impl):
    rl = impl.RateLimiter(limit=3, window_s=1)
    assert rl.allow("u", 0) is True
    assert rl.allow("u", 100) is True
    assert rl.allow("u", 200) is True
    assert rl.allow("u", 300) is False  # (-700, 300] holds 0,100,200 -> at limit
    assert rl.allow("u", 1000) is True  # (0, 1000] excludes t=0 (left-open) -> count 2


@pytest.mark.part1
@pytest.mark.edge
def test_window_boundary_exclusive_start_inclusive_end(impl):
    rl = impl.RateLimiter(limit=1, window_s=1)  # window_ms = 1000
    assert rl.allow("u", 0) is True
    assert rl.allow("u", 999) is False  # (-1, 999] still holds t=0
    assert rl.allow("u", 1000) is True  # (0, 1000] excludes t=0 exactly at the boundary


@pytest.mark.part1
@pytest.mark.edge
def test_denied_requests_are_never_recorded(impl):
    rl = impl.RateLimiter(limit=2, window_s=1)
    assert rl.allow("u", 0) is True
    assert rl.allow("u", 0) is True
    for _ in range(20):
        assert rl.allow("u", 0) is False  # a long burst of denials
    assert rl.allow("u", 1000) is True  # denials never extended the window/lockout


@pytest.mark.part1
def test_clients_are_independent(impl):
    rl = impl.RateLimiter(limit=1, window_s=1)
    assert rl.allow("a", 0) is True
    assert rl.allow("a", 0) is False
    assert rl.allow("b", 0) is True  # b has its own independent budget


# ---------------------------------------------------------------- Part 2: saving memory
@pytest.mark.part2
@pytest.mark.edge
def test_log_size_never_exceeds_limit(impl):
    rl = impl.RateLimiter(limit=5, window_s=1)
    for t in range(0, 2000, 10):  # 200 calls, far more than `limit`
        rl.allow("u", t)
    assert rl.log_size("u") <= 5


@pytest.mark.part2
def test_evict_idle_boundary_and_count(impl):
    rl = impl.RateLimiter(limit=2, window_s=60)  # window_ms = 60000
    assert rl.evict_idle(0) == 0
    assert rl.allow("a", 0) is True
    assert rl.allow("b", 0) is True
    assert rl.evict_idle(59999) == 0  # both still inside (0, 59999]
    assert rl.evict_idle(60000) == 2  # (0, 60000] excludes t=0 -> both idle


@pytest.mark.part2
@pytest.mark.edge
def test_evicted_client_gets_a_fresh_budget(impl):
    rl = impl.RateLimiter(limit=1, window_s=60)
    assert rl.allow("a", 0) is True
    assert rl.allow("a", 0) is False  # budget exhausted
    assert rl.evict_idle(60000) == 1  # a is idle by t=60000, gets dropped
    assert rl.log_size("a") == 0
    assert rl.allow("a", 60000) is True  # fresh budget, not "remembered" as exhausted


@pytest.mark.part2
@pytest.mark.edge
def test_evict_idle_ignores_active_clients(impl):
    rl = impl.RateLimiter(limit=3, window_s=60)
    assert rl.allow("a", 0) is True
    assert rl.allow("a", 30000) is True  # still active at t=60000's window
    assert rl.evict_idle(60000) == 0
    assert rl.log_size("a") == 1  # only the t=0 entry was trimmed away


# ---------------------------------------------------------------- Part 3: tricky situations
@pytest.mark.part3
@pytest.mark.edge
def test_clock_rollback_is_clamped_not_rejected(impl):
    rl = impl.RateLimiter(limit=1, window_s=1)
    assert rl.allow("c", 500) is True
    assert rl.allow("c", 300) is False  # clamped to 500 -> window (-500,500] at limit
    assert rl.allow("c", 1500) is True  # (500, 1500] excludes t=500 -> fresh capacity


@pytest.mark.part3
@pytest.mark.edge
def test_clock_rollback_is_per_client(impl):
    rl = impl.RateLimiter(limit=1, window_s=1)
    assert rl.allow("a", 500) is True
    assert rl.allow("a", 100) is False  # a clamped, denied
    assert rl.allow("b", 100) is True  # b's clock is untouched by a's rollback


@pytest.mark.part3
@pytest.mark.edge
def test_limit_zero_always_denies(impl):
    rl = impl.RateLimiter(limit=0, window_s=60)
    assert rl.allow("a", 0) is False
    assert rl.allow("a", 100) is False
    assert rl.allow("", 999999) is False


@pytest.mark.part3
@pytest.mark.edge
def test_burst_at_identical_timestamp_exact_count(impl):
    rl = impl.RateLimiter(limit=4, window_s=1)
    results = [rl.allow("u", 0) for _ in range(10)]
    assert results == [True, True, True, True, False, False, False, False, False, False]


@pytest.mark.part3
@pytest.mark.edge
def test_empty_client_id_is_a_valid_independent_client(impl):
    rl = impl.RateLimiter(limit=1, window_s=1)
    assert rl.allow("", 0) is True
    assert rl.allow("", 0) is False
    assert rl.allow("nonempty", 0) is True  # "" and a real id don't collide


@pytest.mark.part3
@pytest.mark.edge
def test_very_large_timestamp_does_not_crash(impl):
    rl = impl.RateLimiter(limit=2, window_s=1)
    big = 10**15
    assert rl.allow("u", big) is True
    assert rl.allow("u", big + 500) is True
    assert rl.allow("u", big + 999) is False
    assert rl.allow("u", big + 1000) is True


# ---------------------------------------------------------------- Part 4: multiple threads
@pytest.mark.part4
def test_concurrent_allow_yields_exact_count(impl):
    rl = impl.RateLimiter(limit=100, window_s=1)
    per_thread: list[int] = []
    lock = threading.Lock()

    def worker() -> None:
        allowed = sum(1 for _ in range(1000) if rl.allow("shared", 0))
        with lock:
            per_thread.append(allowed)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert sum(per_thread) == 100  # exact, not "approximately"


@pytest.mark.part4
def test_concurrent_allow_different_clients_independent(impl):
    rl = impl.RateLimiter(limit=50, window_s=1)
    totals: dict[str, int] = {"a": 0, "b": 0}
    lock = threading.Lock()

    def worker(client_id: str) -> None:
        allowed = sum(1 for _ in range(500) if rl.allow(client_id, 0))
        with lock:
            totals[client_id] += allowed

    threads = [threading.Thread(target=worker, args=(cid,)) for cid in ("a", "b") for _ in range(4)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert totals["a"] == 50
    assert totals["b"] == 50


@pytest.mark.part4
@pytest.mark.edge
def test_concurrent_allow_and_evict_idle_do_not_corrupt_state(impl):
    rl = impl.RateLimiter(limit=10, window_s=1)

    def allower() -> None:
        for t in range(0, 2000, 2):
            rl.allow("u", t)

    def evictor() -> None:
        for now in range(0, 2000, 3):
            rl.evict_idle(now)

    threads = [threading.Thread(target=allower), threading.Thread(target=evictor)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    # no crash, and the log never exceeds the documented O(limit) bound afterwards
    assert rl.log_size("u") <= 10


# ---------------------------------------------------------------- fmt / io / perf
@pytest.mark.part3
@pytest.mark.fmt
def test_command_stream_output_strings_exact(impl):
    out = impl.run_commands(
        [
            "LIMIT 2 1",
            "ALLOW u 0",
            "ALLOW u 0",
            "ALLOW u 0",
            "CLEANUP 1000",
            "ALLOW x oops",
            "FROB x",
        ]
    )
    assert out == ["ALLOW", "ALLOW", "DENY", "EVICTED 1", "ERROR", "ERROR"]


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    stdin = "LIMIT 3 1\n" + "\n".join(f"ALLOW u {t}" for t in (0, 100, 200, 300, 1000)) + "\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ALLOW\nALLOW\nALLOW\nDENY\nALLOW\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_sequential_allow_calls(run_script):
    rng = random.Random(0)
    n_clients = 2000
    lines = ["LIMIT 20 60"]
    t = 0
    for _ in range(100_000):
        t += rng.randrange(0, 5)
        lines.append(f"ALLOW client_{rng.randrange(n_clients)} {t}")
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 100_000
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
