import random

import pytest


# ---------------------------------------------------------------- Part 1: LC210 topo sort
@pytest.mark.part1
def test_example_simple_pair(impl):
    assert impl.part1(2, [[1, 0]]) == [0, 1]


@pytest.mark.part1
def test_example_diamond(impl):
    assert impl.part1(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]


@pytest.mark.part1
def test_example_cycle_returns_empty(impl):
    assert impl.part1(2, [[1, 0], [0, 1]]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_min_heap_tiebreak_smallest_id_first(impl):
    # two independent chains: ready set at start is {0,2}; must pop 0 before 2,
    # then after unlocking 1 the ready set is {1,2} -> pop 1 before 2.
    assert impl.part1(4, [[1, 0], [3, 2]]) == [0, 1, 2, 3]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_courses(impl):
    assert impl.part1(0, []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_single_course_no_prereqs(impl):
    assert impl.part1(1, []) == [0]


@pytest.mark.part1
@pytest.mark.edge
def test_self_loop_is_a_cycle_part1(impl):
    assert impl.part1(1, [[0, 0]]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_long_chain_forces_unique_order(impl):
    n = 500
    prereqs = [[i, i - 1] for i in range(1, n)]
    assert impl.part1(n, prereqs) == list(range(n))


@pytest.mark.part1
@pytest.mark.edge
def test_disconnected_components(impl):
    # two independent 3-chains: 0<-1<-2 style via [a,b]=a requires b
    prereqs = [[1, 0], [2, 1], [4, 3], [5, 4]]
    assert impl.part1(6, prereqs) == [0, 1, 2, 3, 4, 5]


@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_dag(run_script):
    rng = random.Random(0)
    n = 20_000
    # random DAG: every edge points from a lower-indexed course to a higher one
    # (a requires b, with b < a) so no cycles are possible, then shuffled.
    edges = []
    for a in range(1, n):
        num_prereqs = rng.randint(1, 3)
        for _ in range(num_prereqs):
            b = rng.randint(0, a - 1)
            edges.append((a, b))
    lines = ["PART 1", str(n), str(len(edges))]
    lines += [f"{a} {b}" for a, b in edges]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    order = [int(x) for x in r.stdout.split()]
    assert len(order) == n
    assert sorted(order) == list(range(n))
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"


# ---------------------------------------------------------------- Part 2: parallel semesters
@pytest.mark.part2
def test_example_diamond_three_semesters(impl):
    assert impl.part2(4, [[1, 2], [1, 3], [2, 4], [3, 4]]) == 3


@pytest.mark.part2
def test_example_cycle_returns_minus_one(impl):
    assert impl.part2(2, [[1, 2], [2, 1]]) == -1


@pytest.mark.part2
def test_example_no_dependencies_one_semester(impl):
    assert impl.part2(3, []) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_zero_courses_is_zero_semesters(impl):
    assert impl.part2(0, []) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_single_course_one_semester(impl):
    assert impl.part2(1, []) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_self_loop_is_a_cycle_part2(impl):
    assert impl.part2(1, [[1, 1]]) == -1


@pytest.mark.part2
@pytest.mark.edge
def test_disconnected_chains_take_the_longer_chains_length(impl):
    # two independent chains of length 3: 1->2->3 and 4->5->6
    assert impl.part2(6, [[1, 2], [2, 3], [4, 5], [5, 6]]) == 3


@pytest.mark.part2
@pytest.mark.edge
def test_long_chain_needs_n_semesters(impl):
    n = 500
    relations = [[i, i + 1] for i in range(1, n)]
    assert impl.part2(n, relations) == n


@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_layered_dag(run_script):
    rng = random.Random(0)
    n = 20_000
    layers = 200
    # assign each course (1..n) to a random layer 1..layers, then link every course
    # in layer k to a random course in layer k+1 (guarantees a DAG with exactly
    # `layers` semesters and lets courses in the same layer run in parallel).
    course_layer = [0] + [rng.randint(1, layers) for _ in range(n)]
    by_layer: dict[int, list[int]] = {}
    for course in range(1, n + 1):
        by_layer.setdefault(course_layer[course], []).append(course)
    edges = []
    for layer in range(1, layers):
        if layer not in by_layer or (layer + 1) not in by_layer:
            continue
        nxt = by_layer[layer + 1]
        for course in by_layer[layer]:
            edges.append((course, rng.choice(nxt)))
    lines = ["PART 2", str(n), str(len(edges))]
    lines += [f"{a} {b}" for a, b in edges]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout.strip()) >= 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\n4\n4\n1 0\n2 0\n3 1\n3 2\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 1 2 3\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1_cycle_blank_line(run_script):
    stdin = "PART 1\n2\n2\n1 0\n0 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\n4\n4\n1 2\n1 3\n2 4\n3 4\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3\n"
