"""cd04 RateLimiter (4-part) — reference solution.

One class covers all four parts at once (Part 1's "naive unbounded list" sketch described in
problem.md is a teaching device, not a separate code path here): a per-client deque of allowed
timestamps, trimmed against the sliding window on every call, so a client's deque never holds more
than `limit` entries (Part 1 + Part 2's memory bound). `t` is always **milliseconds**. Backward
clock jumps are clamped per-client, `limit == 0` always denies, and the whole critical section is
guarded by one `threading.Lock` for exact correctness under concurrent callers (Part 3 + Part 4).

Window convention (matches problems/q23_rate_limiter): a request at `t` counts against the window
`(t - window_ms, t]` — left-open, right-closed. Denied requests are never recorded.
"""

from __future__ import annotations

import sys
import threading
from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window_s: int) -> None:
        self.limit = limit
        self.window_ms = window_s * 1000
        self._log: dict[str, deque[int]] = {}
        self._last_seen: dict[str, int] = {}
        self._lock = threading.Lock()

    def _effective_t(self, client_id: str, t: int) -> int:
        """Clock-rollback rule (Part 3): a t smaller than this client's last-seen t is clamped
        forward to that last-seen t, per client (other clients are unaffected)."""
        last = self._last_seen.get(client_id)
        return t if last is None or t >= last else last

    def allow(self, client_id: str, t: int) -> bool:
        """True iff client_id has fewer than `limit` allowed requests in (t - window_ms, t];
        a denied call is never recorded. Backward t is clamped per client (see _effective_t)."""
        with self._lock:
            eff_t = self._effective_t(client_id, t)
            self._last_seen[client_id] = eff_t
            dq = self._log.setdefault(client_id, deque())
            cutoff = eff_t - self.window_ms
            while dq and dq[0] <= cutoff:  # trim expired entries (Part 2: bounds memory)
                dq.popleft()
            if self.limit <= 0 or len(dq) >= self.limit:
                return False  # denied requests are never recorded
            dq.append(eff_t)
            return True

    def evict_idle(self, now: int) -> int:
        """Trim every client's deque against `now`; drop clients left with an empty deque
        (no allowed request in (now - window_ms, now]). Returns the number of clients evicted."""
        with self._lock:
            cutoff = now - self.window_ms
            idle: list[str] = []
            for client_id, dq in self._log.items():
                while dq and dq[0] <= cutoff:
                    dq.popleft()
                if not dq:
                    idle.append(client_id)
            for client_id in idle:
                del self._log[client_id]
                del self._last_seen[client_id]
            return len(idle)

    def log_size(self, client_id: str) -> int:
        """Observability hook for Part 2's memory-bound claim: how many timestamps are
        currently retained for this client (0 for unknown/never-seen/evicted)."""
        with self._lock:
            dq = self._log.get(client_id)
            return len(dq) if dq is not None else 0


def run_commands(lines: list[str]) -> list[str]:
    """First line 'LIMIT <limit> <window_s>' configures the limiter; then:
        ALLOW <client_id> <t_ms>   -> ALLOW | DENY
        CLEANUP <now_ms>           -> EVICTED <n>
    Malformed lines -> ERROR, processing continues."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    out: list[str] = []
    if not lines:
        return out
    head = lines[0].split()
    if len(head) == 3 and head[0] == "LIMIT":
        limiter = RateLimiter(int(head[1]), int(head[2]))
        body = lines[1:]
    else:
        limiter = RateLimiter(5, 1)  # default: 5 requests / 1 s, mirrors q23's documented default
        body = lines

    for raw in body:
        fields = raw.split()
        verb = fields[0] if fields else ""
        try:
            if verb == "ALLOW" and len(fields) == 3:
                client_id, t = fields[1], int(fields[2])
                out.append("ALLOW" if limiter.allow(client_id, t) else "DENY")
            elif verb == "CLEANUP" and len(fields) == 2:
                out.append(f"EVICTED {limiter.evict_idle(int(fields[1]))}")
            else:
                raise ValueError("bad command")
        except ValueError:
            out.append("ERROR")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = run_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
