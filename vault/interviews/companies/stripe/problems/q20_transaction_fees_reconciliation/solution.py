"""q20 Transaction Fees / Receivables / Reconciliation — reference solution.

All money is integer cents.  Part 1 percentage: (amount*21 + 500) // 1000 == 2.1 % rounded
half-up.  Part 2 table rates: amount*bps // 10000 (floor, per the PracHub spec) + fixed.
"""
from __future__ import annotations

import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal

DISPUTE_FEE = 1500       # $15.00 flat on dispute_lost (and dispute_won on card)
DEFAULT_PCT_PER_MILLE = 21   # 2.1 % == 21 / 1000
DEFAULT_FIXED = 30       # $0.30


def to_cents(s: str) -> int:
    """'1000' -> 1000 ; '10.00' / '-0.5' -> 1000 / -50 exactly (Decimal, no float)."""
    s = s.strip()
    if "." in s:
        cents = Decimal(s) * 100
        if cents != cents.to_integral_value():
            raise ValueError(f"amount '{s}' is not a whole number of cents")
        return int(cents)
    return int(s)


def parse_csv(lines: list[str]) -> list[dict]:
    text = "\n".join(ln for ln in lines if ln.strip())
    rows = []
    for raw in csv.DictReader(io.StringIO(text), skipinitialspace=True):
        rows.append({(k or "").strip(): (v or "").strip() for k, v in raw.items()})
    return rows


def parse_rates(lines: list[str]) -> dict:
    rates = {}
    for ln in lines:
        if not ln.strip():
            continue
        provider, country, bps, fixed = (p.strip() for p in ln.split(","))
        rates[(provider, country)] = (int(bps), int(fixed))
    return rates


def _lookup_rate(rates: dict, provider: str, country: str):
    """Exact -> (provider, *) -> (*, country) -> (*, *) -> None."""
    for key in ((provider, country), (provider, "*"), ("*", country), ("*", "*")):
        if key in rates:
            return rates[key]
    return None


def fee_cents(row: dict, rates: dict | None = None) -> int:
    status = row.get("status", "")
    provider = row.get("payment_provider", "")
    if status == "payment_completed":
        amount = to_cents(row["amount"])
        hit = _lookup_rate(rates, provider, row.get("buyer_country", "")) if rates else None
        if hit is not None:
            bps, fixed = hit
            return amount * bps // 10000 + fixed            # table rate: FLOOR (PracHub spec)
        return (amount * DEFAULT_PCT_PER_MILLE + 500) // 1000 + DEFAULT_FIXED  # 2.1 % half-up + 30
    if status == "dispute_lost":
        return DISPUTE_FEE
    if status == "dispute_won":
        return DISPUTE_FEE if provider == "card" else 0    # exact, case-sensitive provider match
    return 0  # pending / failed / refund / unknown


def part1(lines: list[str]) -> list[str]:
    return [f"{row['id']},{fee_cents(row)}" for row in parse_csv(lines)]


def part2(rate_lines: list[str], csv_lines: list[str]) -> list[str]:
    rates = parse_rates(rate_lines)
    return [f"{row['id']},{fee_cents(row, rates)}" for row in parse_csv(csv_lines)]


def receivables(rows: list[dict], rates: dict | None = None) -> list[str]:
    net: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        key = (row["merchant_id"], row["card_type"], row["payout_date"])
        fee = fee_cents(row, rates) if "status" in row else 0  # csoahelp shape: pure sum
        net[key] += to_cents(row["amount"]) - fee
    out = ["merchant_id,card_type,payout_date,net"]
    for key in sorted(net):  # merchant_id, then card_type, then payout_date — plain string order
        out.append(f"{key[0]},{key[1]},{key[2]},{net[key]}")
    return out


def part3(lines: list[str]) -> list[str]:
    return receivables(parse_csv(lines))


def _totals(lines: list[str]) -> dict[str, int]:
    tot: dict[str, int] = defaultdict(int)  # duplicate ids inside one list are summed
    for ln in lines:
        if ln.strip():
            tid, amount = (p.strip() for p in ln.split(",", 1))
            tot[tid] += to_cents(amount)
    return tot


def reconcile(system: list[str], gateway: list[str], include_matches: bool = False) -> list[str]:
    sys_t, gw_t = _totals(system), _totals(gateway)
    out = []
    for tid in sorted(set(sys_t) | set(gw_t)):
        if tid not in gw_t:
            out.append(f"MISSING_IN_GATEWAY {tid}")
        elif tid not in sys_t:
            out.append(f"MISSING_IN_SYSTEM {tid}")
        elif sys_t[tid] != gw_t[tid]:
            out.append(f"AMOUNT_MISMATCH {tid} {sys_t[tid]} {gw_t[tid]}")
        elif include_matches:
            out.append(f"MATCH {tid}")
    return out


def part4(system: list[str], gateway: list[str]) -> list[str]:
    return reconcile(system, gateway)


def _sections(lines: list[str], names: tuple[str, ...]) -> dict[str, list[str]]:
    """Split lines on marker lines (RATES/TRANSACTIONS or SYSTEM/GATEWAY)."""
    buckets: dict[str, list[str]] = {n: [] for n in names}
    current = names[0]
    for ln in lines:
        if ln in names:
            current = ln
        else:
            buckets[current].append(ln)
    return buckets


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    body = lines[1:]
    if part == 1:
        out = part1(body)
    elif part == 2:
        s = _sections(body, ("RATES", "TRANSACTIONS"))
        out = part2(s["RATES"], s["TRANSACTIONS"])
    elif part == 3:
        out = part3(body)
    else:
        s = _sections(body, ("SYSTEM", "GATEWAY"))
        out = part4(s["SYSTEM"], s["GATEWAY"])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
