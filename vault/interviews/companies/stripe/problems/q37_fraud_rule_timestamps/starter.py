"""q37 Fraud Rule Timestamps — YOUR implementation. Run: python drill.py test q37

Part 1 effective_from -> Part 2 versions (latest effective_from <= t wins; 'none' = off)
-> Part 3 effective_to (exclusive) -> Part 4 any line order, output sorted by (timestamp, id).
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Version(NamedTuple):
    effective_from: int
    seq: int                  # line order, breaks effective_from ties (later line wins)
    effective_to: int | None  # exclusive; None = forever
    condition: str            # 'merchant=bobs_burgers', 'amount>1000', 'none'


class Auth(NamedTuple):
    id: str
    timestamp: int
    merchant: str
    amount: int


def matches(condition: str, auth: Auth) -> bool:
    # TODO
    return False


def decide(rules: dict[str, list[Version]], auth: Auth) -> str:
    """'REJECT' if any rule's in-force version at auth.timestamp matches, else 'APPROVE'."""
    # TODO
    return "APPROVE"


def process(lines: list[str]) -> list[str]:
    """RULE/AUTH lines in any order -> ['timestamp,id,amount,DECISION', ...] sorted by (timestamp, id)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
