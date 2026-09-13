"""cd04 RateLimiter (4-part) — YOUR implementation. Run: pytest against this file with IMPL=starter.

See problem.md for the full contract: t is always MILLISECONDS, window is (t-window_ms, t]
(left-open, right-closed), backward clock is CLAMPED per client (not rejected), limit==0 always
denies, and allow()/evict_idle() must be exact under concurrent callers.
"""

from __future__ import annotations

import sys
import threading  # noqa: F401
from collections import deque  # noqa: F401


class RateLimiter:
    def __init__(self, limit: int, window_s: int) -> None:
        pass  # TODO: store limit, window_ms, per-client deque of allowed timestamps, a lock

    def allow(self, client_id: str, t: int) -> bool:
        """t is milliseconds. Window (t - window_ms, t], left-open/right-closed. A denied
        request is never recorded. Backward t for this client is clamped to its last-seen t."""
        raise NotImplementedError  # TODO

    def evict_idle(self, now: int) -> int:
        """Trim every client's log against now; drop clients left with an empty log entirely.
        Return the number of clients evicted."""
        raise NotImplementedError  # TODO

    def log_size(self, client_id: str) -> int:
        """Observability hook: how many timestamps are currently retained for this client
        (0 for unknown/never-seen/evicted). Used by Part 2 tests to prove the memory bound."""
        raise NotImplementedError  # TODO


def run_commands(lines: list[str]) -> list[str]:
    """First line 'LIMIT <limit> <window_s>' configures the limiter (default 'LIMIT 5 1' if
    absent); then 'ALLOW <client_id> <t_ms>' -> ALLOW/DENY, 'CLEANUP <now_ms>' -> 'EVICTED <n>'.
    Malformed lines -> ERROR, processing continues."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = run_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
