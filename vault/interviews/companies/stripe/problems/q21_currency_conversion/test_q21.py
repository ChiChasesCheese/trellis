import random

import pytest

RATES = "USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110"
BEST = "AUD:USD:0.7,USD:CAD:1.2,AUD:GBP:0.5,GBP:CAD:1.7"


# ---------------------------------------------------------------- parsing / fmt
@pytest.mark.part1
def test_parse_rates_basic_and_whitespace(impl):
    assert impl.parse_rates(RATES) == {("USD", "AUD"): 1.4, ("CAD", "USD"): 0.8, ("USD", "JPY"): 110.0}
    assert impl.parse_rates(" USD : AUD : 1.4 , ,CAD:USD:0.8 ") == {("USD", "AUD"): 1.4, ("CAD", "USD"): 0.8}
    assert impl.parse_rates("") == {}


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_pair_last_wins_and_zero_rate_invalid(impl):
    assert impl.parse_rates("USD:AUD:1.4,USD:AUD:1.5") == {("USD", "AUD"): 1.5}
    with pytest.raises(ValueError):
        impl.parse_rates("USD:AUD:0")
    with pytest.raises(ValueError):
        impl.parse_rates("USD:AUD:-2")
    with pytest.raises(ValueError):
        impl.parse_rates("USD:AUD:abc")


@pytest.mark.part1
@pytest.mark.fmt
def test_fmt_rate_exact(impl):
    assert impl.fmt_rate(1.4) == "1.4"
    assert impl.fmt_rate(1 / 1.4) == "0.714286"
    assert impl.fmt_rate(88.0) == "88"
    assert impl.fmt_rate(1.0) == "1"
    assert impl.fmt_rate(0.8 * 1.4) == "1.12"          # 1.1200000000000001 in float
    assert impl.fmt_rate(1 / 110) == "0.009091"
    assert impl.fmt_rate(0.0000001) == "0"


# ---------------------------------------------------------------- Part 1: direct
@pytest.mark.part1
def test_example_part1(impl):
    r = impl.parse_rates(RATES)
    assert impl.convert(r, "USD", "AUD") == 1.4
    assert impl.convert(r, "CAD", "USD") == 0.8
    assert impl.convert(r, "AUD", "USD") is None       # inverse NOT allowed in part 1
    assert impl.convert(r, "USD", "USD") == 1.0
    assert impl.convert(r, "USD", "GBP") is None


@pytest.mark.part1
@pytest.mark.edge
def test_part1_same_currency_unknown_and_empty(impl):
    assert impl.convert({}, "XXX", "XXX") == 1.0
    assert impl.convert({}, "USD", "AUD") is None
    assert impl.convert(impl.parse_rates(RATES), "GBP", "USD") is None


# ---------------------------------------------------------------- Part 2: inverse
@pytest.mark.part2
def test_example_part2(impl):
    r = impl.parse_rates(RATES)
    assert impl.convert_with_inverse(r, "AUD", "USD") == pytest.approx(1 / 1.4)
    assert impl.convert_with_inverse(r, "USD", "CAD") == pytest.approx(1.25)
    assert impl.convert_with_inverse(r, "USD", "AUD") == 1.4
    assert impl.fmt_rate(impl.convert_with_inverse(r, "AUD", "USD")) == "0.714286"


@pytest.mark.part2
@pytest.mark.edge
def test_part2_direct_beats_inverse_and_no_multihop(impl):
    r = impl.parse_rates("USD:AUD:1.4,AUD:USD:0.8")   # inconsistent both ways
    assert impl.convert_with_inverse(r, "AUD", "USD") == 0.8
    assert impl.convert_with_inverse(r, "USD", "AUD") == 1.4
    r2 = impl.parse_rates(RATES)
    assert impl.convert_with_inverse(r2, "AUD", "JPY") is None   # needs 2 hops -> part 3
    assert impl.convert_with_inverse(r2, "JPY", "JPY") == 1.0
    assert impl.convert_with_inverse(r2, "USD", "ZZZ") is None


# ---------------------------------------------------------------- Part 3: multi-hop
@pytest.mark.part3
def test_example_part3_paths_and_rates(impl):
    r = impl.parse_rates(RATES)
    rate, path = impl.best_conversion(r, "AUD", "JPY")
    assert path == ["AUD", "USD", "JPY"] and impl.fmt_rate(rate) == "78.571429"
    rate, path = impl.best_conversion(r, "CAD", "AUD")
    assert path == ["CAD", "USD", "AUD"] and impl.fmt_rate(rate) == "1.12"
    rate, path = impl.best_conversion(r, "CAD", "JPY")
    assert path == ["CAD", "USD", "JPY"] and impl.fmt_rate(rate) == "88"
    assert impl.best_conversion(r, "JPY", "JPY") == (1.0, ["JPY"])
    assert impl.find_path(r, "AUD", "JPY") == ["AUD", "USD", "JPY"]
    assert impl.find_path(r, "JPY", "JPY") == ["JPY"]


@pytest.mark.part3
def test_example_best_path_beats_first_path(impl):
    r = impl.parse_rates(BEST)
    rate, path = impl.best_conversion(r, "AUD", "CAD")
    assert path == ["AUD", "GBP", "CAD"] and rate == pytest.approx(0.85)
    assert impl.find_path(r, "AUD", "CAD") == ["AUD", "USD", "CAD"]   # BFS: first 2-hop found


@pytest.mark.part3
@pytest.mark.edge
def test_part3_disconnected_unknown(impl):
    r = impl.parse_rates("USD:AUD:1.4,EUR:GBP:0.9")
    assert impl.best_conversion(r, "USD", "GBP") is None
    assert impl.find_path(r, "USD", "GBP") is None
    assert impl.best_conversion(r, "USD", "XXX") is None
    assert impl.best_conversion(r, "XXX", "USD") is None
    assert impl.best_conversion({}, "A", "B") is None
    assert impl.best_conversion(r, "USD", "AUD") == (1.4, ["USD", "AUD"])   # still works inside a component


@pytest.mark.part3
@pytest.mark.edge
def test_part3_longer_path_can_be_best(impl):
    # A->D direct 1.2 ; A->B->C->D = 1.1^3 = 1.331
    r = impl.parse_rates("A:D:1.2,A:B:1.1,B:C:1.1,C:D:1.1")
    rate, path = impl.best_conversion(r, "A", "D")
    assert path == ["A", "B", "C", "D"] and rate == pytest.approx(1.331)
    assert impl.find_path(r, "A", "D") == ["A", "D"]                # fewest hops


@pytest.mark.part3
@pytest.mark.edge
def test_part3_cycles_ignored_and_inverse_used(impl):
    # inconsistent quotes both ways create an arbitrage loop USD->AUD->USD = 1.12; must not inflate
    r = impl.parse_rates("USD:AUD:1.4,AUD:USD:0.8,USD:JPY:110")
    rate, path = impl.best_conversion(r, "AUD", "JPY")
    assert path == ["AUD", "USD", "JPY"] and rate == pytest.approx(88.0)
    # inverse edge used on a hop: JPY->USD->CAD = (1/110) * (1/0.8)
    r2 = impl.parse_rates(RATES)
    rate, path = impl.best_conversion(r2, "JPY", "CAD")
    assert path == ["JPY", "USD", "CAD"] and rate == pytest.approx(1 / 110 / 0.8)


@pytest.mark.part3
@pytest.mark.fmt
def test_part3_tie_break_fewer_hops_then_lexicographic(impl):
    # A->B direct 2.0 ; A->C->B = 1.0*2.0 = 2.0 (tie) -> fewer hops wins
    r = impl.parse_rates("A:B:2,A:C:1,C:B:2")
    assert impl.best_conversion(r, "A", "B")[1] == ["A", "B"]
    # A->Z->B and A->M->B both 2.0 and 2 hops -> lexicographically smaller path
    r = impl.parse_rates("A:Z:1,Z:B:2,A:M:1,M:B:2")
    assert impl.best_conversion(r, "A", "B")[1] == ["A", "M", "B"]


# ---------------------------------------------------------------- Part 4: payouts
@pytest.mark.part4
def test_example_part4(impl):
    r = impl.parse_rates(RATES)
    out = impl.convert_payouts(r, ["100,USD,AUD", "100,AUD,JPY", "0.375,USD,AUD", "0.15625,CAD,USD",
                                   "50,USD,GBP", "7,EUR,EUR"])
    assert out == [
        "100 USD -> AUD = 140.00",
        "100 AUD -> JPY = 7857.14",
        "0.375 USD -> AUD = 0.53",
        "0.15625 CAD -> USD = 0.13",
        "50 USD -> GBP = N/A",
        "7 EUR -> EUR = 7.00",
    ]


@pytest.mark.part4
@pytest.mark.fmt
def test_part4_half_up_not_bankers_and_zero(impl):
    r = impl.parse_rates("A:B:0.5,B:C:1")
    assert impl.convert_payouts(r, ["1.25,A,B"]) == ["1.25 A -> B = 0.63"]   # 0.625 -> 0.63
    assert impl.convert_payouts(r, ["1.25,A,C"]) == ["1.25 A -> C = 0.63"]   # via B, same
    assert impl.convert_payouts(r, ["0,A,B", "3,B,A"]) == ["0 A -> B = 0.00", "3 B -> A = 6.00"]
    assert impl.convert_payouts(r, []) == []


@pytest.mark.part4
@pytest.mark.edge
def test_part4_decimal_path_product_no_float_noise(impl):
    # 0.1 * 3 in float is 0.30000000000000004; along a path (1.1 * 1.1 * 1.1 = 1.331) Decimal keeps 1.331 exactly
    r = impl.parse_rates("A:B:1.1,B:C:1.1,C:D:1.1")
    assert impl.convert_payouts(r, ["1000,A,D"]) == ["1000 A -> D = 1331.00"]
    # inverse hop: D->A = 1/1.331 -> 1000 * 0.7513148... = 751.31
    assert impl.convert_payouts(r, ["1000,D,A"]) == ["1000 D -> A = 751.31"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_part3_exact(run_script):
    r = run_script(f"PART 3\n{RATES}\nAUD JPY\nCAD AUD\nCAD JPY\nJPY JPY\nUSD GBP\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "78.571429 AUD->USD->JPY\n1.12 CAD->USD->AUD\n88 CAD->USD->JPY\n1 JPY\nN/A\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_parts_1_2_4_exact(run_script):
    r = run_script(f"PART 1\n{RATES}\nUSD AUD\nAUD USD\nUSD USD\n")
    assert r.stdout == "1.4\nN/A\n1\n"
    r = run_script(f"PART 2\n{RATES}\nAUD USD\nUSD CAD\n")
    assert r.stdout == "0.714286\n1.25\n"
    r = run_script(f"PART 4\n{RATES}\n100,USD,AUD\n\n100,AUD,JPY\n")
    assert r.stdout == "100 USD -> AUD = 140.00\n100 AUD -> JPY = 7857.14\n"
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_payouts(run_script):
    rng = random.Random(0)
    cur = [f"C{i:02d}" for i in range(30)]
    # realistic table: everything quoted against USD (=C00) plus a few cross rates
    quotes = [f"{cur[0]}:{c}:{rng.uniform(0.5, 150):.4f}" for c in cur[1:]]
    for _ in range(6):
        a, b = rng.sample(cur[1:], 2)
        quotes.append(f"{a}:{b}:{rng.uniform(0.5, 2):.4f}")
    lines = [f"{rng.randrange(1, 10_000_00) / 100:.2f},{rng.choice(cur)},{rng.choice(cur)}" for _ in range(100_000)]
    r = run_script("PART 4\n" + ",".join(quotes) + "\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000 and "N/A" not in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
