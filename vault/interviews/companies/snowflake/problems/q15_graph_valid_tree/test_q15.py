import random
from collections import deque

import pytest


def _brute_valid_tree(n, edges):
    """BFS-based connectivity check, independent of union-find: a connected
    undirected graph with exactly n-1 edges is always a tree."""
    if len(edges) != n - 1:
        return False
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    visited[0] = True
    q = deque([0])
    count = 1
    while q:
        x = q.popleft()
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                count += 1
                q.append(y)
    return count == n


def _brute_online(n, edges):
    """Fresh BFS after each edge to count components; a forest has exactly
    n - components edges, so comparing the running edge count to that formula
    is an independent cycle check (no union-find involved)."""
    adj = [[] for _ in range(n)]
    out = []
    for i, (u, v) in enumerate(edges):
        adj[u].append(v)
        adj[v].append(u)
        edges_so_far = i + 1
        visited = [False] * n
        components = 0
        for start in range(n):
            if not visited[start]:
                components += 1
                visited[start] = True
                q = deque([start])
                while q:
                    x = q.popleft()
                    for y in adj[x]:
                        if not visited[y]:
                            visited[y] = True
                            q.append(y)
        acyclic = edges_so_far == (n - components)
        out.append((acyclic, components))
    return out


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "n,edges,expected",
    [
        (5, [[0, 1], [0, 2], [0, 3], [1, 4]], True),               # LC261 example 1
        (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False),      # LC261 example 2 (cycle 1-2-3-1)
        (1, [], True),
        (2, [[0, 1]], True),
    ],
)
def test_worked_examples(impl, n, edges, expected):
    assert impl.valid_tree(n, edges) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_disconnected_but_right_edge_count_is_not_a_tree(impl):
    # 4 nodes, 3 edges, but split into a triangle (with an extra node isolated
    # elsewhere) is impossible with only 3 edges among 4 nodes forming 2 comps
    # without a cycle unless connected -- use two disjoint components explicitly:
    # {0,1} connected, {2,3} connected, {2,3} has an extra edge making a self-cycle
    # is invalid; instead use 4 nodes/3 edges where one component has a cycle:
    assert impl.valid_tree(4, [[0, 1], [1, 2], [0, 2]]) is False  # triangle + isolated node 3


@pytest.mark.part1
@pytest.mark.edge
def test_too_few_edges_is_disconnected(impl):
    assert impl.valid_tree(4, [[0, 1], [2, 3]]) is False


@pytest.mark.part1
@pytest.mark.edge
def test_too_many_edges_has_a_cycle(impl):
    assert impl.valid_tree(3, [[0, 1], [1, 2], [0, 2]]) is False


@pytest.mark.part1
@pytest.mark.edge
def test_single_node_no_edges_is_a_tree(impl):
    assert impl.valid_tree(1, []) is True


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "n,edges",
    [
        (0, []),
        (3, [[0, 3]]),      # out of range
        (3, [[1, 1]]),      # self-loop
        (3, [[0]]),          # wrong arity
        (3, [["a", 1]]),    # non-int
    ],
)
def test_invalid_input_raises(impl, n, edges):
    with pytest.raises(ValueError):
        impl.valid_tree(n, edges)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_bfs_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 8)
        max_edges = n * (n - 1) // 2
        m = rng.randint(0, min(max_edges, n + 2))
        possible = [(u, v) for u in range(n) for v in range(u + 1, n)]
        rng.shuffle(possible)
        edges = [list(e) for e in possible[:m]]
        assert impl.valid_tree(n, edges) == _brute_valid_tree(n, edges), (n, edges)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(0)
    n = 100_000
    nodes = list(range(n))
    rng.shuffle(nodes)
    edges = [(nodes[i], nodes[i + 1]) for i in range(n - 1)]  # a valid random tree
    body = "\n".join(f"{u} {v}" for u, v in edges)
    r = run_script(f"PART 1\n{n} {len(edges)}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "true"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_building_a_path_stays_acyclic(impl):
    assert impl.valid_tree_online(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == [
        (True, 4),
        (True, 3),
        (True, 2),
        (True, 1),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_cycle_flips_acyclic_and_stays_flipped(impl):
    result = impl.valid_tree_online(4, [[0, 1], [2, 3], [1, 2], [0, 2]])
    assert result == [(True, 3), (True, 2), (True, 1), (False, 1)]
    # once broken, adding more (non-cycle-relevant) edges never repairs it
    result2 = impl.valid_tree_online(5, [[0, 1], [2, 3], [1, 2], [0, 2], [3, 4]])
    assert [ok for ok, _ in result2] == [True, True, True, False, False]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_no_edges(impl):
    assert impl.valid_tree_online(3, []) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.valid_tree_online(3, [[0, 5]])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_random_against_fresh_bfs_brute_force(impl):
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(1, 7)
        max_edges = n * (n - 1) // 2
        m = rng.randint(0, min(max_edges, n + 2))
        possible = [(u, v) for u in range(n) for v in range(u + 1, n)]
        rng.shuffle(possible)
        edges = [list(e) for e in possible[:m]]
        assert impl.valid_tree_online(n, edges) == _brute_online(n, edges), (n, edges)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k(run_script):
    rng = random.Random(2)
    n = 100_000
    nodes = list(range(n))
    rng.shuffle(nodes)
    edges = [(nodes[i], nodes[i + 1]) for i in range(n - 1)]
    body = "\n".join(f"{u} {v}" for u, v in edges)
    r = run_script(f"PART 2\n{n} {len(edges)}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip().splitlines()
    assert len(lines) == len(edges)
    assert lines[-1] == "true 1"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n5 4\n0 1\n0 2\n0 3\n1 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n5 4\n0 1\n1 2\n2 3\n3 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true 4\ntrue 3\ntrue 2\ntrue 1\n"
