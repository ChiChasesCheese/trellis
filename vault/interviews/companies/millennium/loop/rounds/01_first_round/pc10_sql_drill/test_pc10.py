import sqlite3

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_part1_worked_example_daily_notional(impl, db):
    rows = db.execute(impl.part1()).fetchall()
    assert rows == [
        ("AAPL", "2026-01-05", 52650.0),
        ("AAPL", "2026-01-06", 15200.0),
        ("AAPL", "2026-01-08", 1530.0),
        ("AAPL", "2026-01-09", 1540.0),
        ("AAPL", "2026-01-10", 1550.0),
        ("BUND", "2026-01-06", 98500.0),
        ("EURUSD", "2026-01-06", 110000.0),
        ("GILT", "2026-01-07", 19800.0),
        ("MSFT", "2026-01-05", 93000.0),
        ("MSFT", "2026-01-06", 15450.0),
        ("MSFT", "2026-01-09", 6220.0),
        ("VOD", "2026-01-05", 50000.0),
    ]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_drops_the_null_symbol_cash_trade(impl, db):
    rows = db.execute(impl.part1()).fetchall()
    symbols = {r[0] for r in rows}
    assert None not in symbols
    assert sum(1 for r in rows if r[0] == "AAPL" and r[1] == "2026-01-08") == 1
    # the cash trade is also dated 2026-01-08 but carries no symbol; it must not surface here.


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_notional_rounded_to_two_decimals(impl, db):
    rows = db.execute(impl.part1()).fetchall()
    for symbol, trade_date, notional in rows:
        assert round(notional, 2) == notional


@pytest.mark.part1
@pytest.mark.edge
def test_part1_no_trades_yields_no_rows(impl):
    conn = sqlite3.connect(":memory:")
    from pathlib import Path
    base = Path(__file__).resolve().parent
    conn.executescript((base / "schema.sql").read_text())
    conn.execute("INSERT INTO instruments (symbol, desk, currency) VALUES ('X', 'EQUITY', 'USD')")
    assert conn.execute(impl.part1()).fetchall() == []


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example_latest_trade_per_trader(impl, db):
    rows = db.execute(impl.part2()).fetchall()
    assert rows == [
        ("alice", "AAPL", "2026-01-10", "2026-01-10 09:00:00", 10, 155.0),
        ("bob", "MSFT", "2026-01-09", "2026-01-09 09:00:00", 20, 311.0),
        ("dan", "EURUSD", "2026-01-06", "2026-01-06 10:00:00", 100000, 1.1),
        ("garcia", None, "2026-01-08", "2026-01-08 12:00:00", 1, 500.0),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_keeps_null_symbol_when_it_really_is_the_latest_trade(impl, db):
    rows = db.execute(impl.part2()).fetchall()
    garcia = next(r for r in rows if r[0] == "garcia")
    assert garcia[1] is None  # the cash adjustment IS garcia's most recent trade
    assert garcia[2] == "2026-01-08"


@pytest.mark.part2
@pytest.mark.edge
def test_part2_exactly_one_row_per_distinct_trader(impl, db):
    rows = db.execute(impl.part2()).fetchall()
    traders = [r[0] for r in rows]
    assert len(traders) == len(set(traders)) == 4


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == (
        "alice\tAAPL\t2026-01-10\t2026-01-10 09:00:00\t10\t155.0\n"
        "bob\tMSFT\t2026-01-09\t2026-01-09 09:00:00\t20\t311.0\n"
        "dan\tEURUSD\t2026-01-06\t2026-01-06 10:00:00\t100000\t1.1\n"
        "garcia\t\t2026-01-08\t2026-01-08 12:00:00\t1\t500.0\n"
    )


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_example_desk_usd_notional(impl, db):
    rows = db.execute(impl.part3()).fetchall()
    assert rows == [
        ("EQUITY", 249640.0),
        ("FX", 110000.0),
        ("RATES", 131526.0),
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_usd_instrument_needs_no_fx_rates_row(impl, db):
    # EURUSD is priced in USD; fx_rates has zero USD rows in the seed data, yet FX still totals.
    rows = dict(db.execute(impl.part3()).fetchall())
    assert rows["FX"] == 110000.0


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_trades_yields_no_rows(impl):
    conn = sqlite3.connect(":memory:")
    from pathlib import Path
    base = Path(__file__).resolve().parent
    conn.executescript((base / "schema.sql").read_text())
    conn.execute("INSERT INTO instruments (symbol, desk, currency) VALUES ('X', 'EQUITY', 'USD')")
    assert conn.execute(impl.part3()).fetchall() == []


# ------------------------------------------------------------------------ Part 4
@pytest.mark.part4
def test_part4_worked_example_streaks(impl, db):
    rows = db.execute(impl.part4()).fetchall()
    assert rows == [
        ("alice", "2026-01-08", "2026-01-10", 3),
        ("bob", "2026-01-05", "2026-01-06", 2),
        ("dan", "2026-01-06", "2026-01-06", 1),
        ("garcia", "2026-01-05", "2026-01-05", 1),
    ]


@pytest.mark.part4
@pytest.mark.edge
def test_part4_excludes_the_cash_only_day_from_trading_days(impl, db):
    rows = db.execute(impl.part4()).fetchall()
    garcia = next(r for r in rows if r[0] == "garcia")
    assert "2026-01-08" not in (garcia[1], garcia[2])  # cash-only day, no real symbol traded


@pytest.mark.part4
@pytest.mark.edge
def test_part4_tie_breaks_to_the_earliest_starting_streak(impl, db):
    # garcia has two 1-day islands (2026-01-05 VOD, 2026-01-07 GILT); equal length, earliest wins.
    rows = db.execute(impl.part4()).fetchall()
    garcia = next(r for r in rows if r[0] == "garcia")
    assert garcia == ("garcia", "2026-01-05", "2026-01-05", 1)


@pytest.mark.part4
@pytest.mark.edge
def test_part4_requires_sqlite_with_window_function_support(impl):
    # part4 uses ROW_NUMBER() OVER (...), added in sqlite 3.25 (2018-09).
    assert sqlite3.sqlite_version_info >= (3, 25, 0), (
        f"sqlite3 {sqlite3.sqlite_version} predates window function support (>= 3.25 required)"
    )


@pytest.mark.part4
@pytest.mark.perf
def test_perf_part4_streaks_over_50k_synthetic_trades(impl):
    import random
    import time
    from pathlib import Path

    conn = sqlite3.connect(":memory:")
    base = Path(__file__).resolve().parent
    conn.executescript((base / "schema.sql").read_text())
    conn.execute("INSERT INTO instruments (symbol, desk, currency) VALUES ('SYN', 'EQUITY', 'USD')")
    rng = random.Random(0)
    traders = [f"trader{i}" for i in range(200)]
    rows = []
    for trade_id in range(1, 50_001):
        trader = traders[trade_id % len(traders)]
        day = 1 + (trade_id * 7 + rng.randint(0, 2)) % 300
        trade_date = f"2026-{1 + day // 28:02d}-{1 + day % 28:02d}"
        ts = trade_date + " 09:00:00"
        rows.append((trade_id, "SYN", trader, trade_date, ts, 10, 1.0))
    conn.executemany(
        "INSERT INTO trades (trade_id, symbol, trader, trade_date, ts, qty, price) VALUES (?,?,?,?,?,?,?)",
        rows,
    )
    t0 = time.perf_counter()
    result = conn.execute(impl.part4()).fetchall()
    elapsed = time.perf_counter() - t0
    assert len(result) == len(traders)
    assert elapsed < 2.0, f"took {elapsed:.2f}s"


# ------------------------------------------------------------------------ Part 5
@pytest.mark.part5
def test_part5_worked_example_never_traded_by_garcia(impl, db):
    rows = db.execute(impl.part5()).fetchall()
    assert rows == [("AAPL",), ("BUND",), ("EURUSD",), ("MSFT",), ("ORPHAN",)]


@pytest.mark.part5
@pytest.mark.edge
def test_part5_includes_an_instrument_with_zero_trades_at_all(impl, db):
    # ORPHAN never appears in `trades`; a naive "SELECT DISTINCT symbol FROM trades WHERE ..."
    # driver (instead of driving from `instruments`) would miss it entirely.
    rows = db.execute(impl.part5()).fetchall()
    assert ("ORPHAN",) in rows


@pytest.mark.part5
@pytest.mark.edge
def test_part5_not_in_with_a_null_in_the_subquery_is_the_documented_trap(impl, db):
    buggy_not_in = """
        SELECT i.symbol FROM instruments AS i
        WHERE i.symbol NOT IN (SELECT t.symbol FROM trades AS t WHERE t.trader = 'garcia')
        ORDER BY i.symbol
    """
    # garcia has a symbol IS NULL cash trade, so the NOT IN subquery contains a NULL: every
    # comparison becomes UNKNOWN and the buggy query silently returns nothing.
    assert db.execute(buggy_not_in).fetchall() == []
    assert db.execute(impl.part5()).fetchall() != []


@pytest.mark.part5
@pytest.mark.io
def test_stdin_stdout_part5(run_script):
    r = run_script("PART 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "AAPL\nBUND\nEURUSD\nMSFT\nORPHAN\n"
