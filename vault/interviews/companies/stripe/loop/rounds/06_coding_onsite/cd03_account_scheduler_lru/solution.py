"""cd03 AccountScheduler — reference solution.

Fixed pool of account ids (passed to __init__), two dicts (`locked_until`, `last_used`), and a
construction-order index used as the LRU tie-break. Unknown ids raise KeyError, duration <= 0
raises ValueError — the class never returns a sentinel for a caller bug, only for a legitimate
"not available right now" / "nothing to pick" outcome (False / None). main() is the only layer
that turns exceptions into an `ERROR` line, per the stream-level error policy in problem.md.
"""

from __future__ import annotations

import sys


class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None:
        # de-duplicate while preserving first-seen order: that order is the LRU tie-break key
        self._accounts: list[str] = list(dict.fromkeys(accounts))
        self._order: dict[str, int] = {aid: i for i, aid in enumerate(self._accounts)}
        self.locked_until: dict[str, int] = {}  # account_id -> t at which it becomes free again
        self.last_used: dict[str, int] = {}  # account_id -> t of its last SUCCESSFUL acquire

    def _check_known(self, account_id: str) -> None:
        if account_id not in self._order:
            raise KeyError(account_id)

    def _lock(self, account_id: str, t: int, duration: int) -> None:
        """Shared write path for a successful lock; both acquire() and acquire_any() end here."""
        self.locked_until[account_id] = t + duration
        self.last_used[account_id] = t

    def is_available(self, account_id: str, t: int) -> bool:
        """Registered and (never locked, or its lock's exclusive end <= t)."""
        self._check_known(account_id)
        end = self.locked_until.get(account_id)
        return end is None or t >= end

    def acquire(self, account_id: str, t: int, duration: int) -> bool:
        """Lock [t, t+duration) if available at t. duration <= 0 -> ValueError (checked first,
        before the unknown-id check that is_available performs)."""
        if duration <= 0:
            raise ValueError("duration must be > 0")
        if not self.is_available(account_id, t):  # raises KeyError for unknown ids
            return False
        self._lock(account_id, t, duration)
        return True

    def acquire_any(self, t: int, duration: int) -> str | None:
        """LRU-select among accounts available at t: never-acquired first (construction order),
        then oldest last_used (ties -> construction order). Locks the winner and returns its id;
        None if nothing is available. duration <= 0 -> ValueError, same as acquire."""
        if duration <= 0:
            raise ValueError("duration must be > 0")
        candidates = [aid for aid in self._accounts if self.is_available(aid, t)]
        if not candidates:
            return None

        def key(aid: str) -> tuple[int, int, int]:
            used = aid in self.last_used
            return (1 if used else 0, self.last_used.get(aid, 0), self._order[aid])

        chosen = min(candidates, key=key)
        self._lock(chosen, t, duration)
        return chosen


_ARITY = {"AVAIL": 2, "ACQ": 3, "ANY": 2}


def run_commands(lines: list[str]) -> list[str]:
    """First line is `ACCOUNTS id1 id2 ...` (construction order); every following line is a
    command. Malformed lines / KeyError / ValueError -> 'ERROR', processing continues."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    out: list[str] = []
    if not lines:
        return out
    head = lines[0].split()
    scheduler = AccountScheduler(head[1:]) if head and head[0] == "ACCOUNTS" else AccountScheduler([])
    body = lines[1:] if head and head[0] == "ACCOUNTS" else lines

    for raw in body:
        fields = raw.split()
        verb, args = fields[0], fields[1:]
        try:
            if verb not in _ARITY or len(args) != _ARITY[verb]:
                raise ValueError("bad command")
            if verb == "AVAIL":
                aid, t = args[0], int(args[1])
                out.append("true" if scheduler.is_available(aid, t) else "false")
            elif verb == "ACQ":
                aid, t, duration = args[0], int(args[1]), int(args[2])
                out.append("true" if scheduler.acquire(aid, t, duration) else "false")
            else:  # ANY
                t, duration = int(args[0]), int(args[1])
                result = scheduler.acquire_any(t, duration)
                out.append(result if result is not None else "none")
        except (KeyError, ValueError):
            out.append("ERROR")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = run_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
