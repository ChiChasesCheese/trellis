"""q09 Jupyter Load Balancer — reference solution.

State: load[t], conns (id -> user, object, target, arrival seq), members[t] (ids on t), the
object -> target pin, and a min-heap of (load, target) with lazy invalidation so "least loaded"
is O(log n) instead of O(num_targets) per request.
"""
from __future__ import annotations

import heapq
import sys


def route_requests(num_targets: int, max_connections_per_target: int, requests: list[str],
                   *, shutdown_permanent: bool = False, variant_b: bool = False) -> list[str]:
    cap = max_connections_per_target
    load = [0] * num_targets
    down = [False] * num_targets
    heap = [(0, t) for t in range(num_targets)]          # (load, index): sorted ⇒ valid heap
    conns: dict[str, tuple[str | None, str | None, int, int]] = {}  # id -> (user, obj, target, seq)
    members: list[dict[str, None]] = [{} for _ in range(num_targets)]  # target -> ids (ordered)
    pin: dict[str, int] = {}                              # object -> target (Part 3)
    objs_on: list[set[str]] = [set() for _ in range(num_targets)]
    log: list[str] = []

    def least_loaded() -> int | None:
        """Top of the heap once stale / down entries are dropped; None when every target is full."""
        while heap:
            ld, t = heap[0]
            if ld != load[t] or down[t]:
                heapq.heappop(heap)
                continue
            # Part 4: the least-loaded target being full means all targets are full (load <= cap)
            return t if ld < cap else None
        return None

    def place(cid: str, user: str | None, obj: str | None, seq: int) -> bool:
        if obj is not None and obj in pin:               # Part 3: sticky wins over load
            t = pin[obj]
            if load[t] >= cap:                           # Part 4: full sticky target ⇒ reject
                return False
        else:
            t = least_loaded()                           # Part 1: fewest connections, smallest index
            if t is None:
                return False
            if obj is not None:
                pin[obj] = t
                objs_on[t].add(obj)
        load[t] += 1
        heapq.heappush(heap, (load[t], t))
        conns[cid] = (user, obj, t, seq)
        members[t][cid] = None
        log.append(f"{cid} {t + 1}" if variant_b else f"{cid},{user},{t + 1}")  # 1-based
        return True

    for seq, raw in enumerate(requests):
        parts = raw.split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "CONNECT":
            cid = parts[1]
            if cid in conns:                             # duplicate active id ⇒ ignore
                continue
            if variant_b:
                user, obj = None, parts[2]
            else:
                user, obj = parts[2], (parts[3] if len(parts) > 3 else None)
            place(cid, user, obj, seq)
        elif cmd == "DISCONNECT":
            info = conns.pop(parts[1], None)
            if info is None:                             # Part 2: unknown id ⇒ ignore
                continue
            t = info[2]
            load[t] -= 1
            heapq.heappush(heap, (load[t], t))
            del members[t][parts[1]]
        elif cmd == "SHUTDOWN":
            t = int(parts[1]) - 1                        # 1-based on input too
            if not 0 <= t < num_targets or down[t]:
                continue
            # Part 5: evict in original arrival order, clear pins, re-route with t unavailable
            evicted = sorted(members[t], key=lambda c: conns[c][3])
            infos = [conns.pop(c) for c in evicted]
            members[t].clear()
            load[t] = 0
            for obj in objs_on[t]:
                pin.pop(obj, None)
            objs_on[t].clear()
            down[t] = True
            for cid, (user, obj, _, s) in zip(evicted, infos):
                place(cid, user, obj, s)                 # dropped silently when it does not fit
            if not shutdown_permanent:                   # prachub: rejoins with load 0
                down[t] = False
                heapq.heappush(heap, (0, t))
    return log


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    n, cap = (int(x) for x in lines[0].split())
    out = route_requests(n, cap, lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
