import random

import pytest

EXAMPLE1 = dict(m=2, n=3, cost=[[1, 5, 1], [4, 1, 1]], switch_cost=3)
EXAMPLE2 = dict(m=2, n=1, cost=[[5], [2]], switch_cost=100)
EXAMPLE3 = dict(m=2, n=2, cost=[[1, 100], [100, 1]], switch_cost=1)


def brute_force(m, n, cost, switch_cost):
    """Exhaustive reference used only inside the test suite's own cross-check,
    independent of part1/part2, for small m/n."""
    import itertools

    best = None
    for assign in itertools.product(range(m), repeat=n):
        total = sum(cost[assign[i]][i] for i in range(n))
        total += sum(switch_cost for i in range(1, n) if assign[i] != assign[i - 1])
        if best is None or total < best:
            best = total
    return best


# ---------------------------------------------------------------- Part 1: O(m^2 n) baseline
@pytest.mark.part1
def test_example1_part1(impl):
    e = EXAMPLE1
    assert impl.part1(e["m"], e["n"], e["cost"], e["switch_cost"]) == 6


@pytest.mark.part1
def test_example2_part1(impl):
    e = EXAMPLE2
    assert impl.part1(e["m"], e["n"], e["cost"], e["switch_cost"]) == 2


@pytest.mark.part1
def test_example3_part1(impl):
    e = EXAMPLE3
    assert impl.part1(e["m"], e["n"], e["cost"], e["switch_cost"]) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_n_zero_is_zero_cost(impl):
    assert impl.part1(2, 0, [[], []], 5) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_single_server_no_switching_possible_part1(impl):
    assert impl.part1(1, 3, [[5, 3, 9]], 100) == 17


@pytest.mark.part1
@pytest.mark.edge
def test_switch_cost_zero_degenerates_to_independent_minima(impl):
    cost = [[3, 9, 1], [7, 2, 8], [5, 6, 4]]
    assert impl.part1(3, 3, cost, 0) == 3 + 2 + 1  # col mins: 3(server0),2(server1),1(server0)


@pytest.mark.part1
@pytest.mark.edge
def test_huge_switch_cost_sticks_to_lowest_row_sum_part1(impl):
    # row sums: 6, 30, 100 -> never worth switching off row 0
    cost = [[1, 2, 3], [10, 10, 10], [0, 0, 100]]
    assert impl.part1(3, 3, cost, 10**9) == 6


# ---------------------------------------------------------------- Part 2: O(m n) + reconstruction
@pytest.mark.part2
def test_example1_part2_cost_and_assignment(impl):
    e = EXAMPLE1
    total, assignment = impl.part2(e["m"], e["n"], e["cost"], e["switch_cost"])
    assert total == 6
    assert assignment == [1, 1, 1]


@pytest.mark.part2
def test_example2_part2_cost_and_assignment(impl):
    e = EXAMPLE2
    total, assignment = impl.part2(e["m"], e["n"], e["cost"], e["switch_cost"])
    assert total == 2
    assert assignment == [1]


@pytest.mark.part2
def test_example3_part2_cost_and_assignment(impl):
    e = EXAMPLE3
    total, assignment = impl.part2(e["m"], e["n"], e["cost"], e["switch_cost"])
    assert total == 3
    assert assignment == [0, 1]


@pytest.mark.part2
@pytest.mark.edge
def test_n_zero_returns_empty_assignment(impl):
    assert impl.part2(2, 0, [[], []], 5) == (0, [])


@pytest.mark.part2
@pytest.mark.edge
def test_single_server_no_switching_possible(impl):
    total, assignment = impl.part2(1, 3, [[5, 3, 9]], 100)
    assert total == 17
    assert assignment == [0, 0, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_switch_cost_zero_picks_per_slot_minimum(impl):
    cost = [[3, 9, 1], [7, 2, 8], [5, 6, 4]]
    total, assignment = impl.part2(3, 3, cost, 0)
    assert total == 3 + 2 + 1  # col mins: 3(server0),2(server1),1(server0)
    assert assignment == [0, 1, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_huge_switch_cost_sticks_to_lowest_row_sum(impl):
    cost = [[1, 2, 3], [10, 10, 10], [0, 0, 100]]
    total, assignment = impl.part2(3, 3, cost, 10**9)
    assert total == 6
    assert assignment == [0, 0, 0]


@pytest.mark.part2
@pytest.mark.fmt
def test_tie_break_prefers_not_switching_then_lowest_index(impl):
    # both servers cost identically at every slot and switch_cost is 0 -> every
    # transition ties between "stay" and "switch"; tie-break prefers staying, so
    # the whole assignment must stick to server 0 (lowest index at slot 0).
    cost = [[2, 2, 2], [2, 2, 2]]
    total, assignment = impl.part2(2, 3, cost, 0)
    assert total == 6
    assert assignment == [0, 0, 0]


@pytest.mark.part2
def test_randomized_cross_check_against_part1_and_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        m = rng.randint(1, 4)
        n = rng.randint(1, 6)
        cost = [[rng.randint(0, 9) for _ in range(n)] for _ in range(m)]
        switch_cost = rng.randint(0, 15)
        expected = brute_force(m, n, cost, switch_cost)
        c1 = impl.part1(m, n, cost, switch_cost)
        c2, assignment = impl.part2(m, n, cost, switch_cost)
        assert c1 == expected, (m, n, cost, switch_cost)
        assert c2 == expected, (m, n, cost, switch_cost)
        # assignment must actually realize the returned cost
        total = sum(cost[assignment[i]][i] for i in range(n))
        total += sum(switch_cost for i in range(1, n) if assignment[i] != assignment[i - 1])
        assert total == c2


@pytest.mark.part2
def test_randomized_cross_check_larger_scale(impl):
    rng = random.Random(1)
    for _ in range(30):
        m = rng.randint(2, 15)
        n = rng.randint(1, 15)
        cost = [[rng.randint(0, 50) for _ in range(n)] for _ in range(m)]
        switch_cost = rng.randint(0, 100)
        c1 = impl.part1(m, n, cost, switch_cost)
        c2, _assignment = impl.part2(m, n, cost, switch_cost)
        assert c1 == c2, (m, n, cost, switch_cost)


# ---------------------------------------------------------------- io
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\n2 3 3\n1 5 1\n4 1 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n1 1 1\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\n2 3 3\n1 5 1\n4 1 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_n_zero(run_script):
    stdin = "PART 2\n2 0 5\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_1000x1000(run_script):
    rng = random.Random(0)
    m, n = 1000, 1000
    cost_rows = [[rng.randint(0, 999) for _ in range(n)] for _ in range(m)]
    switch_cost = 37
    lines = ["PART 2", f"{m} {n} {switch_cost}"]
    lines += [" ".join(str(v) for v in row) for row in cost_rows]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out_lines = r.stdout.splitlines()
    assert len(out_lines) == 2
    assignment = [int(x) for x in out_lines[1].split()]
    assert len(assignment) == n
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
