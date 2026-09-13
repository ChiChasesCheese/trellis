import random
import time

import pytest

EX1 = ([[3, 50], [7, 10], [12, 25]], 10)
EX2 = ([[1, 0], [4, 25], [5, 50]], 2)
EX3 = ([[2, 50]], 0)


# ---------------------------------------------------------------- Part 1: LC 2303
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.calculate_tax(*EX1) == pytest.approx(2.65, abs=1e-5)
    assert impl.calculate_tax(*EX2) == pytest.approx(0.25, abs=1e-5)
    assert impl.calculate_tax(*EX3) == pytest.approx(0.0, abs=1e-5)


@pytest.mark.part1
@pytest.mark.edge
def test_income_on_bracket_boundaries(impl):
    b = [[3, 50], [7, 10], [12, 25]]
    assert impl.calculate_tax(b, 3) == pytest.approx(1.5)      # == upper_0 -> all in bracket 0
    assert impl.calculate_tax(b, 4) == pytest.approx(1.6)      # one above -> 10% on the extra dollar
    assert impl.calculate_tax(b, 2) == pytest.approx(1.0)      # one below
    assert impl.calculate_tax(b, 12) == pytest.approx(3.15)    # == last upper: 1.5 + 0.4 + 1.25


@pytest.mark.part1
@pytest.mark.edge
def test_single_bracket_and_extreme_percents(impl):
    assert impl.calculate_tax([[1000, 100]], 1000) == pytest.approx(1000.0)
    assert impl.calculate_tax([[1000, 0]], 1000) == pytest.approx(0.0)
    assert impl.calculate_tax([[5, 100], [10, 0]], 10) == pytest.approx(5.0)


@pytest.mark.part1
@pytest.mark.edge
def test_no_float_drift_on_many_brackets(impl):
    # 100 brackets of width 10 at 3%: 1000 * 0.03 = 30 exactly; naive float sums drift
    brackets = [[10 * (i + 1), 3] for i in range(100)]
    assert impl.calculate_tax(brackets, 1000) == 30.0


# ---------------------------------------------------------------- Part 2: breakdown
@pytest.mark.part2
def test_breakdown_examples(impl):
    lines = impl.tax_breakdown(*EX1)
    assert [tuple(l) for l in lines] == [(0, 3, 50, 3, 1.5), (3, 7, 10, 4, 0.4), (7, 12, 25, 3, 0.75)]
    lines = impl.tax_breakdown(*EX2)
    assert [tuple(l) for l in lines] == [(0, 1, 0, 1, 0.0), (1, 4, 25, 1, 0.25)]


@pytest.mark.part2
@pytest.mark.edge
def test_breakdown_zero_income_and_sum_matches_part1(impl):
    assert impl.tax_breakdown(*EX3) == []
    b = [[3, 50], [7, 10], [12, 25]]
    for inc in range(0, 13):
        assert sum(l.tax for l in impl.tax_breakdown(b, inc)) == pytest.approx(impl.calculate_tax(b, inc))
        assert sum(l.taxable for l in impl.tax_breakdown(b, inc)) == inc


@pytest.mark.part2
def test_breakdown_fields_by_name(impl):
    line = impl.tax_breakdown([[3, 50], [7, 10]], 5)[1]
    assert line.lower == 3 and line.upper == 7 and line.percent == 10 and line.taxable == 2
    assert line.tax == pytest.approx(0.2)


# ---------------------------------------------------------------- Part 3: cents
@pytest.mark.part3
def test_cents_example(impl):
    assert impl.calculate_tax_cents([[300, 50], [700, 10], [1200, 25]], 1000) == 265


@pytest.mark.part3
@pytest.mark.fmt
def test_cents_half_up_per_bracket(impl):
    # 25 cents at 50% = 12.5 -> 13 per bracket (two brackets -> 26, not 25)
    assert impl.calculate_tax_cents([[25, 50], [50, 50]], 50) == 26
    assert impl.calculate_tax_cents([[25, 50]], 25) == 13
    # 1 cent at 49% = 0.49 -> 0 ; at 50% = 0.5 -> 1 ; at 51% -> 1
    assert impl.calculate_tax_cents([[1, 49]], 1) == 0
    assert impl.calculate_tax_cents([[1, 50]], 1) == 1
    assert impl.calculate_tax_cents([[1, 51]], 1) == 1


@pytest.mark.part3
@pytest.mark.edge
def test_cents_zero_and_huge(impl):
    assert impl.calculate_tax_cents([[100, 50]], 0) == 0
    # 10^12 cents at 7% -> exact integer 7*10^10 (float would lose cents)
    assert impl.calculate_tax_cents([[10**12, 7]], 10**12) == 7 * 10**10
    assert impl.calculate_tax_cents([[10**12, 7]], 10**12 - 1) == (7 * (10**12 - 1) + 50) // 100


# ---------------------------------------------------------------- Part 4: mode
@pytest.mark.part4
def test_volume_examples(impl):
    b = [[3, 50], [7, 10], [12, 25]]
    assert impl.calculate_tax_mode(b, 10, "volume") == pytest.approx(2.5)
    assert impl.calculate_tax_mode(b, 7, "volume") == pytest.approx(0.7)
    assert impl.calculate_tax_mode(b, 8, "volume") == pytest.approx(2.0)
    assert impl.calculate_tax_mode(b, 10, "graduated") == pytest.approx(2.65)
    assert impl.calculate_tax_mode(b, 10) == pytest.approx(2.65)  # default graduated


@pytest.mark.part4
@pytest.mark.edge
def test_volume_boundaries_and_zero(impl):
    b = [[3, 50], [7, 10], [12, 25]]
    assert impl.calculate_tax_mode(b, 3, "volume") == pytest.approx(1.5)   # == upper_0 -> 50%
    assert impl.calculate_tax_mode(b, 4, "volume") == pytest.approx(0.4)   # one above -> 10%
    assert impl.calculate_tax_mode(b, 0, "volume") == 0.0
    assert impl.calculate_tax_mode([[2, 50]], 0, "volume") == 0.0
    assert impl.calculate_tax_mode(b, 12, "volume") == pytest.approx(3.0)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_part1(run_script):
    r = run_script("PART 1\n10\n3,50\n7,10\n12,25\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2.65\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_part2_part3_part4(run_script):
    r = run_script("PART 2\n2\n1,0\n4,25\n5,50\n")
    assert r.stdout == "0-1 @0%: 1 -> 0.00\n1-4 @25%: 1 -> 0.25\n"
    r = run_script("PART 3\n50\n25, 50\n50, 50\n")
    assert r.stdout == "$0.26\n"
    r = run_script("PART 4\n10\nMODE volume\n3,50\n7,10\n12,25\n\n")
    assert r.stdout == "2.50\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max_and_stress(impl, run_script):
    # LC max: 100 brackets, income 1000 — trivially fast; make it meaningful with 10^4 calls
    rng = random.Random(0)
    uppers = sorted(rng.sample(range(1, 1001), 100))
    brackets = [[u, rng.randrange(0, 101)] for u in uppers]
    t0 = time.perf_counter()
    for inc in range(0, 1001):
        for _ in range(10):
            impl.calculate_tax(brackets, inc)
    assert time.perf_counter() - t0 < 2.0
    # stdin path at LC max
    text = "PART 1\n1000\n" + "\n".join(f"{u},{p}" for u, p in brackets) + "\n"
    r = run_script(text)
    assert r.returncode == 0 and r.seconds < 2.0 and r.max_rss_mb < 256
