import random

import pytest


# ---------------------------------------------------------------- worked examples (both parts)
EXAMPLES = [
    ([1, 2], [1, 2], 3),
    ([5, 1], [3, 1], 5),
    ([5, 100, 1], [3, 1, 1], 5),
    ([1, 1, 1000], [2, 1, 1], 2),  # queueing beats the free server
]


@pytest.mark.part1
def test_part1_worked_examples(impl):
    for cost, time_, expected in EXAMPLES:
        assert impl.part1(cost, time_) == expected, (cost, time_)


@pytest.mark.part2
def test_part2_worked_examples(impl):
    for cost, time_, expected in EXAMPLES:
        assert impl.part2(cost, time_) == expected, (cost, time_)


# ---------------------------------------------------------------- edge cases
@pytest.mark.part1
@pytest.mark.edge
def test_part1_empty_and_single(impl):
    assert impl.part1([], []) == 0
    assert impl.part1([7], [3]) == 7
    assert impl.part1([0], [0]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_part2_empty_and_single(impl):
    assert impl.part2([], []) == 0
    assert impl.part2([7], [3]) == 7
    assert impl.part2([0], [0]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_part2_zero_time_forces_repeatedly(impl):
    # time[i] = 0 means the paid server is instantly free again -> next task can also be forced.
    assert impl.part2([1, 1, 1000], [0, 0, 0]) == 1002


@pytest.mark.part2
@pytest.mark.edge
def test_part2_huge_values_stay_exact(impl):
    # 1e9-scale cost/time: no float accumulation allowed.
    cost = [1_000_000_000, 1_000_000_000]
    time_ = [1_000_000_000, 1_000_000_000]
    # task0 forced: cost 1e9, free_at=1e9 (way beyond i=1, so task1 is a genuine choice)
    # cheapest is to skip task1 for free
    assert impl.part2(cost, time_) == 1_000_000_000


@pytest.mark.part2
@pytest.mark.edge
def test_part2_queueing_beats_free_server_variant(impl):
    # A second "queueing wins" construction with different numbers, hand-traced state by state:
    # task0 forced: cost=2, free_at=3.
    # task1 (i=1, free_at=3>1, choice): skip keeps free_at=3, cost=2.
    # task2 (i=2, free_at=3>2, choice): if we NAIVELY skip again, free_at stays 3 and task3
    #   (i=3, free_at=3<=3) is forced to pay cost[3]=500 -> total 2+500=502.
    #   Instead QUEUE task2 (cost+=1 -> 3, free_at=3+1=4): task3 (i=3, free_at=4>3) is now a
    #   genuine choice, and skipping it for free wins -> total cost = 2+1 = 3.
    # So the optimum queues task2 (not task1) to push the paid server's idle point past task3.
    cost = [2, 3, 1, 500]
    time_ = [3, 2, 1, 1]
    assert impl.part1(cost, time_) == 3
    assert impl.part2(cost, time_) == 3


# ---------------------------------------------------------------- part1 vs part2 cross-check
@pytest.mark.part2
def test_part1_part2_agree_random(impl):
    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(0, 12)
        cost = [rng.randint(0, 30) for _ in range(n)]
        time_ = [rng.randint(0, 6) for _ in range(n)]
        assert impl.part1(cost, time_) == impl.part2(cost, time_), (cost, time_)


@pytest.mark.part2
@pytest.mark.edge
def test_part1_part2_agree_on_worked_examples(impl):
    for cost, time_, expected in EXAMPLES:
        a, b = impl.part1(cost, time_), impl.part2(cost, time_)
        assert a == b == expected, (cost, time_, a, b)


# ---------------------------------------------------------------- fmt / io
@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_exact(run_script):
    stdin = "PART 2\n3\n5 100 1\n3 1 1\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\n2\n1 2\n1 2\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.edge
def test_stdin_stdout_empty_arrays(run_script):
    stdin = "PART 2\n0\n\n\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.edge
def test_stdin_stdout_n_zero_no_trailing_lines(run_script):
    # arrays entirely omitted, not even blank lines
    stdin = "PART 2\n0\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2(run_script):
    # NOTE: see REPORT.md "复杂度与实测" for why this problem's exact Pareto-frontier DP is
    # empirically O(n * frontier_size) with frontier_size growing close to linearly in n even
    # under uniform random data (not just adversarial inputs) -- there is no known sub-quadratic
    # exact algorithm for this formalization. n is sized to what the reference solution
    # demonstrably clears inside the 2s budget on this machine, with a comfortable margin,
    # rather than the generic 1e5-1e6 guideline.
    rng = random.Random(0)
    n = 1200
    cost = [rng.randint(1, 10**6) for _ in range(n)]
    time_ = [rng.randint(0, 9) for _ in range(n)]
    stdin = "PART 2\n" + f"{n}\n" + " ".join(map(str, cost)) + "\n" + " ".join(map(str, time_)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert int(r.stdout.strip()) > 0
