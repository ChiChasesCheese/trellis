import random

import pytest

EX1 = [
    "visa,txn_123,2500,usd,fraudulent,2024-01-05",
    "mastercard,txn_124,1999,eur,product_not_received,2024-01-06",
    "amex,txn_125,5000,gbp,duplicate,2024-01-07",
    "discover,txn_126,2500,jpy,general,2024-01-08",
]
EX1_OUT = [
    "[VISA] txn_123: $25.00 USD - fraudulent (2024-01-05)",
    "[MASTERCARD] txn_124: €19.99 EUR - product_not_received (2024-01-06)",
    "[AMEX] txn_125: £50.00 GBP - duplicate (2024-01-07)",
    "[DISCOVER] txn_126: ¥2500 JPY - general (2024-01-08)",
]
EX2 = [
    "visa,txn_1,2500,usd,fraudulent,2024-01-05",
    "visa,txn_2,25.00,usd,fraudulent,2024-01-05",
    "paypal,txn_3,100,usd,fraudulent,2024-01-05",
    "visa,txn_4,100,usd,fraudulent,2024-02-30",
    "visa,txn_5,100,usd,fraudulent",
    "visa,txn_6,100,usd,fraudulent,2024-01-05,extra",
]
EX2_OUT = ["[VISA] txn_1: $25.00 USD - fraudulent (2024-01-05)", "SKIPPED: 5"]
EX3 = [
    "visa,txn_1,2500,usd,fraudulent,2024-01-05",
    "visa,txn_1,2500,usd,withdrawn,2024-01-09",
    "mastercard,txn_1,2500,usd,fraudulent,2024-01-05",
    "visa,txn_2,100,usd,withdrawn,2024-01-01",
    "visa,txn_2,100,usd,fraudulent,2024-01-03",
    "visa,txn_3,700,usd,general,2024-01-03",
]
EX3_OUT = [
    "[MASTERCARD] txn_1: $25.00 USD - fraudulent (2024-01-05)",
    "[VISA] txn_3: $7.00 USD - general (2024-01-03)",
    "SKIPPED: 0",
]


def row(amount, currency="usd", network="visa", txn="t", reason="fraudulent", date="2024-01-05"):
    return f"{network},{txn},{amount},{currency},{reason},{date}"


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.fmt
def test_money_two_decimal_edge_amounts(impl):
    assert impl.part1([row(5)]) == ["[VISA] t: $0.05 USD - fraudulent (2024-01-05)"]
    assert impl.part1([row(100)]) == ["[VISA] t: $1.00 USD - fraudulent (2024-01-05)"]
    assert impl.part1([row(0)]) == ["[VISA] t: $0.00 USD - fraudulent (2024-01-05)"]
    assert impl.part1([row(123456789)]) == ["[VISA] t: $1234567.89 USD - fraudulent (2024-01-05)"]


@pytest.mark.part1
@pytest.mark.fmt
def test_money_zero_decimal_and_unknown_currency(impl):
    assert impl.part1([row(5, "jpy")]) == ["[VISA] t: ¥5 JPY - fraudulent (2024-01-05)"]
    assert impl.part1([row(2500, "krw")]) == ["[VISA] t: ₩2500 KRW - fraudulent (2024-01-05)"]
    assert impl.part1([row(1234, "cad")]) == ["[VISA] t: 12.34 CAD - fraudulent (2024-01-05)"]
    assert impl.part1([row(1234, "EUR")]) == ["[VISA] t: €12.34 EUR - fraudulent (2024-01-05)"]


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_blank_lines_case_and_order_preserved(impl):
    lines = ["", "  Visa , b , 100 , usd , general , 2024-01-05  ", row(1, txn="a"), ""]
    assert impl.part1(lines) == ["[VISA] b: $1.00 USD - general (2024-01-05)", "[VISA] a: $0.01 USD - fraudulent (2024-01-05)"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_single(impl):
    assert impl.part1([]) == []
    assert impl.part1([row(1)]) == ["[VISA] t: $0.01 USD - fraudulent (2024-01-05)"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_each_corruption_kind_individually(impl):
    bad = [
        row("25.00"), row("abc"), row(""), row(-1),                        # amount
        row(1, date="2024-02-30"), row(1, date="2024-13-01"), row(1, date="01/05/2024"), row(1, date=""),  # date
        row(1, network="paypal"), row(1, network="visa2"), row(1, network=""),                          # network
        "visa,t,1,usd,fraudulent", "visa,t,1,usd,fraudulent,2024-01-05,x", "visa", ",,,,,",              # fields
        row(1, txn=""), row(1, currency=""), row(1, reason=""),                                          # empty fields
    ]
    for b in bad:
        assert impl.part2([b]) == ["SKIPPED: 1"], b


@pytest.mark.part2
@pytest.mark.edge
def test_leap_day_and_non_padded_date_normalized(impl):
    assert impl.part2([row(1, date="2024-02-29")]) == ["[VISA] t: $0.01 USD - fraudulent (2024-02-29)", "SKIPPED: 0"]
    assert impl.part2([row(1, date="2023-02-29")]) == ["SKIPPED: 1"]
    assert impl.part2([row(1, date="2024-2-3")]) == ["[VISA] t: $0.01 USD - fraudulent (2024-02-03)", "SKIPPED: 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_skipped_zero_and_empty_input(impl):
    assert impl.part2([]) == ["SKIPPED: 0"]
    assert impl.part2(["", "  "]) == ["SKIPPED: 0"]
    assert impl.part2(EX1) == EX1_OUT + ["SKIPPED: 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_networks_case_insensitive_and_all_four_valid(impl):
    lines = [row(1, network=n) for n in ["VISA", "MasterCard", "amex", "DISCOVER"]]
    out = impl.part2(lines)
    assert out[-1] == "SKIPPED: 0"
    assert [o.split("]")[0] for o in out[:-1]] == ["[VISA", "[MASTERCARD", "[AMEX", "[DISCOVER"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_withdrawn_first_double_withdrawn_and_lone_withdrawn(impl):
    orig = row(100, txn="x")
    wd = row(100, txn="x", reason="withdrawn", date="2024-01-09")
    assert impl.part3([wd, orig]) == ["SKIPPED: 0"]
    assert impl.part3([orig, wd, wd]) == ["SKIPPED: 0"]
    assert impl.part3([wd]) == ["SKIPPED: 0"]
    assert impl.part3([orig, orig]) == [impl.part1([orig])[0]] * 2 + ["SKIPPED: 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_same_id_different_network_is_distinct(impl):
    v = row(100, txn="x", network="visa")
    m = row(100, txn="x", network="mastercard")
    wd = row(100, txn="x", network="visa", reason="withdrawn")
    assert impl.part3([v, m, wd]) == ["[MASTERCARD] x: $1.00 USD - fraudulent (2024-01-05)", "SKIPPED: 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_corrupted_withdrawal_does_not_cancel_and_is_counted(impl):
    orig = row(100, txn="x")
    bad_wd = row("1.0", txn="x", reason="withdrawn")
    assert impl.part3([orig, bad_wd]) == ["[VISA] x: $1.00 USD - fraudulent (2024-01-05)", "SKIPPED: 1"]
    # withdrawn rows removed by the rule are NOT counted as skipped
    assert impl.part3([orig, row(100, txn="x", reason="withdrawn"), row("z")]) == ["SKIPPED: 1"]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_survivors_keep_input_order_and_part1_part2_unchanged(impl):
    lines = [row(3, txn="c"), row(1, txn="a", reason="withdrawn"), row(2, txn="b"), row(1, txn="a")]
    assert impl.part3(lines) == ["[VISA] c: $0.03 USD - fraudulent (2024-01-05)", "[VISA] b: $0.02 USD - fraudulent (2024-01-05)", "SKIPPED: 0"]
    assert impl.part3(EX1) == EX1_OUT + ["SKIPPED: 0"]
    assert impl.part3(EX2) == EX2_OUT
    assert impl.part2(EX3) == [impl.part1([l])[0] for l in EX3] + ["SKIPPED: 0"]  # part 2 does not cancel


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.stdout == "\n".join(EX2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    assert run_script("PART 1\n").stdout == ""
    assert run_script("PART 2\n").stdout == "SKIPPED: 0\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_200k_rows(run_script):
    rng = random.Random(0)
    nets = ["visa", "mastercard", "amex", "discover", "paypal"]
    curs = ["usd", "eur", "gbp", "jpy"]
    lines = []
    for i in range(200_000):
        k = rng.random()
        amt = rng.randrange(0, 10_000_000) if k > 0.05 else "12.5"
        date = f"2024-{rng.randrange(1, 13):02d}-{rng.randrange(1, 32):02d}"
        reason = "withdrawn" if k < 0.15 else "fraudulent"
        lines.append(f"{rng.choice(nets)},txn_{rng.randrange(100_000)},{amt},{rng.choice(curs)},{reason},{date}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip("\n").splitlines()[-1].startswith("SKIPPED: ")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
