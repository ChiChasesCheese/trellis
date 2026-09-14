"""ps02 Shipping Cost Pricing — reference solution.

Three unlock-next-part levels over the same shape (a RATES table + an ORDERS list):
  Part 1: flat per-unit price lookup.
  Part 2: quantity tiers — the whole order is billed at the single band containing `quantity`
          (exactly what Part 3 calls a 'fixed' band).
  Part 3: each band also carries a type in {incremental, fixed}; the MATCHED band's type decides
          whether the order pays one rate ('fixed') or walks every band from qty 1 up to the
          matched one, tax-bracket style ('incremental').

Money is integer cents end to end (`parse_money_to_cents` / `fmt_cents`) — no floats anywhere.
Errors are raised as `PricingError` inside the pricing rules and turned into the three verbatim
`ERROR ...` strings in exactly one place (`_price_orders`), so the rules never touch formatting.
"""

from __future__ import annotations

import sys
from typing import Callable, NamedTuple

TIER_TYPES = ("incremental", "fixed")


class Band(NamedTuple):
    min_qty: int
    max_qty: int | None  # None == the literal 'inf' (open-ended top band)
    cost: int  # per-unit rate in cents
    kind: str  # 'incremental' | 'fixed'

    def contains(self, qty: int) -> bool:
        """Closed interval [min_qty, max_qty] — both boundaries belong to this band."""
        return self.min_qty <= qty and (self.max_qty is None or qty <= self.max_qty)


class PricingError(Exception):
    """One of the three pinned messages: unknown product / no tier / incremental gap."""


# ------------------------------------------------------------------ money


def parse_money_to_cents(raw: str) -> int:
    """'5', '5.0', '5.00', '12.50' -> cents. More than 2 decimal digits is a format error
    (a rate table is not free text — stay strict rather than silently rounding)."""
    whole, _, frac = raw.strip().partition(".")
    if len(frac) > 2:
        raise ValueError(f"too many decimal places: {raw!r}")
    return int(whole) * 100 + int(frac.ljust(2, "0"))  # '5.5' -> frac '50', not '05'


def fmt_cents(cents: int) -> str:
    """Two decimals, '$' sign, no thousands separator: 1450 -> '$14.50'."""
    return f"${cents // 100}.{cents % 100:02d}"


# ------------------------------------------------------------------ parsing


def _split_sections(lines: list[str]) -> tuple[list[str], list[str]]:
    """'RATES', rate rows..., 'ORDERS', order rows... -> (rate_rows, order_rows), blanks dropped."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    if not lines or lines[0] != "RATES":
        raise ValueError("expected a RATES section")
    split = lines.index("ORDERS")
    return lines[1:split], lines[split + 1 :]


def _parse_flat_rates(rate_rows: list[str]) -> dict[tuple[str, str], int]:
    """'country,product,unit_cost' rows -> {(country, product): unit_cost_cents}."""
    table: dict[tuple[str, str], int] = {}
    for row in rate_rows:
        country, product, unit_cost = (p.strip() for p in row.split(","))
        table[(country, product)] = parse_money_to_cents(unit_cost)
    return table


def _parse_tiered_rates(rate_rows: list[str], with_type: bool) -> dict[tuple[str, str], list[Band]]:
    """'country,product,min,max,cost[,type]' rows -> {(country, product): bands sorted by min_qty}.
    The file order of bands is untrusted; Part 2 rows have no type column and behave as 'fixed'."""
    table: dict[tuple[str, str], list[Band]] = {}
    for row in rate_rows:
        fields = [p.strip() for p in row.split(",")]
        country, product, min_qty, max_qty, cost = fields[:5]
        kind = fields[5] if with_type else "fixed"
        if kind not in TIER_TYPES:
            raise ValueError(f"invalid tier type: {kind!r}")
        band = Band(
            int(min_qty), None if max_qty == "inf" else int(max_qty), parse_money_to_cents(cost), kind
        )
        table.setdefault((country, product), []).append(band)
    for bands in table.values():
        bands.sort(key=lambda b: b.min_qty)
    return table


# ------------------------------------------------------------------ pricing rules (cents in, cents out)


def _price_flat(table: dict[tuple[str, str], int], country: str, product: str, qty: int) -> int:
    """Part 1: unit_cost * qty; the product must exist even when qty == 0."""
    if (country, product) not in table:
        raise PricingError(f"unknown product {country}/{product}")
    return qty * table[(country, product)]


def _price_incremental(bands: list[Band], qty: int, label: str) -> int:
    """Graduated billing: walk bands ascending from qty 1, each band charging its own rate for the
    units inside it, until the band holding `qty`. The chain must be contiguous from 1 up to
    there — a hole the order actually has to cross is an 'incremental gap' error."""
    total, expected_start = 0, 1
    for band in bands:
        if band.min_qty != expected_start:
            raise PricingError(f"incremental gap for {label} at qty={qty}")
        upper = qty if band.max_qty is None else min(qty, band.max_qty)
        total += (upper - band.min_qty + 1) * band.cost
        if upper == qty:
            return total
        expected_start = band.max_qty + 1
    raise PricingError(f"no tier for {label} at qty={qty}")  # unreachable once a band matched


def _price_tiered(table: dict[tuple[str, str], list[Band]], country: str, product: str, qty: int) -> int:
    """Parts 2 & 3: find the band containing qty; bill the whole order by that band's type."""
    label = f"{country}/{product}"
    if (country, product) not in table:
        raise PricingError(f"unknown product {label}")
    if qty == 0:
        return 0  # zero items cost zero; no tier lookup needed (but the product had to exist)
    bands = table[(country, product)]
    matched = next((b for b in bands if b.contains(qty)), None)
    if matched is None:
        raise PricingError(f"no tier for {label} at qty={qty}")
    if matched.kind == "fixed":
        return qty * matched.cost  # Part 2's rule, verbatim
    return _price_incremental(bands, qty, label)


# ------------------------------------------------------------------ output boundary


def _price_orders(order_rows: list[str], price_one: Callable[[str, str, int], int]) -> list[str]:
    """'order_id,country,product,quantity' rows -> 'order_id: $x.xx' or 'order_id: ERROR <msg>',
    one per order in input order. The only place errors become strings."""
    out: list[str] = []
    for row in order_rows:
        order_id, country, product, qty = (p.strip() for p in row.split(","))
        try:
            out.append(f"{order_id}: {fmt_cents(price_one(country, product, int(qty)))}")
        except PricingError as err:
            out.append(f"{order_id}: ERROR {err}")
    return out


def part1(lines: list[str]) -> list[str]:
    """Flat per-unit price: RATES rows 'country,product,unit_cost'; ORDERS rows
    'order_id,country,product,quantity'. Output 'order_id: $x.xx' (or ERROR), input order."""
    rate_rows, order_rows = _split_sections(lines)
    table = _parse_flat_rates(rate_rows)
    return _price_orders(order_rows, lambda c, p, q: _price_flat(table, c, p, q))


def part2(lines: list[str]) -> list[str]:
    """Quantity tiers: RATES rows 'country,product,min_qty,max_qty,cost' (closed interval
    [min_qty, max_qty]; max_qty may be the literal 'inf'). The whole order quantity is billed
    at the single matched band's rate (no cumulative summation — see Part 3 for that)."""
    rate_rows, order_rows = _split_sections(lines)
    table = _parse_tiered_rates(rate_rows, with_type=False)
    return _price_orders(order_rows, lambda c, p, q: _price_tiered(table, c, p, q))


def part3(lines: list[str]) -> list[str]:
    """Same tiers as Part 2 plus a trailing 'incremental'/'fixed' column per band. The type of
    the band that CONTAINS the order's quantity decides the whole order's pricing mode."""
    rate_rows, order_rows = _split_sections(lines)
    table = _parse_tiered_rates(rate_rows, with_type=True)
    return _price_orders(order_rows, lambda c, p, q: _price_tiered(table, c, p, q))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not raw:
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
