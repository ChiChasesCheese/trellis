import random

import pytest

# ---- verbatim examples from joeytor/StripeInterview StripeCapital.java ----------------------
EX0 = ["CREATE_LOAN: acct_foobar,loan1,5000", "PAY_LOAN: acct_foobar,loan1,1000"]
EX0_OUT = ["acct_foobar,4000"]
EX1 = [
    "CREATE_LOAN: acct_foobar,loan1,5000",
    "CREATE_LOAN: acct_foobar,loan2,5000",
    "TRANSACTION_PROCESSED: acct_foobar,loan1,500,10",
    "TRANSACTION_PROCESSED: acct_foobar,loan2,500,1",
]
EX1_OUT = ["acct_foobar,9945"]
EX2 = [
    "CREATE_LOAN: acct_foobar,loan1,1000",
    "CREATE_LOAN: acct_foobar,loan2,2000",
    "CREATE_LOAN: acct_barfoo,loan1,3000",
    "TRANSACTION_PROCESSED: acct_foobar,loan1,100,1",
    "PAY_LOAN: acct_barfoo,loan1,1000",
    "INCREASE_LOAN: acct_foobar,loan2,1000",
]
EX2_OUT = ["acct_barfoo,2000", "acct_foobar,3999"]
EX3 = [
    "CREATE_LOAN: m1,l1,100",
    "PAY_LOAN: m1,l9,50",
    "PAY_LOAN: m2,l1,50",
    "TRANSACTION_PROCESSED: m1,l1,1000,0",
    "CREATE_LOAN: m1,l1,999",
    "CREATE_LOAN: m3,l1,40",
    "PAY_LOAN: m3,l1,45",
]
EX3_OUT = ["m1,100"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example0_manual_repayment(impl):
    assert impl.part1(EX0) == EX0_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_overpayment_capped_and_merchant_skipped(impl):
    assert impl.part1(["CREATE_LOAN: m,l,100", "PAY_LOAN: m,l,100"]) == []          # exactly 0
    assert impl.part1(["CREATE_LOAN: m,l,100", "PAY_LOAN: m,l,101"]) == []          # one over -> capped
    assert impl.part1(["CREATE_LOAN: m,l,100", "PAY_LOAN: m,l,99"]) == ["m,1"]      # one below


@pytest.mark.part1
@pytest.mark.edge
def test_overpayment_remainder_not_carried_to_other_loan(impl):
    lines = ["CREATE_LOAN: m,a,100", "CREATE_LOAN: m,b,100", "PAY_LOAN: m,a,150"]
    assert impl.part1(lines) == ["m,100"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_zero_amount_loan(impl):
    assert impl.part1([]) == []
    assert impl.part1(["CREATE_LOAN: m,l,0"]) == []


@pytest.mark.part1
def test_spaces_after_commas_and_blank_lines(impl):
    assert impl.part1(["CREATE_LOAN: merchant1, loan1, 1000", "", "  PAY_LOAN: merchant1 , loan1 , 1 "]) == ["merchant1,999"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example1_transaction_repayment(impl):
    assert impl.part2(EX1) == EX1_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_truncation_of_withheld_amount(impl):
    # 4336 * 10 / 100 = 433.6 -> 433
    assert impl.part2(["CREATE_LOAN: m,l,1000", "TRANSACTION_PROCESSED: m,l,4336,10"]) == ["m,567"]
    # 99 * 1 / 100 = 0.99 -> 0: nothing repaid
    assert impl.part2(["CREATE_LOAN: m,l,1000", "TRANSACTION_PROCESSED: m,l,99,1"]) == ["m,1000"]
    # 100% withheld
    assert impl.part2(["CREATE_LOAN: m,l,1000", "TRANSACTION_PROCESSED: m,l,300,100"]) == ["m,700"]


@pytest.mark.part2
@pytest.mark.edge
def test_transaction_overpays_capped(impl):
    assert impl.part2(["CREATE_LOAN: m,l,10", "TRANSACTION_PROCESSED: m,l,10000,50"]) == []


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example2_multiple_actions(impl):
    assert impl.part3(EX2) == EX2_OUT


@pytest.mark.part3
def test_increase_then_pay_and_loan_ids_scoped_per_merchant(impl):
    lines = ["CREATE_LOAN: m1,loan1,100", "CREATE_LOAN: m2,loan1,100", "INCREASE_LOAN: m1,loan1,50", "PAY_LOAN: m2,loan1,30"]
    assert impl.part3(lines) == ["m1,150", "m2,70"]


@pytest.mark.part3
@pytest.mark.fmt
def test_output_sorted_plain_string_order(impl):
    lines = ["CREATE_LOAN: m2,l,1", "CREATE_LOAN: m10,l,1", "CREATE_LOAN: B,l,1", "CREATE_LOAN: a,l,1"]
    assert impl.part3(lines) == ["B,1", "a,1", "m10,1", "m2,1"]


@pytest.mark.part3
@pytest.mark.edge
def test_loanless_transaction_repays_oldest_first(impl):
    lines = [
        "CREATE_LOAN: m,old,100",
        "CREATE_LOAN: m,new,100",
        "TRANSACTION_PROCESSED: m,1500,10",  # 150 withheld: 100 clears 'old', 50 off 'new'
    ]
    assert impl.part3(lines) == ["m,50"]
    assert impl.part3(lines + ["TRANSACTION_PROCESSED: m,10000,10"]) == []   # excess ignored


@pytest.mark.part3
def test_increase_revives_a_repaid_loan(impl):
    lines = ["CREATE_LOAN: m,l,100", "PAY_LOAN: m,l,100", "INCREASE_LOAN: m,l,5"]
    assert impl.part3(lines) == ["m,5"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example3_invalid_actions(impl):
    assert impl.part4(EX3) == EX3_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_unknown_merchant_or_loan_is_noop(impl):
    base = ["CREATE_LOAN: m,l,100"]
    for bad in ["PAY_LOAN: x,l,10", "PAY_LOAN: m,x,10", "INCREASE_LOAN: m,x,10", "TRANSACTION_PROCESSED: x,l,100,10", "TRANSACTION_PROCESSED: m,x,100,10"]:
        assert impl.part4(base + [bad]) == ["m,100"], bad
    assert impl.part4(["PAY_LOAN: m,l,10"]) == []


@pytest.mark.part4
@pytest.mark.edge
def test_percentage_bounds_and_negative_amounts(impl):
    base = ["CREATE_LOAN: m,l,1000"]
    assert impl.part4(base + ["TRANSACTION_PROCESSED: m,l,1000,0"]) == ["m,1000"]     # below 1
    assert impl.part4(base + ["TRANSACTION_PROCESSED: m,l,1000,1"]) == ["m,990"]      # == 1
    assert impl.part4(base + ["TRANSACTION_PROCESSED: m,l,1000,100"]) == []           # == 100
    assert impl.part4(base + ["TRANSACTION_PROCESSED: m,l,1000,101"]) == ["m,1000"]   # above 100
    assert impl.part4(base + ["PAY_LOAN: m,l,-5"]) == ["m,1000"]
    assert impl.part4(base + ["INCREASE_LOAN: m,l,-5"]) == ["m,1000"]
    assert impl.part4(["CREATE_LOAN: m,l,-5"]) == []


@pytest.mark.part4
@pytest.mark.edge
def test_duplicate_create_default_ignored_and_variants(impl):
    lines = ["CREATE_LOAN: m,l,100", "CREATE_LOAN: m,l,5"]
    assert impl.part4(lines) == ["m,100"]
    assert impl.process(lines, duplicate_create="replace") == ["m,5"]
    assert impl.process(lines, duplicate_create="add") == ["m,105"]


@pytest.mark.part4
@pytest.mark.edge
def test_unknown_method_and_garbage_ignored(impl):
    assert impl.part4(["CREATE_LOAN: m,l,100", "REFUND: m,l,10", "hello world", "PAY_LOAN: m,l"]) == ["m,100"]


@pytest.mark.part4
@pytest.mark.edge
def test_source_example0_verbatim_loan_typo_is_noop(impl):
    # the prose says 'loan' (nonexistent) -> Part 4 no-op, so the balance stays 5000
    assert impl.part4(["CREATE_LOAN: acct_foobar,loan1,5000", "PAY_LOAN: acct_foobar,loan,1000"]) == ["acct_foobar,5000"]


@pytest.mark.part4
@pytest.mark.edge
def test_large_balances_stay_exact(impl):
    lines = ["CREATE_LOAN: m,l,1000000000000", "TRANSACTION_PROCESSED: m,l,999999999999,33"]
    assert impl.part4(lines) == ["m,670000000001"]  # 999999999999*33//100 = 329999999999


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "acct_barfoo,2000\nacct_foobar,3999\n"


@pytest.mark.part4
@pytest.mark.io
def test_empty_stdin_and_all_repaid(run_script):
    assert run_script("").stdout == ""
    assert run_script("CREATE_LOAN: m,l,5\nPAY_LOAN: m,l,5\n").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_actions(run_script):
    rng = random.Random(0)
    lines = [f"CREATE_LOAN: m{i},l{j},{rng.randrange(1, 10**6)}" for i in range(2000) for j in range(3)]
    for _ in range(100_000):
        m, l = f"m{rng.randrange(2000)}", f"l{rng.randrange(4)}"
        k = rng.randrange(3)
        if k == 0:
            lines.append(f"PAY_LOAN: {m},{l},{rng.randrange(0, 1000)}")
        elif k == 1:
            lines.append(f"INCREASE_LOAN: {m},{l},{rng.randrange(0, 1000)}")
        else:
            lines.append(f"TRANSACTION_PROCESSED: {m},{l},{rng.randrange(0, 10**5)},{rng.randrange(1, 101)}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") <= 2000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
