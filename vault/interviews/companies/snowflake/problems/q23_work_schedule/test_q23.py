import itertools
import random

import pytest

MOD = 1_000_000_007


def _brute1(pattern, work_hours, day_hours):
    q_positions = [i for i, c in enumerate(pattern) if c == "?"]
    results = []
    for combo in itertools.product(range(day_hours + 1), repeat=len(q_positions)):
        chars = list(pattern)
        for p, v in zip(q_positions, combo):
            chars[p] = str(v)
        if sum(int(c) for c in chars) == work_hours:
            results.append("".join(chars))
    return sorted(results)


def _brute2(pattern, work_hours, day_hours):
    return len(_brute1(pattern, work_hours, day_hours)) % MOD


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    result = impl.all_schedules("0?????8", 20, 8)
    assert len(result) == 1645
    assert result[:3] == ["0000488", "0000578", "0000668"]
    assert result == sorted(result)


@pytest.mark.part1
@pytest.mark.edge
def test_no_question_marks_matching(impl):
    assert impl.all_schedules("1234321", 16, 8) == ["1234321"]


@pytest.mark.part1
@pytest.mark.edge
def test_no_question_marks_not_matching(impl):
    assert impl.all_schedules("1234321", 99, 8) == []


@pytest.mark.part1
@pytest.mark.edge
def test_all_question_marks_zero_target(impl):
    assert impl.all_schedules("???????", 0, 8) == ["0000000"]


@pytest.mark.part1
@pytest.mark.edge
def test_target_too_high_for_any_completion(impl):
    assert impl.all_schedules("8888888", 55, 8) == []  # fixed sum is 56, can never be 55


@pytest.mark.part1
@pytest.mark.edge
def test_max_target_exact(impl):
    assert impl.all_schedules("???????", 56, 8) == ["8888888"]


@pytest.mark.part1
@pytest.mark.fmt
def test_lexicographic_order(impl):
    result = impl.all_schedules("??00000", 3, 8)
    assert result == sorted(result)
    assert result == ["0300000", "1200000", "2100000", "3000000"]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "pattern,work_hours,day_hours",
    [
        ("123456", 10, 8),   # wrong length
        ("12345678", 10, 8),  # wrong length
        ("1234569", 10, 8),  # '9' not allowed as a literal digit
        ("1234abc", 10, 8),  # non-digit, non-'?'
        ("1234567", -1, 8),  # negative workHours
        ("1234567", 10, 9),  # dayHours out of [0,8]
        ("1234567", 10, -1),
    ],
)
def test_invalid_input_raises(impl, pattern, work_hours, day_hours):
    with pytest.raises(ValueError):
        impl.all_schedules(pattern, work_hours, day_hours)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(150):
        pattern = "".join(rng.choice("012345678?") for _ in range(7))
        day_hours = rng.randint(0, 8)
        work_hours = rng.randint(0, 56)
        assert impl.all_schedules(pattern, work_hours, day_hours) == _brute1(pattern, work_hours, day_hours), (
            pattern, work_hours, day_hours,
        )


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_worst_case(run_script):
    # all 7 positions '?' is the largest branching factor; workHours near the middle maximises
    # the number of valid completions that must actually be emitted.
    stdin = "PART 1\n???????\n28 8\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert len(lines) == len(set(lines))  # no duplicates
    assert lines == sorted(lines)
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_matches_part1_count(impl):
    assert impl.count_schedules_mod("0?????8", 20, 8) == 1645


@pytest.mark.part2
@pytest.mark.edge
def test_zero_ways(impl):
    assert impl.count_schedules_mod("8888888", 0, 8) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_impossible_target_beyond_max(impl):
    assert impl.count_schedules_mod("???????", 10000, 8) == 0  # max reachable is 7*8=56


@pytest.mark.part2
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(1)
    for _ in range(150):
        pattern = "".join(rng.choice("012345678?") for _ in range(7))
        day_hours = rng.randint(0, 8)
        work_hours = rng.randint(0, 56)
        assert impl.count_schedules_mod(pattern, work_hours, day_hours) == _brute2(pattern, work_hours, day_hours)


def _brute_count_general(pattern, work_hours, day_hours):
    """Same brute force as _brute1, but not tied to the 7-char Part1 constraint (Part2 allows
    longer patterns)."""
    q_positions = [i for i, c in enumerate(pattern) if c == "?"]
    fixed = sum(int(c) for c in pattern if c != "?")
    count = 0
    for combo in itertools.product(range(day_hours + 1), repeat=len(q_positions)):
        if fixed + sum(combo) == work_hours:
            count += 1
    return count % MOD


@pytest.mark.part2
@pytest.mark.edge
def test_agrees_with_brute_on_longer_patterns(impl):
    # patterns beyond length 7 are allowed for Part2 only; keep day_hours small so the brute
    # force (day_hours+1)^8 stays cheap
    assert impl.count_schedules_mod("?" * 8, 12, 3) == _brute_count_general("?" * 8, 12, 3)


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.count_schedules_mod("123456789", 10, 8)  # '9' not allowed
    with pytest.raises(ValueError):
        impl.count_schedules_mod("??????", -1, 8)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_1000_10000(run_script):
    stdin = f"PART 2\n{'?' * 1000}\n8000 8\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert 0 <= int(r.stdout) < MOD
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n1234321\n16 8\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1234321\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n1234321\n16 8\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n"
