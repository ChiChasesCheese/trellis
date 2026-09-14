import random

import pytest

HEADER = "id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status"
ROWS = [
    "py_1,1,1000,eur,2025-01-01,acct_1,ie,payment,card,payment_completed",
    "py_2,2,500,eur,2025-01-01,acct_1,ie,payment,klarna,payment_completed",
    "py_3,3,1000,eur,2025-01-02,acct_1,ie,payment,card,payment_pending",
    "dp_1,4,1000,eur,2025-01-03,acct_1,ie,dispute,card,dispute_lost",
    "dp_2,5,1000,eur,2025-01-03,acct_2,de,dispute,card,dispute_won",
    "dp_3,6,1000,eur,2025-01-03,acct_2,de,dispute,klarna,dispute_won",
    "rf_1,7,1000,eur,2025-01-04,acct_2,de,refund,card,refund_completed",
]
P1_OUT = ["py_1,51", "py_2,41", "py_3,0", "dp_1,1500", "dp_2,1500", "dp_3,0", "rf_1,0"]
RATES = ["card,ie,140,25", "klarna,*,290,0"]
P2_OUT = ["py_1,39", "py_2,14", "py_3,0", "dp_1,1500", "dp_2,1500", "dp_3,0", "rf_1,0"]

RECV_HEADER = "customer_id,merchant_id,payout_date,card_type,amount"
RECV = ["c1,m1,2024-10-01,visa,1000", "c2,m1,2024-10-01,visa,500", "c3,m1,2024-10-01,master,200", "c4,m2,2024-09-30,visa,700"]
RECV_OUT = ["merchant_id,card_type,payout_date,net", "m1,master,2024-10-01,200", "m1,visa,2024-10-01,1500", "m2,visa,2024-09-30,700"]

SYSTEM = ["txn_1,1000", "txn_2,2000", "txn_4,300"]
GATEWAY = ["txn_1,1000", "txn_3,500", "txn_4,350"]
P4_OUT = ["MISSING_IN_GATEWAY txn_2", "MISSING_IN_SYSTEM txn_3", "AMOUNT_MISMATCH txn_4 300 350"]


def row(amount, status="payment_completed", provider="card", country="ie", **extra):
    d = {"id": "x", "amount": str(amount), "status": status, "payment_provider": provider, "buyer_country": country}
    d.update(extra)
    return d


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1([HEADER] + ROWS) == P1_OUT


@pytest.mark.part1
@pytest.mark.fmt
def test_percentage_half_up_hand_cases(impl):
    f = impl.fee_cents
    assert f(row(1000)) == 51
    assert f(row(1234)) == 56   # 25.914 -> 26
    assert f(row(500)) == 41    # 10.5 -> 11 (half-up, not banker's 10)
    assert f(row(1500)) == 62   # 31.5 -> 32
    assert f(row(99)) == 32     # 2.079 -> 2
    assert f(row(0)) == 30      # fixed part always applies
    assert f(row(10**12)) == 21 * 10**9 + 30


@pytest.mark.part1
@pytest.mark.edge
def test_dispute_and_other_statuses(impl):
    f = impl.fee_cents
    assert f(row(1, "dispute_lost", "klarna")) == 1500
    assert f(row(1, "dispute_won", "card")) == 1500
    assert f(row(1, "dispute_won", "klarna")) == 0
    assert f(row(1, "dispute_won", "Card")) == 0        # exact, case-sensitive provider match
    for st in ("payment_pending", "payment_failed", "refund_completed", "", "bogus"):
        assert f(row(1000, st)) == 0, st


@pytest.mark.part1
@pytest.mark.edge
def test_csv_by_header_whitespace_decimals_and_empty(impl):
    lines = ["status , amount , id , extra", " payment_completed , 10.00 , a , zzz", "", "dispute_lost,0,b,-"]
    assert impl.part1(lines) == ["a,51", "b,1500"]
    assert impl.part1([HEADER]) == []
    assert impl.part1([]) == []
    assert impl.to_cents("10.00") == 1000 and impl.to_cents("0.05") == 5 and impl.to_cents("-0.5") == -50
    with pytest.raises(ValueError):
        impl.to_cents("0.005")


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(RATES, [HEADER] + ROWS) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_table_floor_precedence_and_disputes_ignore_table(impl):
    rates = impl.parse_rates(["card,ie,140,25", "card,*,200,10", "*,de,300,0", "*,*,1,1"])
    f = impl.fee_cents
    assert f(row(1000, country="ie"), rates) == 39            # exact
    assert f(row(1000, country="fr"), rates) == 30            # (card, *) : 20 + 10
    assert f(row(1000, provider="klarna", country="de"), rates) == 30  # (*, de)
    assert f(row(1000, provider="klarna", country="fr"), rates) == 1   # (*, *) : 0 + 1
    assert f(row(999, provider="klarna", country="fr"), rates) == 1    # 0.0999 floored
    assert f(row(1234, provider="klarna"), impl.parse_rates(["klarna,*,290,0"])) == 35  # 35.786 floored
    assert f(row(1234, provider="klarna"), impl.parse_rates(["card,ie,140,25"])) == 56  # no match -> default half-up
    assert f(row(1000, "dispute_lost"), rates) == 1500
    assert f(row(1000, "dispute_won", "card"), rates) == 1500
    assert f(row(1000, "payment_pending"), rates) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_empty_rate_table_equals_part1(impl):
    assert impl.part2([], [HEADER] + ROWS) == P1_OUT


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_receivables_no_status(impl):
    assert impl.part3([RECV_HEADER] + RECV) == RECV_OUT


@pytest.mark.part3
def test_example_receivables_with_status(impl):
    h = RECV_HEADER + ",status,payment_provider"
    rows = ["c1,m1,2024-10-01,visa,1000,payment_completed,card",
            "c2,m1,2024-10-01,visa,500,dispute_lost,card",
            "c3,m1,2024-10-01,master,200,payment_completed,card",
            "c4,m2,2024-09-30,visa,700,payment_completed,card"]
    assert impl.part3([h] + rows) == ["merchant_id,card_type,payout_date,net",
                                      "m1,master,2024-10-01,166", "m1,visa,2024-10-01,-51", "m2,visa,2024-09-30,655"]


@pytest.mark.part3
@pytest.mark.fmt
def test_receivables_sort_keys_string_order_and_zero_groups(impl):
    rows = ["c,m2,2024-01-01,visa,1", "c,m10,2024-01-01,visa,1", "c,m2,2024-01-01,amex,0",
            "c,m2,2023-12-31,visa,5", "c,m2,2024-01-01,visa,-1"]
    assert impl.part3([RECV_HEADER] + rows) == [
        "merchant_id,card_type,payout_date,net",
        "m10,visa,2024-01-01,1",
        "m2,amex,2024-01-01,0",
        "m2,visa,2023-12-31,5",
        "m2,visa,2024-01-01,0",
    ]
    assert impl.part3([RECV_HEADER]) == ["merchant_id,card_type,payout_date,net"]


@pytest.mark.part3
@pytest.mark.edge
def test_receivables_column_order_and_rates(impl):
    lines = ["amount,card_type,merchant_id,payout_date,status,payment_provider,buyer_country",
             "1000,visa,m1,2024-10-01,payment_completed,card,ie",
             "1000,visa,m1,2024-10-01,payment_completed,card,ie"]
    assert impl.part3(lines)[1] == "m1,visa,2024-10-01,1898"           # 2 × (1000 − 51)
    rows = impl.parse_csv(lines)
    assert impl.receivables(rows, impl.parse_rates(["card,ie,140,25"]))[1] == "m1,visa,2024-10-01,1922"  # 2 × (1000 − 39)


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_reconcile(impl):
    assert impl.part4(SYSTEM, GATEWAY) == P4_OUT
    assert impl.reconcile(SYSTEM, GATEWAY, include_matches=True) == ["MATCH txn_1"] + P4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_reconcile_duplicates_empty_and_sort(impl):
    # duplicates inside one list are summed: gateway split txn_1 into 600 + 400
    assert impl.reconcile(["txn_1,1000"], ["txn_1,600", "txn_1,400"]) == []
    assert impl.reconcile(["txn_1,1000", "txn_1,1"], ["txn_1,1000"]) == ["AMOUNT_MISMATCH txn_1 1001 1000"]
    assert impl.reconcile([], []) == []
    assert impl.reconcile(["b,1", "a,1"], []) == ["MISSING_IN_GATEWAY a", "MISSING_IN_GATEWAY b"]
    assert impl.reconcile([], ["t10,1", "t2,1"]) == ["MISSING_IN_SYSTEM t10", "MISSING_IN_SYSTEM t2"]
    # zero and negative amounts still compare; decimals accepted
    assert impl.reconcile(["r,-500"], ["r,-5.00"]) == []
    assert impl.reconcile(["z,0"], ["z,1"]) == ["AMOUNT_MISMATCH z 0 1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 4\nSYSTEM\n" + "\n".join(SYSTEM) + "\nGATEWAY\n" + "\n".join(GATEWAY) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P4_OUT) + "\n"
    r = run_script("PART 1\n" + HEADER + "\n" + "\n".join(ROWS) + "\n")
    assert r.stdout == "\n".join(P1_OUT) + "\n"
    r = run_script("PART 2\nRATES\n" + "\n".join(RATES) + "\nTRANSACTIONS\n" + HEADER + "\n" + "\n".join(ROWS) + "\n")
    assert r.stdout == "\n".join(P2_OUT) + "\n"
    r = run_script("PART 3\n" + RECV_HEADER + "\n" + "\n".join(RECV) + "\n\n")
    assert r.stdout == "\n".join(RECV_OUT) + "\n"
    assert run_script("").stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_rows_receivables_and_200k_reconcile(run_script):
    rng = random.Random(0)
    statuses = ["payment_completed", "payment_completed", "dispute_lost", "dispute_won", "payment_pending"]
    lines = ["PART 3", RECV_HEADER + ",status,payment_provider,buyer_country"]
    for i in range(100_000):
        lines.append(f"c{i},m{rng.randrange(500)},2024-{rng.randrange(1, 13):02d}-{rng.randrange(1, 29):02d},"
                     f"{rng.choice(['visa', 'master', 'amex'])},{rng.randrange(0, 100000)},{rng.choice(statuses)},"
                     f"{rng.choice(['card', 'klarna'])},{rng.choice(['ie', 'de', 'br'])}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("merchant_id,card_type,payout_date,net\n") and r.stdout.count("\n") > 1000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    sys_l = [f"t{i},{rng.randrange(1, 10**6)}" for i in range(200_000)]
    gw_l = [ln if rng.random() < 0.9 else f"t{i},{rng.randrange(1, 10**6)}" for i, ln in enumerate(sys_l)]
    r = run_script("PART 4\nSYSTEM\n" + "\n".join(sys_l) + "\nGATEWAY\n" + "\n".join(gw_l[:190_000]) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("MISSING_IN_GATEWAY") == 10_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
