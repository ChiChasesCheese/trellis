"""q37 Fraud Rule Timestamps — reference solution.

Rules are batch declarations, so a decision depends only on timestamps: for each rule name pick
the version with the largest effective_from <= t (later line wins ties), check it has not expired
(t < effective_to, exclusive), evaluate its condition. Any matching rule -> REJECT.
"""
from __future__ import annotations

import re
import sys
from bisect import bisect_right
from collections import defaultdict
from typing import NamedTuple

COND = re.compile(r"^(merchant|amount)(!=|>=|<=|=|>|<)(.+)$")


class Version(NamedTuple):
    effective_from: int
    seq: int
    effective_to: int | None
    condition: str


class Auth(NamedTuple):
    id: str
    timestamp: int
    merchant: str
    amount: int


def matches(condition: str, auth: Auth) -> bool:
    if condition == "none":
        return False
    field, op, value = COND.match(condition).groups()
    lhs = auth.merchant if field == "merchant" else auth.amount
    rhs = value if field == "merchant" else int(value)   # amount compared numerically
    return {"=": lhs == rhs, "!=": lhs != rhs, ">": lhs > rhs, ">=": lhs >= rhs,
            "<": lhs < rhs, "<=": lhs <= rhs}[op]


def in_force(versions: list[Version], t: int) -> Version | None:
    """Latest version with effective_from <= t ('<=': t == effective_from applies); None if expired."""
    i = bisect_right(versions, (t, float("inf"))) - 1   # versions sorted by (effective_from, seq)
    if i < 0:
        return None
    v = versions[i]
    if v.effective_to is not None and t >= v.effective_to:  # end exclusive; no fallback to older
        return None
    return v


def decide(rules: dict[str, list[Version]], auth: Auth) -> str:
    for versions in rules.values():
        v = in_force(versions, auth.timestamp)
        if v is not None and matches(v.condition, auth):
            return "REJECT"
    return "APPROVE"


def process(lines: list[str]) -> list[str]:
    rules: dict[str, list[Version]] = defaultdict(list)
    auths: list[Auth] = []
    for seq, ln in enumerate(lines):
        f = [p.strip() for p in ln.split(",")]
        if f[0] == "RULE":
            to = int(f[3]) if len(f) == 5 else None          # 5 fields = with effective_to
            rules[f[1]].append(Version(int(f[2]), seq, to, f[-1]))
        elif f[0] == "AUTH":
            auths.append(Auth(f[1], int(f[2]), f[3], int(f[4])))
    for versions in rules.values():
        versions.sort()                                       # by (effective_from, seq)
    auths.sort(key=lambda a: (a.timestamp, a.id))             # Part 4: deterministic output order
    return [f"{a.timestamp},{a.id},{a.amount},{decide(rules, a)}" for a in auths]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
