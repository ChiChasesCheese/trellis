import random

import pytest


def _random_forest(rng: random.Random, n: int) -> list[int]:
    """parent[i] is i (root) or a uniformly random earlier index -- guarantees no cycles."""
    parent = [0] * n
    for i in range(n):
        parent[i] = i if (i == 0 or rng.random() < 0.3) else rng.randrange(i)
    return parent


def _brute_children_become_roots(parent: list[int], delete_index: int) -> list[int]:
    n = len(parent)
    new_parent_of = dict(enumerate(parent))
    for child, p in list(new_parent_of.items()):
        if p == delete_index and child != delete_index:
            new_parent_of[child] = child
    del new_parent_of[delete_index]
    remaining = sorted(new_parent_of)
    old_to_new = {old: new for new, old in enumerate(remaining)}
    return [old_to_new[new_parent_of[old]] for old in remaining]


def _brute_subtree(parent: list[int], delete_index: int) -> list[int]:
    n = len(parent)
    children: dict[int, list[int]] = {}
    for i, p in enumerate(parent):
        if i != p:
            children.setdefault(p, []).append(i)
    doomed = set()
    frontier = [delete_index]
    while frontier:
        x = frontier.pop()
        if x in doomed:
            continue
        doomed.add(x)
        frontier.extend(children.get(x, []))
    remaining = [i for i in range(n) if i not in doomed]
    old_to_new = {old: new for new, old in enumerate(remaining)}
    result = []
    for old in remaining:
        p = parent[old]
        result.append(old_to_new[old] if p in doomed or p == old else old_to_new[p])
    return result


def _brute_batch(parent: list[int], delete_indices: list[int]) -> list[int]:
    n = len(parent)
    doomed = set(delete_indices)
    assert len(doomed) == len(delete_indices), "test helper assumes distinct indices"

    def full_chain(node):
        chain = [node]
        cur = node
        while parent[cur] != cur:
            cur = parent[cur]
            chain.append(cur)
        return chain

    remaining = [i for i in range(n) if i not in doomed]
    old_to_new = {old: new for new, old in enumerate(remaining)}
    result = []
    for old in remaining:
        chain = full_chain(old)[1:]  # ancestors, nearest first, excluding old itself
        live = next((a for a in chain if a not in doomed), None)
        result.append(old_to_new[old] if live is None else old_to_new[live])
    return result


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_children_become_roots(impl):
    # chain 0 <- 1 <- 2 <- 3 ; delete 2 -> child 3 becomes a root
    assert impl.delete_node_children_become_roots([0, 0, 1, 2], 2) == [0, 0, 2]


@pytest.mark.part1
@pytest.mark.edge
def test_single_node_forest(impl):
    assert impl.delete_node_children_become_roots([0], 0) == []


@pytest.mark.part1
@pytest.mark.edge
def test_delete_a_leaf(impl):
    # 0 root; 1,2 children of 0; delete leaf 2 -> just drop it and renumber
    assert impl.delete_node_children_become_roots([0, 0, 0], 2) == [0, 0]


@pytest.mark.part1
@pytest.mark.edge
def test_delete_a_root_with_children(impl):
    # two trees: 0 (root, child 1) and 2 (root); delete root 0 -> 1 becomes a root
    result = impl.delete_node_children_become_roots([0, 0, 2], 0)
    # after removing index 0: old 1 -> new 0, old 2 -> new 1
    assert result == [0, 1]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("bad", [-1, 4])
def test_out_of_range_raises(impl, bad):
    with pytest.raises(ValueError):
        impl.delete_node_children_become_roots([0, 0, 1, 2], bad)


@pytest.mark.part1
@pytest.mark.edge
def test_part1_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 12)
        parent = _random_forest(rng, n)
        delete_index = rng.randrange(n)
        assert impl.delete_node_children_become_roots(parent, delete_index) == \
            _brute_children_become_roots(parent, delete_index), (parent, delete_index)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_subtree(impl):
    assert impl.delete_subtree([0, 0, 1, 2], 1) == [0]


@pytest.mark.part2
@pytest.mark.edge
def test_delete_subtree_of_leaf_is_just_the_leaf(impl):
    assert impl.delete_subtree([0, 0, 0], 2) == [0, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_delete_subtree_whole_forest(impl):
    assert impl.delete_subtree([0], 0) == []


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("bad", [-1, 4])
def test_subtree_out_of_range_raises(impl, bad):
    with pytest.raises(ValueError):
        impl.delete_subtree([0, 0, 1, 2], bad)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_against_brute_force(impl):
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 14)
        parent = _random_forest(rng, n)
        delete_index = rng.randrange(n)
        assert impl.delete_subtree(parent, delete_index) == \
            _brute_subtree(parent, delete_index), (parent, delete_index)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_batch(impl):
    # chain 0 <- 1 <- 2 <- 3 ; deleting {1, 2} together: 3's nearest live ancestor is 0
    # (NOT what sequential single-node deletion would give -- see problem.md)
    assert impl.delete_nodes_batch([0, 0, 1, 2], [1, 2]) == [0, 0]


@pytest.mark.part3
@pytest.mark.edge
def test_batch_empty_deletion_is_identity_reindexed(impl):
    assert impl.delete_nodes_batch([0, 1, 1], []) == [0, 1, 1]


@pytest.mark.part3
@pytest.mark.edge
def test_batch_delete_everything(impl):
    assert impl.delete_nodes_batch([0, 0, 1], [0, 1, 2]) == []


@pytest.mark.part3
@pytest.mark.edge
def test_batch_duplicate_index_raises(impl):
    with pytest.raises(ValueError):
        impl.delete_nodes_batch([0, 0, 1], [1, 1])


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize("bad", [[-1], [3, 0]])
def test_batch_out_of_range_raises(impl, bad):
    with pytest.raises(ValueError):
        impl.delete_nodes_batch([0, 0, 1], bad)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_against_brute_force(impl):
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 14)
        parent = _random_forest(rng, n)
        k = rng.randint(0, n)
        delete_indices = rng.sample(range(n), k)
        assert impl.delete_nodes_batch(parent, delete_indices) == \
            _brute_batch(parent, delete_indices), (parent, delete_indices)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_subtree_delete(run_script):
    rng = random.Random(0)
    n = 200_000
    parent = _random_forest(rng, n)
    line = " ".join(map(str, parent)) + " | 0"
    r = run_script("PART 2\n" + line + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n0 0 1 2 | 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 0 2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n0 0 1 2 | 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n0 0 1 2 | 1 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 0\n"
