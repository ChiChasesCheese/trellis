"""q26 AccountScheduler — reference solution.

Per account: locked_until (None = free), last_used (None = never acquired), and a version counter
that invalidates stale heap entries. Two heaps make acquire_any O(log n):
  free   : (never_used_flag, last_used, id, ver)   -> LRU order among accounts believed free
  locked : (locked_until, id, ver)                 -> moved back to `free` once t >= locked_until
Entries whose ver != current ver are skipped (lazy invalidation). Because a popped `free` entry is
re-checked against `t`, queries with non-monotonic t are still answered correctly.
A simpler O(n) scan of all accounts in acquire_any is fine for small pools (~10^3) but would be
~10^9 steps on the 10^5 x 10^4 perf test.
"""
from __future__ import annotations

import heapq
import sys


class Account:
    __slots__ = ("id", "locked_until", "last_used", "ver")

    def __init__(self, account_id: str) -> None:
        self.id = account_id
        self.locked_until: int | None = None
        self.last_used: int | None = None
        self.ver = 0


class AccountScheduler:
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = {}
        self.free: list[tuple[int, int, str, int]] = []
        self.locked: list[tuple[int, str, int]] = []

    def _lru_key(self, a: Account) -> tuple[int, int, str, int]:
        # never-used first (flag 0), then oldest last_used, then id (plain string order)
        return (0 if a.last_used is None else 1, a.last_used or 0, a.id, a.ver)

    def _push_free(self, a: Account) -> None:
        a.ver += 1
        heapq.heappush(self.free, self._lru_key(a))

    def add_account(self, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        a = self.accounts[account_id] = Account(account_id)
        self._push_free(a)
        return True

    def is_available(self, account_id: str, t: int) -> bool:
        a = self.accounts.get(account_id)
        # lock end is EXCLUSIVE: free again exactly at locked_until
        return a is not None and (a.locked_until is None or a.locked_until <= t)

    def _lock(self, a: Account, duration: int, t: int) -> None:
        a.locked_until, a.last_used = t + duration, t
        a.ver += 1
        heapq.heappush(self.locked, (a.locked_until, a.id, a.ver))

    def acquire(self, account_id: str, duration: int, t: int) -> bool:
        if duration <= 0 or not self.is_available(account_id, t):   # duration must be > 0
            return False
        self._lock(self.accounts[account_id], duration, t)
        return True

    def acquire_any(self, duration: int, t: int) -> str | None:
        if duration <= 0:
            return None
        # 1) locks that have expired by t go back to the LRU pool
        while self.locked and self.locked[0][0] <= t:
            _, aid, ver = heapq.heappop(self.locked)
            a = self.accounts[aid]
            if ver == a.ver:                      # still the live lock entry; keep locked_until so
                self._push_free(a)                #   an earlier-t query still sees the old lock
        # 2) pop the LRU candidate, skipping stale entries and (non-monotonic t) still-locked ones
        parked = []
        chosen = None
        while self.free:
            _, _, aid, ver = heapq.heappop(self.free)
            a = self.accounts[aid]
            if ver != a.ver:
                continue
            if a.locked_until is not None and a.locked_until > t:
                parked.append((a.locked_until, a.id, ver))
                continue
            chosen = a
            break
        for entry in parked:
            heapq.heappush(self.locked, entry)
        if chosen is None:
            return None
        self._lock(chosen, duration, t)
        return chosen.id

    def release(self, account_id: str) -> bool:
        a = self.accounts.get(account_id)
        if a is None:
            return False
        if a.locked_until is not None:            # idempotent: releasing a free account is a no-op
            a.locked_until = None
            self._push_free(a)                    # last_used unchanged -> keeps its LRU position
        return True


ARITY = {"ADD": (1, 1), "AVAILABLE": (2, 1), "ACQUIRE": (3, 1), "ACQUIRE_ANY": (2, 2), "RELEASE": (1, 3)}


def run_commands(lines: list[str], max_part: int = 4) -> list[str]:
    s = AccountScheduler()
    out: list[str] = []
    for raw in lines:
        f = raw.split()
        if not f:
            continue
        verb, args = f[0].upper(), f[1:]
        spec = ARITY.get(verb)
        try:
            if spec is None or len(args) != spec[0] or spec[1] > max_part:
                raise ValueError(verb)
            if verb == "ADD":
                out.append("OK" if s.add_account(args[0]) else "EXISTS")
            elif verb == "AVAILABLE":
                out.append("true" if s.is_available(args[0], int(args[1])) else "false")
            elif verb == "ACQUIRE":
                out.append("true" if s.acquire(args[0], int(args[1]), int(args[2])) else "false")
            elif verb == "ACQUIRE_ANY":
                out.append(s.acquire_any(int(args[0]), int(args[1])) or "NONE")
            else:  # RELEASE
                out.append("OK" if s.release(args[0]) else "UNKNOWN")
        except ValueError:
            out.append("ERROR")
    return out


def part1(lines: list[str]) -> list[str]:
    return run_commands(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return run_commands(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return run_commands(lines, 3)


def part4(lines: list[str]) -> list[str]:
    return run_commands(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = part4(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
