"""ps02 Shipping Cost Pricing — YOUR implementation.

Input shape (see problem.md): stdin is `PART n`, then a `RATES` section (rate rows, schema
depends on n), then an `ORDERS` section (`order_id,country,product,quantity` rows).
"""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """Flat unit price. RATES rows 'country,product,unit_cost'.
    Return ['order_id: $x.xx', ...] (or 'order_id: ERROR ...'), one per order, input order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Quantity tiers. RATES rows 'country,product,min_qty,max_qty,cost' (closed interval,
    max_qty may be 'inf'). Whole quantity billed at the single matched band's rate."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same tiers plus a trailing 'incremental'/'fixed' type column. The matched band's type
    decides: 'fixed' = same as Part 2; 'incremental' = graduated billing through every band
    from min_qty=1 up to the matched band."""
    # TODO
    return []


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
