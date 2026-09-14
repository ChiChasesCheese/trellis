import random

import pytest


def _brute_sizes(intervals, queries):
    out = []
    for q in queries:
        best = None
        for l, r in intervals:
            if l <= q <= r:
                size = r - l + 1
                if best is None or size < best:
                    best = size
        out.append(best if best is not None else -1)
    return out


def _brute_bounds(intervals, queries):
    out = []
    for q in queries:
        best_key = None
        best_bounds = (-1, -1)
        for l, r in intervals:
            if l <= q <= r:
                key = (r - l + 1, l)
                if best_key is None or key < best_key:
                    best_key = key
                    best_bounds = (l, r)
        out.append(best_bounds)
    return out


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "intervals,queries,expected",
    [
        ([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5], [3, 3, 1, 4]),  # LC1851 example 1
        ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22], [2, -1, 4, 6]),  # LC1851 example 2
        ([], [1, 2], [-1, -1]),
    ],
)
def test_worked_examples(impl, intervals, queries, expected):
    assert impl.min_interval_sizes(intervals, queries) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_no_queries(impl):
    assert impl.min_interval_sizes([[1, 5]], []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_single_point_interval(impl):
    assert impl.min_interval_sizes([[5, 5]], [5, 4, 6]) == [1, -1, -1]


@pytest.mark.part1
@pytest.mark.edge
def test_query_at_exact_interval_boundary(impl):
    assert impl.min_interval_sizes([[1, 10]], [1, 10, 0, 11]) == [10, 10, -1, -1]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_intervals_same_bounds(impl):
    assert impl.min_interval_sizes([[3, 7], [3, 7]], [5]) == [5]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "intervals,queries",
    [
        ([[5, 1]], [1]),      # left > right
        ([[1]], [1]),         # wrong arity
        ([[1, "x"]], [1]),    # non-int bound
    ],
)
def test_malformed_interval_raises(impl, intervals, queries):
    with pytest.raises(ValueError):
        impl.min_interval_sizes(intervals, queries)


@pytest.mark.part1
@pytest.mark.edge
def test_malformed_query_raises(impl):
    with pytest.raises(ValueError):
        impl.min_interval_sizes([[1, 5]], ["x"])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_quadratic_brute_force(impl):
    rng = random.Random(0)
    for _ in range(400):
        n = rng.randint(0, 6)
        intervals = []
        for _ in range(n):
            a = rng.randint(0, 15)
            b = rng.randint(a, 15)
            intervals.append([a, b])
        queries = [rng.randint(0, 15) for _ in range(rng.randint(0, 6))]
        assert impl.min_interval_sizes(intervals, queries) == _brute_sizes(intervals, queries), (
            intervals,
            queries,
        )


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(0)
    n = 100_000
    intervals = []
    for _ in range(n):
        a = rng.randint(1, 10 ** 9)
        b = min(10 ** 9, a + rng.randint(0, 1000))
        intervals.append((a, b))
    queries = [rng.randint(1, 10 ** 9) for _ in range(n)]
    body = "\n".join(f"{a} {b}" for a, b in intervals)
    r = run_script(f"PART 1\n{n} {n}\n{body}\n{' '.join(map(str, queries))}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_examples(impl):
    assert impl.min_interval_bounds([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]) == [
        (2, 4),
        (2, 4),
        (4, 4),
        (3, 6),
    ]
    assert impl.min_interval_bounds([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]) == [
        (2, 3),
        (-1, -1),
        (2, 5),
        (20, 25),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_tie_breaks_on_smallest_start(impl):
    # [1,4] and [2,5] both have size 4 and both contain 3 -> smaller start wins
    assert impl.min_interval_bounds([[1, 4], [2, 5]], [3]) == [(1, 4)]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_uncovered_query_returns_sentinel(impl):
    assert impl.min_interval_bounds([[10, 20]], [5]) == [(-1, -1)]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_random_against_quadratic_brute_force(impl):
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(0, 6)
        intervals = []
        for _ in range(n):
            a = rng.randint(0, 15)
            b = rng.randint(a, 15)
            intervals.append([a, b])
        queries = [rng.randint(0, 15) for _ in range(rng.randint(0, 6))]
        assert impl.min_interval_bounds(intervals, queries) == _brute_bounds(intervals, queries), (
            intervals,
            queries,
        )


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k(run_script):
    rng = random.Random(1)
    n = 100_000
    intervals = []
    for _ in range(n):
        a = rng.randint(1, 10 ** 9)
        b = min(10 ** 9, a + rng.randint(0, 1000))
        intervals.append((a, b))
    queries = [rng.randint(1, 10 ** 9) for _ in range(n)]
    body = "\n".join(f"{a} {b}" for a, b in intervals)
    r = run_script(f"PART 2\n{n} {n}\n{body}\n{' '.join(map(str, queries))}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n4 4\n1 4\n2 4\n3 6\n4 4\n2 3 4 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3 3 1 4\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n4 4\n1 4\n2 4\n3 6\n4 4\n2 3 4 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2,4 2,4 4,4 3,6\n"
