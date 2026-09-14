import random

import pytest

SETUP = [
    "MERCHANT,acct_a,5411",
    "MERCHANT,acct_b,5812",
    "MERCHANT,acct_c,5411",
    "THRESHOLD,5411,2",
    "THRESHOLD,5812,0.5",
    "FRAUD_CODES,stolen_card,fraudulent",
    "MIN_COUNT,3",
]
EX1 = [
    "CHARGE,ch_1,acct_a,1000,approved",
    "CHARGE,ch_2,acct_a,2500,stolen_card",
    "CHARGE,ch_3,acct_a,300,fraudulent",
    "CHARGE,ch_4,acct_b,900,stolen_card",
    "CHARGE,ch_5,acct_b,900,approved",
    "CHARGE,ch_6,acct_c,100,stolen_card",
]
EX2 = EX1 + ["DISPUTE,ch_2"]
EX3 = [
    "CHARGE,ch_4,acct_b,900,stolen_card",
    "CHARGE,ch_5,acct_b,900,approved",
    "CHARGE,ch_7,acct_b,900,stolen_card",
    "DISPUTE,ch_5",
    "CHARGE,ch_8,acct_b,900,approved",
    "DISPUTE,ch_5",
    "DISPUTE,ch_999",
]


def setup_with(*thresholds, min_count=0, codes="FRAUD_CODES,fraud"):
    return [f"MERCHANT,m,{i}" for i in range(0)] + [
        "MERCHANT,m,1000", *[f"THRESHOLD,1000,{t}" for t in thresholds], codes, f"MIN_COUNT,{min_count}"]


def charges(n_fraud, n_ok, acct="m"):
    return [f"CHARGE,f{i},{acct},100,fraud" for i in range(n_fraud)] + [f"CHARGE,o{i},{acct},100,ok" for i in range(n_ok)]


# ---------------------------------------------------------------- Part 1: setup parsing
@pytest.mark.part1
def test_example_setup_parse(impl):
    s = impl.part1(SETUP + EX1)
    assert s["merchant_mcc"] == {"acct_a": "5411", "acct_b": "5812", "acct_c": "5411"}
    assert s["thresholds"] == {"5411": ("count", 2, 1), "5812": ("ratio", 5, 10)}
    assert s["fraud_codes"] == {"stolen_card", "fraudulent"}
    assert s["min_count"] == 3


@pytest.mark.part1
@pytest.mark.edge
def test_threshold_literal_decides_kind(impl):
    # integer literal -> count; any decimal literal -> ratio, exactly, even 1.0
    s = impl.part1(["THRESHOLD,a,1", "THRESHOLD,b,1.0", "THRESHOLD,c,0.25", "THRESHOLD,d,0.50", "THRESHOLD,e,0.333"])
    assert s["thresholds"] == {"a": ("count", 1, 1), "b": ("ratio", 10, 10), "c": ("ratio", 25, 100),
                               "d": ("ratio", 50, 100), "e": ("ratio", 333, 1000)}


@pytest.mark.part1
@pytest.mark.edge
def test_setup_tolerates_noise_repeats_and_missing(impl):
    s = impl.part1(["  MERCHANT , x , 1 ", "MERCHANT,x,2", "FRAUD_CODES,a", "FRAUD_CODES,b,a", ""])
    assert s["merchant_mcc"] == {"x": "2"}  # last MERCHANT wins
    assert s["fraud_codes"] == {"a", "b"}   # union across repeated lines
    assert s["min_count"] == 0 and s["thresholds"] == {} and s["sticky"] is False
    assert impl.part1([]) == {"merchant_mcc": {}, "thresholds": {}, "fraud_codes": set(), "min_count": 0, "sticky": False}


@pytest.mark.part1
@pytest.mark.fmt
@pytest.mark.io
def test_part1_render_via_stdin(run_script):
    r = run_script("PART 1\n" + "\n".join(SETUP + ["MERCHANT,acct_z,9999"] + EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "acct_a,5411,count,2\nacct_b,5812,ratio,0.5\nacct_c,5411,count,2\nacct_z,9999,NONE\n"


# ---------------------------------------------------------------- Part 2: counters
@pytest.mark.part2
def test_example_counts(impl):
    assert impl.part2(SETUP + EX1) == {"acct_a": (2, 3), "acct_b": (1, 2), "acct_c": (1, 1)}


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_code_unknown_merchant_duplicate_charge(impl):
    lines = SETUP + ["CHARGE,c1,ghost,5,stolen_card", "CHARGE,c2,acct_a,5,weird_code", "CHARGE,c2,acct_a,5,stolen_card"]
    assert impl.part2(lines) == {"ghost": (1, 1), "acct_a": (0, 1)}  # undeclared account counted; dup id ignored


@pytest.mark.part2
@pytest.mark.edge
def test_part2_ignores_disputes_and_empty(impl):
    assert impl.part2(SETUP + EX2) == impl.part2(SETUP + EX1)
    assert impl.part2([]) == {} and impl.part2(SETUP) == {}


# ---------------------------------------------------------------- Part 3: flagging
@pytest.mark.part3
def test_example1_flags(impl):
    assert impl.part3(SETUP + EX1) == ["acct_a"]


@pytest.mark.part3
@pytest.mark.edge
def test_count_threshold_boundary(impl):
    s = setup_with(3)
    assert impl.part3(s + charges(2, 5)) == ["NONE"]  # one below
    assert impl.part3(s + charges(3, 5)) == ["m"]     # == threshold is fraudulent (non-strict)
    assert impl.part3(s + charges(4, 0)) == ["m"]     # one above


@pytest.mark.part3
@pytest.mark.edge
def test_ratio_threshold_integer_comparison(impl):
    assert impl.part3(setup_with("0.5") + charges(1, 1)) == ["m"]      # exactly 1/2
    assert impl.part3(setup_with("0.5") + charges(1, 2)) == ["NONE"]   # 1/3 < 0.5
    assert impl.part3(setup_with("0.33") + charges(1, 2)) == ["m"]     # 1/3 = 0.333.. >= 0.33
    assert impl.part3(setup_with("0.34") + charges(1, 2)) == ["NONE"]  # 1/3 < 0.34
    assert impl.part3(setup_with("0.1") + charges(1, 9)) == ["m"]      # 0.1 exact (float 0.1 is not)
    assert impl.part3(setup_with("0.0") + charges(0, 1)) == ["m"]      # 0/1 >= 0.0


@pytest.mark.part3
@pytest.mark.edge
def test_min_count_gates_ratio_only(impl):
    assert impl.part3(setup_with("0.5", min_count=4) + charges(2, 1)) == ["NONE"]  # total 3 < 4
    assert impl.part3(setup_with("0.5", min_count=4) + charges(2, 2)) == ["m"]     # total == 4
    assert impl.part3(setup_with(1, min_count=99) + charges(1, 0)) == ["m"]        # count threshold ignores MIN_COUNT


@pytest.mark.part3
@pytest.mark.edge
def test_one_vs_one_point_zero_zero_volume_and_no_threshold(impl):
    assert impl.part3(setup_with("1.0") + charges(2, 1)) == ["NONE"]  # ratio 2/3 < 1.0
    assert impl.part3(setup_with("1.0") + charges(3, 0)) == ["m"]
    assert impl.part3(setup_with(1) + charges(1, 5)) == ["m"]          # count 1
    assert impl.part3(setup_with("0.0")) == ["NONE"]                    # zero volume never flagged
    assert impl.part3(["MERCHANT,m,7", "FRAUD_CODES,fraud"] + charges(9, 0)) == ["NONE"]  # MCC without threshold
    assert impl.part3(["THRESHOLD,7,1", "FRAUD_CODES,fraud"] + charges(9, 0)) == ["NONE"]  # account without MERCHANT


@pytest.mark.part3
@pytest.mark.fmt
def test_output_sorted_plain_string_order_and_none(impl):
    lines = ["THRESHOLD,1,1", "FRAUD_CODES,f"] + [f"MERCHANT,{a},1" for a in ("acct_2", "acct_10", "B", "a")]
    lines += [f"CHARGE,c_{a},{a},1,f" for a in ("acct_2", "acct_10", "B", "a")]
    assert impl.part3(lines) == ["B,a,acct_10,acct_2"]
    assert impl.part3([]) == ["NONE"]


# ---------------------------------------------------------------- Part 4: disputes
@pytest.mark.part4
def test_example2_dispute_unflags_unless_sticky(impl):
    assert impl.part4(SETUP + EX2) == ["NONE"]
    assert impl.part4(SETUP + EX2, sticky=True) == ["acct_a"]
    assert impl.part4(SETUP + ["STICKY"] + EX2) == ["acct_a"]  # STICKY setup line == sticky=True
    assert impl.part3(SETUP + EX2) == ["acct_a"]                # Part 3 ignores DISPUTE


@pytest.mark.part4
def test_example3_ratio_merchant_with_disputes(impl):
    assert impl.part4(SETUP + EX3) == ["acct_b"]
    assert impl.part2(SETUP + EX3) == {"acct_b": (2, 4)}  # part2 still ignores disputes


@pytest.mark.part4
@pytest.mark.edge
def test_disputing_non_fraud_charge_can_push_ratio_over(impl):
    lines = setup_with("0.5") + charges(1, 2) + ["DISPUTE,o0"]  # 1/3 -> 1/2
    assert impl.part4(lines) == ["m"]
    assert impl.part4(lines, dispute_removes_charge=False) == ["NONE"]  # variant: total stays 3


@pytest.mark.part4
@pytest.mark.edge
def test_variant_dispute_marks_non_fraud_but_keeps_total(impl):
    lines = setup_with(2) + charges(2, 0) + ["DISPUTE,f0"]
    assert impl.part4(lines) == ["NONE"]
    assert impl.part4(lines, dispute_removes_charge=False) == ["NONE"]  # fraud 1/2 < 2
    lines2 = setup_with("0.5") + charges(2, 2) + ["DISPUTE,f0", "DISPUTE,f0"]
    assert impl.part4(lines2, dispute_removes_charge=False) == ["NONE"]  # 1/4, double dispute no-op
    assert impl.part4(lines2) == ["NONE"]                                # 1/3


# ---------------------------------------------------------------- Part 5: edge cases
@pytest.mark.part5
@pytest.mark.edge
def test_double_dispute_unknown_dispute_all_disputed(impl):
    base = setup_with(2) + charges(3, 0)
    assert impl.part5(base + ["DISPUTE,f0"]) == ["m"]                      # 2/2 still >= 2
    assert impl.part5(base + ["DISPUTE,f0", "DISPUTE,f0"]) == ["m"]        # second dispute is a no-op
    assert impl.part5(base + ["DISPUTE,f0", "DISPUTE,f1"]) == ["NONE"]     # 1/1
    assert impl.part5(base + ["DISPUTE,nope"]) == ["m"]                    # unknown id ignored
    assert impl.part5(base + ["DISPUTE,f0", "DISPUTE,f1", "DISPUTE,f2"]) == ["NONE"]  # 0/0: no ZeroDivision
    assert impl.part5(setup_with("0.0") + charges(0, 1) + ["DISPUTE,o0"]) == ["NONE"]  # 0/0 with ratio 0.0


@pytest.mark.part5
@pytest.mark.edge
def test_sticky_survives_dispute_and_reflag_after_recovery(impl):
    lines = setup_with("0.5", min_count=2) + charges(1, 1) + ["DISPUTE,f0", "CHARGE,x,m,1,ok"]  # 1/2 -> 0/1 -> 0/2
    assert impl.part5(lines) == ["NONE"]
    assert impl.part5(lines, sticky=True) == ["m"]
    # order matters: dispute before the charge that would have flagged it
    assert impl.part5(setup_with(1) + ["DISPUTE,f0"] + charges(1, 0)) == ["m"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part5
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(SETUP + EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "acct_b\n"
    r = run_script("\n".join(SETUP + EX2) + "\n")
    assert r.stdout == "NONE\n"
    r = run_script("PART 2\n" + "\n".join(SETUP + EX2) + "\n")
    assert r.stdout == "acct_a,2,3\nacct_b,1,2\nacct_c,1,1\n"
    r = run_script("PART 3\n" + "\n".join(SETUP + EX2) + "\n")
    assert r.stdout == "acct_a\n"
    assert run_script("").stdout == "NONE\n"


@pytest.mark.part5
@pytest.mark.perf
def test_perf_100k_events(run_script):
    rng = random.Random(0)
    lines = [f"MERCHANT,acct_{i},{rng.randrange(20)}" for i in range(5000)]
    lines += [f"THRESHOLD,{m},{rng.choice(['3', '5', '0.2', '0.5'])}" for m in range(20)]
    lines += ["FRAUD_CODES,stolen,fraud", "MIN_COUNT,5"]
    for i in range(100_000):
        if i % 4 == 3:
            lines.append(f"DISPUTE,ch_{rng.randrange(i)}")
        else:
            lines.append(f"CHARGE,ch_{i},acct_{rng.randrange(5000)},{rng.randrange(100000)},{rng.choice(['ok', 'ok', 'stolen', 'fraud'])}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.endswith("\n") and r.stdout.count("\n") == 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
