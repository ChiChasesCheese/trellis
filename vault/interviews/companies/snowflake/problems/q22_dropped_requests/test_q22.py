import random

import pytest


def _brute_all(times):
    """O(n^2) recompute from scratch every step -- independent of the sliding-deque logic.
    Windows count every arrival (dropped or not)."""
    dropped = []
    for i, t in enumerate(times):
        prefix = times[: i + 1]
        same = sum(1 for x in prefix if x == t)
        w10 = sum(1 for x in prefix if x >= t - 9)
        w60 = sum(1 for x in prefix if x >= t - 59)
        if same > 3 or w10 > 20 or w60 > 60:
            dropped.append(t)
    return dropped


def _brute_accepted_only(times):
    """O(n^2) recompute from scratch, tracking only the accepted subset."""
    accepted = []
    dropped = []
    for t in times:
        same = sum(1 for x in accepted if x == t) + 1
        w10 = sum(1 for x in accepted if x >= t - 9) + 1
        w60 = sum(1 for x in accepted if x >= t - 59) + 1
        if same > 3 or w10 > 20 or w60 > 60:
            dropped.append(t)
        else:
            accepted.append(t)
    return dropped


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_same_second_rule_alone(impl):
    assert impl.dropped_requests_count_all([5, 5, 5, 5]) == [5]


@pytest.mark.part1
def test_window10_rule_alone(impl):
    times = [t for t in range(1, 8) for _ in range(3)]  # 21 events across 7 seconds
    assert impl.dropped_requests_count_all(times) == [7]


@pytest.mark.part1
def test_window60_rule_alone(impl):
    times = list(range(1, 61)) + [60]  # 61 events, all within a 60s span
    assert impl.dropped_requests_count_all(times) == [60]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input(impl):
    assert impl.dropped_requests_count_all([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_no_drops_below_all_thresholds(impl):
    assert impl.dropped_requests_count_all([1, 2, 3]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_exact_boundary_not_dropped(impl):
    # exactly 3 in the same second, exactly 20 in a 10s window: none of these should be dropped
    times = [t for t in range(1, 8) for _ in range(3)][:20]  # first 20 of the 21-event stream
    assert impl.dropped_requests_count_all(times) == []


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.dropped_requests_count_all([2, 1])
    with pytest.raises(ValueError):
        impl.dropped_requests_count_all([-1])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(80):
        n = rng.randint(0, 40)
        times = sorted(rng.randint(0, 30) for _ in range(n))
        assert impl.dropped_requests_count_all(times) == _brute_all(times), times


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(1)
    n = 100_000
    times = []
    t = 0
    for _ in range(n):
        t += rng.choice([0, 0, 0, 1])  # dense bursts to stress all three windows
        times.append(t)
    stdin = f"PART 1\n{n}\n" + " ".join(map(str, times)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_diverges_from_part1(impl):
    times = [1] * 10 + [t for t in range(2, 11) for _ in range(2)]
    all_variant = impl.dropped_requests_count_all(times)
    accepted_variant = impl.dropped_requests_count_accepted_only(times)
    assert all_variant == [1, 1, 1, 1, 1, 1, 1, 7, 7, 8, 8, 9, 9, 10, 10]
    assert accepted_variant == [1, 1, 1, 1, 1, 1, 1, 10]
    assert all_variant != accepted_variant


@pytest.mark.part2
@pytest.mark.edge
def test_same_second_rule_alone(impl):
    assert impl.dropped_requests_count_accepted_only([5, 5, 5, 5]) == [5]


@pytest.mark.part2
@pytest.mark.edge
def test_accepted_only_never_drops_more_than_all_variant(impl):
    rng = random.Random(2)
    for _ in range(80):
        n = rng.randint(0, 30)
        times = sorted(rng.randint(0, 25) for _ in range(n))
        all_dropped = impl.dropped_requests_count_all(times)
        accepted_dropped = impl.dropped_requests_count_accepted_only(times)
        assert len(accepted_dropped) <= len(all_dropped), times


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.dropped_requests_count_accepted_only([2, 1])


@pytest.mark.part2
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(0, 40)
        times = sorted(rng.randint(0, 30) for _ in range(n))
        assert impl.dropped_requests_count_accepted_only(times) == _brute_accepted_only(times), times


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k(run_script):
    rng = random.Random(4)
    n = 100_000
    times = []
    t = 0
    for _ in range(n):
        t += rng.choice([0, 0, 0, 1])
        times.append(t)
    stdin = f"PART 2\n{n}\n" + " ".join(map(str, times)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n4\n5 5 5 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2_empty_output(run_script):
    r = run_script("PART 2\n3\n1 2 3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == ""
