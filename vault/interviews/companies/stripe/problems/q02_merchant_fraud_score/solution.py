"""q02 Merchant Fraud Score — reference solution.

Scores, amounts and factors are integers (amounts in minor units). The three rules are three
separate passes over the whole transaction list, in order: multiply, then repeat-customer add,
then hourly-density add/subtract. Pass order matters because pass 1 multiplies the *base* score.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict

Merchant = tuple[str, int]                  # (merchant_id, base_score)
Txn = tuple[str, int, str, int]             # (merchant_id, amount, customer_id, hour)
Rule = tuple[int, int, int, int]            # (min_amount, multiplicative, additive, penalty)

REPEAT_THRESHOLD = 3        # rule 2: 3rd and later transaction of a (merchant, customer) pair
HOURLY_THRESHOLD = 3        # rule 3: 3rd and later transaction of (merchant, customer, hour)


def parse(lines: list[str]) -> tuple[list[Merchant], list[Txn], list[Rule]]:
    merchants: list[Merchant] = []
    txns: list[Txn] = []
    rules: list[Rule] = []
    section = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        head = line.upper()
        if head in ("MERCHANTS", "TRANSACTIONS", "RULES"):
            section = head
            continue
        f = [p.strip() for p in line.split(",")]
        if section == "MERCHANTS":
            merchants.append((f[0], int(f[1])))
        elif section == "TRANSACTIONS":
            txns.append((f[0], int(f[1]), f[2], int(f[3])))
        elif section == "RULES":
            rules.append((int(f[0]), int(f[1]), int(f[2]), int(f[3])))
    return merchants, txns, rules


def hour_sign(hour: int) -> int:
    """Rule 3 band: +1 for 12..17, -1 for 9..11 and 18..21, 0 otherwise (all inclusive)."""
    if 12 <= hour <= 17:
        return 1
    if 9 <= hour <= 11 or 18 <= hour <= 21:
        return -1
    return 0


def score(merchants: list[Merchant], transactions: list[Txn], rules: list[Rule],
          upto: int = 3, repeat_mode: str = "cumulative") -> list[str]:
    scores: dict[str, int] = {m: base for m, base in merchants}
    # rule i belongs to transaction i; transactions of unknown merchants are ignored
    pairs = [(t, r) for t, r in zip(transactions, rules) if t[0] in scores]

    # Pass 1 — amount rule: strictly greater than the threshold multiplies the score.
    for (m, amount, _c, _h), (min_amount, mult, _add, _pen) in pairs:
        if amount > min_amount:                  # strict '>' — equal amount does nothing
            scores[m] *= mult

    # Pass 2 — repeat customer.
    if upto >= 2:
        if repeat_mode == "cumulative":          # primary: 3rd, 4th, ... transaction of the pair adds
            seen: Counter = Counter()
            for (m, _a, c, _h), (_mn, _mu, add, _pen) in pairs:
                seen[(m, c)] += 1                # count includes the current transaction
                if seen[(m, c)] >= REPEAT_THRESHOLD:
                    scores[m] += add
        else:                                    # variant: pair with >= 3 txns adds ALL its factors once
            total: Counter = Counter((t[0], t[2]) for t, _r in pairs)
            for (m, _a, c, _h), (_mn, _mu, add, _pen) in pairs:
                if total[(m, c)] >= REPEAT_THRESHOLD:
                    scores[m] += add

    # Pass 3 — hourly density: 3rd and later transaction in the same (merchant, customer, hour).
    if upto >= 3:
        seen_h: Counter = Counter()
        for (m, _a, c, h), (_mn, _mu, _add, pen) in pairs:
            seen_h[(m, c, h)] += 1
            if seen_h[(m, c, h)] >= HOURLY_THRESHOLD:
                scores[m] += hour_sign(h) * pen  # +penalty 12-17, -penalty 9-11 / 18-21, else 0

    return render(scores)


def score_variant_grouped(merchants: list[Merchant], transactions: list[Txn]) -> list[str]:
    """programhelp NG variant: no rule list. (m,c) groups with >= 3 txns add their total amount;
    (m,c,h) groups with >= 3 txns add their total amount again."""
    scores: dict[str, int] = {m: base for m, base in merchants}
    by_pair: dict[tuple, list[int]] = defaultdict(list)
    by_hour: dict[tuple, list[int]] = defaultdict(list)
    for m, amount, c, h in transactions:
        if m not in scores:
            continue
        by_pair[(m, c)].append(amount)
        by_hour[(m, c, h)].append(amount)
    for (m, _c), amounts in by_pair.items():
        if len(amounts) >= REPEAT_THRESHOLD:     # count of transactions, not amount
            scores[m] += sum(amounts)
    for (m, _c, _h), amounts in by_hour.items():
        if len(amounts) >= HOURLY_THRESHOLD:
            scores[m] += sum(amounts)
    return render(scores)


def render(scores: dict[str, int]) -> list[str]:
    # every merchant, plain string order of the id, 'id, score'
    return [f"{m}, {scores[m]}" for m in sorted(scores)]


def part1(lines: list[str]) -> list[str]:
    return score(*parse(lines), upto=1)


def part2(lines: list[str]) -> list[str]:
    return score(*parse(lines), upto=2)


def part3(lines: list[str]) -> list[str]:
    return score(*parse(lines), upto=3)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
