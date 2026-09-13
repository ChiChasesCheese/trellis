"""q03 Chat Billing — reference solution.

All money is integer cents. Allowance bookkeeping is integer tokens. The only rounding in the
problem is the prorated fee (15.00 * fixed/total) -> half-up to the cent, done with integer math.
"""
from __future__ import annotations

import sys
from collections import defaultdict

BLOCK = 100
IN_CENTS_PER_BLOCK = 3       # $0.03 per 100 input tokens
OUT_CENTS_PER_BLOCK = 4      # $0.04 per 100 output tokens
FIXED_FEE_CENTS = 1500       # $15.00 / month
ALLOWANCE_TOKENS = 40_000    # included in the fixed plan (input + output combined)


def parse(lines: list[str]) -> dict[str, list[tuple[int, int, str]]]:
    """user_id -> [(input_tokens, output_tokens, plan), ...] in input order."""
    by_user: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        user, inp, out, plan = (p.strip() for p in raw.split(","))
        by_user[user].append((int(inp), int(out), plan))
    return by_user


def billable(tokens: int) -> int:
    """Tokens that count, per session: complete 100-blocks only."""
    return (tokens // BLOCK) * BLOCK


def bill_user(sessions: list[tuple[int, int, str]]) -> int:
    """Total cents for one user's month."""
    total = len(sessions)
    fixed = sum(1 for _, _, p in sessions if p == "fixed")
    if fixed == 0:
        fee, allowance = 0, 0
    elif fixed == total:
        fee, allowance = FIXED_FEE_CENTS, ALLOWANCE_TOKENS
    else:  # Part 3: prorate by session count
        # half-up rounding of 1500 * fixed / total to the cent, in integers
        fee = (2 * FIXED_FEE_CENTS * fixed + total) // (2 * total)
        allowance = ALLOWANCE_TOKENS * fixed // total  # floor

    cents = fee
    for inp, out, plan in sessions:
        b_in, b_out = billable(inp), billable(out)
        if plan == "payg":
            cents += (b_in // BLOCK) * IN_CENTS_PER_BLOCK + (b_out // BLOCK) * OUT_CENTS_PER_BLOCK
            continue
        # fixed: consume allowance, input before output inside the session
        use = min(allowance, b_in)
        allowance -= use
        cents += ((b_in - use) // BLOCK) * IN_CENTS_PER_BLOCK
        use = min(allowance, b_out)
        allowance -= use
        cents += ((b_out - use) // BLOCK) * OUT_CENTS_PER_BLOCK
    return cents


def fmt(cents: int) -> str:
    return f"${cents // 100}.{cents % 100:02d}"


def calculate_monthly_billing(sessions: list[str]) -> list[str]:
    by_user = parse(sessions)
    return [f"{u}: {fmt(bill_user(by_user[u]))}" for u in sorted(by_user)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = calculate_monthly_billing(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
