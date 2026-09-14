import random

import pytest

# ------------------------------------------------------------------------ worked examples
EX1_PRIV = [["A"], ["B"], ["C"]]
EX1_GRANTS = [[0, 1], [1, 2]]
EX1_OUT = [["A"], ["A", "B"], ["A", "B", "C"]]

EX2_EDGES = [[0, 1], [0, 2], [1, 3], [2, 3]]
EX2_ALLOW = [["P"], [], [], []]
EX2_DENY = [[], [], ["P"], []]
EX2_OUT = [["P"], ["P"], [], []]

EX3_ALLOW = [["P"], [], [], []]
EX3_DENY = [["P"], [], [], []]
EX3_GLOBAL_OUT = [[], [], [], []]
EX3_LOCAL_OUT = [[], ["P"], ["P"], ["P"]]

EX4_PRIV = [["read"], ["write"], []]
EX4_GRANTS = [[0, 1]]
EX4_EFFECTIVE = [["read"], ["read", "write"], []]
EX4_ASSIGNMENTS = [("alice", 0), ("bob", 1), ("carol", 2)]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.get_effective_privileges(EX1_PRIV, EX1_GRANTS) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_empty_graph(impl):
    assert impl.get_effective_privileges([], []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_no_privileges_anywhere(impl):
    assert impl.get_effective_privileges([[], []], [[0, 1]]) == [[], []]


@pytest.mark.part1
@pytest.mark.edge
def test_diamond_dag_unions_both_parent_chains(impl):
    # 0 and 1 both feed into 2 (diamond via a shared-ish shape): 3 has two independent parents
    # 0 -> 2, 1 -> 3, 2 -> 3 style: node 3 must get BOTH chains' privileges, not just one
    privileges = [["A"], ["B"], [], []]
    grants = [[0, 2], [1, 3], [2, 3]]
    result = impl.get_effective_privileges(privileges, grants)
    assert result[3] == ["A", "B"]


@pytest.mark.part1
@pytest.mark.edge
def test_cycle_raises(impl):
    with pytest.raises(ValueError):
        impl.get_effective_privileges([["A"], ["B"]], [[0, 1], [1, 0]])


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_range_edge_raises(impl):
    with pytest.raises(ValueError):
        impl.get_effective_privileges([["A"], ["B"]], [[0, 5]])


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_2(impl):
    assert impl.get_effective_access(EX2_ALLOW, EX2_DENY, EX2_EDGES) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_deny_propagates_from_any_ancestor_not_just_direct_parent(impl):
    # deny declared far up the chain must still block a distant descendant
    allow = [["P"], [], [], []]
    deny = [["P"], [], [], []]
    assert impl.get_effective_access(allow, deny, EX2_EDGES) == EX3_GLOBAL_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_no_allow_anywhere_is_empty_everywhere(impl):
    n = 3
    allow = [[] for _ in range(n)]
    deny = [[] for _ in range(n)]
    assert impl.get_effective_access(allow, deny, [[0, 1], [1, 2]]) == [[], [], []]


@pytest.mark.part2
@pytest.mark.edge
def test_cycle_raises(impl):
    with pytest.raises(ValueError):
        impl.get_effective_access([["A"], []], [[], []], [[0, 1], [1, 0]])


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_3_local_deny(impl):
    assert impl.get_effective_access_local_deny(EX3_ALLOW, EX3_DENY, EX2_EDGES) == EX3_LOCAL_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_part2_and_part3_diverge_on_same_input(impl):
    global_out = impl.get_effective_access(EX3_ALLOW, EX3_DENY, EX2_EDGES)
    local_out = impl.get_effective_access_local_deny(EX3_ALLOW, EX3_DENY, EX2_EDGES)
    assert global_out != local_out
    assert global_out == EX3_GLOBAL_OUT
    assert local_out == EX3_LOCAL_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_part2_and_part3_agree_when_deny_only_on_leaves(impl):
    # deny only ever declared on a leaf (no descendants) -> nothing to propagate -> same result
    allow = [["P"], [], [], []]
    deny = [[], [], [], ["P"]]  # only the leaf "service" denies
    g = impl.get_effective_access(allow, deny, EX2_EDGES)
    l = impl.get_effective_access_local_deny(allow, deny, EX2_EDGES)
    assert g == l == [["P"], ["P"], ["P"], []]


@pytest.mark.part3
@pytest.mark.edge
def test_local_deny_out_of_range_edge_raises(impl):
    with pytest.raises(ValueError):
        impl.get_effective_access_local_deny([["A"], []], [[], []], [[0, 9]])


# ------------------------------------------------------------------------ Part 4
@pytest.mark.part4
def test_worked_example_4_users_with_privilege(impl):
    assert impl.users_with_privilege(EX4_EFFECTIVE, EX4_ASSIGNMENTS, "read") == ["alice", "bob"]


@pytest.mark.part4
def test_worked_example_4_filter_users_by_role(impl):
    assert impl.filter_users_by_role(EX4_ASSIGNMENTS, 1) == ["bob"]


@pytest.mark.part4
@pytest.mark.edge
def test_users_with_privilege_dedupes_multi_role_user(impl):
    effective = [["read"], ["read"]]
    assignments = [("alice", 0), ("alice", 1), ("bob", 1)]
    assert impl.users_with_privilege(effective, assignments, "read") == ["alice", "bob"]


@pytest.mark.part4
@pytest.mark.edge
def test_users_with_privilege_no_holders_returns_empty(impl):
    assert impl.users_with_privilege([["read"]], [("alice", 0)], "write") == []


@pytest.mark.part4
@pytest.mark.edge
def test_users_with_privilege_unknown_role_raises(impl):
    with pytest.raises(ValueError):
        impl.users_with_privilege([["read"]], [("alice", 3)], "read")


@pytest.mark.part4
@pytest.mark.edge
def test_filter_users_by_role_unknown_role_returns_empty_not_error(impl):
    # asymmetric on purpose: role_id here is a free filter key, not a declared catalog lookup
    assert impl.filter_users_by_role(EX4_ASSIGNMENTS, 99) == []


@pytest.mark.part4
@pytest.mark.edge
def test_filter_users_by_role_dedupes_repeated_assignment(impl):
    assert impl.filter_users_by_role([("bob", 1), ("bob", 1), ("alice", 2)], 1) == ["bob"]


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_strings_exact(impl):
    out = impl.part1(["3", "A", "B", "C", "2", "0 1", "1 2"])
    assert out == ["A", "A,B", "A,B,C"]


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_dash_placeholder_for_empty(impl):
    # 2 roles, no privileges, 0 edges
    out = impl.part1(["2", "-", "-", "0"])
    assert out == ["-", "-"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["3", "A", "B", "C", "2", "0 1", "1 2"]
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "A\nA,B\nA,B,C\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["4", "P", "-", "-", "-", "-", "-", "P", "-", "4", "0 1", "0 2", "1 3", "2 3"]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "P\nP\n-\n-\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    body = ["4", "P", "-", "-", "-", "P", "-", "-", "-", "4", "0 1", "0 2", "1 3", "2 3"]
    r = run_script("PART 3\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "-\nP\nP\nP\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact_part4(run_script):
    body = [
        "3", "read", "write", "-",
        "1", "0 1",
        "3", "alice 0", "bob 1", "carol 2",
        "2", "PRIV read", "ROLE 1",
    ]
    r = run_script("PART 4\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "alice,bob\nbob\n"


# ------------------------------------------------------------------------ perf
@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_node_binary_tree_dag(run_script):
    # a balanced binary-tree-shaped DAG keeps each node's ancestor chain O(log n) deep, so total
    # DP work stays near-linear -- a long single chain would make the OUTPUT itself O(n^2), which
    # is inherent to the problem, not something an implementation can avoid.
    n = 100_000
    lines = [str(n)]
    lines.extend(f"p{i}" for i in range(n))
    edges = [(i - 1) // 2 for i in range(1, n)]
    lines.append(str(n - 1))
    lines.extend(f"{parent} {child}" for child, parent in enumerate(edges, start=1))
    result = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == n
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_assignments_reverse_query(run_script):
    rng = random.Random(0)
    n_roles = 200
    lines = [str(n_roles)]
    lines.extend(f"perm{i % 50}" for i in range(n_roles))
    lines.append("0")  # no grants -- keep Part1 cost negligible so this isolates Part4's cost
    n_assign = 100_000
    lines.append(str(n_assign))
    for i in range(n_assign):
        role = rng.randrange(n_roles)
        lines.append(f"user{i} {role}")
    lines.append("1")
    lines.append("PRIV perm0")
    result = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 1
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
