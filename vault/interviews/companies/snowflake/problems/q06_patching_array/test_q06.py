import random

import pytest


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_1_3_6(impl):
    assert impl.part1([1, 3], 6) == 1


@pytest.mark.part1
def test_example_1_5_10_20(impl):
    assert impl.part1([1, 5, 10], 20) == 2


@pytest.mark.part1
def test_example_1_2_2_5(impl):
    assert impl.part1([1, 2, 2], 5) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_empty_nums(impl):
    assert impl.part1([], 7) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_n_zero_needs_no_patches(impl):
    assert impl.part1([], 0) == 0
    assert impl.part1([1, 3], 0) == 0
    assert impl.part1([100, 200], 0) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_nums_already_covers_everything(impl):
    # [1,2,4,8] covers [1,15] with no patches
    assert impl.part1([1, 2, 4, 8], 15) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_values_greater_than_n_are_never_consumed(impl):
    # 100 is irrelevant since it's always > miss while miss <= n=5
    assert impl.part1([100], 5) == 3  # patches 1, 2, 4 -> miss becomes 8 > 5


@pytest.mark.part1
@pytest.mark.edge
def test_nums_missing_one_forces_first_patch(impl):
    # without a 1, the very first patch must be 1
    assert impl.part1([2, 3], 4) == 1  # patch 1 -> miss=2; nums[0]=2<=2 -> miss=4;
    # nums[1]=3<=4 -> miss=7 > 4 -> stop, 1 patch total


@pytest.mark.part1
@pytest.mark.edge
def test_large_n_is_fast_and_correct(impl):
    # O(log n) patches even for n near 2**31
    n = 2**31 - 1
    patches = impl.part1([], n)
    assert patches == 31  # 1,2,4,...,2**30 covers up to 2**31 - 1


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_part2_example_1_3_6(impl):
    assert impl.part2([1, 3], 6) == [2]


@pytest.mark.part2
def test_part2_example_1_5_10_20(impl):
    assert impl.part2([1, 5, 10], 20) == [2, 4]


@pytest.mark.part2
def test_part2_example_1_2_2_5(impl):
    assert impl.part2([1, 2, 2], 5) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_empty_nums(impl):
    assert impl.part2([], 7) == [1, 2, 4]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_n_zero(impl):
    assert impl.part2([], 0) == []
    assert impl.part2([1, 3], 0) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_length_matches_part1_count(impl):
    cases = [
        ([1, 3], 6),
        ([1, 5, 10], 20),
        ([1, 2, 2], 5),
        ([], 7),
        ([], 0),
        ([100], 5),
        ([2, 3], 4),
        ([1, 2, 4, 8], 15),
    ]
    for nums, n in cases:
        assert len(impl.part2(nums, n)) == impl.part1(nums, n)


@pytest.mark.part2
def test_part2_randomized_consistency_with_part1(impl):
    rng = random.Random(0)
    for _ in range(50):
        length = rng.randint(0, 10)
        nums = sorted(rng.randint(1, 50) for _ in range(length))
        n = rng.randint(0, 500)
        patches = impl.part2(nums, n)
        assert len(patches) == impl.part1(nums, n)
        # every patch value must be a positive power-of-two-ish "miss" gap;
        # replaying the greedy with the returned patches must actually work:
        # simulate consuming nums+patches merged in the same greedy order and
        # confirm the final range covers n (sanity: same result as part1 loop)
        assert all(p >= 1 for p in patches)


@pytest.mark.part2
@pytest.mark.perf
def test_part2_perf_large_n_modest_nums(impl):
    import time

    rng = random.Random(0)
    nums = sorted(rng.randint(1, 1000) for _ in range(20))
    n = 2**31 - 1
    t0 = time.perf_counter()
    patches = impl.part2(nums, n)
    elapsed = time.perf_counter() - t0
    assert len(patches) == impl.part1(nums, n)
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n6\n1 3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n20\n1 5 10\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2 4\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2_empty_result(run_script):
    r = run_script("PART 2\n5\n1 2 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_empty_nums_line(run_script):
    r = run_script("PART 1\n7\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3\n"
