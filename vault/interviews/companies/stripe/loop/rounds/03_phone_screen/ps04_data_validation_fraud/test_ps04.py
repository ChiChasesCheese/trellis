import random

import pytest

HEADER = "txn_id,user_id,amount,currency,payment_method,country,timestamp"

BODY = [
    "RULES",
    "10.00,5000.00",
    "BLOCKLIST",
    "prepaid_card,gift_card",
    "PROFILES",
    "u1,US;CA,8,20,10.00,500.00",
    "u2,GB,0,23,5.00,10000.00",
    "TRANSACTIONS",
    HEADER,
    "t1,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00",
    "t2,u1,150.00,USD,prepaid_card,US,2026-08-01T14:30:00",
    "t3,u1,6000.00,USD,credit_card,US,2026-08-01T14:30:00",
    "t4,u1,150.00,USD,credit_card,,2026-08-01T14:30:00",
    "t5,u1,150.00,,credit_card,FR,2026-08-01T03:00:00",
    "t6,u3,150.00,USD,credit_card,US,2026-08-01T14:30:00",
    "t7,u1,9000.00,USD,gift_card,DE,2026-08-01T02:00:00",
    ",u1,150.00,USD,credit_card,US,2026-08-01T14:30:00",
]

EXPECTED_PART1 = [
    "t1: OK",
    "t2: OK",
    "t3: OK",
    "t4: MISSING_FIELD",
    "t5: MISSING_FIELD",
    "t6: OK",
    "t7: OK",
    ": MISSING_FIELD",
]

EXPECTED_PART2 = [
    "t1: OK",
    "t2: BLOCKED_METHOD",
    "t3: AMOUNT_OUT_OF_RANGE",
    "t4: MISSING_FIELD",
    "t5: MISSING_FIELD",
    "t6: OK",
    "t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE",
    ": MISSING_FIELD",
]

EXPECTED_PART3 = [
    "t1: OK",
    "t2: BLOCKED_METHOD",
    "t3: AMOUNT_OUT_OF_RANGE",
    "t4: MISSING_FIELD",
    "t5: MISSING_FIELD,SUSPICIOUS",
    "t6: OK",
    "t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE,SUSPICIOUS",
    ": MISSING_FIELD",
]

EXPECTED_PART4 = [
    "t1  OK",
    "t2  BLOCKED_METHOD",
    "t3  AMOUNT_OUT_OF_RANGE",
    "t4  MISSING_FIELD",
    "t5  MISSING_FIELD,SUSPICIOUS",
    "t6  OK",
    "t7  BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE",
    "    MISSING_FIELD",
]


# ---------------------------------------------------------------- Part 1: completeness
@pytest.mark.part1
def test_worked_example_part1(impl):
    assert impl.part1(BODY) == EXPECTED_PART1


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_only_field_is_missing(impl):
    body = [
        "RULES",
        "0,999999",
        "BLOCKLIST",
        "",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,u1,10.00,USD,  ,US,2026-01-01T00:00:00",
    ]
    assert impl.part1(body) == ["t1: MISSING_FIELD"]


@pytest.mark.part1
@pytest.mark.edge
def test_fewer_than_seven_columns_is_missing(impl):
    body = [
        "RULES",
        "0,999999",
        "BLOCKLIST",
        "",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,u1,10.00,USD,credit_card,US",  # timestamp column absent
    ]
    assert impl.part1(body) == ["t1: MISSING_FIELD"]


@pytest.mark.part1
def test_complete_row_is_ok_under_part1_even_with_other_violations(impl):
    # part1 does not evaluate range/blocklist/suspicious at all
    body = [
        "RULES",
        "0.00,1.00",
        "BLOCKLIST",
        "credit_card",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,u1,9999.00,USD,credit_card,ZZ,2026-01-01T00:00:00",
    ]
    assert impl.part1(body) == ["t1: OK"]


# ---------------------------------------------------------------- Part 2: range + blocklist
@pytest.mark.part2
def test_worked_example_part2(impl):
    assert impl.part2(BODY) == EXPECTED_PART2


@pytest.mark.part2
@pytest.mark.edge
def test_amount_inclusive_boundaries(impl):
    body_tmpl = ["RULES", "10.00,5000.00", "BLOCKLIST", "", "PROFILES", "TRANSACTIONS", HEADER]
    lo = body_tmpl + ["t1,u1,10.00,USD,credit_card,US,2026-01-01T00:00:00"]
    hi = body_tmpl + ["t1,u1,5000.00,USD,credit_card,US,2026-01-01T00:00:00"]
    below = body_tmpl + ["t1,u1,9.99,USD,credit_card,US,2026-01-01T00:00:00"]
    above = body_tmpl + ["t1,u1,5000.01,USD,credit_card,US,2026-01-01T00:00:00"]
    assert impl.part2(lo) == ["t1: OK"]
    assert impl.part2(hi) == ["t1: OK"]
    assert impl.part2(below) == ["t1: AMOUNT_OUT_OF_RANGE"]
    assert impl.part2(above) == ["t1: AMOUNT_OUT_OF_RANGE"]


@pytest.mark.part2
@pytest.mark.edge
def test_blocklist_case_insensitive_and_empty_blocks_nothing(impl):
    body = [
        "RULES",
        "0,999999",
        "BLOCKLIST",
        "Prepaid_Card",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,u1,10.00,USD,PREPAID_CARD,US,2026-01-01T00:00:00",
    ]
    assert impl.part2(body) == ["t1: BLOCKED_METHOD"]
    body[3] = ""  # empty blocklist line
    assert impl.part2(body) == ["t1: OK"]


# ---------------------------------------------------------------- Part 3: behavior match
@pytest.mark.part3
def test_worked_example_part3(impl):
    assert impl.part3(BODY) == EXPECTED_PART3


@pytest.mark.part3
@pytest.mark.edge
def test_two_of_three_match_is_not_suspicious_one_of_three_is(impl):
    body_tmpl = [
        "RULES",
        "0,999999",
        "BLOCKLIST",
        "",
        "PROFILES",
        "u1,US,8,20,10.00,500.00",
        "TRANSACTIONS",
        HEADER,
    ]
    # country match + hour match, amount out of profile range (2/3) -> OK
    two_of_three = body_tmpl + ["t1,u1,9000.00,USD,credit_card,US,2026-01-01T14:00:00"]
    # only amount matches (1/3) -> SUSPICIOUS
    one_of_three = body_tmpl + ["t1,u1,150.00,USD,credit_card,FR,2026-01-01T03:00:00"]
    assert impl.part3(two_of_three) == ["t1: OK"]
    assert impl.part3(one_of_three) == ["t1: SUSPICIOUS"]


@pytest.mark.part3
@pytest.mark.edge
def test_no_profile_never_suspicious(impl):
    body = [
        "RULES",
        "0,999999",
        "BLOCKLIST",
        "",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,ghost,999999.00,USD,credit_card,ZZ,2026-01-01T03:00:00",
    ]
    assert impl.part3(body) == ["t1: OK"]


# ---------------------------------------------------------------- Part 4: priority report
@pytest.mark.part4
def test_worked_example_part4(impl):
    assert impl.part4(BODY) == EXPECTED_PART4


@pytest.mark.part4
@pytest.mark.fmt
def test_column_width_follows_longest_txn_id(impl):
    body = [
        "RULES",
        "10.00,5000.00",
        "BLOCKLIST",
        "",
        "PROFILES",
        "TRANSACTIONS",
        HEADER,
        "t1,u1,150.00,USD,credit_card,US,2026-01-01T00:00:00",
        "transaction-42,u1,150.00,USD,credit_card,US,2026-01-01T00:00:00",
    ]
    out = impl.part4(body)
    width = len("transaction-42")
    assert out[0] == f"{'t1':<{width}}  OK"
    assert out[1] == f"{'transaction-42':<{width}}  OK"


@pytest.mark.part4
@pytest.mark.edge
def test_more_than_two_codes_truncated_to_top_two(impl):
    body = [
        "RULES",
        "0.00,1.00",
        "BLOCKLIST",
        "credit_card",
        "PROFILES",
        "u1,US,8,20,0.00,1.00",
        "TRANSACTIONS",
        HEADER,
        # missing field + blocked method + out of range + suspicious -> keep top 2 only
        "t1,u1,9999.00,,credit_card,ZZ,2026-01-01T03:00:00",
    ]
    out = impl.part4(body)
    assert out == ["t1  MISSING_FIELD,BLOCKED_METHOD"]


@pytest.mark.part4
def test_part4_empty_transactions(impl):
    body = ["RULES", "0,1", "BLOCKLIST", "", "PROFILES", "TRANSACTIONS", HEADER]
    assert impl.part4(body) == []


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 4\n" + "\n".join(BODY) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EXPECTED_PART4) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_transactions(run_script):
    rng = random.Random(0)
    countries = ["US", "CA", "GB", "FR", "DE"]
    methods = ["credit_card", "debit_card", "prepaid_card", "bank_transfer"]
    n_users = 2000
    profile_lines = [
        f"u{i},{rng.choice(countries)};{rng.choice(countries)},{rng.randrange(0,12)},"
        f"{rng.randrange(12,24)},10.00,1000.00"
        for i in range(n_users)
    ]
    txn_lines = []
    for i in range(100_000):
        hour = rng.randrange(0, 24)
        txn_lines.append(
            f"t{i},u{rng.randrange(n_users)},{rng.randrange(1, 200000) / 100:.2f},USD,"
            f"{rng.choice(methods)},{rng.choice(countries)},2026-01-01T{hour:02d}:00:00"
        )
    body = (
        ["RULES", "10.00,5000.00", "BLOCKLIST", "prepaid_card", "PROFILES"]
        + profile_lines
        + ["TRANSACTIONS", HEADER]
        + txn_lines
    )
    r = run_script("PART 4\n" + "\n".join(body) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
