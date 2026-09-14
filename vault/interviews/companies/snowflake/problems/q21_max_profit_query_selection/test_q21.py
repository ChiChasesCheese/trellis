import random

import pytest


def _brute_single(durations, revenues, k):
    return max((k // d) * r for d, r in zip(durations, revenues))


def _brute_two(durations, revenues, k):
    """Independent brute force: for every pair, sweep every count of the first type and take
    the maximal count of the second that fits in the leftover budget (revenues are >= 0 so more
    runs of the second type is never worse)."""
    best = _brute_single(durations, revenues, k)
    n = len(durations)
    for i in range(n):
        for j in range(i + 1, n):
            di, ri, dj, rj = durations[i], revenues[i], durations[j], revenues[j]
            for a in range(k // di + 1):
                leftover = k - a * di
                b = leftover // dj
                profit = a * ri + b * rj
                if profit > best:
                    best = profit
    return best


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    assert impl.max_profit_single([3, 5], [10, 11], 10) == 30


@pytest.mark.part1
@pytest.mark.edge
def test_zero_budget(impl):
    assert impl.max_profit_single([3, 5], [10, 11], 0) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_single_type(impl):
    assert impl.max_profit_single([4], [7], 20) == 5 * 7


@pytest.mark.part1
@pytest.mark.edge
def test_zero_revenue_type_never_wins(impl):
    assert impl.max_profit_single([1, 2], [0, 5], 10) == 25


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "durations,revenues,k",
    [
        ([], [], 5),
        ([3], [1, 2], 5),
        ([0], [1], 5),
        ([-1], [1], 5),
        ([1], [-1], 5),
        ([1], [1], -1),
    ],
)
def test_invalid_input_raises(impl, durations, revenues, k):
    with pytest.raises(ValueError):
        impl.max_profit_single(durations, revenues, k)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute(impl):
    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(1, 6)
        durations = [rng.randint(1, 20) for _ in range(n)]
        revenues = [rng.randint(0, 20) for _ in range(n)]
        k = rng.randint(0, 50)
        assert impl.max_profit_single(durations, revenues, k) == _brute_single(durations, revenues, k)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k_types(run_script):
    rng = random.Random(1)
    n = 100_000
    durations = [rng.randint(1, 10 ** 9) for _ in range(n)]
    revenues = [rng.randint(0, 10 ** 9) for _ in range(n)]
    k = 10 ** 9
    stdin = f"PART 1\n{n} {k}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, revenues)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout) >= 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_mixing_beats_single(impl):
    # single best: 2x duration-3 = 8; mixing 1 of each = 4 + 5 = 9
    assert impl.max_profit_two_types([3, 4], [4, 5], 7) == 9


@pytest.mark.part2
@pytest.mark.edge
def test_two_types_never_worse_than_one(impl):
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 5)
        durations = [rng.randint(1, 10) for _ in range(n)]
        revenues = [rng.randint(0, 10) for _ in range(n)]
        k = rng.randint(0, 30)
        assert impl.max_profit_two_types(durations, revenues, k) >= impl.max_profit_single(durations, revenues, k)


@pytest.mark.part2
@pytest.mark.edge
def test_single_type_input_falls_back_to_part1(impl):
    assert impl.max_profit_two_types([4], [7], 20) == impl.max_profit_single([4], [7], 20)


@pytest.mark.part2
@pytest.mark.edge
def test_zero_budget(impl):
    assert impl.max_profit_two_types([3, 4], [4, 5], 0) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_random_against_independent_brute(impl):
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 6)
        durations = [rng.randint(1, 15) for _ in range(n)]
        revenues = [rng.randint(0, 15) for _ in range(n)]
        k = rng.randint(0, 40)
        assert impl.max_profit_two_types(durations, revenues, k) == _brute_two(durations, revenues, k), (
            durations, revenues, k,
        )


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.max_profit_two_types([0], [1], 5)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_bounded_n_and_k(run_script):
    # Part2 is deliberately small-scale (reconstructed): n <= 30, k <= 2000.
    rng = random.Random(4)
    n, k = 30, 2000
    durations = [rng.randint(1, 200) for _ in range(n)]
    revenues = [rng.randint(0, 200) for _ in range(n)]
    stdin = f"PART 2\n{n} {k}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, revenues)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout) >= 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n2 10\n3 5\n10 11\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "30\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n2 7\n3 4\n4 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "9\n"
