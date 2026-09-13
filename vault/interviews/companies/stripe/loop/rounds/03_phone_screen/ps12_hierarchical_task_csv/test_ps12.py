import pytest

# ---------------------------------------------------------------- shared fixtures / examples
P1_LINES = [
    "01/01/2025,task,T1,cook dinner",
    "01/01/2025,task,T2,walk the dog",
]
P1_OUT = ["T1 cook dinner", "T2 walk the dog"]

P2_LINES = [
    "01/01/2025,task,T1,cook dinner",
    "01/01/2025,subtask,T1,T2,buy groceries",
    "01/01/2025,subtask,T1,T3,prepare meal",
]
P2_OUT = ["T1 cook dinner", "├─ T2 buy groceries", "├─ T3 prepare meal"]

P3_LINES = P2_LINES  # same input shape, different (fixed) rendering rule
P3_OUT = ["T1 cook dinner", "├─ T2 buy groceries", "└─ T3 prepare meal"]

P4_LINES = [
    "01/01/2025,task,T1,cook dinner",
    "01/01/2025,subtask,T1,T2,buy groceries",
    "01/01/2025,subtask,T2,T4,buy milk",
    "01/01/2025,subtask,T1,T3,prepare meal",
]
P4_OUT = [
    "T1 cook dinner",
    "├─ T2 buy groceries",
    "│  └─ T4 buy milk",
    "└─ T3 prepare meal",
]


# ---------------------------------------------------------------- Part 1: roots only
@pytest.mark.part1
def test_example_multiple_roots(impl):
    assert impl.part1(P1_LINES) == P1_OUT


@pytest.mark.part1
def test_single_root(impl):
    assert impl.part1(["01/01/2025,task,T1,solo task"]) == ["T1 solo task"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input(impl):
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_blank_lines_ignored(impl):
    lines = ["01/01/2025,task,T1,a", "", "  ", "01/01/2025,task,T2,b"]
    assert impl.part1(lines) == ["T1 a", "T2 b"]


@pytest.mark.part1
@pytest.mark.fmt
def test_quoted_comma_and_escaped_quote_in_name(impl):
    lines = [
        '01/01/2025,task,T1,"cook dinner, tonight"',
        '01/01/2025,task,T2,"say ""hi"" now"',
    ]
    assert impl.part1(lines) == ["T1 cook dinner, tonight", 'T2 say "hi" now']


# ---------------------------------------------------------------- Part 2: naive uniform connector
@pytest.mark.part2
def test_example_uniform_connector(impl):
    assert impl.part2(P2_LINES) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_root_with_zero_subtasks(impl):
    assert impl.part2(["01/01/2025,task,T1,alone"]) == ["T1 alone"]


@pytest.mark.part2
@pytest.mark.edge
def test_root_with_one_subtask_still_gets_non_final_connector(impl):
    lines = ["01/01/2025,task,T1,a", "01/01/2025,subtask,T1,T2,b"]
    assert impl.part2(lines) == ["T1 a", "├─ T2 b"]  # NOT "└─ " -- that's part3's fix


@pytest.mark.part2
def test_multiple_roots_independent_subtask_lists(impl):
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,a-child",
        "01/01/2025,task,T3,b",
        "01/01/2025,subtask,T3,T4,b-child",
    ]
    assert impl.part2(lines) == ["T1 a", "├─ T2 a-child", "T3 b", "├─ T4 b-child"]


# ---------------------------------------------------------------- Part 3: fixed last-child connector
@pytest.mark.part3
def test_example_fixed_connector(impl):
    assert impl.part3(P3_LINES) == P3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_root_with_zero_subtasks_part3(impl):
    assert impl.part3(["01/01/2025,task,T1,alone"]) == ["T1 alone"]


@pytest.mark.part3
@pytest.mark.edge
def test_single_subtask_gets_final_connector(impl):
    lines = ["01/01/2025,task,T1,a", "01/01/2025,subtask,T1,T2,only child"]
    assert impl.part3(lines) == ["T1 a", "└─ T2 only child"]  # first AND last -> "last" wins


@pytest.mark.part3
def test_three_subtasks_only_last_is_final(impl):
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,x",
        "01/01/2025,subtask,T1,T3,y",
        "01/01/2025,subtask,T1,T4,z",
    ]
    assert impl.part3(lines) == ["T1 a", "├─ T2 x", "├─ T3 y", "└─ T4 z"]


# ---------------------------------------------------------------- Part 4: arbitrary depth
@pytest.mark.part4
def test_example_two_level_nesting(impl):
    assert impl.part4(P4_LINES) == P4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_three_level_chain(impl):
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,b",
        "01/01/2025,subtask,T2,T3,c",
        "01/01/2025,subtask,T3,T4,d",
    ]
    assert impl.part4(lines) == [
        "T1 a",
        "└─ T2 b",
        "   └─ T3 c",
        "      └─ T4 d",
    ]


@pytest.mark.part4
@pytest.mark.edge
def test_non_final_branch_propagates_continuation_bar_through_deep_descendants(impl):
    # T2 is a NON-final child of T1 (T5 follows it); every descendant of T2 must carry "│  ",
    # not three spaces, at that ancestor level -- regardless of how deep T2's own subtree goes.
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,b",
        "01/01/2025,subtask,T2,T3,c",
        "01/01/2025,subtask,T3,T4,d",
        "01/01/2025,subtask,T1,T5,e",
    ]
    assert impl.part4(lines) == [
        "T1 a",
        "├─ T2 b",
        "│  └─ T3 c",
        "│     └─ T4 d",
        "└─ T5 e",
    ]


@pytest.mark.part4
@pytest.mark.edge
def test_middle_node_final_but_has_its_own_children(impl):
    # T3 is the LAST child of T1 (so gets "└─ ") but itself has a child T4 -- T4's ancestor
    # prefix must be three spaces (T3 was final), not "│  ".
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,b",
        "01/01/2025,subtask,T1,T3,c",
        "01/01/2025,subtask,T3,T4,d",
    ]
    assert impl.part4(lines) == [
        "T1 a",
        "├─ T2 b",
        "└─ T3 c",
        "   └─ T4 d",
    ]


@pytest.mark.part4
@pytest.mark.fmt
def test_timestamps_are_not_a_sort_key(impl):
    # Input order is T2, T3, T4 -- but their timestamps DECREASE. Output must still follow
    # input order, never timestamp order (which would print T3, T4, T2 or similar).
    lines = [
        "01/01/2025,task,T1,root",
        "03/01/2025,subtask,T1,T2,first-in-input-latest-timestamp",
        "02/01/2025,subtask,T1,T3,second-in-input-middle-timestamp",
        "01/01/2025,subtask,T1,T4,third-in-input-earliest-timestamp",
    ]
    out = impl.part4(lines)
    assert out == [
        "T1 root",
        "├─ T2 first-in-input-latest-timestamp",
        "├─ T3 second-in-input-middle-timestamp",
        "└─ T4 third-in-input-earliest-timestamp",
    ]


@pytest.mark.part4
@pytest.mark.edge
def test_multiple_roots_each_with_nested_trees(impl):
    lines = [
        "01/01/2025,task,T1,a",
        "01/01/2025,subtask,T1,T2,a1",
        "01/01/2025,task,T3,b",
        "01/01/2025,subtask,T3,T4,b1",
        "01/01/2025,subtask,T4,T5,b1a",
    ]
    assert impl.part4(lines) == [
        "T1 a",
        "└─ T2 a1",
        "T3 b",
        "└─ T4 b1",
        "   └─ T5 b1a",
    ]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_OUT) + "\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    r = run_script("PART 4\n" + "\n".join(P4_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.edge
def test_deep_chain_no_recursion_error(impl):
    # A chain deeper than Python's default recursion limit (1000) -- a naive recursive renderer
    # raises RecursionError here; the reference solution's explicit-stack DFS does not. Kept at a
    # moderate depth (not the perf test's 2*10**5) because ancestor-prefix length grows linearly
    # per level, so total output size is O(depth**2) -- a 200k-deep chain would be gigabytes.
    depth = 2000
    lines = ["01/01/2025,task,T0,root"]
    for i in range(1, depth):
        lines.append(f"01/01/2025,subtask,T{i - 1},T{i},n{i}")
    out = impl.part4(lines)
    assert len(out) == depth
    assert out[0] == "T0 root"
    assert out[1] == "└─ T1 n1"
    assert out[-1] == ("   " * (depth - 2)) + f"└─ T{depth - 1} n{depth - 1}"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_200k_wide_tree(run_script):
    # A single root with 199,999 direct children (one level -- total output stays O(n), unlike a
    # deep chain where ancestor-prefix length would make output O(n**2)). Exercises parsing +
    # rendering volume at the stated 2*10**5-line budget.
    n = 200_000
    lines = ["01/01/2025,task,T0,root"]
    for i in range(1, n):
        lines.append(f"01/01/2025,subtask,T0,T{i},node {i}")
    r = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out_lines = r.stdout.splitlines()
    assert len(out_lines) == n
    assert out_lines[0] == "T0 root"
    assert out_lines[1] == "├─ T1 node 1"
    assert out_lines[-1] == f"└─ T{n - 1} node {n - 1}"
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
