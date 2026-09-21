"""pc10 SQL Drill -- reference solution.

Five small SQL questions against three tables (trades / instruments / fx_rates, see schema.sql +
seed.sql in this directory). Each partN() returns a SQL string; the test suite executes it
against an in-memory sqlite3 database seeded from the same two files and compares the resulting
rows to literals computed once from this solution. sqlite3 syntax throughout; part4 uses window
functions (ROW_NUMBER), which need sqlite >= 3.25 -- checked in test_pc10.py via
sqlite3.sqlite_version_info.

Two NULL-handling decisions apply across every part and are worth stating up front: a trade row
with symbol IS NULL is a cash adjustment, not tied to any instrument, so every "by symbol" or
"by trading day" query below INNER JOINs to instruments (or filters symbol IS NOT NULL) to drop
it -- except part2, which reports "each trader's most recent trade" and deliberately keeps it,
because for that trader the cash entry really is their latest trade. Part5 is where the NULL
trap is graded explicitly: a NOT IN subquery that can return NULL silently empties the whole
result, so the fix is NOT EXISTS.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


# --------------------------------------------------------------------------- Part 1
def part1() -> str:
    """Daily traded notional per symbol: SUM(|qty| * price), grouped by (symbol, trade_date).
    Notional is trade value regardless of buy/sell direction, so qty is wrapped in ABS(). Joining
    to instruments (rather than grouping trades directly) drops the symbol IS NULL cash-adjustment
    row -- a cash entry isn't "a symbol's" notional."""
    return """
        SELECT t.symbol, t.trade_date, ROUND(SUM(ABS(t.qty) * t.price), 2) AS notional
        FROM trades AS t
        JOIN instruments AS i ON i.symbol = t.symbol
        GROUP BY t.symbol, t.trade_date
        ORDER BY t.symbol, t.trade_date
    """


# --------------------------------------------------------------------------- Part 2
def part2() -> str:
    """Each trader's single most recent trade (by full timestamp, not just trade_date), via
    ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC) = 1. Unlike part1, this keeps a
    symbol IS NULL row if it genuinely is that trader's latest trade (see garcia's cash entry in
    the seed data) -- it is still "their most recent trade", cash or not."""
    return """
        WITH ranked AS (
            SELECT symbol, trader, trade_date, ts, qty, price,
                   ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC) AS rn
            FROM trades
        )
        SELECT trader, symbol, trade_date, ts, qty, price
        FROM ranked
        WHERE rn = 1
        ORDER BY trader
    """


# --------------------------------------------------------------------------- Part 3
def part3() -> str:
    """Per-desk notional converted to USD. Each instrument trades in its own currency
    (instruments.currency); fx_rates gives same-day currency -> USD rates. USD instruments never
    need a lookup (CASE short-circuits it, so EURUSD -- priced in USD -- doesn't require a
    'USDUSD' row in fx_rates); everything else joins fx_rates on (currency, trade_date)."""
    return """
        SELECT i.desk,
               ROUND(SUM(ABS(t.qty) * t.price *
                     CASE WHEN i.currency = 'USD' THEN 1.0 ELSE fx.rate_to_usd END), 2) AS usd_notional
        FROM trades AS t
        JOIN instruments AS i ON i.symbol = t.symbol
        LEFT JOIN fx_rates AS fx ON fx.currency = i.currency AND fx.rate_date = t.trade_date
        GROUP BY i.desk
        ORDER BY i.desk
    """


# --------------------------------------------------------------------------- Part 4
def part4() -> str:
    """Longest run of consecutive calendar trading days per trader (gaps-and-islands). Trading
    days are DISTINCT (trader, trade_date) with symbol IS NOT NULL -- a cash-adjustment-only day
    doesn't count as "traded". The island trick: julianday(trade_date) minus a per-trader
    ROW_NUMBER() ordered by date is constant within one consecutive run and changes at every
    gap, so grouping on that difference isolates each run. Ties (same longest length) keep the
    earliest-starting run."""
    return """
        WITH trading_days AS (
            SELECT DISTINCT trader, trade_date
            FROM trades
            WHERE symbol IS NOT NULL
        ),
        numbered AS (
            SELECT trader, trade_date,
                   CAST(julianday(trade_date) AS INTEGER)
                       - ROW_NUMBER() OVER (PARTITION BY trader ORDER BY trade_date) AS grp
            FROM trading_days
        ),
        islands AS (
            SELECT trader, MIN(trade_date) AS streak_start, MAX(trade_date) AS streak_end,
                   COUNT(*) AS streak_len
            FROM numbered
            GROUP BY trader, grp
        ),
        ranked AS (
            SELECT trader, streak_start, streak_end, streak_len,
                   ROW_NUMBER() OVER (PARTITION BY trader ORDER BY streak_len DESC, streak_start ASC) AS rn
            FROM islands
        )
        SELECT trader, streak_start, streak_end, streak_len
        FROM ranked
        WHERE rn = 1
        ORDER BY trader
    """


# --------------------------------------------------------------------------- Part 5
def part5() -> str:
    """Every listed instrument trader 'garcia' has never traded -- driven from `instruments`
    (already deduplicated by its PRIMARY KEY, and includes symbols with zero trades at all, e.g.
    ORPHAN) rather than `SELECT DISTINCT symbol FROM trades` (which would miss ORPHAN entirely).
    Uses NOT EXISTS, not NOT IN: garcia also has a symbol IS NULL cash trade, and
    `symbol NOT IN (subquery containing a NULL)` is SQL's classic trap -- if even one row in the
    NOT IN subquery is NULL, the whole comparison evaluates to UNKNOWN for every candidate row and
    the query silently returns zero rows. NOT EXISTS is a correlated per-row check, so a NULL in
    trades.symbol just never matches -- it can't poison every other row."""
    return """
        SELECT i.symbol
        FROM instruments AS i
        WHERE NOT EXISTS (
            SELECT 1 FROM trades AS t
            WHERE t.trader = 'garcia' AND t.symbol = i.symbol
        )
        ORDER BY i.symbol
    """


# --------------------------------------------------------------------------- main() / io
def _connect() -> sqlite3.Connection:
    base = Path(__file__).resolve().parent
    conn = sqlite3.connect(":memory:")
    conn.executescript((base / "schema.sql").read_text())
    conn.executescript((base / "seed.sql").read_text())
    return conn


def _format_row(row: tuple) -> str:
    return "\t".join("" if v is None else str(v) for v in row)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    sql = {1: part1, 2: part2, 3: part3, 4: part4, 5: part5}[n]()
    conn = _connect()
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    out = [_format_row(row) for row in rows]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
