import random

import pytest

EX1 = (5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5])
EX2 = (3, [], [5, 3, 8])
EX3 = (4, [[1, 2], [3, 4]], [1, 5, 2, 4])
EX4 = (4, [[1, 2], [1, 3], [2, 4], [3, 4]], [1, 2, 2, 3])


def _brute_minimum_time(n, relations, time):
    """Longest-path-in-DAG brute force via memoized DFS (independent of the Kahn implementation)."""
    preds = {i: [] for i in range(1, n + 1)}
    for u, v in relations:
        preds[v].append(u)
    memo = {}

    def finish(v):
        if v in memo:
            return memo[v]
        best = max((finish(u) for u in preds[v]), default=0)
        memo[v] = time[v - 1] + best
        return memo[v]

    return max(finish(v) for v in range(1, n + 1))


def _valid_critical_path(n, relations, time, best, path):
    edges = {(u, v) for u, v in relations}
    if not path or len(set(path)) != len(path):
        return False
    if not all(1 <= c <= n for c in path):
        return False
    if sum(time[c - 1] for c in path) != best:
        return False
    return all((path[i], path[i + 1]) in edges for i in range(len(path) - 1))


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize("case,expected", [(EX1, 12), (EX2, 8), (EX3, 6), (EX4, 6)])
def test_worked_examples(impl, case, expected):
    n, relations, time = case
    assert impl.minimum_time(n, relations, time) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_single_course(impl):
    assert impl.minimum_time(1, [], [7]) == 7


@pytest.mark.part1
@pytest.mark.edge
def test_no_relations_is_longest_single_course(impl):
    assert impl.minimum_time(4, [], [2, 9, 1, 4]) == 9


@pytest.mark.part1
@pytest.mark.edge
def test_cycle_raises(impl):
    with pytest.raises(ValueError):
        impl.minimum_time(3, [[1, 2], [2, 3], [3, 1]], [1, 1, 1])


@pytest.mark.part1
@pytest.mark.edge
def test_self_loop_raises(impl):
    with pytest.raises(ValueError):
        impl.minimum_time(2, [[1, 1]], [1, 1])


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_range_relation_raises(impl):
    with pytest.raises(ValueError):
        impl.minimum_time(2, [[1, 3]], [1, 1])


@pytest.mark.part1
@pytest.mark.edge
def test_time_length_mismatch_raises(impl):
    with pytest.raises(ValueError):
        impl.minimum_time(2, [], [1])


@pytest.mark.part1
@pytest.mark.edge
def test_nonpositive_time_raises(impl):
    with pytest.raises(ValueError):
        impl.minimum_time(2, [], [1, 0])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 8)
        relations = [[u, v] for u in range(1, n + 1) for v in range(u + 1, n + 1) if rng.random() < 0.3]
        time = [rng.randint(1, 9) for _ in range(n)]
        assert impl.minimum_time(n, relations, time) == _brute_minimum_time(n, relations, time), (
            n,
            relations,
            time,
        )


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize(
    "case,expected",
    [
        (EX1, (12, [3, 4, 5])),
        (EX2, (8, [3])),
        (EX3, (6, [1, 2])),
        (EX4, (6, [1, 2, 4])),
    ],
)
def test_part2_worked_examples(impl, case, expected):
    n, relations, time = case
    assert impl.critical_path(n, relations, time) == expected


@pytest.mark.part2
@pytest.mark.edge
def test_part2_single_course(impl):
    assert impl.critical_path(1, [], [7]) == (7, [1])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_path_is_structurally_valid_on_random_inputs(impl):
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 8)
        relations = [[u, v] for u in range(1, n + 1) for v in range(u + 1, n + 1) if rng.random() < 0.3]
        time = [rng.randint(1, 9) for _ in range(n)]
        best, path = impl.critical_path(n, relations, time)
        assert best == _brute_minimum_time(n, relations, time)
        assert _valid_critical_path(n, relations, time, best, path), (n, relations, time, best, path)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_ties_pick_lexicographically_smallest(impl):
    # three independent single-course "chains" with equal weight -> smallest id wins
    assert impl.critical_path(3, [], [5, 5, 5]) == (5, [1])


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    assert impl.part2(["4 2", "1 2", "3 4", "1 5 2 4"]) == ["6", "1 2"]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_dense_dag_3000(run_script):
    rng = random.Random(2)
    n = 3000
    relations = []
    for v in range(2, n + 1):
        for u in rng.sample(range(1, v), min(v - 1, 4)):
            relations.append((u, v))
    time_vals = [rng.randint(1, 5) for _ in range(n)]
    lines = [f"{n} {len(relations)}", *[f"{u} {v}" for u, v in relations], " ".join(map(str, time_vals))]
    r = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 1 perf (LC scale)
@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_chain_50000(run_script):
    n = 50_000
    relations = [f"{i} {i + 1}" for i in range(1, n)]
    times = " ".join("1" for _ in range(n))
    lines = [f"{n} {n - 1}", *relations, times]
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(n)
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n5 5\n1 5\n2 5\n3 5\n3 4\n4 5\n1 2 3 4 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "12\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n4 2\n1 2\n3 4\n1 5 2 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n1 2\n"
