import random
import sys
import time

import pytest


def chain_tree(TreeNode, n: int):
    """A right-skewed chain of n nodes with values 0..n-1, built iteratively (never recurses)."""
    root = TreeNode(0)
    cur = root
    for i in range(1, n):
        cur.right = TreeNode(i)
        cur = cur.right
    return root


def balanced_tree(TreeNode, values: list[int]):
    """Build a balanced BST-shaped tree (by index, not by value order) from a sorted list,
    iteratively via an explicit work-queue (never recurses), so construction itself never hits
    Python's recursion limit even for ~1e5 nodes."""
    if not values:
        return None
    nodes = [TreeNode(v) for v in values]
    n = len(nodes)

    def build_range(lo, hi):
        # returns index of the root of nodes[lo:hi] arranged as a balanced BST
        stack = [(lo, hi, None, None)]  # (lo, hi, parent_idx, side)
        root_idx = None
        while stack:
            lo, hi, parent_idx, side = stack.pop()
            if lo >= hi:
                continue
            mid = (lo + hi) // 2
            if parent_idx is None:
                root_idx = mid
            elif side == "L":
                nodes[parent_idx].left = nodes[mid]
            else:
                nodes[parent_idx].right = nodes[mid]
            stack.append((lo, mid, mid, "L"))
            stack.append((mid + 1, hi, mid, "R"))
        return root_idx

    root_idx = build_range(0, n)
    return nodes[root_idx]


# ---------------------------------------------------------------- build_tree
@pytest.mark.part1
def test_build_tree_worked_example(impl):
    root = impl.build_tree(["1", "null", "2", "3"])
    assert impl.part1(root) == [1, 3, 2]


@pytest.mark.part1
@pytest.mark.edge
def test_build_tree_empty(impl):
    assert impl.build_tree([]) is None
    assert impl.part1(None) == []


@pytest.mark.part1
@pytest.mark.edge
def test_build_tree_single_node(impl):
    root = impl.build_tree(["1"])
    assert impl.part1(root) == [1]


@pytest.mark.part1
def test_build_tree_bigger(impl):
    # root5, left3,right8; 3's children 1,4; 8's children 7,9
    root = impl.build_tree(["5", "3", "8", "1", "4", "7", "9"])
    assert impl.part1(root) == [1, 3, 4, 5, 7, 8, 9]


# ---------------------------------------------------------------- Part 1: recursive
@pytest.mark.part1
@pytest.mark.edge
def test_part1_left_only_chain(impl):
    root = impl.build_tree(["3", "2", "null", "1"])
    assert impl.part1(root) == [1, 2, 3]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_right_only_chain(impl):
    root = impl.build_tree(["1", "null", "2", "null", "3"])
    assert impl.part1(root) == [1, 2, 3]


# ---------------------------------------------------------------- Part 2: iterative
@pytest.mark.part2
def test_part2_matches_part1_worked_examples(impl):
    for vals in (["1", "null", "2", "3"], [], ["1"], ["5", "3", "8", "1", "4", "7", "9"]):
        root = impl.build_tree(vals)
        assert impl.part2(root) == impl.part1(root)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_left_and_right_only_chains(impl):
    left_chain = impl.build_tree(["3", "2", "null", "1"])
    right_chain = impl.build_tree(["1", "null", "2", "null", "3"])
    assert impl.part2(left_chain) == [1, 2, 3]
    assert impl.part2(right_chain) == [1, 2, 3]


@pytest.mark.part2
def test_part2_matches_part1_random_trees(impl):
    rng = random.Random(0)
    for _ in range(20):
        n = rng.randrange(0, 30)
        vals = sorted(rng.sample(range(1000), n)) if n else []
        root = balanced_tree(impl.TreeNode, vals)
        assert impl.part2(root) == impl.part1(root) == vals


# ---------------------------------------------------------------- Part 3: Morris
@pytest.mark.part3
def test_part3_matches_part1_worked_examples(impl):
    for vals in (["1", "null", "2", "3"], [], ["1"], ["5", "3", "8", "1", "4", "7", "9"]):
        root = impl.build_tree(vals)
        assert impl.part3(root) == impl.part1(root)


@pytest.mark.part3
def test_part3_restores_tree_shape(impl):
    root = impl.build_tree(["5", "3", "8", "1", "4", "7", "9"])
    before = impl.part1(root)
    result = impl.part3(root)
    after = impl.part1(root)  # re-run recursive traversal on the SAME tree object
    assert result == before == after, "Morris must restore the tree so later traversals still work"


@pytest.mark.part3
def test_part3_no_dangling_threads(impl):
    root = impl.build_tree(["5", "3", "8", "1", "4", "7", "9"])
    impl.part3(root)

    def check(node):
        # after restoration, no left-subtree's rightmost descendant should point back up
        if node is None:
            return
        if node.left is not None:
            pred = node.left
            while pred.right is not None:
                assert pred.right is not node, "dangling Morris thread left behind"
                pred = pred.right
        check(node.left)
        check(node.right)

    check(root)


# --------------------------------------------------- critical: recursion-depth differentiator
@pytest.mark.part3
@pytest.mark.edge
def test_morris_and_iterative_survive_constrained_recursion_limit(impl):
    """The key differentiator: naive recursion blows the call stack on a deep tree; Morris (O(1)
    call stack) and the explicit-stack iterative version (heap, not call stack) do not."""
    n = 2000
    deep_root = chain_tree(impl.TreeNode, n)
    expected = list(range(n))

    old_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(300)

        with pytest.raises(RecursionError):
            impl.part1(deep_root)

        assert impl.part3(deep_root) == expected
        assert impl.part2(deep_root) == expected
    finally:
        sys.setrecursionlimit(old_limit)


# ---------------------------------------------------------------- perf
@pytest.mark.part3
@pytest.mark.perf
def test_perf_morris_on_large_balanced_tree(impl):
    n = 100_000
    values = list(range(n))
    root = balanced_tree(impl.TreeNode, values)
    t0 = time.perf_counter()
    result = impl.part3(root)
    elapsed = time.perf_counter() - t0
    assert result == values
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script):
    r = run_script("PART 1\n1,null,2,3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1,3,2\n"


@pytest.mark.part2
@pytest.mark.io
def test_io_part2(run_script):
    r = run_script("PART 2\n5,3,8,1,4,7,9\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1,3,4,5,7,8,9\n"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3(run_script):
    r = run_script("PART 3\n5,3,8,1,4,7,9\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1,3,4,5,7,8,9\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_io_empty_tree(run_script):
    r = run_script("PART 1\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""
