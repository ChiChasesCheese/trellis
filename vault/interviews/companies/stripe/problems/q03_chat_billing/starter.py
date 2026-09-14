"""q03 Chat Billing — YOUR implementation. Run: python drill.py test q03"""
from __future__ import annotations

import sys


def calculate_monthly_billing(sessions: list[str]) -> list[str]:
    """sessions: raw lines 'user_id,input_tokens,output_tokens,plan'.
    Return ['user: $x.xx', ...] sorted by user_id."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    stdout.write("\n".join(calculate_monthly_billing(lines)) + ("\n" if lines else ""))


if __name__ == "__main__":
    main()
