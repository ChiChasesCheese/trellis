import random
import sys

import pytest


def _brute_array_sums(root1: list[int]) -> list[int]:
    """Independent (recursive -- safe for the small complete trees used here) reference for
    Part1."""
    n = len(root1)

    def rec(i):
        if i >= n:
            return 0
        return root1[i] + rec(2 * i + 1) + rec(2 * i + 2)

    return [rec(i) for i in range(n)]


def _random_complete_array(rng: random.Random, n: int) -> list[int]:
    return [rng.randint(-5, 20) for _ in range(n)]


def _make_node(impl, spec):
    """spec: None, or (val, left_spec, right_spec) -- build an impl.TreeNode tree recursively
    (trees built here are always small/shallow, so plain recursion is fine for TEST helpers)."""
    if spec is None:
        return None
    val, left_spec, right_spec = spec
    node = impl.TreeNode(val)
    node.left = _make_node(impl, left_spec)
    node.right = _make_node(impl, right_spec)
    return node


def _brute_tree_sums(root):
    """Independent recursive reference for Part2 (safe for the shallow trees used in
    correctness tests; the perf test checks the iterative implementation separately at depth
    1e5, where this recursive brute force would blow the stack, so it isn't used there)."""
    if root is None:
        return None

    def rec(node):
        if node is None:
            return 0, None
        ls, lnode = rec(node.left)
        rs, rnode = rec(node.right)
        total = node.val + ls + rs
        new = type(node)(total)
        new.left, new.right = lnode, rnode
        return total, new

    return rec(root)[1]


def _tree_to_tuple(root):
    """(value tree) -> nested tuple, for equality comparisons independent of object identity."""
    if root is None:
        return None
    return (root.val, _tree_to_tuple(root.left), _tree_to_tuple(root.right))


def _random_tree_spec(rng: random.Random, max_depth: int):
    if max_depth <= 0 or rng.random() < 0.25:
        return None
    val = rng.randint(-5, 20)
    return (val, _random_tree_spec(rng, max_depth - 1), _random_tree_spec(rng, max_depth - 1))


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    root1 = [5, 2, 3, 1, 4, 6, 7]
    root2 = [0] * 7
    assert impl.rewrite_subtree_sums(root1, root2) == [28, 7, 16, 1, 4, 6, 7]


@pytest.mark.part1
@pytest.mark.edge
def test_single_node(impl):
    assert impl.rewrite_subtree_sums([9], [0]) == [9]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_tree(impl):
    assert impl.rewrite_subtree_sums([], []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_shape_mismatch_raises(impl):
    with pytest.raises(ValueError):
        impl.rewrite_subtree_sums([1, 2, 3], [1, 2])


@pytest.mark.part1
@pytest.mark.edge
def test_root2_values_are_irrelevant(impl):
    root1 = [5, 2, 3, 1, 4, 6, 7]
    a = impl.rewrite_subtree_sums(root1, [0] * 7)
    b = impl.rewrite_subtree_sums(root1, [999] * 7)
    assert a == b == [28, 7, 16, 1, 4, 6, 7]


@pytest.mark.part1
@pytest.mark.edge
def test_negative_values(impl):
    root1 = [-1, -2, 3]
    assert impl.rewrite_subtree_sums(root1, [0, 0, 0]) == [0, -2, 3]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(0, 40)
        root1 = _random_complete_array(rng, n)
        root2 = [0] * n
        assert impl.rewrite_subtree_sums(root1, root2) == _brute_array_sums(root1), root1


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_tree_worked_example(impl):
    root1 = _make_node(impl, (5, (2, (1, None, None), (4, None, None)), (3, (6, None, None), (7, None, None))))
    result = impl.rewrite_subtree_sums_tree(root1)
    assert _tree_to_tuple(result) == (28, (7, (1, None, None), (4, None, None)), (16, (6, None, None), (7, None, None)))
    # original tree must be untouched (a NEW tree is returned)
    assert _tree_to_tuple(root1) == (5, (2, (1, None, None), (4, None, None)), (3, (6, None, None), (7, None, None)))


@pytest.mark.part2
@pytest.mark.edge
def test_tree_none(impl):
    assert impl.rewrite_subtree_sums_tree(None) is None


@pytest.mark.part2
@pytest.mark.edge
def test_tree_single_node(impl):
    node = _make_node(impl, (7, None, None))
    assert _tree_to_tuple(impl.rewrite_subtree_sums_tree(node)) == (7, None, None)


@pytest.mark.part2
@pytest.mark.edge
def test_tree_left_only_chain(impl):
    # chain via left children only: 1 -> 2 -> 3 (leaf). Subtree sums bottom-up: 3, 2+3=5, 1+5=6.
    spec = (1, (2, (3, None, None), None), None)
    root1 = _make_node(impl, spec)
    result = impl.rewrite_subtree_sums_tree(root1)
    assert _tree_to_tuple(result) == (6, (5, (3, None, None), None), None)


@pytest.mark.part2
@pytest.mark.edge
def test_tree_gaps_missing_right_children(impl):
    # node with only a left child, and a node with only a right child
    spec = (10, (2, None, (3, None, None)), None)
    root1 = _make_node(impl, spec)
    result = impl.rewrite_subtree_sums_tree(root1)
    assert _tree_to_tuple(result) == (15, (5, None, (3, None, None)), None)


@pytest.mark.part2
@pytest.mark.edge
def test_tree_against_brute_force_random(impl):
    rng = random.Random(1)
    for _ in range(200):
        spec = _random_tree_spec(rng, max_depth=6)
        root1 = _make_node(impl, spec)
        expected = _tree_to_tuple(_brute_tree_sums(root1))
        actual = _tree_to_tuple(impl.rewrite_subtree_sums_tree(root1))
        assert actual == expected, spec


@pytest.mark.part2
@pytest.mark.perf
def test_tree_deep_skewed_no_recursion_error(impl):
    """A depth-100000 fully-left-skewed tree: recursion would raise RecursionError; the
    iterative implementation must handle it, and quickly."""
    depth = 100_000
    root = impl.TreeNode(1)
    cur = root
    for _ in range(depth - 1):
        cur.left = impl.TreeNode(1)
        cur = cur.left
    result = impl.rewrite_subtree_sums_tree(root)
    # subtree sum of the root of a depth-`depth` chain of 1s is `depth`; walk down the left spine
    node, expected = result, depth
    seen = 0
    while node is not None:
        assert node.val == expected, (seen, node.val, expected)
        expected -= 1
        node = node.left
        seen += 1
    assert seen == depth


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_complete_array(run_script):
    rng = random.Random(0)
    n = 200_000
    root1 = [rng.randint(-5, 20) for _ in range(n)]
    line = " ".join(map(str, root1)) + " | " + " ".join("0" for _ in range(n))
    r = run_script("PART 1\n" + line + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n5 2 3 1 4 6 7 | 0 0 0 0 0 0 0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "28 7 16 1 4 6 7\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n5 2 1 # # 4 # # 3 6 # # 7 # #\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "28 7 1 # # 4 # # 16 6 # # 7 # #\n"
