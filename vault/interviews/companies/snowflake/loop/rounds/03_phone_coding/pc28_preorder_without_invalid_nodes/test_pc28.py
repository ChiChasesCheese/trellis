import random

import pytest

EDGES = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
N = 6


def _brute_preorder(n, edges, root, invalid, mode):
    children = [[] for _ in range(n)]
    for p, c in edges:
        children[p].append(c)
    bad = set(invalid)
    out = []

    def dfs(node):
        if mode == "prune" and node in bad:
            return
        if mode == "splice" and node not in bad:
            out.append(node)
        elif mode == "prune":
            out.append(node)
        for c in children[node]:
            dfs(c)

    dfs(root)
    return out


# ------------------------------------------------------------------------ Part 1 (splice)
@pytest.mark.part1
def test_worked_examples_splice(impl):
    assert impl.preorder_skip_invalid_splice(N, EDGES, 0, []) == [0, 1, 3, 4, 2, 5]
    assert impl.preorder_skip_invalid_splice(N, EDGES, 0, [1]) == [0, 3, 4, 2, 5]
    assert impl.preorder_skip_invalid_splice(N, EDGES, 0, [0]) == [1, 3, 4, 2, 5]


@pytest.mark.part1
@pytest.mark.edge
def test_splice_all_invalid(impl):
    assert impl.preorder_skip_invalid_splice(N, EDGES, 0, list(range(N))) == []


@pytest.mark.part1
@pytest.mark.edge
def test_splice_leaf_invalid(impl):
    assert impl.preorder_skip_invalid_splice(N, EDGES, 0, [3]) == [0, 1, 4, 2, 5]


@pytest.mark.part1
@pytest.mark.edge
def test_splice_single_node_tree(impl):
    assert impl.preorder_skip_invalid_splice(1, [], 0, []) == [0]
    assert impl.preorder_skip_invalid_splice(1, [], 0, [0]) == []


@pytest.mark.part1
def test_splice_agrees_with_brute_force_random(impl):
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 12)
        edges = []
        for child in range(1, n):
            parent = rng.randint(0, child - 1)
            edges.append((parent, child))
        rng.shuffle(edges)
        invalid = [x for x in range(n) if rng.random() < 0.3]
        assert impl.preorder_skip_invalid_splice(n, edges, 0, invalid) == _brute_preorder(
            n, edges, 0, invalid, "splice"
        ), (n, edges, invalid)


@pytest.mark.part1
@pytest.mark.edge
def test_splice_deep_chain_is_iterative(impl):
    depth = 3000
    edges = [(i, i + 1) for i in range(depth - 1)]
    result = impl.preorder_skip_invalid_splice(depth, edges, 0, [])
    assert result == list(range(depth))


# ------------------------------------------------------------------------ Part 2 (prune)
@pytest.mark.part2
def test_worked_examples_prune(impl):
    assert impl.preorder_skip_invalid_prune(N, EDGES, 0, [1]) == [0, 2, 5]
    assert impl.preorder_skip_invalid_prune(N, EDGES, 0, [0]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_prune_leaf_invalid_same_as_splice(impl):
    assert impl.preorder_skip_invalid_prune(N, EDGES, 0, [3]) == [0, 1, 4, 2, 5]


@pytest.mark.part2
@pytest.mark.edge
def test_prune_single_node_tree(impl):
    assert impl.preorder_skip_invalid_prune(1, [], 0, []) == [0]
    assert impl.preorder_skip_invalid_prune(1, [], 0, [0]) == []


@pytest.mark.part2
def test_prune_agrees_with_brute_force_random(impl):
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(1, 12)
        edges = []
        for child in range(1, n):
            parent = rng.randint(0, child - 1)
            edges.append((parent, child))
        rng.shuffle(edges)
        invalid = [x for x in range(n) if rng.random() < 0.3]
        assert impl.preorder_skip_invalid_prune(n, edges, 0, invalid) == _brute_preorder(
            n, edges, 0, invalid, "prune"
        ), (n, edges, invalid)


@pytest.mark.part2
@pytest.mark.edge
def test_prune_deep_chain_is_iterative(impl):
    depth = 3000
    edges = [(i, i + 1) for i in range(depth - 1)]
    result = impl.preorder_skip_invalid_prune(depth, edges, 0, [depth // 2])
    assert result == list(range(depth // 2))


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_deep_chain_splice(run_script):
    depth = 100_000
    edge_lines = "\n".join(f"{i} {i+1}" for i in range(depth - 1))
    stdin = f"PART 1\nNODES {depth}\nN {depth-1}\n{edge_lines}\nROOT 0\nINVALID 50000\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count(" ") == depth - 2  # depth-1 numbers output -> depth-2 spaces
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    edge_lines = "\n".join(f"{p} {c}" for p, c in EDGES)
    stdin = f"PART 1\nNODES {N}\nN {len(EDGES)}\n{edge_lines}\nROOT 0\nINVALID 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 3 4 2 5\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    edge_lines = "\n".join(f"{p} {c}" for p, c in EDGES)
    stdin = f"PART 2\nNODES {N}\nN {len(EDGES)}\n{edge_lines}\nROOT 0\nINVALID 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 2 5\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2_empty_result(run_script):
    edge_lines = "\n".join(f"{p} {c}" for p, c in EDGES)
    stdin = f"PART 2\nNODES {N}\nN {len(EDGES)}\n{edge_lines}\nROOT 0\nINVALID 0\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "-\n"
