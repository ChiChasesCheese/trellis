import random

import pytest


def _brute_div(nums, k):
    c = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s % k == 0:
                c += 1
    return c


def _brute_sum(nums, k):
    c = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s == k:
                c += 1
    return c


def _brute_longest(nums, k):
    best = (0, -1, -1)
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s == k and (j - i + 1) > best[0]:
                best = (j - i + 1, i, j)
    return best


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.count_subarrays_div_k([4, 5, 0, -2, -3, 1], 5) == 7


@pytest.mark.part1
def test_worked_example_2(impl):
    assert impl.count_subarrays_div_k([5, 0, 0], 5) == 6


@pytest.mark.part1
@pytest.mark.edge
def test_empty_nums(impl):
    assert impl.count_subarrays_div_k([], 5) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_single_element(impl):
    assert impl.count_subarrays_div_k([5], 5) == 1
    assert impl.count_subarrays_div_k([3], 5) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_all_duplicates(impl):
    # [0, 0, 0]: every one of the 6 subarrays sums to a multiple of k
    assert impl.count_subarrays_div_k([0, 0, 0], 7) == 6


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_k_raises(impl):
    with pytest.raises(ValueError):
        impl.count_subarrays_div_k([1, 2, 3], 0)
    with pytest.raises(ValueError):
        impl.count_subarrays_div_k([1, 2, 3], -5)


@pytest.mark.part1
@pytest.mark.edge
def test_non_int_element_raises(impl):
    with pytest.raises(ValueError):
        impl.count_subarrays_div_k([1, "2", 3], 5)
    with pytest.raises(ValueError):
        impl.count_subarrays_div_k("not a list", 5)


@pytest.mark.part1
@pytest.mark.edge
def test_against_brute_force_random(impl):
    rng = random.Random(0)
    for _ in range(400):
        n = rng.randint(0, 14)
        nums = [rng.randint(-9, 9) for _ in range(n)]
        k = rng.randint(1, 8)
        assert impl.count_subarrays_div_k(nums, k) == _brute_div(nums, k), (nums, k)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_1_part2(impl):
    assert impl.count_subarrays_sum_k([1, 1, 1], 2) == 2


@pytest.mark.part2
def test_worked_example_2_part2(impl):
    assert impl.count_subarrays_sum_k([1, 2, 3], 3) == 2


@pytest.mark.part2
def test_worked_example_3_part2_zero_target(impl):
    assert impl.count_subarrays_sum_k([1, -1, 0], 0) == 3


@pytest.mark.part2
@pytest.mark.edge
def test_empty_and_single_part2(impl):
    assert impl.count_subarrays_sum_k([], 0) == 0
    assert impl.count_subarrays_sum_k([5], 5) == 1
    assert impl.count_subarrays_sum_k([5], 0) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_negative_target(impl):
    assert impl.count_subarrays_sum_k([-1, -1, 1], -2) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_k_type_raises(impl):
    with pytest.raises(ValueError):
        impl.count_subarrays_sum_k([1, 2, 3], "3")


@pytest.mark.part2
@pytest.mark.edge
def test_against_brute_force_random_part2(impl):
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(0, 14)
        nums = [rng.randint(-9, 9) for _ in range(n)]
        k = rng.randint(-10, 10)
        assert impl.count_subarrays_sum_k(nums, k) == _brute_sum(nums, k), (nums, k)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_1_part3(impl):
    assert impl.longest_subarray_sum_k([1, -1, 5, -2, 3], 3) == (4, 0, 3)


@pytest.mark.part3
def test_worked_example_2_part3_tie_break_leftmost(impl):
    # [-1, 2] (indices 1..2) and [1] (index 3) both sum to 1; longest wins, and it is the
    # leftmost among subarrays of the max length.
    assert impl.longest_subarray_sum_k([-2, -1, 2, 1], 1) == (2, 1, 2)


@pytest.mark.part3
def test_worked_example_3_part3_none_found(impl):
    assert impl.longest_subarray_sum_k([1, 2, 3], 100) == (0, -1, -1)


@pytest.mark.part3
@pytest.mark.edge
def test_empty_nums_part3(impl):
    assert impl.longest_subarray_sum_k([], 5) == (0, -1, -1)


@pytest.mark.part3
@pytest.mark.edge
def test_single_element_part3(impl):
    assert impl.longest_subarray_sum_k([7], 7) == (1, 0, 0)
    assert impl.longest_subarray_sum_k([7], 5) == (0, -1, -1)


@pytest.mark.part3
@pytest.mark.edge
def test_all_duplicates_part3(impl):
    # [1, 1, 1, 1], k=2: longest run summing to 2 is any adjacent pair; leftmost is (0, 1).
    assert impl.longest_subarray_sum_k([1, 1, 1, 1], 2) == (2, 0, 1)


@pytest.mark.part3
@pytest.mark.edge
def test_invalid_nums_raises_part3(impl):
    with pytest.raises(ValueError):
        impl.longest_subarray_sum_k([1, 2.0, 3], 3)


@pytest.mark.part3
@pytest.mark.edge
def test_against_brute_force_random_part3(impl):
    rng = random.Random(2)
    for _ in range(400):
        n = rng.randint(0, 14)
        nums = [rng.randint(-9, 9) for _ in range(n)]
        k = rng.randint(-10, 10)
        assert impl.longest_subarray_sum_k(nums, k) == _brute_longest(nums, k), (nums, k)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_elements(run_script):
    rng = random.Random(0)
    nums = [rng.randint(-1000, 1000) for _ in range(100_000)]
    body = " ".join(map(str, nums)) + "\n5\n"
    r = run_script("PART 1\n" + body, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n4 5 0 -2 -3 1\n5\n5 0 0\n5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7\n6\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n1 1 1\n2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n1 -1 5 -2 3\n3\n\n100\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "4 0 3\n0 -1 -1\n"
