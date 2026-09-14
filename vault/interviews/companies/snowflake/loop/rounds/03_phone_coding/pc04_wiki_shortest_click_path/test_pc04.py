import random

import pytest

EX1_GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["D"]}

EX2_GRAPH = {"A": ["B", "C"], "B": ["E"], "C": ["D", "F"], "F": ["D"], "E": []}
EX2_OUT = ["A", "C", "D"]

EX3_GRAPH = {"A": ["C", "B"], "B": ["D"], "C": ["D"]}
EX3_OUT = ["A", "B", "D"]

EX4_GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "E": ["D"]}


def _make_fetch(graph, failing):
    def fetch(page):
        if page in failing:
            raise RuntimeError(f"fetch failed for {page!r}")
        return graph.get(page, [])

    return fetch


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.shortest_path_length(EX1_GRAPH, "A", "D") == 2
    assert impl.shortest_path_length(EX1_GRAPH, "D", "A") == -1
    assert impl.shortest_path_length(EX1_GRAPH, "A", "A") == 0


@pytest.mark.part1
@pytest.mark.edge
def test_unreachable_returns_minus_one(impl):
    assert impl.shortest_path_length({"A": ["B"]}, "A", "Z") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_directed_edges_are_not_bidirectional(impl):
    graph = {"A": ["B"]}
    assert impl.shortest_path_length(graph, "A", "B") == 1
    assert impl.shortest_path_length(graph, "B", "A") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_isolated_start_equals_end(impl):
    assert impl.shortest_path_length({}, "X", "X") == 0


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_2_dead_end_trap(impl):
    assert impl.shortest_path(EX2_GRAPH, "A", "D") == EX2_OUT


@pytest.mark.part2
def test_worked_example_3_true_tie_lexicographic(impl):
    assert impl.shortest_path(EX3_GRAPH, "A", "D") == EX3_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_greedy_first_step_trap(impl):
    # first step's lexicographically smaller branch ("Bz") dead-ends; the correct answer must
    # go through "Ca" even though "Bz" < "Ca"
    graph = {"A": ["Bz", "Ca"], "Bz": ["Z"], "Ca": ["D"], "Z": []}
    assert impl.shortest_path(graph, "A", "D") == ["A", "Ca", "D"]


@pytest.mark.part2
@pytest.mark.edge
def test_unreachable_returns_empty_list(impl):
    assert impl.shortest_path({"A": ["B"]}, "A", "Z") == []


@pytest.mark.part2
@pytest.mark.edge
def test_start_equals_end_returns_singleton(impl):
    assert impl.shortest_path({}, "X", "X") == ["X"]


@pytest.mark.part2
@pytest.mark.edge
def test_adjacency_order_does_not_affect_output(impl):
    # C listed before B in the adjacency list, but B still must win on lexicographic merit
    graph = {"A": ["C", "B"], "B": ["D"], "C": ["D"]}
    assert impl.shortest_path(graph, "A", "D")[1] == "B"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_4_failure_forces_detour(impl):
    fetch = _make_fetch(EX4_GRAPH, {"B"})
    assert impl.crawl_shortest_path(fetch, "A", "D") == (["A", "C", "E", "D"], 1)


@pytest.mark.part3
def test_worked_example_4_no_failures_takes_shortest(impl):
    fetch = _make_fetch(EX4_GRAPH, set())
    assert impl.crawl_shortest_path(fetch, "A", "D") == (["A", "B", "D"], 0)


@pytest.mark.part3
@pytest.mark.edge
def test_start_equals_end_never_calls_fetch(impl):
    def fetch(page):
        raise AssertionError("fetch should not be called when start == end")

    assert impl.crawl_shortest_path(fetch, "X", "X") == (["X"], 0)


@pytest.mark.part3
@pytest.mark.edge
def test_all_paths_fail_gives_unreachable_and_counts_failures(impl):
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"]}
    fetch = _make_fetch(graph, {"B", "C"})
    path, failures = impl.crawl_shortest_path(fetch, "A", "D")
    assert path == []
    assert failures == 2


@pytest.mark.part3
@pytest.mark.edge
def test_each_page_fetched_at_most_once(impl):
    # two different frontier nodes both link to "shared" -- fetch must only be attempted once
    graph = {"A": ["B", "C"], "B": ["shared"], "C": ["shared"], "shared": ["D"]}
    calls = []

    def fetch(page):
        calls.append(page)
        return graph.get(page, [])

    path, failures = impl.crawl_shortest_path(fetch, "A", "D")
    assert failures == 0
    assert calls.count("shared") == 1
    assert path[-1] == "D"


@pytest.mark.part3
@pytest.mark.edge
def test_unreachable_still_counts_failures_along_the_way(impl):
    graph = {"A": ["B"], "B": []}
    fetch = _make_fetch(graph, {"B"})
    path, failures = impl.crawl_shortest_path(fetch, "A", "Z")
    assert path == []
    assert failures == 1


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_format_exact(impl):
    out = impl.part2(["4", "A B", "A C", "B D", "C D", "A D"])
    assert out == ["A,B,D"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["4", "A B", "A C", "B D", "C D", "A D"]
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["6", "A B", "A C", "B E", "C D", "C F", "F D", "A D"]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,C,D\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    body = ["4", "A B", "A C", "B D", "C E", "E D", "1", "B", "A D"]
    # NOTE: edge count line must match the number of edge lines that follow
    body = ["5", "A B", "A C", "B D", "C E", "E D", "1", "B", "A D"]
    r = run_script("PART 3\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A,C,E,D\n1\n"


# ------------------------------------------------------------------------ perf
@pytest.mark.part2
@pytest.mark.perf
def test_perf_50k_node_sparse_graph(run_script):
    rng = random.Random(0)
    n = 50_000
    nodes = [f"p{i}" for i in range(n)]
    lines = []
    edge_count = 0
    edges = []
    for i in range(n):
        if i + 1 < n:
            edges.append(f"{nodes[i]} {nodes[i + 1]}")
        for _ in range(2):
            j = rng.randrange(0, n)
            edges.append(f"{nodes[i]} {nodes[j]}")
    lines.append(str(len(edges)))
    lines.extend(edges)
    lines.append(f"{nodes[0]} {nodes[-1]}")
    result = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
