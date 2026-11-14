"""Multi-channel message queue: channels as bits, fan-out by intersection, union-find over shared channels,
and the fewest channels for a set of producer -> consumer patterns.

    uv run --project <repo root> python solution.py      # a short demo
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable

# ---------------------------------------------------------------- Part 1: the queue


@dataclass(frozen=True)
class Message:
    id: int
    producer: str
    channels: frozenset[str]
    payload: Any


def bits_to_names(mask: int, names: list[str]) -> set[str]:
    """Channel names for the set bits of mask (bit i = names[i]). Costs one step per set bit."""
    out = set()
    while mask:
        low = mask & -mask  # lowest set bit
        out.add(names[low.bit_length() - 1])
        mask ^= low
    return out


class MessageQueue:
    """Each channel is one bit; a participant's channels are an int used as a bit set, so "which channels do
    these two share" is one AND (C/64 machine words for C channels) instead of a set intersection.

    Delivery is push: enqueue looks up the subscribers of each tagged channel, takes the union (a consumer on two of
    the tags still gets the message once) and appends to each recipient's inbox. Consumers only get messages
    enqueued while they are subscribed."""

    def __init__(self, channels: Iterable[str] = ()):
        self._bit: dict[str, int] = {}  # channel -> bit index
        self._names: list[str] = []  # bit index -> channel
        self._subs: dict[str, set[str]] = {}  # channel -> subscribed consumers
        self._consumer_mask: dict[str, int] = {}
        self._producer_mask: dict[str, int] = {}  # channels each producer has published to
        self._inbox: dict[str, deque[Message]] = {}
        self._next_id = 0
        for c in channels:
            self.add_channel(c)

    # channels
    def add_channel(self, name: str) -> int:
        """O(1). Returns the channel's bit index. Existing masks stay valid: old bits never move."""
        if name in self._bit:
            raise ValueError(f"channel {name!r} exists")
        self._bit[name] = len(self._names)
        self._names.append(name)
        self._subs[name] = set()
        return self._bit[name]

    def channel_mask(self, names: Iterable[str]) -> int:
        mask = 0
        for n in names:
            if n not in self._bit:
                raise KeyError(f"unknown channel {n!r}")
            mask |= 1 << self._bit[n]
        return mask

    # subscriptions
    def subscribe(self, consumer: str, channel: str) -> None:
        self._consumer_mask[consumer] = self._consumer_mask.get(consumer, 0) | self.channel_mask([channel])
        self._subs[channel].add(consumer)
        self._inbox.setdefault(consumer, deque())

    def unsubscribe(self, consumer: str, channel: str) -> None:
        """No-op when not subscribed. Messages already in the inbox stay there."""
        bit = self.channel_mask([channel])
        self._consumer_mask[consumer] = self._consumer_mask.get(consumer, 0) & ~bit
        self._subs[channel].discard(consumer)

    def subscriptions(self, consumer: str) -> set[str]:
        return bits_to_names(self._consumer_mask.get(consumer, 0), self._names)

    # messages
    def enqueue(self, producer: str, channels: Iterable[str], payload: Any) -> int:
        """O(k + R): k tagged channels, R recipients. Returns the message id."""
        channels = frozenset(channels)
        if not channels:
            raise ValueError("a message needs at least one channel")
        mask = self.channel_mask(channels)  # validates every name before anything changes
        self._producer_mask[producer] = self._producer_mask.get(producer, 0) | mask
        msg = Message(self._next_id, producer, channels, payload)
        self._next_id += 1
        recipients = set().union(*(self._subs[c] for c in channels))
        for consumer in recipients:
            self._inbox[consumer].append(msg)
        return msg.id

    def consume(self, consumer: str, max_n: int | None = None) -> list[Message]:
        """Oldest first; removes what it returns. Unknown consumer -> []."""
        box = self._inbox.get(consumer, deque())
        n = len(box) if max_n is None else min(max_n, len(box))
        return [box.popleft() for _ in range(n)]

    def pending(self, consumer: str) -> int:
        return len(self._inbox.get(consumer, ()))

    def shared_channels(self, a: str, b: str) -> set[str]:
        """Channels two participants have in common (a producer's channels = those it has published to)."""
        return bits_to_names(self._mask_of(a) & self._mask_of(b), self._names)

    def _mask_of(self, who: str) -> int:
        return self._consumer_mask.get(who, 0) | self._producer_mask.get(who, 0)

    # Part 2 on live state
    def share_groups(self) -> list[list[str]]:
        """Rebuilt on each call: union-find cannot undo a union, so an unsubscribe is handled by rebuilding
        (O(total memberships)) rather than by deleting."""
        members = {w: bits_to_names(self._mask_of(w), self._names)
                   for w in set(self._consumer_mask) | set(self._producer_mask)}
        return groups(members)


# ---------------------------------------------------------------- Part 2: union-find


class UnionFind:
    """Disjoint sets with path halving + union by size: each operation is O(alpha(n)), effectively constant."""

    def __init__(self):
        self.parent: dict[Any, Any] = {}
        self.size: dict[Any, int] = {}

    def add(self, x) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1

    def find(self, x):
        self.add(x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # point to the grandparent: halves the path
            x = self.parent[x]
        return x

    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra  # small tree under big tree: depth stays O(log n)
        self.size[ra] += self.size[rb]
        return True


def groups(memberships: dict[str, Iterable[str]]) -> list[list[str]]:
    """Participants that share a channel directly or through others, as sorted lists, sorted by first member.
    Channel nodes join the union-find too, so the cost is O(total memberships), not O(participants^2).
    A participant with no channel is not in any group."""
    uf = UnionFind()
    for who, chans in memberships.items():
        for ch in chans:
            uf.union(("p", who), ("c", ch))  # tagged keys: a channel may share a name with a participant
    by_root: dict[Any, list[str]] = {}
    for who, chans in memberships.items():
        if chans:
            by_root.setdefault(uf.find(("p", who)), []).append(who)
    return sorted(sorted(g) for g in by_root.values())


# ---------------------------------------------------------------- Part 3: fewest channels, isolation rule


def plan_channels(pairs: Iterable[tuple[str, str]]) -> dict[str, str]:
    """pairs = (producer, consumer) that must talk. Rule: each pair shares a channel, and two participants with no
    path of pairs between them never share one. Then each connected group needs one channel and one is enough.
    Returns participant -> channel name (ch0, ch1, ... in order of each group's first member)."""
    uf = UnionFind()
    for p, c in pairs:
        uf.union(p, c)
    comps: dict[Any, list[str]] = {}
    for x in uf.parent:
        comps.setdefault(uf.find(x), []).append(x)
    plan = {}
    for i, comp in enumerate(sorted(sorted(c) for c in comps.values())):
        for x in comp:
            plan[x] = f"ch{i}"
    return plan


def min_channels(pairs: Iterable[tuple[str, str]]) -> int:
    return len(set(plan_channels(pairs).values()))


# ---------------------------------------------------------------- Part 4 (stretch): exact delivery


def min_channels_exact(pairs: Iterable[tuple[str, str]], limit: int = 14) -> list[tuple[frozenset, frozenset]]:
    """Stricter rule: a consumer must receive messages ONLY from the producers it is paired with. A channel is then
    a (producers, consumers) block where every producer-consumer combination is a wanted pair (a biclique), and the
    blocks must cover every pair. Fewest blocks = minimum biclique cover: NP-hard in general, so this is exact search
    for small inputs only (at most `limit` producers).

    1. Candidates: only maximal blocks are needed (growing a block never hurts). For every non-empty set S of
       producers, the consumers they all reach are T = N(S); the maximal block is (every producer that reaches all
       of T, T).
    2. Smallest cover: iterative deepening; branch on the uncovered pair with the fewest candidate blocks."""
    pairs = set(pairs)
    if not pairs:
        return []
    prods = sorted({p for p, _ in pairs})
    cons = sorted({c for _, c in pairs})
    if set(prods) & set(cons):
        raise ValueError("exact planning assumes producers and consumers are different names")
    if len(prods) > limit:
        raise ValueError(f"more than {limit} producers: use a heuristic")
    reach = {p: frozenset(c for q, c in pairs if q == p) for p in prods}
    blocks = set()
    for r in range(1, len(prods) + 1):
        for s in combinations(prods, r):
            t = frozenset.intersection(*(reach[p] for p in s))
            if t:
                blocks.add((frozenset(p for p in prods if t <= reach[p]), t))
    blocks = sorted(blocks, key=lambda b: (sorted(b[0]), sorted(b[1])))
    covers = {e: [b for b in blocks if e[0] in b[0] and e[1] in b[1]] for e in pairs}

    def search(uncovered: set, depth: int, chosen: list) -> list | None:
        if not uncovered:
            return chosen
        if depth == 0:
            return None
        e = min(uncovered, key=lambda e: (len(covers[e]), e))
        for b in covers[e]:
            got = search({x for x in uncovered if not (x[0] in b[0] and x[1] in b[1])}, depth - 1, chosen + [b])
            if got is not None:
                return got
        return None

    for k in range(1, len(pairs) + 1):
        found = search(set(pairs), k, [])
        if found is not None:
            return found
    raise AssertionError("unreachable: one block per pair always works")


def main() -> None:
    q = MessageQueue(["train", "eval", "alerts"])
    q.subscribe("dashboard", "eval")
    q.subscribe("dashboard", "alerts")
    q.subscribe("pager", "alerts")
    q.enqueue("ci", ["eval", "alerts"], "eval regressed 3%")
    print("dashboard:", [m.payload for m in q.consume("dashboard")], "pager:", [m.payload for m in q.consume("pager")])
    q.add_channel("perf")
    q.subscribe("perf-bot", "perf")
    q.enqueue("bench", ["perf"], "p99 up")
    print("groups:", q.share_groups())
    pairs = [("p1", "c1"), ("p1", "c2"), ("p2", "c2"), ("p3", "c3")]
    print("min channels (isolation):", min_channels(pairs), "exact:", len(min_channels_exact(pairs)))


if __name__ == "__main__":
    main()
