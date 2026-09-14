"""q19 Accept-Language — YOUR implementation. Run: python drill.py test q19"""
from __future__ import annotations

import sys


def parse_accept_language(header: str, supported: list[str], zero_q: str = "exclude") -> list[str]:
    """Return supported tags (in supported spelling) satisfying the header, most preferred first.
    zero_q: 'exclude' (q=0 tags never appear) | 'last' (q=0 tags appended at the end)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    header = lines[0] if lines else ""
    supported = [t.strip() for t in (lines[1] if len(lines) > 1 else "").split(",") if t.strip()]
    out = parse_accept_language(header, supported) or ["NONE"]
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
