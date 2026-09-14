import random

import pytest

EX1 = [-1, 0, 0, 1, 1]
EX1_TRACE = [
    "0->1:GET_COUNT",
    "0->2:GET_COUNT",
    "1->3:GET_COUNT",
    "1->4:GET_COUNT",
    "2->0:REPORT 1",
    "3->1:REPORT 1",
    "4->1:REPORT 1",
    "1->0:REPORT 3",
    "ROOT_COUNT:5",
]
EX_ROOT_NOT_ZERO = [1, -1, 1, 0]
EX_ROOT_NOT_ZERO_TRACE = [
    "1->0:GET_COUNT",
    "1->2:GET_COUNT",
    "0->3:GET_COUNT",
    "2->1:REPORT 1",
    "3->0:REPORT 1",
    "0->1:REPORT 2",
    "ROOT_COUNT:4",
]


def _random_tree(rng, n):
    base = [-1] + [rng.randrange(0, i) for i in range(1, n)]
    perm = list(range(n))
    rng.shuffle(perm)
    parent = [-1] * n
    for i, p in enumerate(base):
        parent[perm[i]] = -1 if p == -1 else perm[p]
    return parent


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_source_trace(impl):
    assert impl.simulate_tree_count(EX1) == EX1_TRACE


@pytest.mark.part1
def test_root_not_at_index_zero(impl):
    assert impl.simulate_tree_count(EX_ROOT_NOT_ZERO) == EX_ROOT_NOT_ZERO_TRACE


@pytest.mark.part1
@pytest.mark.edge
def test_single_node(impl):
    assert impl.simulate_tree_count([-1]) == ["ROOT_COUNT:1"]


@pytest.mark.part1
@pytest.mark.edge
def test_two_nodes(impl):
    assert impl.simulate_tree_count([-1, 0]) == ["0->1:GET_COUNT", "1->0:REPORT 1", "ROOT_COUNT:2"]


@pytest.mark.part1
@pytest.mark.edge
def test_chain_reports_bubble_up(impl):
    out = impl.simulate_tree_count([-1, 0, 1, 2])
    assert out == [
        "0->1:GET_COUNT",
        "1->2:GET_COUNT",
        "2->3:GET_COUNT",
        "3->2:REPORT 1",
        "2->1:REPORT 2",
        "1->0:REPORT 3",
        "ROOT_COUNT:4",
    ]


@pytest.mark.part1
@pytest.mark.edge
def test_children_sent_in_increasing_id_order(impl):
    out = impl.simulate_tree_count([-1, 0, 0, 0])
    assert out[:3] == ["0->1:GET_COUNT", "0->2:GET_COUNT", "0->3:GET_COUNT"]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("bad", [[], [0], [-1, -1], [-1, 5], [1, 2, 0, -1], [-1, 1]])
def test_invalid_parent_arrays_raise(impl, bad):
    with pytest.raises(ValueError):
        impl.simulate_tree_count(bad)


@pytest.mark.part1
@pytest.mark.edge
def test_random_trees_count_and_message_budget(impl):
    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(1, 40)
        out = impl.simulate_tree_count(_random_tree(rng, n))
        assert out[-1] == f"ROOT_COUNT:{n}"
        assert len(out) == 2 * (n - 1) + 1  # one GET_COUNT and one REPORT per edge


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_lost_once_then_retried(impl):
    assert impl.simulate_tree_count(EX1, {0}) == [
        "0->1:GET_COUNT LOST",
        "0->2:GET_COUNT",
        "0->1:GET_COUNT",
        "2->0:REPORT 1",
        "1->3:GET_COUNT",
        "1->4:GET_COUNT",
        "3->1:REPORT 1",
        "4->1:REPORT 1",
        "1->0:REPORT 3",
        "ROOT_COUNT:5",
    ]


@pytest.mark.part2
def test_part2_retry_also_lost_gives_partial(impl):
    assert impl.simulate_tree_count(EX1, {0, 2}) == [
        "0->1:GET_COUNT LOST",
        "0->2:GET_COUNT",
        "0->1:GET_COUNT GIVEUP",
        "2->0:REPORT 1",
        "ROOT_COUNT:2 PARTIAL",
    ]


@pytest.mark.part2
def test_part2_lost_report_is_retried(impl):
    out = impl.simulate_tree_count(EX1, {6})
    assert "4->1:REPORT 1 LOST" in out
    assert out[-1] == "ROOT_COUNT:5"


@pytest.mark.part2
@pytest.mark.edge
def test_part2_leaf_given_up_mid_tree(impl):
    out = impl.simulate_tree_count(EX1, {1, 4})
    assert "0->2:GET_COUNT GIVEUP" in out
    assert out[-1] == "ROOT_COUNT:4 PARTIAL"


@pytest.mark.part2
@pytest.mark.edge
def test_part2_no_drops_equals_part1(impl):
    assert impl.simulate_tree_count(EX1, set()) == EX1_TRACE


@pytest.mark.part2
@pytest.mark.edge
def test_part2_random_invariants(impl):
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 30)
        parent = _random_tree(rng, n)
        drops = {rng.randrange(0, 4 * n) for _ in range(rng.randint(0, 5))}
        out = impl.simulate_tree_count(parent, drops)
        assert out[-1].startswith("ROOT_COUNT:")
        gave_up = any(line.endswith(" GIVEUP") for line in out)
        assert out[-1].endswith(" PARTIAL") == gave_up
        count = int(out[-1].split(":")[1].split()[0])
        assert (count == n) if not gave_up else (1 <= count < n)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_nodes(run_script):
    rng = random.Random(0)
    n = 100_000
    parent = [-1] + [rng.randrange(max(0, i - 50), i) for i in range(1, n)]
    r = run_script("PART 1\n" + " ".join(map(str, parent)) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[-1] == f"ROOT_COUNT:{n}"
    assert len(lines) == 2 * (n - 1) + 1
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n-1 0 0 1 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_TRACE) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n-1 0 0 1 1\nDROPS 0 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[-1] == "ROOT_COUNT:2 PARTIAL"
