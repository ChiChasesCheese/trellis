import random
import time

import pytest

EX1 = (["daniel", "daniel", "daniel", "luis", "luis", "luis", "luis"],
       ["10:00", "10:40", "10:40", "09:40", "11:00", "13:00", "15:00"])
EX2 = (["alice", "alice", "alice", "bob", "bob", "bob", "bob"],
       ["12:01", "12:00", "18:00", "21:00", "21:20", "21:30", "23:00"])


def brute(names, times, k=3, window=60):
    mins = [int(t[:2]) * 60 + int(t[3:]) for t in times]
    out = set()
    for n in set(names):
        ts = [m for nm, m in zip(names, mins) if nm == n]
        for a in ts:
            if sum(1 for b in ts if a <= b <= a + window) >= k:
                out.add(n)
    return sorted(out)


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.alert_names(*EX1) == ["daniel"]
    assert impl.alert_names(*EX2) == ["bob"]


@pytest.mark.part1
@pytest.mark.edge
def test_sixty_minute_boundary_inclusive(impl):
    assert impl.alert_names(["a"] * 3, ["10:00", "10:40", "11:00"]) == ["a"]
    assert impl.alert_names(["a"] * 3, ["10:00", "10:40", "11:01"]) == []
    assert impl.alert_names(["a"] * 3, ["10:00", "10:00", "10:00"]) == ["a"]  # identical times count


@pytest.mark.part1
@pytest.mark.edge
def test_unsorted_input_and_fewer_than_three(impl):
    assert impl.alert_names(["a", "a", "a"], ["11:00", "10:00", "10:40"]) == ["a"]
    assert impl.alert_names(["a", "a"], ["10:00", "10:00"]) == []
    assert impl.alert_names(["a"], ["10:00"]) == []
    assert impl.alert_names([], []) == []
    # four uses where only a non-adjacent triple is close: sorted scan must still find 10:00,10:30,10:59
    assert impl.alert_names(["a"] * 4, ["10:59", "10:00", "23:00", "10:30"]) == ["a"]


@pytest.mark.part1
@pytest.mark.edge
def test_no_midnight_wrap_and_padding(impl):
    assert impl.alert_names(["a"] * 3, ["23:30", "23:50", "00:10"]) == []   # 00:10 is 23 h earlier, not 40 min later
    assert impl.alert_names(["a"] * 3, ["00:00", "00:30", "01:00"]) == ["a"]
    assert impl.alert_names(["a"] * 3, ["09:05", "09:06", "09:07"]) == ["a"]


@pytest.mark.part1
@pytest.mark.fmt
def test_output_unique_and_sorted(impl):
    names = ["zed"] * 3 + ["amy"] * 3 + ["bob"] * 6
    times = ["10:00", "10:10", "10:20"] * 4
    assert impl.alert_names(names, times) == ["amy", "bob", "zed"]


@pytest.mark.part1
def test_random_against_brute(impl):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randrange(0, 12)
        names = [rng.choice("abc") for _ in range(n)]
        times = [f"{rng.randrange(0, 24):02d}:{rng.randrange(0, 60):02d}" for _ in range(n)]
        assert impl.alert_names(names, times) == brute(names, times)


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_generic_k_window_examples(impl):
    assert impl.alert_names_k(*EX2, k=2, window=1) == ["alice"]
    assert impl.alert_names_k(*EX2, k=4, window=120) == ["bob"]
    assert impl.alert_names_k(*EX2, k=4, window=119) == []
    assert impl.alert_names_k(*EX2, k=1) == ["alice", "bob"]
    assert impl.alert_names_k(*EX1) == impl.alert_names(*EX1)


@pytest.mark.part2
@pytest.mark.edge
def test_generic_boundaries_and_errors(impl):
    assert impl.alert_names_k(["a", "a"], ["10:00", "10:00"], k=2, window=0) == ["a"]
    assert impl.alert_names_k(["a", "a"], ["10:00", "10:01"], k=2, window=0) == []
    assert impl.alert_names_k(["a"] * 5, ["10:00"] * 5, k=6, window=1440) == []
    with pytest.raises(ValueError):
        impl.alert_names_k(["a"], ["10:00"], k=0)
    with pytest.raises(ValueError):
        impl.alert_names_k(["a"], ["10:00"], window=-1)


@pytest.mark.part2
def test_generic_against_brute(impl):
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randrange(0, 12)
        names = [rng.choice("ab") for _ in range(n)]
        times = [f"{rng.randrange(9, 12):02d}:{rng.randrange(0, 60):02d}" for _ in range(n)]
        k, w = rng.randrange(1, 5), rng.randrange(0, 90)
        assert impl.alert_names_k(names, times, k, w) == brute(names, times, k, w)


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_limiter_example(impl):
    lim = impl.KeyCardLimiter(limit=2, window=60)
    assert [lim.swipe("a", t) for t in ["10:00", "10:40", "11:00", "11:01", "11:40"]] == [True, True, False, True, False]
    assert lim.denied == [("a", "11:00"), ("a", "11:40")]


@pytest.mark.part3
@pytest.mark.edge
def test_limiter_keys_independent_and_denied_do_not_count(impl):
    lim = impl.KeyCardLimiter(limit=1, window=10)
    assert lim.swipe("a", "10:00") is True
    assert lim.swipe("b", "10:00") is True      # other key unaffected
    assert lim.swipe("a", "10:10") is False     # 10:00 still inside [10:00, 10:10]
    assert lim.swipe("a", "10:11") is True      # 10:00 evicted; the denied 10:10 never counted
    assert lim.swipe("a", "10:11") is False
    with pytest.raises(ValueError):
        lim.swipe("a", "10:05")                  # backwards in time for the same key
    assert lim.swipe("b", "10:05") is False     # b's own clock is at 10:00, so 10:05 is fine (and denied by window)


@pytest.mark.part3
def test_limiter_blocks_exactly_the_lc_alert_swipe(impl):
    # every name that LC alerts has at least one denied swipe under limit=2/window=60, and vice versa
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randrange(1, 10)
        swipes = sorted((rng.choice("ab"), f"{rng.randrange(9, 12):02d}:{rng.randrange(0, 60):02d}") for _ in range(n))
        swipes.sort(key=lambda s: s[1])
        lim = impl.KeyCardLimiter(2, 60)
        for name, t in swipes:
            lim.swipe(name, t)
        alerted = impl.alert_names([s[0] for s in swipes], [s[1] for s in swipes])
        assert sorted({n for n, _ in lim.denied}) == alerted


@pytest.mark.part3
@pytest.mark.fmt
def test_limiter_denied_order_interleaved_keys(impl):
    lim = impl.KeyCardLimiter(limit=1, window=5)
    seq = [("b", "10:00"), ("a", "10:00"), ("a", "10:03"), ("b", "10:04"), ("a", "10:06"), ("b", "10:06")]
    assert [lim.swipe(n, t) for n, t in seq] == [True, True, False, False, True, True]
    assert lim.denied == [("a", "10:03"), ("b", "10:04")]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    ex2 = "\n".join(f"{n} {t}" for n, t in zip(*EX2)) + "\n"
    r = run_script("PART 1\n" + ex2)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "bob\n"
    assert run_script("PART 2\n1 60\n" + ex2).stdout == "alice\nbob\n"
    assert run_script("PART 2\n4 119\n" + ex2 + "\n").stdout == ""
    r = run_script("PART 3\n2 60\na 10:00\na 10:40\na 11:00\na 11:01\n")
    assert r.stdout == "a 10:00 ALLOW\na 10:40 ALLOW\na 11:00 DENY\na 11:01 ALLOW\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    n = 100_000
    names = [f"w{rng.randrange(2000)}" for _ in range(n)]
    times = [f"{rng.randrange(0, 24):02d}:{rng.randrange(0, 60):02d}" for _ in range(n)]
    t0 = time.perf_counter()
    res = impl.alert_names(names, times)
    assert res == sorted(set(res))
    assert time.perf_counter() - t0 < 2.0
    r = run_script("PART 1\n" + "\n".join(f"{a} {b}" for a, b in zip(names, times)) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == res
    assert r.seconds < 2.0 and r.max_rss_mb < 256
