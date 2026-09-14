import random

import pytest

EXAMPLE = dict(
    start=[10, 5, 15, 18, 30],
    duration=[30, 12, 20, 35, 35],
    volume=[50, 51, 20, 25, 10],
)
EXAMPLE_ANSWER = 76


def _run(impl, part, **kw):
    fn = impl.part1 if part == 1 else impl.part2
    return fn(kw["start"], kw["duration"], kw["volume"])


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_matches_verified_answer(impl):
    assert _run(impl, 1, **EXAMPLE) == EXAMPLE_ANSWER


@pytest.mark.part1
def test_all_calls_mutually_overlapping_picks_single_max(impl):
    # all calls span [0, 100); answer is the single max-volume call
    start = [0, 0, 0, 0]
    duration = [100, 100, 100, 100]
    volume = [10, 20, 15, 5]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 20


@pytest.mark.part1
def test_all_calls_disjoint_sums_everything(impl):
    start = [0, 10, 20, 30]
    duration = [5, 5, 5, 5]
    volume = [1, 2, 3, 4]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 10


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input_is_zero(impl):
    assert _run(impl, 1, start=[], duration=[], volume=[]) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_single_call_is_its_own_volume(impl):
    assert _run(impl, 1, start=[7], duration=[3], volume=[42]) == 42


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_start_times(impl):
    # two calls start at the same time but different durations/volumes; only one fits
    start = [0, 0]
    duration = [10, 3]
    volume = [5, 5]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_touching_endpoints_are_not_overlapping(impl):
    # call A ends exactly when call B starts -> both schedulable
    start = [0, 18]
    duration = [18, 5]
    volume = [10, 7]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 17


@pytest.mark.part1
@pytest.mark.edge
def test_zero_duration_calls_are_always_included(impl):
    # a zero-duration call [5,5) never conflicts with anything; optimal must include it
    # alongside a normal call that would otherwise conflict with a competing call
    start = [0, 5, 0]
    duration = [10, 0, 10]
    volume = [5, 3, 6]
    # calls: A [0,10) vol5, B [5,5) vol3 (free), C [0,10) vol6 (overlaps A)
    # best: take C (6) + B (3, always free) = 9, better than A+B = 8
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 9


@pytest.mark.part1
@pytest.mark.edge
def test_multiple_zero_duration_calls_all_included(impl):
    start = [0, 0, 0]
    duration = [0, 0, 0]
    volume = [1, 2, 3]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 6


@pytest.mark.part1
@pytest.mark.edge
def test_huge_values_use_exact_integers(impl):
    start = [0, 10**9]
    duration = [10**9, 10**9]
    volume = [10**3, 10**3]
    assert _run(impl, 1, start=start, duration=duration, volume=volume) == 2000


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_part2_matches_example(impl):
    assert _run(impl, 2, **EXAMPLE) == EXAMPLE_ANSWER


@pytest.mark.part2
@pytest.mark.edge
def test_part2_agrees_with_part1_on_edge_shapes(impl):
    cases = [
        ([], [], []),
        ([7], [3], [42]),
        ([0, 0, 0], [0, 0, 0], [1, 2, 3]),
        ([0, 18], [18, 5], [10, 7]),
    ]
    for start, duration, volume in cases:
        assert impl.part1(start, duration, volume) == impl.part2(start, duration, volume)


@pytest.mark.part2
def test_part2_randomized_cross_check_against_part1(impl):
    rng = random.Random(0)
    for _ in range(50):
        n = rng.randint(0, 30)
        start = [rng.randint(0, 50) for _ in range(n)]
        duration = [rng.randint(0, 10) for _ in range(n)]
        volume = [rng.randint(0, 20) for _ in range(n)]
        assert impl.part1(start, duration, volume) == impl.part2(start, duration, volume)


@pytest.mark.part2
@pytest.mark.perf
def test_part2_perf_1e5_calls(impl):
    import time

    rng = random.Random(0)
    n = 100_000
    start = [rng.randrange(0, 10**9) for _ in range(n)]
    duration = [rng.randrange(0, 10**9) for _ in range(n)]
    volume = [rng.randrange(1, 1000) for _ in range(n)]
    t0 = time.perf_counter()
    result = impl.part2(start, duration, volume)
    elapsed = time.perf_counter() - t0
    assert isinstance(result, int)
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    stdin_text = "PART 2\n5\n10 30 50\n5 12 51\n15 20 20\n18 35 25\n30 35 10\n"
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "76\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part1_dispatch(run_script):
    stdin_text = "PART 1\n1\n7 3 42\n"
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "42\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_zero_calls(run_script):
    r = run_script("PART 2\n0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"
