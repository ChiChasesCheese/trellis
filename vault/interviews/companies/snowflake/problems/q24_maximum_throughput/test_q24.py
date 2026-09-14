import itertools
import random

import pytest


def _brute(throughput, cost, budget):
    n = len(throughput)
    max_x = [budget // c for c in cost]
    best = 0
    for combo in itertools.product(*[range(m + 1) for m in max_x]):
        spent = sum(x * c for x, c in zip(combo, cost))
        if spent <= budget:
            capacities = [t * (1 + x) for t, x in zip(throughput, combo)]
            best = max(best, min(capacities))
    return best


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    assert impl.max_min_throughput([2, 10], [1, 100], 5) == 10


@pytest.mark.part1
@pytest.mark.edge
def test_zero_budget_leaves_bottleneck_unchanged(impl):
    assert impl.max_min_throughput([3, 7, 2], [1, 1, 1], 0) == 2


@pytest.mark.part1
@pytest.mark.edge
def test_single_service(impl):
    # budget 26, cost 1 per upgrade -> 26 upgrades -> throughput * 27
    assert impl.max_min_throughput([1], [1], 26) == 27


@pytest.mark.part1
@pytest.mark.edge
def test_already_uniform_throughput(impl):
    assert impl.max_min_throughput([5, 5, 5], [1, 2, 3], 0) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_upgrading_expensive_service_not_worth_it(impl):
    # service 1 costs 100/upgrade; with budget 5 it's cheaper to bring service 0 up to match
    assert impl.max_min_throughput([2, 10], [1, 100], 3) == 8  # 2*(1+3)=8 <= 10


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "throughput,scaling_cost,budget",
    [
        ([], [], 5),
        ([1], [1, 2], 5),
        ([0], [1], 5),
        ([1], [0], 5),
        ([1], [1], -1),
    ],
)
def test_invalid_input_raises(impl, throughput, scaling_cost, budget):
    with pytest.raises(ValueError):
        impl.max_min_throughput(throughput, scaling_cost, budget)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 3)
        throughput = [rng.randint(1, 8) for _ in range(n)]
        scaling_cost = [rng.randint(1, 8) for _ in range(n)]
        budget = rng.randint(0, 15)
        assert impl.max_min_throughput(throughput, scaling_cost, budget) == _brute(throughput, scaling_cost, budget), (
            throughput, scaling_cost, budget,
        )


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k_services(run_script):
    rng = random.Random(1)
    n = 100_000
    throughput = [rng.randint(1, 10 ** 6) for _ in range(n)]
    scaling_cost = [rng.randint(1, 10 ** 6) for _ in range(n)]
    budget = 10 ** 12
    stdin = (
        f"PART 1\n{n} {budget}\n"
        + " ".join(map(str, throughput))
        + "\n"
        + " ".join(map(str, scaling_cost))
        + "\n"
    )
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout) >= min(throughput)
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_plan(impl):
    target, upgrades = impl.max_min_throughput_with_plan([2, 10], [1, 100], 5)
    assert target == 10
    assert upgrades == [4, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_plan_is_self_consistent_on_random_inputs(impl):
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 4)
        throughput = [rng.randint(1, 10) for _ in range(n)]
        scaling_cost = [rng.randint(1, 10) for _ in range(n)]
        budget = rng.randint(0, 40)
        target, upgrades = impl.max_min_throughput_with_plan(throughput, scaling_cost, budget)
        assert len(upgrades) == n
        assert all(x >= 0 for x in upgrades)
        capacities = [t * (1 + x) for t, x in zip(throughput, upgrades)]
        cost = sum(x * c for x, c in zip(upgrades, scaling_cost))
        assert min(capacities) == target
        assert cost <= budget
        assert target == impl.max_min_throughput(throughput, scaling_cost, budget)


@pytest.mark.part2
@pytest.mark.edge
def test_zero_budget_plan_is_all_zero_upgrades(impl):
    target, upgrades = impl.max_min_throughput_with_plan([3, 7, 2], [1, 1, 1], 0)
    assert target == 2
    assert upgrades == [0, 0, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.max_min_throughput_with_plan([0], [1], 5)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k_services(run_script):
    rng = random.Random(3)
    n = 100_000
    throughput = [rng.randint(1, 10 ** 6) for _ in range(n)]
    scaling_cost = [rng.randint(1, 10 ** 6) for _ in range(n)]
    budget = 10 ** 12
    stdin = (
        f"PART 2\n{n} {budget}\n"
        + " ".join(map(str, throughput))
        + "\n"
        + " ".join(map(str, scaling_cost))
        + "\n"
    )
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert len(lines) == 2
    assert len(lines[1].split()) == n
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n2 5\n2 10\n1 100\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "10\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n2 5\n2 10\n1 100\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "10\n4 0\n"
