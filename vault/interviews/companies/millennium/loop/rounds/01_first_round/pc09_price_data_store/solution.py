"""pc09 Price Data Store -- reference solution.

A tick store keyed by symbol: each symbol owns a *sorted* list of timestamps (maintained with
bisect.insort so out-of-order writes stay cheap to query) plus dicts ts -> price / ts -> volume.
latest/as_of/ohlc/vwap are all binary searches or slices over that sorted list -- this is the
part interviewers probe on: a dict-of-list that you `.append()` to stays insertion-ordered, not
time-ordered, so an out-of-order upsert would silently break every range query. Money is Decimal
end to end (see CONVENTIONS.md); floats are rejected at the boundary so nothing ever
float-accumulates. Every method returns an exact Decimal -- rounding to 4 places with
ROUND_HALF_UP happens exactly once, in `_fmt`, at the output boundary.
"""

from __future__ import annotations

import bisect
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

FOUR_PLACES = Decimal("0.0001")


# --------------------------------------------------------------------------- input validation
def _check_symbol(symbol) -> None:
    if not isinstance(symbol, str) or not symbol:
        raise ValueError(f"symbol must be a non-empty str, got {symbol!r}")


def _check_ts(ts) -> None:
    if isinstance(ts, bool) or not isinstance(ts, int):
        raise ValueError(f"ts must be an int, got {ts!r}")


def _to_decimal(value, field: str) -> Decimal:
    """int / str / Decimal -> Decimal. float is rejected: money never float-accumulates
    (CONVENTIONS.md), so a candidate must hand in a string or an already-exact Decimal."""
    if isinstance(value, bool):
        raise ValueError(f"{field} must not be bool, got {value!r}")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, str):
        try:
            return Decimal(value)
        except InvalidOperation as exc:
            raise ValueError(f"{field} is not a valid decimal string: {value!r}") from exc
    if isinstance(value, float):
        raise ValueError(f"{field} must be int, str or Decimal, not float, got {value!r}")
    raise ValueError(f"{field} must be int, str or Decimal, got {type(value).__name__}")


def _fmt(x: Decimal) -> str:
    """Display formatting only: quantize to 4 decimal places, half rounds up. Internal storage
    and every method return keep the exact, unrounded Decimal."""
    return str(x.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP))


def _as_of_lookup(ts_list: list[int], value_map: dict[int, Decimal], ts: int) -> Decimal:
    i = bisect.bisect_right(ts_list, ts) - 1
    if i < 0:
        raise LookupError(f"no value at or before ts={ts}")
    return value_map[ts_list[i]]


# --------------------------------------------------------------------------- Part 1
class PriceStore:
    """Time-series price store: upsert-by-(symbol, ts), latest price, as-of price."""

    def __init__(self) -> None:
        self._ts: dict[str, list[int]] = {}
        self._px: dict[str, dict[int, Decimal]] = {}
        self._vol: dict[str, dict[int, Decimal]] = {}

    def upsert(self, symbol: str, ts: int, price, volume=0) -> None:
        _check_symbol(symbol)
        _check_ts(ts)
        price_d = _to_decimal(price, "price")
        if price_d < 0:
            raise ValueError(f"price must be >= 0, got {price_d}")
        vol_d = _to_decimal(volume, "volume")
        if vol_d < 0:
            raise ValueError(f"volume must be >= 0, got {vol_d}")
        if symbol not in self._ts:
            self._ts[symbol] = []
            self._px[symbol] = {}
            self._vol[symbol] = {}
        if ts not in self._px[symbol]:
            bisect.insort(self._ts[symbol], ts)  # keep time-sorted even if writes arrive out of order
        self._px[symbol][ts] = price_d  # same ts written twice -> last write wins
        self._vol[symbol][ts] = vol_d

    def latest(self, symbol: str) -> Decimal:
        """Price at the largest recorded ts for `symbol` (not the most recently *inserted* tick --
        an out-of-order upsert with a smaller ts does not become "latest")."""
        arr = self._ts.get(symbol)
        if not arr:
            raise KeyError(symbol)
        return self._px[symbol][arr[-1]]

    def as_of(self, symbol: str, ts: int) -> Decimal:
        """Last price with timestamp <= ts."""
        _check_ts(ts)
        arr = self._ts.get(symbol)
        if not arr:
            raise KeyError(symbol)
        try:
            return _as_of_lookup(arr, self._px[symbol], ts)
        except LookupError:
            raise LookupError(f"{symbol}: no price at or before ts={ts}") from None

    # ----------------------------------------------------------------------- Part 2
    def ohlc(self, symbol: str, t0: int, t1: int) -> tuple[Decimal, Decimal, Decimal, Decimal]:
        """(open, high, low, close) over ticks with t0 <= ts <= t1 (open/close use ts order,
        not insertion order)."""
        _check_ts(t0)
        _check_ts(t1)
        if t0 > t1:
            raise ValueError(f"t0 must be <= t1, got t0={t0}, t1={t1}")
        arr = self._ts.get(symbol)
        if not arr:
            raise KeyError(symbol)
        window = arr[bisect.bisect_left(arr, t0):bisect.bisect_right(arr, t1)]
        if not window:
            raise LookupError(f"{symbol}: no price in [{t0}, {t1}]")
        prices = [self._px[symbol][t] for t in window]
        return prices[0], max(prices), min(prices), prices[-1]

    def vwap(self, symbol: str, t0: int, t1: int) -> Decimal:
        """Volume-weighted average price over t0 <= ts <= t1."""
        _check_ts(t0)
        _check_ts(t1)
        if t0 > t1:
            raise ValueError(f"t0 must be <= t1, got t0={t0}, t1={t1}")
        arr = self._ts.get(symbol)
        if not arr:
            raise KeyError(symbol)
        window = arr[bisect.bisect_left(arr, t0):bisect.bisect_right(arr, t1)]
        if not window:
            raise LookupError(f"{symbol}: no price in [{t0}, {t1}]")
        num = sum((self._px[symbol][t] * self._vol[symbol][t] for t in window), Decimal(0))
        den = sum((self._vol[symbol][t] for t in window), Decimal(0))
        if den == 0:
            raise ValueError(f"{symbol}: total volume is 0 in [{t0}, {t1}], vwap is undefined")
        return num / den


# --------------------------------------------------------------------------- Part 3 (reconstructed)
class FXTable:
    """as-of FX rates, keyed by pair (e.g. "EURUSD" = 1 EUR in USD). Same as-of technique as
    PriceStore -- a rate table is just a price store whose "symbol" is a currency pair."""

    def __init__(self) -> None:
        self._ts: dict[str, list[int]] = {}
        self._rate: dict[str, dict[int, Decimal]] = {}

    def upsert(self, pair: str, ts: int, rate) -> None:
        _check_symbol(pair)
        _check_ts(ts)
        rate_d = _to_decimal(rate, "rate")
        if rate_d <= 0:
            raise ValueError(f"rate must be > 0, got {rate_d}")
        if pair not in self._ts:
            self._ts[pair] = []
            self._rate[pair] = {}
        if ts not in self._rate[pair]:
            bisect.insort(self._ts[pair], ts)
        self._rate[pair][ts] = rate_d

    def rate_as_of(self, pair: str, ts: int) -> Decimal:
        _check_ts(ts)
        arr = self._ts.get(pair)
        if not arr:
            raise KeyError(pair)
        try:
            return _as_of_lookup(arr, self._rate[pair], ts)
        except LookupError:
            raise LookupError(f"{pair}: no FX rate at or before ts={ts}") from None


def price_in_base(store: PriceStore, fx: FXTable, symbol: str, ts: int, symbol_ccy: str, base_ccy: str) -> Decimal:
    """as-of price of `symbol` (quoted in `symbol_ccy`) converted into `base_ccy`, using the FX
    rate as-of the same ts. Tries the direct pair symbol_ccy+base_ccy first, then the inverse
    pair (1/rate) -- a desk publishing EURUSD does not always also publish USDEUR."""
    _check_symbol(symbol_ccy)
    _check_symbol(base_ccy)
    px = store.as_of(symbol, ts)
    if symbol_ccy == base_ccy:
        return px
    direct, inverse = symbol_ccy + base_ccy, base_ccy + symbol_ccy
    try:
        return px * fx.rate_as_of(direct, ts)
    except (KeyError, LookupError):
        pass
    try:
        return px / fx.rate_as_of(inverse, ts)
    except (KeyError, LookupError):
        raise LookupError(f"no FX rate for {symbol_ccy}->{base_ccy} at or before ts={ts}") from None


# --------------------------------------------------------------------------- line-driven wrappers
def process_operations(lines: list[str]) -> list[str]:
    """Shared engine for all three parts: one PriceStore + one FXTable per call, dispatched by
    the first token of each line. Commands unused by a given part simply never appear in its
    input, so part1/part2/part3 all delegate here (later parts add commands, they don't need a
    different engine)."""
    store = PriceStore()
    fx = FXTable()
    out: list[str] = []
    for raw in lines:
        tokens = raw.split()
        if not tokens:
            continue
        cmd, args = tokens[0], tokens[1:]
        if cmd == "UPSERT":
            symbol, ts, price = args[0], int(args[1]), args[2]
            volume = args[3] if len(args) > 3 else "0"
            store.upsert(symbol, ts, price, volume)
        elif cmd == "LATEST":
            out.append(_fmt(store.latest(args[0])))
        elif cmd == "ASOF":
            out.append(_fmt(store.as_of(args[0], int(args[1]))))
        elif cmd == "OHLC":
            o, h, l, c = store.ohlc(args[0], int(args[1]), int(args[2]))
            out.append(" ".join(_fmt(x) for x in (o, h, l, c)))
        elif cmd == "VWAP":
            out.append(_fmt(store.vwap(args[0], int(args[1]), int(args[2]))))
        elif cmd == "FX":
            pair, ts, rate = args[0], int(args[1]), args[2]
            fx.upsert(pair, ts, rate)
        elif cmd == "INBASE":
            symbol, ts, symbol_ccy, base_ccy = args[0], int(args[1]), args[2], args[3]
            out.append(_fmt(price_in_base(store, fx, symbol, ts, symbol_ccy, base_ccy)))
        else:
            raise ValueError(f"unknown command: {cmd!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return process_operations(lines)


def part2(lines: list[str]) -> list[str]:
    return process_operations(lines)


def part3(lines: list[str]) -> list[str]:
    return process_operations(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
