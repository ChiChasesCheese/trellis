import random

import pytest

EX1 = ["424242", "1", "1500000000,6555555555,VISA"]
EX1_OUT = ["4242420000000000,4242429999999999,VISA"]

EX2 = ["777777", "2", "1000000000,3999999999,VISA", "4000000000,5999999999,MASTERCARD"]
EX2_OUT = ["7777770000000000,7777773999999999,VISA", "7777774000000000,7777779999999999,MASTERCARD"]

EX3 = ["424242", "3", "1000000000,1999999999,VISA", "5000000000,5999999999,MASTERCARD", "3000000000,3999999999,VISA"]
EX3_P1 = ["4242420000000000,4242421999999999,VISA", "4242423000000000,4242423999999999,VISA", "4242425000000000,4242429999999999,MASTERCARD"]
EX3_P2 = ["4242420000000000,4242422999999999,VISA", "4242423000000000,4242424999999999,VISA", "4242425000000000,4242429999999999,MASTERCARD"]
EX3_P4 = ["4242420000000000,4242424999999999,VISA", "4242425000000000,4242429999999999,MASTERCARD"]

EX4 = ["424242", "3", "1000000000,7999999999,VISA", "2000000000,2999999999,AMEX", "9000000000,9999999999,MASTERCARD"]
EX4_OUT = ["4242420000000000,4242428999999999,VISA", "4242422000000000,4242422999999999,AMEX", "4242429000000000,4242429999999999,MASTERCARD"]

EX5 = ["555555", "4", "0000000000,0999999999,MASTERCARD", "1000000000,1999999999,MASTERCARD", "3000000000,3999999999,VISA", "6000000000,6999999999,VISA"]
EX5_OUT = ["5555550000000000,5555552999999999,MASTERCARD", "5555553000000000,5555559999999999,VISA"]


# ---------------------------------------------------------------- Part 1: outer ends
@pytest.mark.part1
def test_example1_single_range_becomes_whole_bin(impl):
    for p in (impl.part1, impl.part2, impl.part3, impl.part4):
        assert p(EX1) == EX1_OUT


@pytest.mark.part1
def test_example2_touching_ranges(impl):
    for p in (impl.part1, impl.part2, impl.part3, impl.part4):
        assert p(EX2) == EX2_OUT


@pytest.mark.part1
def test_example3_part1_keeps_interior_gaps(impl):
    assert impl.part1(EX3) == EX3_P1


@pytest.mark.part1
@pytest.mark.edge
def test_n_zero_prints_nothing(impl):
    for p in (impl.part1, impl.part2, impl.part3, impl.part4):
        assert p(["424242", "0"]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_zero_padding_and_leading_zero_offsets(impl):
    # offsets with leading zeros parse; 16-digit zero-padded output; full range already covered
    assert impl.part1(["100000", "1", "0000000000,9999999999,X"]) == ["1000000000000000,1000009999999999,X"]
    assert impl.part1(["424242", "1", "0000000005,0000000009,VISA"]) == ["4242420000000000,4242429999999999,VISA"]


@pytest.mark.part1
@pytest.mark.edge
def test_unsorted_input_is_sorted_and_only_outer_ends_move(impl):
    lines = ["424242", "3", "7000000000,7000000000,C", "0000000010,0000000020,A", "3000000000,3000000000,B"]
    assert impl.part1(lines) == [
        "4242420000000000,4242420000000020,A",
        "4242423000000000,4242423000000000,B",
        "4242427000000000,4242429999999999,C",
    ]


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_and_blank_lines_tolerated(impl):
    lines = [" 424242 ", "", "1", "  1500000000 , 6555555555 , VISA  ", ""]
    assert impl.part1(lines) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_full_16_digit_input_variant(impl):
    assert impl.part1(["424242", "1", "4242421500000000,4242426555555555,VISA"]) == EX1_OUT


# ---------------------------------------------------------------- Part 2: interior gaps
@pytest.mark.part2
def test_example3_part2_fills_gaps_by_extending_lower(impl):
    assert impl.part2(EX3) == EX3_P2
    assert impl.part3(EX3) == EX3_P2


@pytest.mark.part2
@pytest.mark.edge
def test_gap_boundary_touching_vs_one_apart(impl):
    # end+1 == next.start: touching, no change
    touching = ["424242", "2", "0000000000,4999999999,A", "5000000000,9999999999,B"]
    assert impl.part2(touching) == ["4242420000000000,4242424999999999,A", "4242425000000000,4242429999999999,B"]
    # gap of exactly one number: A extends by one, to next.start - 1
    one_gap = ["424242", "2", "0000000000,4999999998,A", "5000000000,9999999999,B"]
    assert impl.part2(one_gap) == ["4242420000000000,4242424999999999,A", "4242425000000000,4242429999999999,B"]
    # overlap by one: nothing is trimmed
    overlap = ["424242", "2", "0000000000,5000000000,A", "5000000000,9999999999,B"]
    assert impl.part2(overlap) == ["4242420000000000,4242425000000000,A", "4242425000000000,4242429999999999,B"]


@pytest.mark.part2
@pytest.mark.edge
def test_multiple_gaps_different_brands(impl):
    lines = ["999999", "3", "8000000000,8000000000,C", "2000000000,2000000000,A", "5000000000,5000000000,B"]
    assert impl.part2(lines) == [
        "9999990000000000,9999994999999999,A",
        "9999995000000000,9999997999999999,B",
        "9999998000000000,9999999999999999,C",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_identical_ranges_kept_in_parts_1_to_3(impl):
    lines = ["424242", "2", "1000000000,2000000000,VISA", "1000000000,2000000000,VISA"]
    # the first in sorted order gets LO and (tie on end -> smaller start) HI; the twin keeps its bounds
    expected = ["4242420000000000,4242429999999999,VISA", "4242421000000000,4242422000000000,VISA"]
    assert impl.part1(lines) == expected
    assert impl.part2(lines) == expected
    assert impl.part3(lines) == expected


# ---------------------------------------------------------------- Part 3: nested
@pytest.mark.part3
def test_example4_nested_only_covering_extended(impl):
    assert impl.part3(EX4) == EX4_OUT
    assert impl.part4(EX4) == EX4_OUT  # different brands: nothing merges


@pytest.mark.part3
@pytest.mark.edge
def test_nested_at_the_top_end(impl):
    # contained interval is the last by start; the covering one must get HI, not the contained one
    lines = ["424242", "2", "1000000000,5000000000,VISA", "4000000000,4500000000,AMEX"]
    assert impl.part3(lines) == [
        "4242420000000000,4242429999999999,VISA",
        "4242424000000000,4242424500000000,AMEX",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_partial_overlap_extends_the_one_with_higher_end(impl):
    lines = ["424242", "3", "0000000000,3000000000,A", "2000000000,4000000000,B", "8000000000,9999999999,C"]
    assert impl.part3(lines) == [
        "4242420000000000,4242423000000000,A",
        "4242422000000000,4242427999999999,B",
        "4242428000000000,4242429999999999,C",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_same_end_tie_extends_smaller_start(impl):
    lines = ["424242", "3", "0000000000,3000000000,A", "1000000000,3000000000,B", "5000000000,9999999999,C"]
    assert impl.part3(lines) == [
        "4242420000000000,4242424999999999,A",
        "4242421000000000,4242423000000000,B",
        "4242425000000000,4242429999999999,C",
    ]


# ---------------------------------------------------------------- Part 4: merge
@pytest.mark.part4
def test_example5_merge(impl):
    assert impl.part4(EX5) == EX5_OUT


@pytest.mark.part4
def test_example3_part4_merges_touching_same_brand(impl):
    assert impl.part4(EX3) == EX3_P4


@pytest.mark.part4
@pytest.mark.edge
def test_merge_is_case_sensitive_on_brand(impl):
    lines = ["424242", "2", "0000000000,4999999999,Visa", "5000000000,9999999999,VISA"]
    assert impl.part4(lines) == ["4242420000000000,4242424999999999,Visa", "4242425000000000,4242429999999999,VISA"]


@pytest.mark.part4
@pytest.mark.edge
def test_merge_absorbs_nested_and_identical_same_brand(impl):
    lines = ["424242", "3", "1000000000,7000000000,VISA", "2000000000,3000000000,VISA", "1000000000,7000000000,VISA"]
    assert impl.part4(lines) == ["4242420000000000,4242429999999999,VISA"]


@pytest.mark.part4
@pytest.mark.edge
def test_merge_chain_across_many_pieces(impl):
    pieces = [f"{i}000000000,{i}999999999,A" for i in range(10)]
    assert impl.part4(["424242", "10"] + pieces) == ["4242420000000000,4242429999999999,A"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact_with_part_lines(run_script):
    r = run_script("PART 2\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_P2) + "\n"
    r = run_script("PART 3\n" + "\n".join(EX4) + "\n")
    assert r.stdout == "\n".join(EX4_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX3) + "\n")
    assert r.stdout == "\n".join(EX3_P1) + "\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_without_part_line_defaults_to_full_rules(run_script):
    r = run_script("\n".join(EX5) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX5_OUT) + "\n"
    r = run_script("424242\n0\n")
    assert r.returncode == 0 and r.stdout == ""
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_intervals(run_script):
    rng = random.Random(0)
    n = 100_000
    lines = []
    for _ in range(n):
        s = rng.randrange(0, 10**10 - 1000)
        lines.append(f"{s:010d},{s + rng.randrange(0, 1000):010d},{rng.choice(['VISA', 'MASTERCARD', 'AMEX'])}")
    rng.shuffle(lines)
    r = run_script("424242\n" + f"{n}\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out = r.stdout.rstrip("\n").split("\n")
    assert 1 <= len(out) <= n
    assert out[0].startswith("4242420000000000,") and out[-1].split(",")[1] == "4242429999999999"
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
