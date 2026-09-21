import random
from decimal import Decimal

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_out_of_order_and_overwrite(impl):
    s = impl.PriceStore()
    s.upsert("AAPL", 100, "150.00")
    s.upsert("AAPL", 105, "151.25")
    s.upsert("AAPL", 102, "150.75")  # out-of-order write
    assert s.latest("AAPL") == Decimal("151.25")
    assert s.as_of("AAPL", 103) == Decimal("150.75")
    with pytest.raises(LookupError):
        s.as_of("AAPL", 99)
    s.upsert("AAPL", 100, "149.50")  # overwrite same ts
    assert s.as_of("AAPL", 100) == Decimal("149.50")


@pytest.mark.part1
@pytest.mark.edge
def test_single_record(impl):
    s = impl.PriceStore()
    s.upsert("X", 5, "10")
    assert s.latest("X") == Decimal("10")
    assert s.as_of("X", 5) == Decimal("10")
    assert s.as_of("X", 1000) == Decimal("10")


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_ts_last_write_wins_regardless_of_arrival_order(impl):
    s = impl.PriceStore()
    s.upsert("Y", 10, "1")
    s.upsert("Y", 20, "2")
    s.upsert("Y", 10, "1.5")  # rewrite an older ts after a newer one was already written
    assert s.as_of("Y", 15) == Decimal("1.5")
    assert s.latest("Y") == Decimal("2")


@pytest.mark.part1
@pytest.mark.edge
def test_as_of_before_first_price_raises_lookup_error(impl):
    s = impl.PriceStore()
    s.upsert("A", 100, "1")
    with pytest.raises(LookupError):
        s.as_of("A", 50)


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_symbol_raises_key_error(impl):
    s = impl.PriceStore()
    with pytest.raises(KeyError):
        s.latest("NOPE")
    with pytest.raises(KeyError):
        s.as_of("NOPE", 1)


@pytest.mark.part1
@pytest.mark.edge
def test_upsert_rejects_float_price(impl):
    s = impl.PriceStore()
    with pytest.raises(ValueError):
        s.upsert("A", 1, 150.0)


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "symbol,ts,price,volume",
    [
        ("A", 1, "-1", "0"),      # negative price
        ("A", 1, "1", "-1"),      # negative volume
        ("", 1, "1", "0"),        # empty symbol
        ("A", "x", "1", "0"),     # ts not an int
        ("A", True, "1", "0"),    # bool is not a valid ts
    ],
)
def test_upsert_rejects_invalid_input(impl, symbol, ts, price, volume):
    s = impl.PriceStore()
    with pytest.raises(ValueError):
        s.upsert(symbol, ts, price, volume)


@pytest.mark.part1
@pytest.mark.edge
def test_empty_operations_produce_no_output(impl):
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_extra_whitespace_between_tokens_is_tolerated(impl):
    out = impl.part1(["UPSERT   AAPL   100   150.00", "LATEST AAPL"])
    assert out == ["150.0000"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\nUPSERT AAPL 100 150.00\nUPSERT AAPL 105 151.25\nUPSERT AAPL 102 150.75\nLATEST AAPL\nASOF AAPL 103\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "151.2500\n150.7500\n"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_ohlc_and_vwap(impl):
    s = impl.PriceStore()
    s.upsert("MSFT", 1, "300", "10")
    s.upsert("MSFT", 2, "305", "5")
    s.upsert("MSFT", 3, "295", "20")
    s.upsert("MSFT", 4, "310", "5")
    assert s.ohlc("MSFT", 1, 4) == (Decimal("300"), Decimal("310"), Decimal("295"), Decimal("310"))
    assert s.vwap("MSFT", 1, 4) == Decimal("299.375")


@pytest.mark.part2
@pytest.mark.edge
def test_ohlc_subrange_uses_time_order_not_insertion_order(impl):
    s = impl.PriceStore()
    s.upsert("M", 3, "295")
    s.upsert("M", 1, "300")  # inserted second, but has the smaller ts
    s.upsert("M", 2, "305")
    assert s.ohlc("M", 1, 2) == (Decimal("300"), Decimal("305"), Decimal("300"), Decimal("305"))


@pytest.mark.part2
@pytest.mark.edge
def test_ohlc_single_tick_in_range(impl):
    s = impl.PriceStore()
    s.upsert("S", 1, "7")
    s.upsert("S", 10, "9")
    o, h, l, c = s.ohlc("S", 1, 1)
    assert o == h == l == c == Decimal("7")


@pytest.mark.part2
@pytest.mark.edge
def test_ohlc_t0_greater_than_t1_raises_value_error(impl):
    s = impl.PriceStore()
    s.upsert("S", 1, "1")
    with pytest.raises(ValueError):
        s.ohlc("S", 5, 1)
    with pytest.raises(ValueError):
        s.vwap("S", 5, 1)


@pytest.mark.part2
@pytest.mark.edge
def test_ohlc_no_data_in_range_raises_lookup_error(impl):
    s = impl.PriceStore()
    s.upsert("S", 1, "1")
    with pytest.raises(LookupError):
        s.ohlc("S", 100, 200)
    with pytest.raises(LookupError):
        s.vwap("S", 100, 200)


@pytest.mark.part2
@pytest.mark.edge
def test_vwap_zero_total_volume_raises_value_error(impl):
    s = impl.PriceStore()
    s.upsert("Z", 1, "10", "0")
    s.upsert("Z", 2, "20", "0")
    with pytest.raises(ValueError):
        s.vwap("Z", 1, 2)


@pytest.mark.part2
@pytest.mark.fmt
def test_vwap_rounding_is_half_up_at_the_fifth_decimal(impl):
    out = impl.part2(["UPSERT R 1 1.00005 1", "UPSERT R 2 1.00005 1", "VWAP R 1 2"])
    assert out == ["1.0001"]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_upserts_mostly_increasing_ts(run_script):
    rng = random.Random(0)
    lines = ["PART 2"]
    for i in range(100_000):
        price = 100 + (i % 50)
        lines.append(f"UPSERT AAPL {i} {price} 10")
    lines.append("OHLC AAPL 0 99999")
    lines.append("VWAP AAPL 0 99999")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out_lines = r.stdout.splitlines()
    assert out_lines[0] == "100.0000 149.0000 100.0000 149.0000"
    assert out_lines[1] == "124.5000"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = (
        "PART 2\nUPSERT MSFT 1 300 10\nUPSERT MSFT 2 305 5\nUPSERT MSFT 3 295 20\n"
        "UPSERT MSFT 4 310 5\nOHLC MSFT 1 4\nVWAP MSFT 1 4\n"
    )
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "300.0000 310.0000 295.0000 310.0000\n299.3750\n"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_direct_and_inverse_fx_pairs(impl):
    store = impl.PriceStore()
    store.upsert("VOD", 10, "100.00")
    fx = impl.FXTable()
    fx.upsert("GBPUSD", 5, "1.2500")
    assert impl.price_in_base(store, fx, "VOD", 10, "GBP", "USD") == Decimal("125.000000")
    assert impl.price_in_base(store, fx, "VOD", 10, "USD", "USD") == Decimal("100.00")

    fx2 = impl.FXTable()
    fx2.upsert("USDGBP", 5, "0.8000")  # only the inverse pair is published
    assert impl.price_in_base(store, fx2, "VOD", 10, "GBP", "USD") == Decimal("125")


@pytest.mark.part3
@pytest.mark.edge
def test_same_currency_never_looks_up_fx_table(impl):
    store = impl.PriceStore()
    store.upsert("VOD", 10, "100.00")
    fx = impl.FXTable()  # empty -- if price_in_base queried it, this would raise
    assert impl.price_in_base(store, fx, "VOD", 10, "GBP", "GBP") == Decimal("100.00")


@pytest.mark.part3
@pytest.mark.edge
def test_no_fx_rate_in_either_direction_raises_lookup_error(impl):
    store = impl.PriceStore()
    store.upsert("VOD", 10, "100.00")
    fx = impl.FXTable()
    with pytest.raises(LookupError):
        impl.price_in_base(store, fx, "VOD", 10, "GBP", "USD")


@pytest.mark.part3
@pytest.mark.edge
def test_fx_upsert_rejects_non_positive_rate(impl):
    fx = impl.FXTable()
    with pytest.raises(ValueError):
        fx.upsert("EURUSD", 1, "0")
    with pytest.raises(ValueError):
        fx.upsert("EURUSD", 1, "-1.5")


@pytest.mark.part3
@pytest.mark.edge
def test_fx_rate_as_of_picks_the_latest_rate_not_after_ts(impl):
    fx = impl.FXTable()
    fx.upsert("GBPUSD", 5, "1.2500")
    fx.upsert("GBPUSD", 15, "1.3000")
    assert fx.rate_as_of("GBPUSD", 10) == Decimal("1.2500")
    assert fx.rate_as_of("GBPUSD", 20) == Decimal("1.3000")
    with pytest.raises(LookupError):
        fx.rate_as_of("GBPUSD", 1)
    with pytest.raises(KeyError):
        fx.rate_as_of("EURUSD", 10)


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    stdin = "PART 3\nUPSERT VOD 10 100.00\nFX GBPUSD 5 1.2500\nINBASE VOD 10 GBP USD\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "125.0000\n"
