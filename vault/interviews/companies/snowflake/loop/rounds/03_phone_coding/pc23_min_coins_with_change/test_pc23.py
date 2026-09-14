import random

import pytest

CANONICAL = (1, 5, 10, 50, 100, 200)
INF = float("inf")


def _dp_table(max_x, denoms):
    dp = [0.0] + [INF] * max_x
    for x in range(1, max_x + 1):
        best = INF
        for d in denoms:
            if d <= x and dp[x - d] + 1 < best:
                best = dp[x - d] + 1
        dp[x] = best
    return dp


def _brute_min_total(n, denoms, window):
    """Independent reference implementation used only by tests (not imported from solution)."""
    dp = _dp_table(n + window, denoms)
    best = INF
    for w in range(0, window + 1):
        if dp[n + w] != INF and dp[w] != INF:
            best = min(best, dp[n + w] + dp[w])
    return None if best == INF else int(best)


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "n,expected", [(0, 0), (1, 1), (4, 2), (6, 2), (999, 6), (10000, 50)]
)
def test_worked_examples_fixed(impl, n, expected):
    assert impl.min_total_coins_fixed(n) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_fixed_negative_raises(impl):
    with pytest.raises(ValueError):
        impl.min_total_coins_fixed(-1)


@pytest.mark.part1
@pytest.mark.edge
def test_window_bound_matches_wider_window(impl):
    """The shipped window (max(denoms)) must agree with a much wider search window (5x) for
    every n we can afford to brute force -- this is the empirical justification of the bound
    documented in problem.md, re-checked on every test run rather than trusted once."""
    rng = random.Random(0)
    ns = list(range(0, 300)) + [rng.randint(300, 10000) for _ in range(200)]
    for n in ns:
        wide = _brute_min_total(n, CANONICAL, 5 * max(CANONICAL))
        assert impl.min_total_coins_fixed(n) == wide, n


@pytest.mark.part1
@pytest.mark.edge
def test_fixed_agrees_with_brute_force_small(impl):
    for n in range(0, 250):
        assert impl.min_total_coins_fixed(n) == _brute_min_total(n, CANONICAL, max(CANONICAL))


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_examples_custom(impl):
    assert impl.min_total_coins_custom(6, [1, 3, 4]) == 2  # 3+3, not greedy's 4+1+1
    assert impl.min_total_coins_custom(7, [1, 3, 4]) == 2  # 4+3 exact
    assert impl.min_total_coins_custom(0, [1, 3, 4]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_custom_beats_greedy_on_144(impl):
    # classic non-canonical counterexample set
    assert impl.min_total_coins_custom(6, [1, 3, 4]) < 3  # greedy would use 3 coins (4+1+1)


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("denoms", [[], [0, 3], [-1, 5]])
def test_custom_invalid_denominations_raise(impl, denoms):
    with pytest.raises(ValueError):
        impl.min_total_coins_custom(5, denoms)


@pytest.mark.part2
@pytest.mark.edge
def test_custom_unreachable_raises(impl):
    with pytest.raises(ValueError):
        impl.min_total_coins_custom(3, [2, 4])  # only even amounts reachable
    with pytest.raises(ValueError):
        impl.min_total_coins_custom(3, [7])


@pytest.mark.part2
@pytest.mark.edge
def test_custom_agrees_with_brute_force_random(impl):
    rng = random.Random(1)
    for _ in range(300):
        size = rng.randint(1, 4)
        denoms = sorted(set(rng.randint(1, 30) for _ in range(size)) | {1})  # guarantee reachable
        n = rng.randint(0, 200)
        expected = _brute_min_total(n, tuple(denoms), 5 * max(denoms))
        assert impl.min_total_coins_custom(n, denoms) == expected, (n, denoms)


@pytest.mark.part2
@pytest.mark.edge
def test_window_bound_matches_wider_window_custom(impl):
    denoms = (1, 3, 4)
    for n in range(0, 400):
        wide = _brute_min_total(n, denoms, 5 * max(denoms))
        assert impl.min_total_coins_custom(n, list(denoms)) == wide, n


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_breakdown_worked_examples(impl):
    assert impl.min_total_coins_breakdown(4) == ([5], [1])
    assert impl.min_total_coins_breakdown(999) == ([200, 200, 200, 200, 200], [1])
    assert impl.min_total_coins_breakdown(6, [1, 3, 4]) == ([3, 3], [])


@pytest.mark.part3
@pytest.mark.edge
def test_breakdown_zero(impl):
    assert impl.min_total_coins_breakdown(0) == ([], [])


@pytest.mark.part3
def test_breakdown_is_valid_and_optimal_random(impl):
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(0, 5000)
        paid, change = impl.min_total_coins_breakdown(n)
        assert impl.is_valid_optimal_breakdown(n, paid, change)


@pytest.mark.part3
def test_breakdown_is_valid_and_optimal_custom_denoms(impl):
    denoms = [1, 3, 4]
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(0, 500)
        paid, change = impl.min_total_coins_breakdown(n, denoms)
        assert impl.is_valid_optimal_breakdown(n, paid, change, denoms)


@pytest.mark.part3
@pytest.mark.edge
def test_checker_rejects_bad_breakdown(impl):
    # wrong net amount (1000 - 200 = 800 != 4)
    assert impl.is_valid_optimal_breakdown(4, [200, 200, 200, 200, 200], [200], CANONICAL) is False
    # coin not in the denomination set (6 is not canonical)
    assert impl.is_valid_optimal_breakdown(4, [10], [6], CANONICAL) is False
    # correct net (6 - 2 = 4) but not the optimal coin count (8 coins vs optimal 2)
    assert impl.is_valid_optimal_breakdown(4, [1, 1, 1, 1, 1, 1], [1, 1], CANONICAL) is False
    # correct and optimal
    assert impl.is_valid_optimal_breakdown(4, [5], [1], CANONICAL) is True


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_many_queries(run_script):
    rng = random.Random(0)
    body = "\n".join(str(rng.randint(0, 10000)) for _ in range(3000))
    r = run_script(f"PART 1\nN 3000\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 3000
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nN 4\n0\n4\n6\n999\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n2\n2\n6\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nD 1 3 4\nN 2\n6\n7\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\nD 1 5 10 50 100 200\nN 2\n4\n999\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5|1\n200,200,200,200,200|1\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3_dash_for_empty(run_script):
    r = run_script("PART 3\nD 1 3 4\nN 2\n6\n0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3,3|-\n-|-\n"
