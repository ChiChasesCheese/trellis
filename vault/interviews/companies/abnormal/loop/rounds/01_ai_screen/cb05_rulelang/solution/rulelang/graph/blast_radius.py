"""Who is at risk once an account is compromised: a time-respecting breadth-first walk of ``CommGraph``."""
from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from rulelang.addresses import is_internal, normalize_address
from rulelang.graph.comm_graph import CommGraph


@dataclass(frozen=True)
class Exposure:
    address: str
    hops: int
    path: tuple[str, ...]  # compromised account first, this address last

    def to_dict(self) -> dict[str, Any]:
        return {"address": self.address, "hops": self.hops, "path": list(self.path)}


def blast_radius(
    graph: CommGraph,
    account: str,
    since: datetime,
    max_hops: int,
    internal_domains: Iterable[str],
) -> list[Exposure]:
    """Everyone ``account`` emailed at or after ``since``, and everyone they emailed after that, up to ``max_hops``.

    An edge only counts if the pair was in contact at or after the time the risk reached its sender
    (``last_ts`` is the latest contact, so ``last_ts >= arrival`` means one exists). Reaching an external
    address is reported but not followed: we have no graph for other organisations.
    """
    internal = tuple(internal_domains)
    start = normalize_address(account)
    seen = {start}
    queue: deque[tuple[str, int, tuple[str, ...], datetime]] = deque([(start, 0, (start,), since)])
    found: list[Exposure] = []
    while queue:
        addr, hops, path, arrival = queue.popleft()
        if hops == max_hops:
            continue
        for edge in graph.neighbors(addr):
            if edge.dst in seen or edge.last_ts < arrival:
                continue
            seen.add(edge.dst)
            dst_path = path + (edge.dst,)
            found.append(Exposure(edge.dst, hops + 1, dst_path))
            if is_internal(edge.dst, internal):
                # first_ts is a lower bound on when this contact happened; it never moves arrival backwards.
                queue.append((edge.dst, hops + 1, dst_path, max(arrival, edge.first_ts)))
    return sorted(found, key=lambda e: (e.hops, e.address))
