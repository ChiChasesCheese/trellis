import random

import pytest

INV_A = ["invoiceA,2024-01-01,100", "invoiceB,2024-01-15,200", "invoiceC,2024-02-01,500"]
PAY_A = ["paymentABC,500,Paying off: invoiceC", "payment2,200,Paying off: invoiceA", "payment3,100,invoiceA"]
OUT_A1 = ["invoiceA: UNPAID", "invoiceB: UNPAID", "invoiceC: PAID"]
OUT_A2 = ["invoiceA: PAID", "invoiceB: UNPAID", "invoiceC: PAID"]

INV_B = ["invoiceA,2024-03-01,100", "invoiceB,2024-01-01,100", "invoiceC,2024-02-01,300"]
PAY_B = ["p1,100,", "p2,100,Thanks!", "p3,250,Paying off: invoiceA and invoiceC"]
OUT_B = ["invoiceA: PAID", "invoiceB: PAID", "invoiceC: UNPAID"]

PAY_C = [
    "paymentABC,500,Paying off: invoiceC",
    "payment2,250,",
    "payment3,40,Paying off: invoiceB",
    "payment4,1000,Paying off: invoiceA",
]
OUT_C = ["invoiceA: PAID", "invoiceB: PARTIAL (remaining 10)", "invoiceC: PAID", "payment4: UNAPPLIED 1000"]
OUT_D = [
    "paymentABC -> invoiceC 500",
    "payment2 -> invoiceA 100",
    "payment2 -> invoiceB 150",
    "payment3 -> invoiceB 40",
] + OUT_C


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_a_part1(impl):
    assert impl.part1(INV_A, PAY_A) == OUT_A1


@pytest.mark.part1
@pytest.mark.edge
def test_part1_memo_is_strict(impl):
    inv = ["invoiceA,2024-01-01,100"]
    assert impl.part1(inv, ["p,100,Paying off: invoiceA today"]) == ["invoiceA: UNPAID"]
    assert impl.part1(inv, ["p,100,invoiceA"]) == ["invoiceA: UNPAID"]
    assert impl.part1(inv, ["p,100,Paying off:   invoiceA  "]) == ["invoiceA: PAID"]  # spaces around id ok


@pytest.mark.part1
@pytest.mark.edge
def test_part1_no_double_pay_and_amount_mismatch(impl):
    inv = ["invoiceA,2024-01-01,100", "invoiceB,2024-01-02,100"]
    pays = ["p1,100,Paying off: invoiceA", "p2,100,Paying off: invoiceA", "p3,99,Paying off: invoiceB"]
    # p2 repeats an already-paid invoice -> ignored (must NOT slide onto invoiceB); p3 is 1 cent short
    assert impl.part1(inv, pays) == ["invoiceA: PAID", "invoiceB: UNPAID"]
    assert impl.part1(inv, ["p,101,Paying off: invoiceB"]) == ["invoiceA: UNPAID", "invoiceB: UNPAID"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_unknown_invoice_empty_inputs(impl):
    assert impl.part1(["invoiceA,2024-01-01,100"], ["p,100,Paying off: invoiceZ"]) == ["invoiceA: UNPAID"]
    assert impl.part1([], ["p,100,Paying off: invoiceA"]) == []
    assert impl.part1(["invoiceA,2024-01-01,100"], []) == ["invoiceA: UNPAID"]
    assert impl.part1(["z,2024-01-01,0"], []) == ["z: PAID"]  # zero-amount invoice owes nothing


@pytest.mark.part1
@pytest.mark.fmt
def test_output_is_invoice_input_order_not_due_order(impl):
    inv = ["late,2024-12-31,5", "early,2024-01-01,5"]
    assert impl.part1(inv, ["p,5,Paying off: late", " q , 5 , Paying off: early "]) == ["late: PAID", "early: PAID"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_a_under_part2(impl):
    assert impl.part2(INV_A, PAY_A) == OUT_A2


@pytest.mark.part2
def test_example_b_part2(impl):
    assert impl.part2(INV_B, PAY_B) == OUT_B


@pytest.mark.part2
@pytest.mark.edge
def test_part2_earliest_due_then_input_order(impl):
    inv = ["x,2024-02-01,100", "y,2024-01-01,100", "z,2024-01-01,100"]
    assert impl.part2(inv, ["p,100,"]) == ["x: UNPAID", "y: PAID", "z: UNPAID"]
    assert impl.part2(inv, ["p,100,", "q,100,"]) == ["x: UNPAID", "y: PAID", "z: PAID"]
    assert impl.part2(inv, ["p,100,", "q,100,", "r,100,", "s,100,"]) == ["x: PAID", "y: PAID", "z: PAID"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_mentions_restrict_and_never_fall_back(impl):
    inv = ["a,2024-01-01,100", "b,2024-01-02,100", "c,2024-01-03,100"]
    # mentions b and c -> earliest-due among the mentioned (b), not the globally earliest (a)
    assert impl.part2(inv, ["p,100,for c and b"]) == ["a: UNPAID", "b: PAID", "c: UNPAID"]
    # mentioned invoice has the wrong amount -> ignored; does NOT fall back to a/b
    assert impl.part2(inv, ["p,100,c", "q,50,c"]) == ["a: UNPAID", "b: UNPAID", "c: PAID"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_memo_commas_and_whole_token_match(impl):
    inv = ["invoiceA,2024-01-01,100", "invoiceAB,2024-01-02,100"]
    # memo split only on first two commas; 'invoiceAB' must not count as a mention of 'invoiceA'
    assert impl.part2(inv, ["p,100,Paying off: invoiceAB, thanks"]) == ["invoiceA: UNPAID", "invoiceAB: PAID"]
    assert impl.part2(inv, ["p,100,ref invoiceA/invoiceAB"]) == ["invoiceA: PAID", "invoiceAB: UNPAID"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_c_part3(impl):
    assert impl.part3(INV_A, PAY_C) == OUT_C


@pytest.mark.part3
@pytest.mark.edge
def test_part3_boundaries_equal_below_above(impl):
    inv = ["a,2024-01-01,100"]
    assert impl.part3(inv, ["p,100,"]) == ["a: PAID"]
    assert impl.part3(inv, ["p,99,"]) == ["a: PARTIAL (remaining 1)"]
    assert impl.part3(inv, ["p,101,"]) == ["a: PAID", "p: UNAPPLIED 1"]
    # two partial payments complete the invoice
    assert impl.part3(inv, ["p,60,", "q,40,"]) == ["a: PAID"]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_pour_oldest_first_and_no_spill_when_mentioned(impl):
    inv = ["b,2024-02-01,100", "a,2024-01-01,100", "c,2024-03-01,100"]
    assert impl.part3(inv, ["p,150,"]) == ["b: PARTIAL (remaining 50)", "a: PAID", "c: UNPAID"]
    # mentions only c: leftover stays unapplied even though b and a are open
    assert impl.part3(inv, ["p,150,Paying off: c"]) == ["b: UNPAID", "a: UNPAID", "c: PAID", "p: UNAPPLIED 50"]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_zero_negative_and_large_amounts(impl):
    inv = ["a,2024-01-01,100"]
    assert impl.part3(inv, ["p,0,", "q,-5,Paying off: a"]) == ["a: UNPAID"]
    big = 10**12
    assert impl.part3([f"a,2024-01-01,{big}"], [f"p,{big + 7},"]) == ["a: PAID", "p: UNAPPLIED 7"]
    assert impl.part3([f"a,2024-01-01,{big}"], [f"p,{big - 1},"]) == ["a: PARTIAL (remaining 1)"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_d_part4(impl):
    assert impl.part4(INV_A, PAY_C) == OUT_D


@pytest.mark.part4
@pytest.mark.fmt
def test_part4_audit_order_and_no_line_for_ignored_payment(impl):
    inv = ["a,2024-01-01,10", "b,2024-01-02,10"]
    out = impl.part4(inv, ["p,15,", "z,0,", "q,15,"])
    assert out == ["p -> a 10", "p -> b 5", "q -> b 5", "a: PAID", "b: PAID", "q: UNAPPLIED 10"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    stdin = "PART 4\nINVOICES\n" + "\n".join(INV_A) + "\n\nPAYMENTS\n" + "\n".join(PAY_C) + "\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(OUT_D) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_part1_and_empty(run_script):
    r = run_script("PART 1\nINVOICES\n" + "\n".join(INV_A) + "\nPAYMENTS\n" + "\n".join(PAY_A) + "\n")
    assert r.returncode == 0 and r.stdout == "\n".join(OUT_A1) + "\n"
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_invoices_100k_payments(run_script):
    rng = random.Random(0)
    n = 100_000
    inv = [f"inv{i},2024-{rng.randrange(1, 13):02d}-{rng.randrange(1, 29):02d},{rng.randrange(1, 10_000)}" for i in range(n)]
    pays = []
    for j in range(n):
        if rng.random() < 0.5:
            pays.append(f"pay{j},{rng.randrange(1, 10_000)},Paying off: inv{rng.randrange(n)}")
        else:
            pays.append(f"pay{j},{rng.randrange(1, 10_000)},")
    r = run_script("PART 3\nINVOICES\n" + "\n".join(inv) + "\nPAYMENTS\n" + "\n".join(pays) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= n
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    print(f"\nMeasured: {r.seconds:.2f}s, {r.max_rss_mb:.0f} MB")
