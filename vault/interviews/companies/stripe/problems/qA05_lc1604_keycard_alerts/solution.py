"""qA05 LC 1604 Alert Using Same Key-Card >= 3 Times in 1 Hour — reference solution.

Times become minutes since midnight (no day wrap — LC says all on one day). Per name: sort, then
check a fixed-size window of k consecutive uses: times[i+k-1] - times[i] <= window (inclusive).
Part 3 is the online limiter: a deque of ALLOWED swipe times per name; denied swipes are not kept.
"""
from __future__ import annotations

import sys
from collections import defaultdict, deque


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.strip().split(":")
    return int(h) * 60 + int(m)


def alert_names_k(key_name: list[str], key_time: list[str], k: int = 3, window: int = 60) -> list[str]:
    """Part 2 (Part 1 is k=3, window=60): sorted unique names with k uses inside `window` minutes."""
    if k <= 0 or window < 0:
        raise ValueError("k must be >= 1 and window >= 0")
    times: dict[str, list[int]] = defaultdict(list)
    for name, t in zip(key_name, key_time):
        times[name].append(to_minutes(t))
    alerted = []
    for name, ts in times.items():
        ts.sort()
        # window of k consecutive sorted uses; inclusive bound: exactly `window` minutes still alerts
        if any(ts[i + k - 1] - ts[i] <= window for i in range(len(ts) - k + 1)):
            alerted.append(name)
    return sorted(alerted)


def alert_names(key_name: list[str], key_time: list[str]) -> list[str]:
    """Part 1: LC signature."""
    return alert_names_k(key_name, key_time, 3, 60)


class KeyCardLimiter:
    """Part 3: per-name sliding window over ALLOWED swipes only (denied ones never count)."""

    def __init__(self, limit: int = 2, window: int = 60) -> None:
        self.limit, self.window = limit, window
        self.denied: list[tuple[str, str]] = []
        self._allowed: dict[str, deque[int]] = defaultdict(deque)
        self._last: dict[str, int] = {}

    def swipe(self, name: str, time: str) -> bool:
        t = to_minutes(time)
        if t < self._last.get(name, -1):
            raise ValueError(f"swipe for {name} at {time} is earlier than the previous one")
        self._last[name] = t
        q = self._allowed[name]
        while q and q[0] < t - self.window:  # evict strictly older than t-window (t-window itself counts)
            q.popleft()
        if len(q) >= self.limit:
            self.denied.append((name, time))
            return False
        q.append(t)
        return True


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    body = lines[1:]
    if part == 1:
        names, times = zip(*(ln.split() for ln in body)) if body else ((), ())
        out = alert_names(list(names), list(times))
    elif part == 2:
        k, window = (int(x) for x in body[0].split())
        names, times = zip(*(ln.split() for ln in body[1:])) if body[1:] else ((), ())
        out = alert_names_k(list(names), list(times), k, window)
    else:
        limit, window = (int(x) for x in body[0].split())
        lim = KeyCardLimiter(limit, window)
        out = []
        for ln in body[1:]:
            name, t = ln.split()
            out.append(f"{name} {t} {'ALLOW' if lim.swipe(name, t) else 'DENY'}")
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
