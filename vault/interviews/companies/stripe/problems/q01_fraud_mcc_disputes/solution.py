"""q01 Fraud Detection by MCC — reference solution.

State: two integer counters per account (fraud_count, total_count) + a charge ledger so a DISPUTE can
unwind exactly the charge it refers to. Ratio thresholds are kept as exact integer fractions
(num/den, den = 10^k) and compared by cross-multiplication — no floats anywhere.
"""
from __future__ import annotations

import sys
from collections import defaultdict


def parse_threshold(literal: str) -> tuple[str, int, int]:
    """'3' -> ('count', 3, 1);  '0.25' -> ('ratio', 25, 100);  '1.0' -> ('ratio', 10, 10).
    Rule: a decimal point means RATIO, no decimal point means COUNT."""
    literal = literal.strip()
    if "." not in literal:
        return ("count", int(literal), 1)
    whole, frac = literal.split(".", 1)
    den = 10 ** len(frac)
    return ("ratio", int(whole or "0") * den + int(frac or "0"), den)


def fmt_threshold(t: tuple[str, int, int] | None) -> str:
    if t is None:
        return "NONE"
    kind, num, den = t
    if kind == "count":
        return f"count,{num}"
    k = len(str(den)) - 1  # den is 10^k -> print back the literal with k decimals
    return f"ratio,{num // den}.{num % den:0{k}d}"


def fields(raw: str) -> list[str]:
    return [p.strip() for p in raw.split(",")]


def part1(lines: list[str]) -> dict:
    setup = {"merchant_mcc": {}, "thresholds": {}, "fraud_codes": set(), "min_count": 0, "sticky": False}
    for raw in lines:
        f = fields(raw)
        cmd = f[0].upper()
        if cmd == "MERCHANT":
            setup["merchant_mcc"][f[1]] = f[2]
        elif cmd == "THRESHOLD":
            setup["thresholds"][f[1]] = parse_threshold(f[2])
        elif cmd == "FRAUD_CODES":
            setup["fraud_codes"].update(c for c in f[1:] if c)
        elif cmd == "MIN_COUNT":
            setup["min_count"] = int(f[1])
        elif cmd == "STICKY":
            setup["sticky"] = True
    return setup


def is_fraudulent(setup: dict, acct: str, fraud_count: int, total_count: int) -> bool:
    """Part 3 decision for one account. Unknown merchant / MCC without threshold / zero volume -> False."""
    threshold = setup["thresholds"].get(setup["merchant_mcc"].get(acct))
    if threshold is None or total_count == 0:
        return False
    kind, num, den = threshold
    if kind == "count":
        return fraud_count >= num  # NON-strict: exactly the threshold is fraudulent
    # ratio: min-volume gate (non-strict) then fraud/total >= num/den by cross-multiplication
    return total_count >= setup["min_count"] and fraud_count * den >= num * total_count


def simulate(lines: list[str], *, disputes: bool, sticky: bool | None, dispute_removes_charge: bool = True):
    """Run the event stream. Returns (counts {acct: (fraud, total)}, flagged set)."""
    setup = part1(lines)
    if sticky is None:
        sticky = setup["sticky"]
    fraud: dict[str, int] = defaultdict(int)
    total: dict[str, int] = defaultdict(int)
    charges: dict[str, tuple[str, bool]] = {}  # charge_id -> (account, is_fraud); popped once disputed
    flagged: set[str] = set()
    for raw in lines:
        f = fields(raw)
        cmd = f[0].upper()
        if cmd == "CHARGE":
            _, cid, acct, _amount, code = f[:5]
            if cid in charges:  # duplicate charge id: idempotent, ignore
                continue
            is_fraud = code in setup["fraud_codes"]
            charges[cid] = (acct, is_fraud)
            total[acct] += 1
            fraud[acct] += is_fraud
        elif cmd == "DISPUTE" and disputes:
            cid = f[1]
            if cid not in charges:  # unknown id, or already disputed -> no-op
                continue
            acct, is_fraud = charges[cid]
            fraud[acct] -= is_fraud
            if dispute_removes_charge:  # primary: reverse the charge completely
                total[acct] -= 1
                del charges[cid]
            else:  # variant: charge stays counted but is now non-fraud
                charges[cid] = (acct, False)
        else:
            continue
        # re-evaluate only the touched account
        if is_fraudulent(setup, acct, fraud[acct], total[acct]):
            flagged.add(acct)
        elif not sticky:
            flagged.discard(acct)
    counts = {a: (fraud[a], total[a]) for a in total}
    return counts, flagged


def render(flagged: set[str]) -> list[str]:
    return [",".join(sorted(flagged)) if flagged else "NONE"]  # plain string order, no spaces


def part2(lines: list[str]) -> dict[str, tuple[int, int]]:
    return simulate(lines, disputes=False, sticky=False)[0]


def part3(lines: list[str], *, sticky: bool | None = None) -> list[str]:
    return render(simulate(lines, disputes=False, sticky=sticky)[1])


def part4(lines: list[str], *, sticky: bool | None = None, dispute_removes_charge: bool = True) -> list[str]:
    return render(simulate(lines, disputes=True, sticky=sticky, dispute_removes_charge=dispute_removes_charge)[1])


def part5(lines: list[str], *, sticky: bool | None = None, dispute_removes_charge: bool = True) -> list[str]:
    return part4(lines, sticky=sticky, dispute_removes_charge=dispute_removes_charge)


def render_setup(setup: dict) -> list[str]:
    return [f"{a},{mcc},{fmt_threshold(setup['thresholds'].get(mcc))}" for a, mcc in sorted(setup["merchant_mcc"].items())]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 5
    if lines and lines[0].upper().startswith("PART"):
        part, lines = int(lines[0].split()[1]), lines[1:]
    if part == 1:
        out = render_setup(part1(lines))
    elif part == 2:
        out = [f"{a},{f},{t}" for a, (f, t) in sorted(part2(lines).items())]
    elif part == 3:
        out = part3(lines)
    else:
        out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
