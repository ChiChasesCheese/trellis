import random
import time

import pytest


def _brute_penalty(customers, j):
    return customers[:j].count("N") + customers[j:].count("Y")


def _brute_best(customers):
    return min(range(len(customers) + 1), key=lambda j: (_brute_penalty(customers, j), j))


def _brute_window(customers):
    n = len(customers)
    best = None
    for o in range(n + 1):
        for c in range(o, n + 1):
            p = customers[o:c].count("N") + customers[:o].count("Y") + customers[c:].count("Y")
            if best is None or (p, o, c) < best:
                best = (p, o, c)
    return best[1], best[2], best[0]


def _brute_k(customers, k):
    """Exhaustive over ≤ k disjoint windows (tiny n only)."""
    n = len(customers)
    s = [1 if c == "Y" else -1 for c in customers]
    best = 0

    def rec(start, left, acc):
        nonlocal best
        best = max(best, acc)
        if left == 0:
            return
        for o in range(start, n):
            for c in range(o + 1, n + 1):
                rec(c, left - 1, acc + sum(s[o:c]))

    rec(0, k, 0)
    return customers.count("Y") - best


def _rand(rng, hi=12):
    return "".join(rng.choice("YN") for _ in range(rng.randint(1, hi)))


# ---------------------------------------------------------------- Part 1: LC 2483
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.best_closing_time("YYNY") == 2
    assert impl.best_closing_time("NNNNN") == 0
    assert impl.best_closing_time("YYYY") == 4


@pytest.mark.part1
@pytest.mark.edge
def test_single_char_and_ties_earliest(impl):
    assert impl.best_closing_time("N") == 0
    assert impl.best_closing_time("Y") == 1
    assert impl.best_closing_time("YNYN") == 1     # penalties 2,1,2,1,2 -> earliest
    assert impl.best_closing_time("NY") == 0       # penalties 1,2,1 -> 0 not 2
    assert impl.best_closing_time("YN") == 1


@pytest.mark.part1
def test_penalty_helper(impl):
    assert [impl.penalty("YYNY", j) for j in range(5)] == [3, 2, 1, 2, 1]
    assert impl.penalty("NNNNN", 5) == 5 and impl.penalty("NNNNN", 0) == 0
    assert impl.penalty("YYYY", 0) == 4 and impl.penalty("YYYY", 4) == 0


@pytest.mark.part1
def test_part1_matches_brute_force(impl):
    rng = random.Random(0)
    for _ in range(500):
        c = _rand(rng)
        assert impl.best_closing_time(c) == _brute_best(c), c
        for j in range(len(c) + 1):
            assert impl.penalty(c, j) == _brute_penalty(c, j)


@pytest.mark.part1
@pytest.mark.edge
def test_long_input_is_linear(impl):
    c = "N" * 50_000 + "Y" * 50_000
    assert impl.best_closing_time(c) == 0          # penalties: 50000 at 0 ... tie at 100000 -> earliest
    c2 = "Y" * 50_000 + "N" * 50_000
    assert impl.best_closing_time(c2) == 50_000


# ---------------------------------------------------------------- Part 2: open/close
@pytest.mark.part2
def test_window_examples(impl):
    W = impl.Window
    assert impl.best_open_close("YYNY") == W(0, 2, 1)
    assert impl.best_open_close("NNYYNNYN") == W(2, 4, 1)
    assert impl.best_open_close("NNNNN") == W(0, 0, 0)
    assert impl.best_open_close("YYYY") == W(0, 4, 0)
    assert impl.best_open_close("NYN") == W(1, 2, 0)


@pytest.mark.part2
@pytest.mark.edge
def test_window_ties_and_fields(impl):
    w = impl.best_open_close("YNNY")   # [0,1) and [3,4) both score 1 -> smallest open
    assert (w.open, w.close, w.penalty) == (0, 1, 1)
    w = impl.best_open_close("YNY")    # [0,1) score 1, [0,3) score 1, [2,3) score 1 -> (0,1)
    assert w == impl.Window(0, 1, 1)
    assert impl.best_open_close("N") == impl.Window(0, 0, 0)
    assert impl.best_open_close("Y") == impl.Window(0, 1, 0)
    w = impl.best_open_close("YYNY")
    assert w.penalty == impl.min_penalty_k_windows("YYNY", 1)


@pytest.mark.part2
def test_window_matches_brute_force(impl):
    rng = random.Random(1)
    for _ in range(400):
        c = _rand(rng, 10)
        assert tuple(impl.best_open_close(c)) == _brute_window(c), c


# ---------------------------------------------------------------- Part 3: k windows
@pytest.mark.part3
def test_k_windows_examples(impl):
    assert [impl.min_penalty_k_windows("NNYYNNYN", k) for k in (1, 2, 0, 5)] == [1, 0, 3, 0]
    assert [impl.min_penalty_k_windows("YNYNY", k) for k in (1, 2, 3)] == [2, 1, 0]


@pytest.mark.part3
@pytest.mark.edge
def test_k_windows_boundaries(impl):
    assert impl.min_penalty_k_windows("YYNY", 0) == 3            # never open
    assert impl.min_penalty_k_windows("NNNN", 3) == 0
    assert impl.min_penalty_k_windows("YYYY", 1) == 0
    assert impl.min_penalty_k_windows("YNYNYNY", 4) == 0         # 4 Y-runs
    assert impl.min_penalty_k_windows("YNYNYNY", 3) == 1
    assert impl.min_penalty_k_windows("Y", 1) == 0 and impl.min_penalty_k_windows("N", 1) == 0
    # k = 1 equals Part 2 for every string
    rng = random.Random(5)
    for _ in range(100):
        c = _rand(rng)
        assert impl.min_penalty_k_windows(c, 1) == impl.best_open_close(c).penalty


@pytest.mark.part3
def test_k_windows_matches_exhaustive(impl):
    rng = random.Random(2)
    for _ in range(150):
        c = _rand(rng, 7)
        k = rng.randint(0, 3)
        assert impl.min_penalty_k_windows(c, k) == _brute_k(c, k), (c, k)


# ---------------------------------------------------------------- Part 4: weighted
@pytest.mark.part4
def test_weighted_examples(impl):
    assert impl.best_closing_time_weighted("YYNY", [1, 1, 5, 1]) == 2
    assert impl.best_closing_time_weighted("YYNY", [1, 1, 1, 10]) == 4
    assert impl.best_closing_time_weighted("YYNY", [1, 1, 1, 1]) == 2


@pytest.mark.part4
@pytest.mark.edge
def test_weighted_zero_weights_and_huge(impl):
    assert impl.best_closing_time_weighted("YYNY", [0, 0, 0, 0]) == 0      # all tie -> earliest
    assert impl.best_closing_time_weighted("NNYY", [0, 0, 1, 1]) == 4      # idle N hours are free -> stay open
    assert impl.best_closing_time_weighted("NNYY", [5, 5, 1, 1]) == 0      # opening costs 10 to earn 2
    assert impl.best_closing_time_weighted("NNYY", [1, 1, 10**9, 10**9]) == 4
    rng = random.Random(3)
    for _ in range(200):
        c = _rand(rng)
        w = [rng.randint(0, 5) for _ in c]
        brute = min(range(len(c) + 1), key=lambda j: (sum(w[i] for i in range(j) if c[i] == "N") + sum(w[i] for i in range(j, len(c)) if c[i] == "Y"), j))
        assert impl.best_closing_time_weighted(c, w) == brute, (c, w)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\nYYNY\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"
    assert run_script("PART 1\nY Y N Y\n").stdout == "2\n"                 # spaces tolerated
    assert run_script("PART 2\nNNYYNNYN\n").stdout == "2 4 1\n"
    assert run_script("PART 3\nNNYYNNYN\nK 2\n").stdout == "0\n"
    assert run_script("PART 4\nYYNY\n1 1 5 1\n").stdout == "2\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    c = "".join(rng.choice("YN") for _ in range(100_000))
    t0 = time.perf_counter()
    h = impl.best_closing_time(c)
    assert impl.penalty(c, h) <= impl.penalty(c, 0) and impl.penalty(c, h) <= impl.penalty(c, len(c))
    w = impl.best_open_close(c)
    assert w.penalty == impl.min_penalty_k_windows(c, 1)
    assert impl.min_penalty_k_windows(c, 5) <= w.penalty
    assert impl.best_closing_time_weighted(c, [rng.randint(0, 10**9) for _ in c]) >= 0
    assert time.perf_counter() - t0 < 2.0
    r = run_script(f"PART 1\n{c}\n")
    assert r.returncode == 0 and r.stdout == f"{h}\n" and r.seconds < 2.0 and r.max_rss_mb < 256
