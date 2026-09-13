"""ps11 Factory Cost — tests. RECONSTRUCTED TRAINING PROBLEM (see problem.md's warning block).

Every literal expected value below was produced by running solution.py on the exact input shown
(python3 solution.py, or the impl.partN(...) call itself) and transcribed, not hand-derived --
see problem.md's worked-examples section for the same discipline.
"""

import random

import pytest

# ---------------------------------------------------------------- shared fixtures / examples

P1_LINES = ["FACTORIES", "f1,0,100.00", "f2,10,50.00", "f3,25,80.00", "PENALTIES"]
P1_OUT = ["TOTAL $230.00"]

P2_LINES = [
    "FACTORIES",
    "f1,0,100.00",
    "f2,10,50.00",
    "f3,25,80.00",
    "PENALTIES",
    "16,inf,2.00",  # deliberately listed before the lower band
    "0,15,5.00",
]
P2_OUT = ["TOTAL $240.00"]

P2_GAP_LINES = ["FACTORIES", "f1,0,10.00", "f2,12,10.00", "PENALTIES", "0,10,1.00", "15,inf,1.00"]
P2_GAP_OUT = ["ERROR no penalty band for distance=12"]

P3_TIE_LINES = [
    "FACTORIES",
    "f1,0,10.00",
    "f2,12,10.00",
    "f3,20,10.00",
    "PENALTIES",
    "0,10,1.00",
    "15,inf,1.00",
]
P3_TIE_OUT = ["TOTAL $21.00", "SKIPPED f1"]

P4_EXAMPLE_LINES = [
    "FACTORIES",
    "f1,0,10.00",
    "f2,5,10.00",
    "f3,9,10.00",
    "f4,14,10.00",
    "f5,20,10.00",
    "PENALTIES",
    "0,3,5.00",
    "4,6,3.00",
    "7,100,0.50",
    "SKIP",
    "2",
]
P4_EXAMPLE_OUT = ["TOTAL $31.00", "SKIPPED f2,f4"]


# ---------------------------------------------------------------- Part 1: cumulative build cost
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(P1_LINES) == P1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_zero_factories(impl):
    assert impl.part1(["FACTORIES", "PENALTIES"]) == ["TOTAL $0.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_single_factory(impl):
    assert impl.part1(["FACTORIES", "f1,0,12.34", "PENALTIES"]) == ["TOTAL $12.34"]


@pytest.mark.part1
@pytest.mark.fmt
def test_money_decimal_digit_variants(impl):
    lines = ["FACTORIES", "f1,0,5", "f2,10,5.5", "f3,20,5.50", "PENALTIES"]
    assert impl.part1(lines) == ["TOTAL $16.00"]


# ---------------------------------------------------------------- Part 2: adjacency penalties
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(P2_LINES) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_unsorted_bands_still_correct(impl):
    # P2_LINES already lists the 'inf' band before the low band on purpose
    assert impl.part2(P2_LINES) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_gap_errors(impl):
    assert impl.part2(P2_GAP_LINES) == P2_GAP_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_first_gap_wins_when_two_pairs_are_affected(impl):
    lines = ["FACTORIES", "f1,0,1.00", "f2,5,1.00", "f3,50,1.00", "f4,55,1.00", "PENALTIES", "1,2,1.00"]
    # dist(f1,f2)=5 has no band AND dist(f3,f4)=5 has no band either -> report the first (index 0)
    assert impl.part2(lines) == ["ERROR no penalty band for distance=5"]


@pytest.mark.part2
@pytest.mark.edge
def test_single_factory_never_errors(impl):
    assert impl.part2(["FACTORIES", "f1,0,7.00", "PENALTIES"]) == ["TOTAL $7.00"]


@pytest.mark.part2
@pytest.mark.edge
def test_band_boundary_inclusive_both_ends(impl):
    max_edge = ["FACTORIES", "f1,0,1.00", "f2,10,1.00", "PENALTIES", "0,10,2.00", "11,inf,9.00"]
    min_edge = ["FACTORIES", "f1,0,1.00", "f2,11,1.00", "PENALTIES", "0,10,2.00", "11,inf,9.00"]
    assert impl.part2(max_edge) == ["TOTAL $4.00"]  # dist=10 -> band [0,10]'s $2.00
    assert impl.part2(min_edge) == ["TOTAL $11.00"]  # dist=11 -> band [11,inf]'s $9.00


# ---------------------------------------------------------------- Part 3: skip at most one (A01)
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(P3_TIE_LINES) == P3_TIE_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_skip_nothing_wins_ties_against_every_skip(impl):
    # f1 and f3 (the only skip candidates with a defined bridge-free delta) cost nothing to
    # remove either, so every configuration ties at $5.00 -- 'skip nothing' must win the tie.
    lines = ["FACTORIES", "f1,0,0.00", "f2,10,5.00", "f3,20,0.00", "PENALTIES", "0,10,0.00"]
    assert impl.part3(lines) == ["TOTAL $5.00", "SKIPPED NONE"]


@pytest.mark.part3
@pytest.mark.edge
def test_skip_first_factory_optimal_no_bridge_needed(impl):
    lines = ["FACTORIES", "f1,0,50.00", "f2,2,1.00", "f3,20,1.00", "PENALTIES", "0,3,10.00", "4,100,0.10"]
    assert impl.part3(lines) == ["TOTAL $2.10", "SKIPPED f1"]


@pytest.mark.part3
@pytest.mark.edge
def test_skip_last_factory_optimal_no_bridge_needed(impl):
    lines = ["FACTORIES", "f1,0,1.00", "f2,18,1.00", "f3,20,50.00", "PENALTIES", "0,3,10.00", "4,100,0.10"]
    assert impl.part3(lines) == ["TOTAL $2.10", "SKIPPED f3"]


@pytest.mark.part3
@pytest.mark.edge
def test_tied_single_skip_options_smallest_index_wins(impl):
    assert impl.part3(P3_TIE_LINES) == ["TOTAL $21.00", "SKIPPED f1"]


@pytest.mark.part3
@pytest.mark.edge
def test_no_valid_configuration_at_all(impl):
    lines = ["FACTORIES", "f1,0,1.00", "f2,5,1.00", "f3,50,1.00", "PENALTIES", "100,200,1.00"]
    assert impl.part3(lines) == ["ERROR no valid configuration"]


@pytest.mark.part3
@pytest.mark.edge
def test_zero_and_one_factory_never_skip(impl):
    assert impl.part3(["FACTORIES", "PENALTIES"]) == ["TOTAL $0.00", "SKIPPED NONE"]
    assert impl.part3(["FACTORIES", "f1,0,9.99", "PENALTIES"]) == ["TOTAL $9.99", "SKIPPED NONE"]


# ---------------------------------------------------------------- Part 4: skip up to k (DP + reconstruction)
@pytest.mark.part4
def test_example_part4(impl):
    assert impl.part4(P4_EXAMPLE_LINES) == P4_EXAMPLE_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_k_zero_falls_back_to_part2_success(impl):
    lines = P2_LINES + ["SKIP", "0"]
    assert impl.part4(lines) == ["TOTAL $240.00", "SKIPPED NONE"]


@pytest.mark.part4
@pytest.mark.edge
def test_k_zero_falls_back_to_part2_error(impl):
    lines = P2_GAP_LINES + ["SKIP", "0"]
    assert impl.part4(lines) == ["ERROR no valid configuration within skip budget k=0"]


@pytest.mark.part4
@pytest.mark.edge
def test_skip_all_but_the_cheapest_factory(impl):
    # no band covers any positive distance -> only a single built factory is ever valid;
    # the DP must find the globally cheapest one (f2) and skip every other.
    lines = ["FACTORIES", "f1,0,10.00", "f2,5,1.00", "f3,9,10.00", "f4,14,10.00", "PENALTIES", "SKIP", "3"]
    assert impl.part4(lines) == ["TOTAL $1.00", "SKIPPED f1,f3,f4"]


@pytest.mark.part4
@pytest.mark.edge
def test_optimum_needs_two_non_adjacent_skips(impl):
    assert impl.part4(P4_EXAMPLE_LINES) == P4_EXAMPLE_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_dp_tie_break_prefers_larger_j_at_equal_cost(impl):
    # f1/f2/f3 equally spaced, one flat penalty band everywhere. Reaching f3 by skipping f1
    # (f2->f3) and by skipping f2 (f1->f3) both cost $4.00 -- rule 2 (prefer the larger j, i.e.
    # fewer skips in that one step) must pick "skip f1" (built chain f2->f3), not "skip f2".
    lines = ["FACTORIES", "f1,0,1.00", "f2,10,1.00", "f3,20,1.00", "PENALTIES", "0,100,2.00", "SKIP", "1"]
    assert impl.part4(lines) == ["TOTAL $4.00", "SKIPPED f1"]


@pytest.mark.part4
@pytest.mark.edge
def test_no_valid_configuration_within_budget(impl):
    lines = ["FACTORIES", "f1,0,1.00", "f2,5,1.00", "f3,50,1.00", "PENALTIES", "100,200,1.00", "SKIP", "0"]
    assert impl.part4(lines) == ["ERROR no valid configuration within skip budget k=0"]


@pytest.mark.part4
@pytest.mark.edge
def test_zero_factories_part4(impl):
    assert impl.part4(["FACTORIES", "PENALTIES", "SKIP", "0"]) == ["TOTAL $0.00", "SKIPPED NONE"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_OUT) + "\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact_part4(run_script):
    r = run_script("PART 4\n" + "\n".join(P4_EXAMPLE_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P4_EXAMPLE_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100_factories_dp(run_script):
    # This is a phone-screen DP problem (not a 10^5-row OA) -- 100 factories is the stated max,
    # and Part 4's O(n^2 * k) DP must still comfortably clear the shared 2s/256MB budget.
    rng = random.Random(0)
    n = 100
    positions = sorted(rng.sample(range(1, 100_000), n))
    lines = ["FACTORIES"]
    for i, p in enumerate(positions):
        lines.append(f"f{i},{p},{rng.randrange(1, 10_000)}.{rng.randrange(0, 99):02d}")
    lines.append("PENALTIES")
    bounds = sorted(rng.sample(range(1, 5_000), 19))
    prev = 0
    for b in bounds:
        lines.append(f"{prev},{b},{rng.randrange(0, 500)}.{rng.randrange(0, 99):02d}")
        prev = b + 1
    lines.append(f"{prev},inf,{rng.randrange(0, 500)}.00")
    lines.append("SKIP")
    lines.append("40")
    r = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("TOTAL $")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
