import random

import pytest

EX1 = ["t1,alice,credit,100.00", "t2,bob,credit,50.50", "t3,alice,debit,30.25", "t4,bob,debit,50.50", "t5,carol,debit,10.00"]
EX1_OUT = ["alice 69.75", "carol -10.00"]
EX2_OUT = ["alice 69.75", "REJECTED: t5"]
EX2B = ["t1,a,credit,10.00", "t2,a,debit,10.00", "t3,a,debit,0.01", "t4,a,credit,5.00"]
EX2B_OUT = ["a 5.00", "REJECTED: t3"]
EX3 = [
    "t1,platform,credit,100.00",
    "t2,alice,credit,20.00",
    "t3,alice,debit,50.00",
    "t4,bob,credit,10.00",
    "t5,bob,transfer,alice,25.00",
    "t6,alice,credit,10.00",
    "t7,carol,debit,200.00",
    "t8,bob,debit,100.00",
]
EX3_OUT = ["alice 5.00", "platform 85.00", "REJECTED: t7,t8", "MAX_RESERVE: 45.00"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_zero_balances_omitted_and_empty(impl):
    assert impl.part1([]) == []
    assert impl.part1(["t1,a,credit,5.00", "t2,a,debit,5.00"]) == []
    assert impl.part1(["t1,a,credit,0.00"]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_negative_and_amount_formats(impl):
    assert impl.part1(["t1,a,debit,3.5"]) == ["a -3.50"]
    assert impl.part1(["t1,a,debit,0.5"]) == ["a -0.50"]
    assert impl.part1(["t1,a,credit,7", "t2,a,credit,12.3"]) == ["a 19.30"]
    assert impl.part1(["t1,a,credit,0.10", "t2,a,credit,0.20"]) == ["a 0.30"]


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_plain_string_order(impl):
    lines = ["t1,user2,credit,1", "t2,user10,credit,1", "t3,B,credit,1", "t4,a,credit,1"]
    assert impl.part1(lines) == ["B 1.00", "a 1.00", "user10 1.00", "user2 1.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_and_large_amounts(impl):
    assert impl.part1([" t1 , a , credit , 1.25 ", ""]) == ["a 1.25"]
    assert impl.part1(["t1,a,credit,99999999999.99", "t2,a,credit,0.01"]) == ["a 100000000000.00"]


@pytest.mark.part1
def test_part1_never_rejects(impl):
    assert impl.part1(["t1,a,debit,1.00", "t2,a,debit,1.00"]) == ["a -2.00"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX1) == EX2_OUT
    assert impl.part2(EX2B) == EX2B_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_boundary_exact_one_below_one_above(impl):
    assert impl.part2(["t1,a,credit,10.00", "t2,a,debit,10.00"]) == ["REJECTED: NONE"]
    assert impl.part2(["t1,a,credit,10.00", "t2,a,debit,9.99"]) == ["a 0.01", "REJECTED: NONE"]
    assert impl.part2(["t1,a,credit,10.00", "t2,a,debit,10.01"]) == ["a 10.00", "REJECTED: t2"]


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_user_debit_rejected_and_none(impl):
    assert impl.part2(["t1,ghost,debit,0.01"]) == ["REJECTED: t1"]
    assert impl.part2([]) == ["REJECTED: NONE"]
    assert impl.part2(["t1,a,credit,1"]) == ["a 1.00", "REJECTED: NONE"]


@pytest.mark.part2
@pytest.mark.fmt
def test_rejected_order_and_format(impl):
    lines = ["t9,a,debit,1", "t1,a,credit,1", "t5,a,debit,2", "t2,a,debit,1", "t3,a,debit,0.01"]
    assert impl.part2(lines) == ["REJECTED: t9,t5,t3"]


@pytest.mark.part2
def test_rejected_debit_does_not_change_balance(impl):
    lines = ["t1,a,credit,5", "t2,a,debit,6", "t3,a,debit,5"]
    assert impl.part2(lines) == ["REJECTED: t2"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_no_platform_behaves_like_part2_plus_reserve(impl):
    assert impl.part3(EX1) == ["alice 69.75", "REJECTED: t5", "MAX_RESERVE: 0.00"]
    assert impl.part3([]) == ["REJECTED: NONE", "MAX_RESERVE: 0.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_loan_boundary_equal_and_one_cent_over(impl):
    # platform has exactly the shortfall -> allowed, platform goes to 0 (omitted)
    assert impl.part3(["t1,platform,credit,10.00", "t2,a,debit,10.00"]) == ["REJECTED: NONE", "MAX_RESERVE: 10.00"]
    assert impl.part3(["t1,platform,credit,10.00", "t2,a,debit,10.01"]) == ["platform 10.00", "REJECTED: t2", "MAX_RESERVE: 0.00"]
    # user has some funds: only the shortfall is borrowed
    assert impl.part3(["t1,platform,credit,10.00", "t2,a,credit,4.00", "t3,a,debit,10.00"]) == ["platform 4.00", "REJECTED: NONE", "MAX_RESERVE: 6.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_repayment_capped_and_excess_kept(impl):
    lines = ["t1,platform,credit,10.00", "t2,a,debit,6.00", "t3,a,credit,2.00", "t4,a,credit,10.00"]
    # loan 6; credit 2 -> repay 2 (loan 4, a 0); credit 10 -> repay 4, a keeps 6
    assert impl.part3(lines) == ["a 6.00", "platform 10.00", "REJECTED: NONE", "MAX_RESERVE: 6.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_platform_never_borrows_and_transfers(impl):
    # platform overdraft rejected
    assert impl.part3(["t1,platform,credit,5", "t2,platform,debit,6"]) == ["platform 5.00", "REJECTED: t2", "MAX_RESERVE: 0.00"]
    # platform as transfer source / destination is a plain account
    assert impl.part3(["t1,platform,credit,5", "t2,platform,transfer,a,3", "t3,a,transfer,platform,1"]) == [
        "a 2.00", "platform 3.00", "REJECTED: NONE", "MAX_RESERVE: 0.00"]
    # rejected transfer leaves both sides untouched
    assert impl.part3(["t1,a,credit,1", "t2,a,transfer,b,5"]) == ["a 1.00", "REJECTED: t2", "MAX_RESERVE: 0.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_peak_reserve_measured_before_receiver_repays(impl):
    # a borrows 10 (peak 10); transfers 10 to b; b had a 4 loan -> repays 4 -> loans now 10 (a) ... peak stays 10
    lines = ["t1,platform,credit,20", "t2,b,debit,4", "t3,a,transfer,b,10", "t4,a,credit,10"]
    # after t2: loans b=4 (peak 4). t3: a borrows 10 -> loans 14 (peak 14), b receives 10 -> repays 4, b keeps 6.
    # t4: a repays 10. platform: 20-4-10+4+10 = 20
    assert impl.part3(lines) == ["b 6.00", "platform 20.00", "REJECTED: NONE", "MAX_RESERVE: 14.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_reserve_is_peak_not_final_and_not_sum_of_all_loans(impl):
    lines = ["t1,platform,credit,100", "t2,a,debit,30", "t3,a,credit,30", "t4,a,debit,20", "t5,a,credit,20"]
    # peak 30 (not 50 = total ever borrowed, not 0 = final)
    assert impl.part3(lines) == ["platform 100.00", "REJECTED: NONE", "MAX_RESERVE: 30.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_credit_to_platform_repays_nothing_and_multiple_borrowers(impl):
    lines = ["t1,platform,credit,10", "t2,a,debit,4", "t3,b,debit,6", "t4,platform,credit,1", "t5,c,debit,0.01"]
    # loans a=4,b=6 -> peak 10; platform 0 +1 = 1; c needs 0.01 -> allowed (1 >= 0.01) -> peak 10.01
    assert impl.part3(lines) == ["platform 0.99", "REJECTED: NONE", "MAX_RESERVE: 10.01"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("PART 2\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_200k_transactions(run_script):
    rng = random.Random(0)
    lines = ["t0,platform,credit,1000000.00"]
    for i in range(1, 200_000):
        u = f"u{rng.randrange(5000)}"
        amt = f"{rng.randrange(0, 10000)}.{rng.randrange(100):02d}"
        k = rng.random()
        if k < 0.45:
            lines.append(f"t{i},{u},credit,{amt}")
        elif k < 0.8:
            lines.append(f"t{i},{u},debit,{amt}")
        else:
            lines.append(f"t{i},{u},transfer,u{rng.randrange(5000)},{amt}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip("\n").splitlines()[-1].startswith("MAX_RESERVE: ")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
