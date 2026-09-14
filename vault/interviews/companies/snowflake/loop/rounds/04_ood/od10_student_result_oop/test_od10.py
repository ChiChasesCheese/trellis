import random
from decimal import Decimal

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_reports(impl):
    out = impl.part1(
        ["ADD 7 Ana 34 33 33", "ADD 3 Bo 33 33 33", "ADD 5 Cy 90 85 80",
         "REPORT 7", "REPORT 3", "REPORT 5", "REPORT 9"]
    )
    assert out == ["7 Ana 33.33 PASS", "3 Bo 33.00 FAIL", "5 Cy 85.00 PASS", "NOT_FOUND"]


@pytest.mark.part1
def test_result_is_a_student(impl):
    r = impl.Result(1, "Zoe", [10, 20, 30])
    assert isinstance(r, impl.Student)
    assert r.describe() == "1 Zoe"


@pytest.mark.part1
@pytest.mark.edge
def test_pass_mark_boundary(impl):
    assert impl.Result(1, "A", [34, 33, 33]).passed() is True    # 100/300 -> 33.33
    assert impl.Result(2, "B", [33, 33, 33]).passed() is False   # 99/300 -> 33.00


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.fmt
def test_percentage_is_decimal_half_up_two_places(impl):
    assert impl.Result(1, "A", [100, 100, 99]).percentage() == Decimal("99.67")
    assert impl.Result(2, "B", [1, 1, 0]).percentage() == Decimal("0.67")   # 0.666.. -> 0.67
    assert impl.Result(3, "C", [0, 0, 1]).percentage() == Decimal("0.33")   # 0.333.. -> 0.33
    assert str(impl.Result(4, "D", [0, 0, 0]).percentage()) == "0.00"


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "args",
    [(0, "A", [1, 2, 3]), (-1, "A", [1, 2, 3]), (1, "", [1, 2, 3]), (1, "  ", [1, 2, 3]),
     (1, "A", [1, 2]), (1, "A", [1, 2, 3, 4]), (1, "A", [101, 0, 0]), (1, "A", [-1, 0, 0])],
)
def test_invalid_construction_raises(impl, args):
    with pytest.raises(ValueError):
        impl.Result(*args)


@pytest.mark.part1
@pytest.mark.edge
def test_marks_property_returns_a_copy(impl):
    r = impl.Result(1, "A", [10, 20, 30])
    r.marks.append(99)
    r.marks[0] = 100
    assert r.marks == [10, 20, 30]


@pytest.mark.part1
@pytest.mark.edge
def test_bad_add_and_duplicate_roll_are_errors(impl):
    out = impl.part1(["ADD 3 Bo 33 33 33", "ADD 3 X 1 1 1", "ADD 4 Y 101 1 1", "ADD 5 Z 1 1", "REPORT 3"])
    assert out == ["ERROR", "ERROR", "ERROR", "3 Bo 33.00 FAIL"]


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    out = impl.part2(
        ["ADD 3 Bo 33 33 33", "RECHECK 3 2 40", "REPORT 3", "RECHECK 3 2 50",
         "RECHECK 3 1 10", "RECHECK 3 4 50", "ADD 5 Cy 90 85 80", "ADD 8 Di 80 90 85",
         "TOP 2", "TOP 0"]
    )
    assert out == ["UPDATED", "3 Bo 35.33 PASS", "REJECTED", "UNCHANGED", "REJECTED", "5 8", "-"]


@pytest.mark.part2
@pytest.mark.edge
def test_recheck_once_per_subject_even_when_unchanged(impl):
    r = impl.Result(1, "A", [50, 50, 50])
    assert r.recheck(1, 40) == "UNCHANGED"
    assert r.recheck(1, 90) == "REJECTED"
    assert r.marks == [50, 50, 50]


@pytest.mark.part2
@pytest.mark.edge
def test_recheck_equal_mark_is_unchanged(impl):
    assert impl.Result(1, "A", [50, 50, 50]).recheck(2, 50) == "UNCHANGED"


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("subject,mark", [(0, 60), (4, 60), (1, 101), (1, -5)])
def test_recheck_invalid_is_rejected_and_does_not_consume(impl, subject, mark):
    r = impl.Result(1, "A", [50, 50, 50])
    assert r.recheck(subject, mark) == "REJECTED"
    assert r.recheck(1, 60) == "UPDATED"


@pytest.mark.part2
@pytest.mark.edge
def test_recheck_can_flip_fail_to_pass(impl):
    r = impl.Result(1, "A", [33, 33, 33])
    assert not r.passed()
    r.recheck(3, 34)
    assert r.passed() and str(r.percentage()) == "33.33"


@pytest.mark.part2
@pytest.mark.edge
def test_top_ties_break_by_roll(impl):
    out = impl.part2(["ADD 9 A 50 50 50", "ADD 2 B 50 50 50", "ADD 5 C 60 40 50", "TOP 3", "TOP 10"])
    assert out == ["2 5 9", "2 5 9"]


@pytest.mark.part2
@pytest.mark.edge
def test_recheck_unknown_roll(impl):
    assert impl.part2(["RECHECK 1 1 50", "TOP 1"]) == ["NOT_FOUND", "-"]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_50k_students(run_script):
    rng = random.Random(0)
    lines = []
    for roll in range(1, 50_001):
        lines.append(f"ADD {roll} s{roll} {rng.randint(0, 100)} {rng.randint(0, 100)} {rng.randint(0, 100)}")
    for _ in range(50_000):
        roll = rng.randint(1, 50_000)
        lines.append(f"RECHECK {roll} {rng.randint(1, 3)} {rng.randint(0, 100)}")
    lines.append("TOP 5")
    r = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert len(r.stdout.splitlines()[-1].split()) == 5
    assert r.seconds < 3.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nADD 7 Ana 34 33 33\nREPORT 7\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7 Ana 33.33 PASS\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nADD 3 Bo 33 33 33\nRECHECK 3 2 40\nREPORT 3\nTOP 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "UPDATED\n3 Bo 35.33 PASS\n3\n"
