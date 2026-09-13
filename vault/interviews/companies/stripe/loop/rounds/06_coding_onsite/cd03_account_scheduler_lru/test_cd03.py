import random

import pytest

EX1 = [
    "ACCOUNTS a b",
    "AVAIL a 0",
    "ACQ a 0 10",
    "AVAIL a 9",
    "AVAIL a 10",
    "ACQ a 5 5",
    "ANY 5 10",
    "ANY 5 10",
    "ANY 15 5",
    "ACQ b 16 100",
    "AVAIL b 17",
    "ANY 20 1",
]
EX1_OUT = ["true", "true", "false", "true", "false", "b", "none", "a", "true", "false", "a"]

EX2 = [
    "ACCOUNTS c b a",
    "ANY 0 1",
    "ANY 0 1",
    "ANY 0 1",
    "ANY 0 1",
    "ANY 1 1",
    "ACQ a 1 1",
    "ANY 2 1",
]
EX2_OUT = ["c", "b", "a", "none", "c", "true", "b"]

EX3 = ["ACCOUNTS x", "ACQ x 0 0", "AVAIL y 0", "ACQ x ten 5", "FROB x"]
EX3_OUT = ["ERROR", "ERROR", "ERROR", "ERROR"]


# ---------------------------------------------------------------- Part 1: registry / availability
@pytest.mark.part1
def test_available_when_never_locked_any_t(impl):
    s = impl.AccountScheduler(["a", "b"])
    assert s.is_available("a", 0) is True
    assert s.is_available("a", -100) is True  # no lock ever taken -> free at every t, even negative


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_account_raises_keyerror(impl):
    s = impl.AccountScheduler(["a"])
    with pytest.raises(KeyError):
        s.is_available("ghost", 0)


@pytest.mark.part1
@pytest.mark.edge
def test_lock_end_is_exclusive(impl):
    s = impl.AccountScheduler(["a"])
    assert s.acquire("a", 100, 10) is True  # locks [100, 110)
    assert s.is_available("a", 100) is False
    assert s.is_available("a", 109) is False  # one below the end
    assert s.is_available("a", 110) is True  # == end -> free
    assert s.is_available("a", 111) is True


# ---------------------------------------------------------------- Part 2: acquire (timed lock)
@pytest.mark.part2
def test_acquire_success_then_blocked(impl):
    s = impl.AccountScheduler(["a"])
    assert s.acquire("a", 0, 10) is True
    assert s.acquire("a", 5, 5) is False  # still locked at t=5
    assert s.acquire("a", 10, 1) is True  # re-lock exactly at expiry


@pytest.mark.part2
@pytest.mark.edge
def test_duration_zero_or_negative_raises_valueerror(impl):
    s = impl.AccountScheduler(["a"])
    with pytest.raises(ValueError):
        s.acquire("a", 0, 0)
    with pytest.raises(ValueError):
        s.acquire("a", 0, -3)
    assert s.is_available("a", 0) is True  # rejected before touching state


@pytest.mark.part2
@pytest.mark.edge
def test_acquire_unknown_id_raises_keyerror(impl):
    s = impl.AccountScheduler(["a"])
    with pytest.raises(KeyError):
        s.acquire("ghost", 0, 5)


@pytest.mark.part2
def test_duration_checked_before_unknown_id(impl):
    # both are "wrong" -> duration (ValueError) wins per the documented check order
    s = impl.AccountScheduler(["a"])
    with pytest.raises(ValueError):
        s.acquire("ghost", 0, 0)


# ---------------------------------------------------------------- Part 3: acquire_any (LRU)
@pytest.mark.part3
def test_worked_example_1(impl):
    assert impl.run_commands(EX1) == EX1_OUT


@pytest.mark.part3
def test_worked_example_2_construction_order(impl):
    assert impl.run_commands(EX2) == EX2_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_never_used_first_then_construction_order(impl):
    s = impl.AccountScheduler(["z", "a", "m"])  # NOT alphabetical -> id order would fail this test
    assert s.acquire_any(0, 1) == "z"
    assert s.acquire_any(0, 1) == "a"
    assert s.acquire_any(0, 1) == "m"
    assert s.acquire_any(0, 1) is None


@pytest.mark.part3
@pytest.mark.edge
def test_lru_oldest_last_used_wins_over_construction_order(impl):
    s = impl.AccountScheduler(["a", "b"])
    assert s.acquire("b", 0, 1) is True  # b used at t=0, free again at t=1
    assert s.acquire_any(1, 1) == "a"  # a never used -> ranked ahead of used b
    # now both used: a last_used=1, b last_used=0 -> b is older despite coming later in construction order
    assert s.acquire_any(2, 1) == "b"


@pytest.mark.part3
@pytest.mark.edge
def test_failed_acquire_and_plain_queries_do_not_touch_last_used(impl):
    s = impl.AccountScheduler(["a", "b"])
    assert s.acquire("a", 0, 10) is True
    assert s.acquire("b", 1, 10) is True
    assert s.acquire("a", 5, 5) is False  # fails: still locked; must not update last_used
    s.is_available("b", 100)  # plain query: no side effect
    assert s.acquire_any(100, 1) == "a"  # a (last_used=0) still older than b (last_used=1)


@pytest.mark.part3
@pytest.mark.edge
def test_acquire_any_duration_invalid_raises(impl):
    s = impl.AccountScheduler(["a"])
    with pytest.raises(ValueError):
        s.acquire_any(0, 0)


@pytest.mark.part3
def test_acquire_any_empty_pool_returns_none(impl):
    s = impl.AccountScheduler([])
    assert s.acquire_any(0, 1) is None


# ---------------------------------------------------------------- fmt / io / perf
@pytest.mark.part3
@pytest.mark.fmt
def test_command_stream_output_strings_exact(impl):
    assert impl.run_commands(EX3) == EX3_OUT
    out = impl.run_commands(["ACCOUNTS a", "AVAIL a 0", "ACQ a 0 1", "ANY 5 1"])
    assert out == ["true", "true", "a"]  # lowercase true/false, bare id, no extra text


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_commands(run_script):
    # acquire_any is documented as O(pool size) per call (see REPORT.md); keep the pool at 500
    # accounts and ANY at 10% of traffic so the perf budget exercises realistic mixed traffic
    # rather than a worst-case O(n) stress test of a follow-up optimization the problem doesn't
    # require at this scale.
    rng = random.Random(0)
    n_acc = 500
    lines = ["ACCOUNTS " + " ".join(f"acct_{i}" for i in range(n_acc))]
    t = 0
    for _ in range(100_000):
        t += rng.randrange(0, 3)
        r = rng.random()
        aid = f"acct_{rng.randrange(n_acc)}"
        if r < 0.5:
            lines.append(f"AVAIL {aid} {t}")
        elif r < 0.9:
            lines.append(f"ACQ {aid} {t} {rng.randrange(1, 20)}")
        else:
            lines.append(f"ANY {t} {rng.randrange(1, 20)}")
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 100_000
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
