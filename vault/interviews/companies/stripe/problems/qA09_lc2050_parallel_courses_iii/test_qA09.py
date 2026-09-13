import random
import time as _time

import pytest

EX1 = (3, [[1, 3], [2, 3]], [3, 2, 5])
EX2 = (5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5])


def _random_dag(rng, n, m, tmax=10**4):
    edges = set()
    while len(edges) < m:
        a, b = rng.sample(range(1, n + 1), 2)
        edges.add((min(a, b), max(a, b)))  # a < b guarantees acyclic
    return n, [list(e) for e in edges], [rng.randint(1, tmax) for _ in range(n)]


def _brute_longest(n, relations, time):
    """Reference: memoised longest path (small n only)."""
    preds = {j: [] for j in range(1, n + 1)}
    for p, q in relations:
        preds[q].append(p)
    memo = {}

    def f(j):
        if j not in memo:
            memo[j] = time[j - 1] + max((f(p) for p in preds[j]), default=0)
        return memo[j]

    return max(f(j) for j in range(1, n + 1))


def _check_schedule(n, relations, time, k, slots):
    """Validity: every job once, duration respected, prerequisites finished, <= k overlap."""
    assert sorted(s.job for s in slots) == list(range(1, n + 1))
    end = {s.job: s.end for s in slots}
    start = {s.job: s.start for s in slots}
    for s in slots:
        assert s.end - s.start == time[s.job - 1] and s.start >= 0
    for p, q in relations:
        assert start[q] >= end[p]
    events = sorted([(s.start, 1) for s in slots] + [(s.end, -1) for s in slots])  # ends before starts
    running = 0
    for _, d in events:
        running += d
        assert running <= k
    assert slots == sorted(slots, key=lambda s: (s.start, s.job))


# ---------------------------------------------------------------- Part 1: LC 2050
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.minimum_time(*EX1) == 8
    assert impl.minimum_time(*EX2) == 12


@pytest.mark.part1
@pytest.mark.edge
def test_no_relations_chain_single(impl):
    assert impl.minimum_time(3, [], [4, 9, 2]) == 9      # all parallel -> max
    assert impl.minimum_time(3, [[1, 2], [2, 3]], [4, 9, 2]) == 15  # chain -> sum
    assert impl.minimum_time(1, [], [7]) == 7
    assert impl.minimum_time(1, [], [1]) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_longest_path_is_not_longest_job(impl):
    # job 4 is the single longest (10) but the chain 1->2->3 (4+4+4 = 12) wins
    assert impl.minimum_time(4, [[1, 2], [2, 3]], [4, 4, 4, 10]) == 12
    # diamond: 1 -> {2,3} -> 4 ; longest branch 3
    assert impl.minimum_time(4, [[1, 2], [1, 3], [2, 4], [3, 4]], [1, 5, 2, 1]) == 7


@pytest.mark.part1
@pytest.mark.edge
def test_deep_chain_no_recursion_limit(impl):
    n = 50_000
    relations = [[i, i + 1] for i in range(1, n)]
    assert impl.minimum_time(n, relations, [10**4] * n) == n * 10**4  # 5*10^8


@pytest.mark.part1
@pytest.mark.edge
def test_relations_out_of_order_and_many_prereqs(impl):
    # edges listed child-first; Kahn must not depend on input order
    assert impl.minimum_time(4, [[3, 4], [1, 2], [2, 3]], [1, 1, 1, 1]) == 4
    assert impl.critical_path(4, [[3, 4], [1, 2], [2, 3]], [1, 1, 1, 1]) == [1, 2, 3, 4]
    # one job with every other job as a prerequisite: max(prereqs) + own
    n = 2000
    relations = [[i, n] for i in range(1, n)]
    time = list(range(1, n))  # job i takes i months
    assert impl.minimum_time(n, relations, time + [7]) == (n - 1) + 7
    assert impl.critical_path(n, relations, time + [7]) == [n - 1, n]


@pytest.mark.part1
def test_matches_brute_force_on_random_dags(impl):
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 9)
        m = rng.randint(0, n * (n - 1) // 2)
        case = _random_dag(rng, n, m, tmax=9)
        assert impl.minimum_time(*case) == _brute_longest(*case), case


# ---------------------------------------------------------------- Part 2: critical path
@pytest.mark.part2
def test_critical_path_examples(impl):
    assert impl.critical_path(*EX1) == [1, 3]
    assert impl.critical_path(*EX2) == [3, 4, 5]


@pytest.mark.part2
@pytest.mark.edge
def test_critical_path_ties_smallest_id(impl):
    assert impl.critical_path(2, [], [5, 5]) == [1]                       # tie on the end job
    assert impl.critical_path(3, [[1, 3], [2, 3]], [2, 2, 1]) == [1, 3]   # tie on the predecessor
    assert impl.critical_path(3, [[2, 3], [1, 3]], [2, 2, 1]) == [1, 3]   # relation order irrelevant
    assert impl.critical_path(1, [], [4]) == [1]


@pytest.mark.part2
def test_critical_path_is_valid_chain_with_part1_length(impl):
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(1, 12)
        case = _random_dag(rng, n, rng.randint(0, min(20, n * (n - 1) // 2)), tmax=9)
        n, relations, time = case
        path = impl.critical_path(*case)
        assert sum(time[j - 1] for j in path) == impl.minimum_time(*case)
        edges = {tuple(e) for e in relations}
        assert all((a, b) in edges for a, b in zip(path, path[1:]))


# ---------------------------------------------------------------- Part 3: k workers
@pytest.mark.part3
def test_k_workers_examples(impl):
    S = impl.Slot
    assert impl.makespan_k_workers(*EX2, 1) == 15
    assert impl.schedule_k_workers(*EX2, 2) == [S(2, 0, 2), S(3, 0, 3), S(1, 2, 3), S(4, 3, 7), S(5, 7, 12)]
    assert impl.makespan_k_workers(*EX2, 2) == 12
    assert impl.schedule_k_workers(3, [], [4, 9, 2], 2) == [S(1, 0, 4), S(2, 0, 9), S(3, 4, 6)]
    assert impl.makespan_k_workers(3, [], [3, 3, 3], 2) == 6


@pytest.mark.part3
@pytest.mark.edge
def test_k_workers_boundaries(impl):
    n, relations, time = EX2
    assert impl.makespan_k_workers(n, relations, time, 1) == sum(time)
    assert impl.makespan_k_workers(n, relations, time, n) == impl.minimum_time(n, relations, time)
    assert impl.makespan_k_workers(n, relations, time, 100) == impl.minimum_time(n, relations, time)
    assert impl.makespan_k_workers(1, [], [9], 1) == 9
    # k=2 with three parallel unit jobs: 2, one below k=3: 1
    assert impl.makespan_k_workers(3, [], [1, 1, 1], 2) == 2
    assert impl.makespan_k_workers(3, [], [1, 1, 1], 3) == 1


@pytest.mark.part3
def test_k_workers_schedule_is_valid_and_bounded(impl):
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(1, 12)
        n, relations, time = _random_dag(rng, n, rng.randint(0, min(20, n * (n - 1) // 2)), tmax=9)
        for k in (1, 2, 3, n):
            slots = impl.schedule_k_workers(n, relations, time, k)
            _check_schedule(n, relations, time, k, slots)
            ms = max(s.end for s in slots)
            assert impl.minimum_time(n, relations, time) <= ms <= sum(time)


@pytest.mark.part3
@pytest.mark.fmt
def test_k_workers_priority_longest_tail_then_id(impl):
    # jobs 1,2,3 ready at 0; tails: 1 -> 1+8 (via 4), 2 -> 2, 3 -> 3 ; k=1 -> job 1 first, then 3, then 2
    n, relations, time = 4, [[1, 4]], [1, 2, 3, 8]
    slots = impl.schedule_k_workers(n, relations, time, 1)
    assert [s.job for s in slots] == [1, 4, 3, 2]  # after 1 ends, 4 (tail 8) beats 3 and 2
    # equal tails -> smallest id first
    slots = impl.schedule_k_workers(3, [], [2, 2, 2], 1)
    assert [s.job for s in slots] == [1, 2, 3]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\n3\n3 2 5\n1,3\n2,3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "8\n"
    r = run_script("PART 2\n5\n1 2 3 4 5\n1,5\n2,5\n3, 5\n\n3,4\n4,5\n")
    assert r.stdout == "3 -> 4 -> 5\n12\n"
    r = run_script("PART 3\nK 2\n5\n1 2 3 4 5\n1,5\n2,5\n3,5\n3,4\n4,5\n")
    assert r.stdout == "12\n2 0 2\n3 0 3\n1 2 3\n4 3 7\n5 7 12\n"
    assert run_script("PART 1\n3\n4 9 2\n").stdout == "9\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    n, relations, time = _random_dag(rng, 50_000, 50_000)
    t0 = _time.perf_counter()
    total = impl.minimum_time(n, relations, time)
    path = impl.critical_path(n, relations, time)
    assert sum(time[j - 1] for j in path) == total
    ms = impl.makespan_k_workers(n, relations, time, 8)
    assert ms >= total
    assert _time.perf_counter() - t0 < 2.0
    text = "PART 1\n" + f"{n}\n" + " ".join(map(str, time)) + "\n" + "\n".join(f"{a},{b}" for a, b in relations) + "\n"
    r = run_script(text)
    assert r.returncode == 0 and r.stdout == f"{total}\n" and r.seconds < 2.0 and r.max_rss_mb < 256
