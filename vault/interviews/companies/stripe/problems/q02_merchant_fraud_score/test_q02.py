import random

import pytest

R = "100,2,5,3"  # min 100, x2, +5, penalty 3


def section(merchants, txns, rules=None):
    if rules is None:
        rules = [R] * len(txns)
    return ["MERCHANTS", *merchants, "TRANSACTIONS", *txns, "RULES", *rules]


EX1 = section(["m2,20", "m1,10"], ["m1,500,c1,13", "m2,100,c2,10"], ["100,2,5,3", "100,3,1,1"])
EX1_OUT = ["m1, 20", "m2, 20"]

EX2 = section(
    ["shop,10"],
    ["shop,50,alice,9", "shop,50,alice,9", "shop,50,alice,9", "shop,50,alice,9", "shop,50,bob,9"],
    ["100,2,5,1", "100,2,5,1", "100,2,5,1", "100,2,7,1", "100,2,9,1"],
)
EX2_OUT = ["shop, 22"]

EX3 = section(
    ["m1,5", "m0,50"],
    ["m1,1000,c1,13", "m1,10,c1,13", "m1,10,c1,13", "m1,10,c1,10", "m1,10,c1,10", "m1,10,c1,10"],
    ["500,3,1,4"] * 6,
)
EX3_OUT = ["m0, 50", "m1, 19"]

EX4 = section(
    ["M1,10", "M2,20"],
    ["M1,30000,C1,14", "M1,5000,C1,14", "M1,5000,C1,14", "M2,20000,C2,20", "M2,20000,C3,20", "M2,20000,C2,20"],
    ["10000,2,1,5"] * 6,
)
EX4_OUT = ["M1, 26", "M2, 160"]


# ---------------------------------------------------------------- Part 1: amount rule
@pytest.mark.part1
def test_example1_strict_greater(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_threshold_boundary(impl):
    for amount, want in ((99, 10), (100, 10), (101, 20)):
        assert impl.part1(section(["m,10"], [f"m,{amount},c,0"])) == [f"m, {want}"]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_and_negative_amounts_never_multiply(impl):
    lines = section(["m,7"], ["m,0,c,0", "m,-500,c,0"], ["0,9,1,1", "-1000,9,1,1"])
    # -500 > -1000 IS true: negative thresholds still compare numerically
    assert impl.part1(section(["m,7"], ["m,0,c,0"], ["0,9,1,1"])) == ["m, 7"]
    assert impl.part1(lines) == ["m, 63"]


@pytest.mark.part1
@pytest.mark.edge
def test_merchant_without_transactions_and_empty_sections(impl):
    assert impl.part1(section(["b,3", "a,50"], [])) == ["a, 50", "b, 3"]
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_multipliers_compound_and_zero_factor(impl):
    lines = section(["m,10"], ["m,500,c,0", "m,500,d,0", "m,500,e,0"], ["1,2,0,0", "1,3,0,0", "1,1,0,0"])
    assert impl.part1(lines) == ["m, 60"]
    assert impl.part1(section(["m,10"], ["m,500,c,0"], ["1,0,0,0"])) == ["m, 0"]


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_plain_string_order_and_whitespace_tolerance(impl):
    lines = ["MERCHANTS", " m10 , 1 ", "m2,2", "B,3", "", "TRANSACTIONS", " m2 , 500 , c , 1 ", "RULES", " 1 , 2 , 0 , 0 "]
    assert impl.part1(lines) == ["B, 3", "m10, 1", "m2, 4"]


# ---------------------------------------------------------------- Part 2: repeat customer
@pytest.mark.part2
def test_example2_third_and_later_add(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_repeat_count_boundary_two_vs_three(impl):
    two = section(["m,10"], ["m,1,c,0"] * 2)
    three = section(["m,10"], ["m,1,c,0"] * 3)
    assert impl.part2(two) == ["m, 10"]
    assert impl.part2(three) == ["m, 15"]


@pytest.mark.part2
@pytest.mark.edge
def test_pairs_independent_across_merchants_and_customers(impl):
    txns = ["m1,1,c,0", "m2,1,c,0", "m1,1,c,0", "m2,1,c,0", "m1,1,d,0", "m1,1,c,0"]
    # (m1,c) has 3 -> +5 once ; (m2,c) has 2 ; (m1,d) has 1
    assert impl.part2(section(["m1,0", "m2,0"], txns)) == ["m1, 5", "m2, 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_multiply_happens_before_add_regardless_of_order(impl):
    # additive terms from the earlier repeat transactions must NOT be multiplied by a later large txn
    txns = ["m,1,c,0", "m,1,c,0", "m,1,c,0", "m,500,d,0"]
    rules = ["100,2,5,0"] * 3 + ["100,2,0,0"]
    assert impl.part2(section(["m,10"], txns, rules)) == ["m, 25"]  # 10*2 + 5, not (10+5)*2


@pytest.mark.part2
@pytest.mark.edge
def test_group_variant_adds_all_factors_once(impl):
    m, t, r = impl.parse(section(["m,0"], ["m,1,c,0"] * 3, ["100,1,1,0", "100,1,2,0", "100,1,4,0"]))
    assert impl.score(m, t, r, upto=2) == ["m, 4"]                          # primary: only the 3rd
    assert impl.score(m, t, r, upto=2, repeat_mode="group") == ["m, 7"]     # variant: 1+2+4
    assert impl.score(m, t[:2], r[:2], upto=2, repeat_mode="group") == ["m, 0"]


# ---------------------------------------------------------------- Part 3: hourly density
@pytest.mark.part3
def test_example3_all_passes(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
def test_example4_programhelp_parameters(impl):
    assert impl.part3(EX4) == EX4_OUT


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize("hour,delta", [(8, 0), (9, -3), (11, -3), (12, 3), (17, 3), (18, -3), (21, -3), (22, 0), (0, 0), (23, 0)])
def test_hour_band_boundaries(impl, hour, delta):
    # three identical txns: pass 2 adds 5 once (3rd), pass 3 applies the band once (3rd)
    lines = section(["m,10"], [f"m,1,c,{hour}"] * 3)
    assert impl.part3(lines) == [f"m, {15 + delta}"]


@pytest.mark.part3
@pytest.mark.edge
def test_hourly_applies_to_every_occurrence_from_third(impl):
    lines = section(["m,0"], ["m,1,c,13"] * 5, ["100,1,0,2"] * 5)
    assert impl.part3(lines) == ["m, 6"]  # 3rd, 4th, 5th each +2


@pytest.mark.part3
@pytest.mark.edge
def test_hour_groups_split_and_negative_score(impl):
    # 2 txns at hour 12 + 2 at hour 13 -> repeat rule fires on 3rd and 4th (+5+5) but no hour reaches 3
    lines = section(["m,0"], ["m,1,c,12", "m,1,c,12", "m,1,c,13", "m,1,c,13"])
    assert impl.part3(lines) == ["m, 10"]
    # three txns at hour 20 with additive 0 and penalty 7 -> -7
    assert impl.part3(section(["m,0"], ["m,1,c,20"] * 3, ["100,1,0,7"] * 3)) == ["m, -7"]


@pytest.mark.part3
@pytest.mark.edge
def test_unknown_merchant_transactions_are_ignored(impl):
    assert impl.part3(section(["m,1"], ["ghost,500,c,13"] * 3)) == ["m, 1"]


@pytest.mark.part3
def test_grouped_variant(impl):
    parse = impl.parse
    m, t, _ = parse(section(["m,10", "z,1"], ["m,100,c,12", "m,200,c,12", "m,300,c,12", "m,-50,d,1"]))
    # (m,c) has 3 -> +600 ; (m,c,12) has 3 -> +600 again ; (m,d) single, negative ignored by count
    assert impl.score_variant_grouped(m, t) == ["m, 1210", "z, 1"]
    m, t, _ = parse(section(["m,10"], ["m,0,c,5", "m,0,c,5", "m,0,c,6"]))
    assert impl.score_variant_grouped(m, t) == ["m, 10"]  # pair >=3 but total 0; no hour reaches 3
    m, t, _ = parse(section(["m,10"], ["m,7,c,5", "m,7,c,5"]))
    assert impl.score_variant_grouped(m, t) == ["m, 10"]  # duplicates but only 2
    assert impl.score_variant_grouped([("m", 4)], []) == ["m, 4"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "m0, 50\nm1, 19\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "m1, 20\nm2, 20\n"
    r = run_script("\n".join(EX4) + "\n")  # no PART line -> Part 3
    assert r.stdout == "M1, 26\nM2, 160\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_transactions(run_script):
    rng = random.Random(0)
    merchants = [f"m{i},{rng.randrange(1, 51)}" for i in range(1000)]
    txns = [f"m{rng.randrange(1000)},{rng.randrange(-100, 100000)},c{rng.randrange(300)},{rng.randrange(24)}" for _ in range(100_000)]
    rules = [f"{rng.randrange(0, 50000)},{rng.randrange(1, 3)},{rng.randrange(0, 10)},{rng.randrange(0, 10)}" for _ in range(100_000)]
    r = run_script("PART 3\n" + "\n".join(section(merchants, txns, rules)) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 1000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
