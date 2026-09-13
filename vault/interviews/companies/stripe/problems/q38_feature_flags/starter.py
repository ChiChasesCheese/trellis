"""q38 Feature Flags — YOUR implementation. Run: python drill.py test q38

Order: unknown/off -> requires (Part 4) -> deny -> allow -> attribute rules (Part 3) -> rollout (Part 2).
bucket = zlib.crc32(f"{flag}:{user}".encode()) % 100 ; enabled iff bucket < rollout.
"""
from __future__ import annotations

import sys
import zlib
from typing import NamedTuple


class Flag(NamedTuple):
    name: str
    on: bool
    allow: frozenset = frozenset()
    deny: frozenset = frozenset()
    rollout: int = 100
    requires: tuple = ()
    rules: dict = {}          # key -> set of accepted values; 'ab' -> {'even'}


def bucket(flag: str, user: str) -> int:
    return zlib.crc32(f"{flag}:{user}".encode()) % 100


class FeatureFlags:
    def __init__(self) -> None:
        self.flags: dict[str, Flag] = {}
        self.users: dict[str, dict[str, str]] = {}

    def add_flag(self, flag: Flag) -> None:
        self.flags[flag.name] = flag

    def add_user(self, user: str, attrs: dict[str, str]) -> None:
        self.users[user] = attrs

    def is_enabled(self, flag: str, user: str) -> bool:
        # TODO
        return False


def parse_flag(fields: list[str]) -> Flag:
    """['newui', 'on', 'rollout=50', 'country=US|CA'] -> Flag"""
    # TODO
    return Flag(fields[0], fields[1] == "on")


def process(lines: list[str]) -> list[str]:
    # TODO: FLAG / USER / CHECK -> ['flag,user,ON|OFF', ...]
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
