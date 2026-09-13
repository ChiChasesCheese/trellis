"""q26 AccountScheduler — YOUR implementation. Run: python drill.py test q26"""
from __future__ import annotations

import sys


class AccountScheduler:
    def __init__(self) -> None:
        pass  # TODO

    def add_account(self, account_id: str) -> bool:
        """True if newly registered, False if it already existed (no change)."""
        return False  # TODO

    def is_available(self, account_id: str, t: int) -> bool:
        """Registered and (unlocked or locked_until <= t). Unknown -> False."""
        return False  # TODO

    def acquire(self, account_id: str, duration: int, t: int) -> bool:
        """Lock [t, t+duration) if available at t and duration > 0; record last_used = t."""
        return False  # TODO

    def acquire_any(self, duration: int, t: int) -> str | None:
        """LRU available account: never-used first (by id), then smallest last_used, ties by id."""
        return None  # TODO

    def release(self, account_id: str) -> bool:
        """Unlock immediately (last_used unchanged). Unknown -> False."""
        return False  # TODO


def run_commands(lines: list[str], max_part: int = 4) -> list[str]:
    """Drive one scheduler over the command stream; commands above max_part -> ERROR."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """ADD / AVAILABLE / ACQUIRE only."""
    return run_commands(lines, 1)


def part2(lines: list[str]) -> list[str]:
    """+ ACQUIRE_ANY (LRU)."""
    return run_commands(lines, 2)


def part3(lines: list[str]) -> list[str]:
    """+ RELEASE."""
    return run_commands(lines, 3)


def part4(lines: list[str]) -> list[str]:
    """Full stream with validation (malformed -> ERROR)."""
    return run_commands(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
