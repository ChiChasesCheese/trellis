import random

import pytest

MOD = 1_000_000_007


def _brute(nums, k):
    """Try every way to split up to k doublings across the elements."""
    best = 0

    def rec(i, left, acc):
        nonlocal best
        if i == len(nums):
            best = max(best, acc)
            return
        for t in range(left + 1):
            rec(i + 1, left - t, acc | (nums[i] << t))

    rec(0, k, 0)
    return best


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "nums,k,expected",
    [
        ([12, 9], 1, 30),     # source example; doubling the largest gives only 25
        ([8, 1, 2], 2, 35),   # LC 2680 example 2
        ([5], 3, 40),
        ([1, 2, 4], 0, 7),
    ],
)
def test_worked_examples(impl, nums, k, expected):
    assert impl.max_or_sum(nums, k) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_doubling_the_largest_is_not_always_optimal(impl):
    assert (24 | 9) == 25
    assert impl.max_or_sum([12, 9], 1) == 30


@pytest.mark.part1
@pytest.mark.edge
def test_all_zeros(impl):
    assert impl.max_or_sum([0, 0, 0], 5) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_equal_elements(impl):
    assert impl.max_or_sum([3, 3, 3], 2) == (3 << 2) | 3


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("nums,k", [([], 1), ([1], -1), ([2 ** 31], 1), ([-1], 0)])
def test_invalid_input_raises(impl, nums, k):
    with pytest.raises(ValueError):
        impl.max_or_sum(nums, k)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_splitting_brute_force(impl):
    rng = random.Random(0)
    for _ in range(800):
        nums = [rng.randint(0, 40) for _ in range(rng.randint(1, 5))]
        k = rng.randint(0, 5)
        assert impl.max_or_sum(nums, k) == _brute(nums, k), (nums, k)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(0)
    n, k = 100_000, 15
    nums = " ".join(str(rng.randint(0, 2 ** 31 - 1)) for _ in range(n))
    r = run_script(f"PART 1\n{n} {k}\n{nums}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout) > 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_small_k_matches_exact(impl):
    assert impl.max_or_sum_mod([12, 9], 1) == 30
    assert impl.max_or_sum_mod([8, 1, 2], 2) == 35


@pytest.mark.part2
@pytest.mark.edge
def test_part2_large_k_worked_examples(impl):
    assert impl.max_or_sum_mod([12, 9], 10 ** 9) == 687500014
    assert impl.max_or_sum_mod([3, 3, 1], 100) == 929113844


@pytest.mark.part2
@pytest.mark.edge
def test_part2_agrees_with_exact_modulo_across_threshold(impl):
    rng = random.Random(1)
    for _ in range(1500):
        n = rng.randint(1, 20)
        k = rng.choice([rng.randint(0, 80), rng.randint(60, 130)])
        nums = [rng.randint(0, 2 ** 31 - 1) if rng.random() < 0.5 else rng.randint(0, 64) for _ in range(n)]
        assert impl.max_or_sum_mod(nums, k) == impl.max_or_sum(nums, k) % MOD, (nums, k)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_tie_on_largest_value_uses_others_or(impl):
    # both 6s are the largest; shifting the one whose "others" include 1 wins
    nums = [6, 1, 6]
    assert impl.max_or_sum_mod(nums, 200) == impl.max_or_sum(nums, 200) % MOD


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k_huge_k(run_script):
    rng = random.Random(2)
    n, k = 100_000, 10 ** 9
    nums = " ".join(str(rng.randint(0, 2 ** 31 - 1)) for _ in range(n))
    r = run_script(f"PART 2\n{n} {k}\n{nums}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert 0 <= int(r.stdout) < MOD
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n2 1\n12 9\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "30\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n2 1000000000\n12 9\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "687500014\n"
