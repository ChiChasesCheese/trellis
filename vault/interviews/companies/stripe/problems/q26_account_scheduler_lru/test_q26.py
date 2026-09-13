import random

import pytest

EX1 = ["ADD a", "ADD b", "ADD a", "AVAILABLE a 0", "ACQUIRE a 10 0", "AVAILABLE a 9", "AVAILABLE a 10",
       "ACQUIRE a 5 5", "ACQUIRE_ANY 10 5", "ACQUIRE_ANY 10 5", "ACQUIRE_ANY 5 15", "ACQUIRE b 100 16",
       "RELEASE b", "AVAILABLE b 17", "ACQUIRE_ANY 1 20"]
EX1_OUT = ["OK", "OK", "EXISTS", "true", "true", "false", "true", "false", "b", "NONE", "a", "true",
           "OK", "true", "a"]
EX2 = ["ADD c", "ADD b", "ADD a", "ACQUIRE_ANY 1 0", "ACQUIRE_ANY 1 0", "ACQUIRE_ANY 1 0", "ACQUIRE_ANY 1 0",
       "ACQUIRE_ANY 1 1", "ACQUIRE c 1 1", "ACQUIRE_ANY 1 2"]
EX2_OUT = ["OK", "OK", "OK", "a", "b", "c", "NONE", "a", "true", "b"]
EX3 = ["ADD x", "ADD y", "ACQUIRE x 100 0", "ACQUIRE y 100 0", "ACQUIRE_ANY 1 50", "RELEASE y",
       "ACQUIRE_ANY 1 50", "AVAILABLE y 50", "AVAILABLE y 51", "RELEASE nope", "ACQUIRE x 0 200",
       "ACQUIRE x ten 200", "FROB x"]
EX3_OUT = ["OK", "OK", "true", "true", "NONE", "OK", "y", "false", "true", "UNKNOWN", "false", "ERROR", "ERROR"]


# ---------------------------------------------------------------- Part 1: class basics
@pytest.mark.part1
def test_add_available_and_unknown(impl):
    s = impl.AccountScheduler()
    assert s.add_account("a") is True
    assert s.add_account("a") is False
    assert s.is_available("a", 0) is True
    assert s.is_available("a", -5) is True
    assert s.is_available("ghost", 0) is False
    assert s.acquire("ghost", 5, 0) is False


@pytest.mark.part1
@pytest.mark.edge
def test_lock_end_exclusive_boundaries(impl):
    s = impl.AccountScheduler()
    s.add_account("a")
    assert s.acquire("a", 10, 100) is True
    assert s.is_available("a", 100) is False
    assert s.is_available("a", 109) is False   # one below the end
    assert s.is_available("a", 110) is True    # == end -> free
    assert s.is_available("a", 111) is True
    assert s.acquire("a", 1, 109) is False
    assert s.acquire("a", 1, 110) is True      # re-lock exactly at expiry


@pytest.mark.part1
@pytest.mark.edge
def test_duration_zero_or_negative_rejected(impl):
    s = impl.AccountScheduler()
    s.add_account("a")
    assert s.acquire("a", 0, 5) is False
    assert s.acquire("a", -3, 5) is False
    assert s.is_available("a", 5) is True
    assert s.acquire_any(0, 5) is None


@pytest.mark.part1
def test_part1_stream_rejects_later_commands(impl):
    assert impl.part1(["ADD a", "ACQUIRE a 3 1", "AVAILABLE a 3", "AVAILABLE a 4", "ACQUIRE_ANY 1 9", "RELEASE a"]) == \
        ["OK", "true", "false", "true", "ERROR", "ERROR"]


# ---------------------------------------------------------------- Part 2: LRU
@pytest.mark.part2
def test_example1_verbatim(impl):
    assert impl.part2(EX1[:12]) == EX1_OUT[:12]   # up to the first RELEASE
    assert impl.part3(EX1) == EX1_OUT


@pytest.mark.part2
def test_example2_verbatim(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_never_used_first_then_oldest_then_string_id_order(impl):
    s = impl.AccountScheduler()
    for aid in ["a2", "a10", "b"]:
        s.add_account(aid)
    assert s.acquire("b", 1, 0) is True                                   # b used at 0, free from 1
    # never-used accounts first, in plain string order ('a10' < 'a2'); then b (last_used 0)
    assert [s.acquire_any(1, 2) for _ in range(4)] == ["a10", "a2", "b", None]
    # now last_used: a10=2, a2=2, b=2 -> equal -> id order again
    assert s.acquire_any(1, 3) == "a10"


@pytest.mark.part2
@pytest.mark.edge
def test_ties_on_last_used_break_by_id(impl):
    s = impl.AccountScheduler()
    for aid in ["a2", "a10", "b"]:
        s.add_account(aid)
    assert s.acquire("b", 1, 0) and s.acquire("a2", 1, 0) and s.acquire("a10", 1, 0)
    assert s.acquire_any(1, 1) == "a10"            # equal last_used -> plain string order
    assert s.acquire_any(1, 1) == "a2"
    assert s.acquire_any(1, 1) == "b"


@pytest.mark.part2
@pytest.mark.edge
def test_failed_acquire_and_queries_do_not_touch_last_used(impl):
    s = impl.AccountScheduler()
    s.add_account("a"), s.add_account("b")
    assert s.acquire("a", 10, 0) and s.acquire("b", 10, 1)
    assert s.acquire("a", 5, 5) is False           # fails: still locked; must not bump last_used
    s.is_available("b", 100)
    assert s.acquire_any(1, 100) == "a"            # a (0) older than b (1)


@pytest.mark.part2
@pytest.mark.edge
def test_all_locked_then_one_expires_and_empty_pool(impl):
    s = impl.AccountScheduler()
    assert s.acquire_any(5, 0) is None             # no accounts at all
    s.add_account("a"), s.add_account("b")
    assert s.acquire("a", 10, 0) and s.acquire("b", 20, 0)
    assert s.acquire_any(1, 9) is None
    assert s.acquire_any(1, 10) == "a"             # a's lock ended exactly at 10
    assert s.acquire_any(1, 10) is None
    assert s.acquire_any(1, 20) == "b"             # b (last_used 0) is older than a (last_used 10)


@pytest.mark.part2
@pytest.mark.edge
def test_non_monotonic_time_queries_still_correct(impl):
    # is_available(id, t) is `locked_until <= t`: a lock taken "later" still blocks an earlier t.
    s = impl.AccountScheduler()
    s.add_account("a"), s.add_account("b")
    assert s.acquire("a", 10, 50) is True          # a locked [50, 60)
    assert s.acquire_any(1, 100) == "b"            # b never used -> b, locked [100, 101)
    assert s.acquire_any(1, 55) is None            # a still locked at 55; b's lock ends at 101 > 55
    assert s.is_available("a", 55) is False and s.is_available("b", 55) is False
    assert s.acquire_any(1, 60) == "a"             # a free from 60
    assert s.acquire_any(1, 101) == "a"            # both free; last_used a=60 < b=100 -> a


# ---------------------------------------------------------------- Part 3: release
@pytest.mark.part3
def test_example3_verbatim(impl):
    assert impl.part4(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_release_keeps_last_used_and_is_idempotent(impl):
    s = impl.AccountScheduler()
    s.add_account("a"), s.add_account("b")
    assert s.acquire("a", 100, 0) and s.acquire("b", 100, 1)
    assert s.release("b") is True
    assert s.release("b") is True                  # already free -> still True
    assert s.release("zz") is False
    assert s.is_available("b", 1) is True and s.is_available("b", 0) is True
    assert s.acquire_any(1, 5) == "b"              # only b is free
    s.release("a")
    assert s.acquire_any(1, 6) == "a"              # a (last 0) older than b (5)


@pytest.mark.part3
@pytest.mark.edge
def test_release_then_reacquire_then_expire(impl):
    s = impl.AccountScheduler()
    s.add_account("a")
    assert s.acquire("a", 10, 0)
    assert s.release("a")
    assert s.acquire("a", 5, 3)                    # relock inside the old window
    assert s.is_available("a", 7) is False
    assert s.is_available("a", 8) is True
    assert s.acquire_any(1, 8) == "a"
    assert impl.part3(["RELEASE a"]) == ["UNKNOWN"]


# ---------------------------------------------------------------- Part 4: stream
@pytest.mark.part4
@pytest.mark.fmt
def test_stream_validation_and_case_whitespace(impl):
    assert impl.part4(["", "  add   a  ", "ADD", "ADD a b", "AVAILABLE a x", "ACQUIRE_ANY 1", "acquire_any 1 0", "RELEASE a", "NOPE"]) == \
        ["OK", "ERROR", "ERROR", "ERROR", "ERROR", "a", "OK", "ERROR"]
    assert impl.part4([]) == []


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_commands_20k_accounts(run_script):
    rng = random.Random(0)
    n_acc = 20_000
    lines = [f"ADD acct_{i}" for i in range(n_acc)]
    t = 0
    for _ in range(100_000):
        t += rng.randrange(0, 3)
        r = rng.random()
        if r < 0.7:
            lines.append(f"ACQUIRE_ANY {rng.randrange(1, 500)} {t}")
        elif r < 0.85:
            lines.append(f"ACQUIRE acct_{rng.randrange(n_acc)} {rng.randrange(1, 500)} {t}")
        elif r < 0.95:
            lines.append(f"AVAILABLE acct_{rng.randrange(n_acc)} {t}")
        else:
            lines.append(f"RELEASE acct_{rng.randrange(n_acc)}")
    r = run_script("\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == len(lines)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256
