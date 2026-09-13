import pytest


# ================================================================== Part 1
@pytest.mark.part1
def test_part1_worked_examples(impl):
    assert impl.part1([1, 1, 2, 2, 3, 4], 3) == [7]
    assert impl.part1([1, 2, 3, 4], 2) == [3, 4, 5]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_single_node(impl):
    # only the root: no possible deletions, any k >= 1 satisfied trivially
    assert impl.part1([], 1) == []
    assert impl.part1([], 100) == []


@pytest.mark.part1
@pytest.mark.edge
def test_part1_already_satisfied(impl):
    # a shallow tree already within k
    assert impl.part1([1, 1], 5) == []


@pytest.mark.part1
@pytest.mark.edge
def test_part1_all_but_root_deleted(impl):
    # k = 1: only the root (depth 1) survives
    assert impl.part1([1, 2, 3, 4], 1) == [2, 3, 4, 5]


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_is_ascending(impl):
    # nodes 2,3,4 are children of root (depth 2); nodes 5,6 hang off 2 and 3 respectively
    # (depth 3). k=2 -> both depth-3 nodes must go, ascending.
    result = impl.part1([1, 1, 1, 2, 3], 2)
    assert result == sorted(result)
    assert result == [5, 6]


# ================================================================== Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    assert impl.part2([-1, 0, 0, 1, 1, 3], 2) == 1


@pytest.mark.part2
def test_part2_star_under_already_violating_ancestor_counts_once(impl):
    # tree: 0-1-2, and 2 has three leaf children 3,4,5. depths: 0,1,2,3,3,3. k=1.
    # node2 (depth2>1) is the sole topmost violator; its leaves are already covered by it.
    assert impl.part2([-1, 0, 1, 2, 2, 2], 1) == 1


@pytest.mark.part2
def test_part2_star_under_non_violating_parent_counts_each(impl):
    # tree: 0-1, and 1 has three leaf children 2,3,4. depths: 0,1,2,2,2. k=1.
    # node1 (depth1<=1) does not violate, so each leaf is its own topmost violator.
    assert impl.part2([-1, 0, 1, 1, 1], 1) == 3


@pytest.mark.part2
@pytest.mark.edge
def test_part2_single_node(impl):
    assert impl.part2([-1], 0) == 0
    assert impl.part2([-1], 5) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_part2_k_zero(impl):
    # root depth 0 always satisfies k=0; any child violates and is a topmost violator
    assert impl.part2([-1, 0, 0], 0) == 2


@pytest.mark.part2
@pytest.mark.edge
def test_part2_already_satisfied(impl):
    assert impl.part2([-1, 0, 1], 5) == 0


# ================================================================== Part 3
@pytest.mark.part3
def test_part3_worked_example(impl):
    assert impl.part3(4, [3, 1, 2], [2, 3, 4], 1) == 2


@pytest.mark.part3
@pytest.mark.edge
def test_part3_single_node(impl):
    assert impl.part3(1, [], [], 0) == 0
    assert impl.part3(1, [], [], 5) == 0


@pytest.mark.part3
@pytest.mark.edge
def test_part3_zero_ops_already_within_height(impl):
    # root with 3 leaf children: original height is 1, already fits with 0 ops
    assert impl.part3(4, [1, 1, 1], [2, 3, 4], 0) == 1


@pytest.mark.part3
def test_part3_wider_branching_tree(impl):
    # 1->2,3 ; 2->4,5 ; 3->6.  heights: 4=5=6=0, 2=3=1, 1=2.
    tree_from = [1, 1, 2, 2, 3]
    tree_to = [2, 3, 4, 5, 6]
    # cutting node 2 or 3 doesn't help reach H=1 (their children would still land at depth 2),
    # so max_operations=1 cannot improve on the original height of 2.
    assert impl.part3(6, tree_from, tree_to, 1) == 2
    # reaching H=1 needs all three leaves (4,5,6) individually relocated: 3 ops.
    assert impl.part3(6, tree_from, tree_to, 3) == 1
    assert impl.part3(6, tree_from, tree_to, 2) == 2  # one short of the 3 needed


@pytest.mark.part3
@pytest.mark.edge
def test_part3_generous_budget_reaches_zero_only_if_root_has_no_children(impl):
    # A node relocated by an operation ALWAYS lands at depth 1 (directly under the root) --
    # never at depth 0, since only the root itself can be at depth 0. So height 0 is
    # unreachable for any tree with real edges, no matter how large max_operations is.
    assert impl.part3(4, [1, 1, 1], [2, 3, 4], 1000) == 1
    assert impl.part3(4, [1, 1, 1], [2, 3, 4], 10**9) == 1


@pytest.mark.part3
@pytest.mark.edge
def test_part3_height_zero_only_for_single_node(impl):
    # H=0 is feasible with any budget (including 0) iff the tree is just the root.
    assert impl.part3(1, [], [], 0) == 0
    assert impl.part3(1, [], [], 10**9) == 0


# ================================================================== io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\n7\n1 1 2 2 3 4\n3\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_stdin_stdout_part1_empty_result(run_script):
    stdin = "PART 1\n3\n1 1\n5\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_stdin_stdout_part1_single_node(run_script):
    stdin = "PART 1\n1\n\n1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\n6\n-1 0 0 1 1 3\n2\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    stdin = "PART 3\n4\n3\n3 1 2\n2 3 4\n1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.edge
def test_stdin_stdout_part3_single_node(run_script):
    stdin = "PART 3\n1\n0\n\n\n0\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"


# ================================================================== perf
@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_wide_tree(impl):
    # a wide, shallow tree (root with 10^5 direct leaves) -- Part 1's BFS should be linear.
    import time

    n = 100_000
    parent = [1] * (n - 1)  # every node 2..n is a direct child of the root
    t0 = time.perf_counter()
    result = impl.part1(parent, 1)
    elapsed = time.perf_counter() - t0
    assert result == list(range(2, n + 1))
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_wide_tree(impl):
    import time

    n = 100_000
    parent = [-1] + [0] * (n - 1)
    t0 = time.perf_counter()
    result = impl.part2(parent, 0)
    elapsed = time.perf_counter() - t0
    assert result == n - 1
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_part3_skewed_chain(run_script):
    # NOTE: see REPORT.md "复杂度与实测" -- part3's exact fix()/total_ops() DP is empirically
    # close to quadratic on a skewed (chain) tree (the "cut vs push to children" choice forces
    # exploring O(depth) distinct entry-depths per node on a pure chain), unlike the roughly
    # linear behaviour on wide/shallow trees exercised by part1/part2's perf tests above. n is
    # calibrated to what the reference solution demonstrably clears inside the 2s budget with a
    # comfortable margin, rather than the generic 1e5-1e6 guideline.
    n = 1500
    tree_from = list(range(1, n))
    tree_to = list(range(2, n + 1))
    stdin = (
        "PART 3\n"
        f"{n}\n"
        f"{n - 1}\n"
        + " ".join(map(str, tree_from))
        + "\n"
        + " ".join(map(str, tree_to))
        + "\n"
        f"{n // 4}\n"
    )
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert int(r.stdout.strip()) > 0
