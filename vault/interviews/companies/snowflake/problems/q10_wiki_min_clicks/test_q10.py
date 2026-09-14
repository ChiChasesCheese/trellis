import random
import string

import pytest

EXAMPLE_EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
DISCONNECTED_EDGES = [("A", "B"), ("C", "D")]


# ---------------------------------------------------------------- Part 1: BFS distance
@pytest.mark.part1
def test_example_shortest_distance(impl):
    assert impl.part1(EXAMPLE_EDGES, "A", "E") == 3


@pytest.mark.part1
def test_example_unreachable(impl):
    assert impl.part1(DISCONNECTED_EDGES, "A", "D") == -1


@pytest.mark.part1
def test_example_start_equals_target(impl):
    assert impl.part1(EXAMPLE_EDGES, "A", "A") == 0


@pytest.mark.part1
@pytest.mark.edge
def test_self_loop_does_not_break_or_loop_forever(impl):
    edges = [("A", "A"), ("A", "B")]
    assert impl.part1(edges, "A", "B") == 1


@pytest.mark.part1
@pytest.mark.edge
def test_dead_end_page_has_no_outgoing_links(impl):
    edges = [("A", "B")]
    assert impl.part1(edges, "B", "C") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_edges_do_not_affect_distance(impl):
    edges = [("A", "B"), ("A", "B"), ("B", "C")]
    assert impl.part1(edges, "A", "C") == 2


@pytest.mark.part1
@pytest.mark.edge
def test_page_appearing_only_as_a_target_part1(impl):
    # B never appears as a source; reaching it should still work, and BFS from
    # B (which has no outgoing edges) should correctly report unreachable.
    edges = [("A", "B"), ("C", "B")]
    assert impl.part1(edges, "A", "B") == 1
    assert impl.part1(edges, "B", "C") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_disconnected_graph_component(impl):
    assert impl.part1(DISCONNECTED_EDGES, "C", "D") == 1
    assert impl.part1(DISCONNECTED_EDGES, "A", "C") == -1


@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_sparse_graph(run_script):
    rng = random.Random(0)
    n = 50_000
    nodes = [f"P{i}" for i in range(n)]
    edges = []
    # random forward-leaning edges so a path from P0 usually exists, plus noise
    for i in range(n - 1):
        edges.append((nodes[i], nodes[i + 1]))
    for _ in range(n):
        a, b = rng.randrange(n), rng.randrange(n)
        edges.append((nodes[a], nodes[b]))
    lines = ["PART 1", str(len(edges))]
    lines += [f"{a},{b}" for a, b in edges]
    lines.append(f"{nodes[0]},{nodes[-1]}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    dist = int(r.stdout.strip())
    # reachable (the explicit P0->P1->...->P(n-1) chain guarantees an upper bound
    # of n-1 hops; random shortcut edges can only make it shorter, never -1)
    assert 0 <= dist <= n - 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"


# ---------------------------------------------------------------- Part 2: path reconstruction
@pytest.mark.part2
def test_example_path_matches_deterministic_bfs(impl):
    assert impl.part2(EXAMPLE_EDGES, "A", "E") == ["A", "B", "D", "E"]


@pytest.mark.part2
def test_example_unreachable_returns_empty_list(impl):
    assert impl.part2(DISCONNECTED_EDGES, "A", "D") == []


@pytest.mark.part2
def test_example_start_equals_target_returns_singleton(impl):
    assert impl.part2(EXAMPLE_EDGES, "A", "A") == ["A"]


@pytest.mark.part2
@pytest.mark.edge
def test_self_loop_path(impl):
    edges = [("A", "A"), ("A", "B")]
    assert impl.part2(edges, "A", "B") == ["A", "B"]


@pytest.mark.part2
@pytest.mark.edge
def test_dead_end_returns_empty(impl):
    edges = [("A", "B")]
    assert impl.part2(edges, "B", "C") == []


@pytest.mark.part2
@pytest.mark.edge
def test_duplicate_edges_do_not_affect_path(impl):
    edges = [("A", "B"), ("A", "B"), ("B", "C")]
    assert impl.part2(edges, "A", "C") == ["A", "B", "C"]


@pytest.mark.part2
@pytest.mark.edge
def test_page_appearing_only_as_a_target(impl):
    edges = [("A", "B"), ("C", "B")]
    assert impl.part2(edges, "A", "B") == ["A", "B"]
    assert impl.part2(edges, "B", "C") == []


@pytest.mark.part2
@pytest.mark.fmt
def test_alphabetical_neighbor_order_tiebreak_is_deterministic(impl):
    # A links to C and B (out of alphabetical order in the edge list); both C
    # and B are one hop from A and both link to D. Because neighbors are
    # visited alphabetically (B before C), D's parent must end up being B.
    edges = [("A", "C"), ("A", "B"), ("C", "D"), ("B", "D"), ("D", "E")]
    assert impl.part2(edges, "A", "E") == ["A", "B", "D", "E"]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_sparse_graph_path(run_script):
    rng = random.Random(0)
    n = 50_000
    nodes = [f"P{i}" for i in range(n)]
    edges = [(nodes[i], nodes[i + 1]) for i in range(n - 1)]
    for _ in range(n):
        a, b = rng.randrange(n), rng.randrange(n)
        edges.append((nodes[a], nodes[b]))
    lines = ["PART 2", str(len(edges))]
    lines += [f"{a},{b}" for a, b in edges]
    lines.append(f"{nodes[0]},{nodes[-1]}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    path = r.stdout.strip().split(",")
    assert path[0] == nodes[0] and path[-1] == nodes[-1]
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\n5\nA,B\nA,C\nB,D\nC,D\nD,E\nA,E\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\n5\nA,B\nA,C\nB,D\nC,D\nD,E\nA,E\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,B,D,E\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2_unreachable_blank_line(run_script):
    stdin = "PART 2\n2\nA,B\nC,D\nA,D\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"
