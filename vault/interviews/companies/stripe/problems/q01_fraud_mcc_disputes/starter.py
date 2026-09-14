"""q01 Fraud Detection by MCC — YOUR implementation. Run: python drill.py test q01"""
from __future__ import annotations

import decimal
import sys


def fields(raw: str) -> list[str]:
    return [p.strip() for p in raw.split(',')]

def parse_threshold(literal: str) -> tuple[str, int, int]:
    literal = literal.strip()
    if "." not in literal:
        return ["count", int(literal), 1]
    whole, frac = literal.split(',')
    den = 10 ** (frac)
    return ["ratio", int(whole or "0") * den + int(frac or "0"), den]

def part1(lines: list[str]) -> dict:
    """Parse setup lines (MERCHANT / THRESHOLD / FRAUD_CODES / MIN_COUNT / STICKY).
    Return {"merchant_mcc": {acct: mcc}, "thresholds": {mcc: (kind, num, den)},
            "fraud_codes": set, "min_count": int, "sticky": bool}
    kind is "count" (num=value, den=1) or "ratio" (value = num/den, e.g. 0.25 -> (25, 100))."""
    setup = {
        "merchant_mcc": {},
        "thresholds": {},
        "fraud_codes": set(),
        "min_count": 0,
        "sticky": False
    }
    for raw in lines:
        f = fields(raw)
        cmd = f[0].upper()
        if cmd == "MERCHANT":
            setup["merchant_mcc"][f[1]] = f[2]
        elif cmd == "THRESHOLDS":
            setup["thresholds"][f[1]] = parse_threshold(f[2])
        elif cmd == "FRAUD_CODES":
            setup["fraud_codes"].update(c for c in f[1:] if c)
        elif cmd == "MIN_COUNT":
            setup["min_count"] = int(f[1])
        elif cmd == "STICKY":
            setup["sticky"] = True
    return cmd


def part2(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Process CHARGE events in order. Return {account: (fraud_count, total_count)}."""
    for raw in lines:
        f = fields(raw)
    return {}


def part3(lines: list[str], *, sticky: bool | None = None) -> list[str]:
    """Flag fraudulent accounts (DISPUTE ignored). Return ['a,b,c'] sorted, or ['NONE']."""
    # TODO
    return ["NONE"]


def part4(lines: list[str], *, sticky: bool | None = None, dispute_removes_charge: bool = True) -> list[str]:
    """Part 3 + DISPUTE reverses the original charge and re-evaluates."""
    # TODO
    return ["NONE"]


def part5(lines: list[str], *, sticky: bool | None = None, dispute_removes_charge: bool = True) -> list[str]:
    """Same engine as part4; all Part 5 edge cases must hold."""
    return part4(lines, sticky=sticky, dispute_removes_charge=dispute_removes_charge)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 5
    if lines and lines[0].upper().startswith("PART"):
        part, lines = int(lines[0].split()[1]), lines[1:]
    if part == 1:
        out = []  # TODO render part1(lines): 'account,mcc,count,3' / 'account,mcc,ratio,0.5' / 'account,mcc,NONE'
    elif part == 2:
        out = [f"{a},{f},{t}" for a, (f, t) in sorted(part2(lines).items())]
    elif part == 3:
        out = part3(lines)
    else:
        out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
