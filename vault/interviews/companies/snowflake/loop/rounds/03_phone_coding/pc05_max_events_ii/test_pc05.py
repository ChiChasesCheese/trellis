import itertools
import random

import pytest

EX1 = ([[1, 2, 4], [3, 4, 3], [2, 3, 1]], 2)          # LC 1751 example 1 -> 7
EX2 = ([[1, 2, 4], [3, 4, 3], [2, 3, 10]], 2)         # LC 1751 example 2 -> 10
EX3 = ([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]], 3)  # LC 1751 example 3 -> 9
EX4 = ([[1, 5, 3], [1, 5, 1], [6, 6, 5]], 2)          # same interval twice -> 8, picks 0 and 2


def _brute(events, k):
    best = 0
    for r in range(0, min(k, len(events)) + 1):
        for comb in itertools.combinations(range(len(events)), r):
            iv = sorted((events[i] for i in comb), key=lambda x: x[0])
            if all(iv[t][1] < iv[t + 1][0] for t in range(len(iv) - 1)):
                best = max(best, sum(x[2] for x in iv))
    return best


def _random_events(rng, n):
    out = []
    for _ in range(n):
        a = rng.randint(1, 12)
        out.append([a, a + rng.randint(0, 4), rng.randint(0, 9)])
    return out


def _valid_selection(events, chosen, k, value):
    iv = sorted((events[i] for i in chosen), key=lambda x: x[0])
    return (
        len(chosen) <= k
        and len(set(chosen)) == len(chosen)
        and chosen == sorted(chosen)
        and sum(x[2] for x in iv) == value
        and all(iv[t][1] < iv[t + 1][0] for t in range(len(iv) - 1))
    )


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize("case,expected", [(EX1, 7), (EX2, 10), (EX3, 9), (EX4, 8)])
def test_worked_examples(impl, case, expected):
    events, k = case
    assert impl.max_value(events, k) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_inclusive_end_means_touching_events_overlap(impl):
    # [1,2] and [2,3] share day 2 -> cannot attend both
    assert impl.max_value([[1, 2, 5], [2, 3, 5]], 2) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_k_zero_and_empty(impl):
    assert impl.max_value([[1, 2, 5]], 0) == 0
    assert impl.max_value([], 3) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_k_larger_than_n(impl):
    assert impl.max_value([[1, 1, 1], [3, 3, 2]], 10) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_single_day_events(impl):
    assert impl.max_value([[5, 5, 7], [5, 5, 9], [6, 6, 1]], 2) == 10


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_event_raises(impl):
    with pytest.raises(ValueError):
        impl.max_value([[3, 1, 5]], 1)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(400):
        events = _random_events(rng, rng.randint(0, 7))
        k = rng.randint(0, 4)
        assert impl.max_value(events, k) == _brute(events, k), (events, k)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_examples(impl):
    assert impl.max_value_with_events(*EX1) == (7, [0, 1])
    assert impl.max_value_with_events(*EX2) == (10, [2])
    assert impl.max_value_with_events(*EX3) == (9, [1, 2, 3])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_nothing_chosen(impl):
    assert impl.max_value_with_events([], 2) == (0, [])
    assert impl.max_value_with_events([[1, 2, 5]], 0) == (0, [])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_selection_is_valid_on_random_inputs(impl):
    rng = random.Random(1)
    for _ in range(400):
        events = _random_events(rng, rng.randint(0, 7))
        k = rng.randint(0, 4)
        value, chosen = impl.max_value_with_events(events, k)
        assert value == _brute(events, k)
        assert _valid_selection(events, chosen, k, value), (events, k, value, chosen)


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    lines = ["K 2", "N 3", "1 2 4", "3 4 3", "2 3 10"]
    assert impl.part2(lines) == ["10", "2"]
    assert impl.part2(["K 0", "N 1", "1 1 5"]) == ["0", "-"]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_examples(impl):
    assert impl.max_value_unbounded(EX3[0]) == 10
    assert impl.max_value_unbounded(EX1[0]) == 7


@pytest.mark.part3
@pytest.mark.edge
def test_part3_matches_part1_with_k_equal_n(impl):
    rng = random.Random(2)
    for _ in range(300):
        events = _random_events(rng, rng.randint(0, 8))
        assert impl.max_value_unbounded(events) == _brute(events, len(events)), events


@pytest.mark.part3
@pytest.mark.edge
def test_part3_empty(impl):
    assert impl.max_value_unbounded([]) == 0


@pytest.mark.part3
@pytest.mark.perf
def test_perf_part3_100k(run_script):
    rng = random.Random(0)
    n = 100_000
    lines = [f"N {n}"]
    for _ in range(n):
        s = rng.randint(1, 1_000_000_000)
        lines.append(f"{s} {s + rng.randint(0, 5000)} {rng.randint(1, 1_000_000)}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout.strip()) > 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_k_times_n_1e6(run_script):
    rng = random.Random(3)
    n, k = 20_000, 50
    lines = [f"K {k}", f"N {n}"]
    for _ in range(n):
        s = rng.randint(1, 10_000_000)
        lines.append(f"{s} {s + rng.randint(0, 2000)} {rng.randint(1, 1000)}")
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout.strip()) > 0
    assert r.seconds < 4.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nK 2\nN 3\n1 2 4\n3 4 3\n2 3 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nK 3\nN 4\n1 1 1\n2 2 2\n3 3 3\n4 4 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "9\n1 2 3\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\nN 4\n1 1 1\n2 2 2\n3 3 3\n4 4 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "10\n"
