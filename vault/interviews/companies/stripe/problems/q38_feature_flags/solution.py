"""q38 Feature Flags — reference solution.

Decision order (first decisive step wins): unknown/off -> every required flag ON for this user
(recursive, cycle-safe) -> deny -> allow -> attribute rules (AND across keys, OR within a key,
'ab=even' = numeric id even) -> rollout bucket. Bucket = crc32("flag:user") % 100, ON iff
bucket < rollout, so it is deterministic and differs per flag.
"""
from __future__ import annotations

import re
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
    rules: dict = {}


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

    def _rules_pass(self, flag: Flag, user: str) -> bool:
        attrs = self.users.get(user, {})
        for key, accepted in flag.rules.items():
            if key == "ab":                                   # source variant: even numeric id
                digits = re.sub(r"\D", "", user)
                if not digits or int(digits) % 2 != 0:
                    return False
            elif attrs.get(key) not in accepted:              # missing attribute fails the rule
                return False
        return True

    def is_enabled(self, flag: str, user: str, _seen: frozenset = frozenset()) -> bool:
        f = self.flags.get(flag)
        if f is None or not f.on or flag in _seen:            # unknown, kill switch, or cycle
            return False
        seen = _seen | {flag}
        if not all(self.is_enabled(r, user, seen) for r in f.requires):  # Part 4, before allow
            return False
        if user in f.deny:
            return False
        if user in f.allow:
            return True                                       # bypasses attributes and rollout
        if not self._rules_pass(f, user):
            return False
        return bucket(flag, user) < f.rollout                 # strict '<': rollout=0 nobody, 100 all


def parse_flag(fields: list[str]) -> Flag:
    name, on, *opts = fields
    kw: dict = {"rules": {}}
    for opt in opts:
        key, _, val = opt.partition("=")
        vals = val.split("|")
        if key in ("allow", "deny"):
            kw[key] = frozenset(vals)
        elif key == "rollout":
            kw[key] = int(val)
        elif key == "requires":
            kw[key] = tuple(vals)
        else:
            kw["rules"][key] = set(vals)
    return Flag(name, on == "on", **kw)


def process(lines: list[str]) -> list[str]:
    ff, out = FeatureFlags(), []
    for ln in lines:
        cmd, *f = [p.strip() for p in ln.split(",")]
        if cmd == "FLAG":
            ff.add_flag(parse_flag(f))
        elif cmd == "USER":
            ff.add_user(f[0], dict(kv.partition("=")[::2] for kv in f[1:]))
        elif cmd == "CHECK":
            out.append(f"{f[0]},{f[1]},{'ON' if ff.is_enabled(f[0], f[1]) else 'OFF'}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
