"""pc26 Top K Hashtags -- reference solution.

Popularity of a hashtag = number of DISTINCT users who have ever posted it (not total post
count). Sort by popularity descending, hashtag ascending, take the top k.

Part2 (reconstructed): a streaming class with add(user, tag) and top(k), where top() is called
often -- we maintain per-tag sets of users plus a small max-heap-free "just re-sort on demand"
strategy, and discuss the state/complexity tradeoff in problem.md (a full O(1)-amortised design
needs an order-statistics structure; this drill's scale doesn't need it).

Part3 (reconstructed): a sliding time window of W seconds -- events carry a timestamp, only
events within the last W seconds (relative to the latest event's timestamp) count, and a user
counts at most once per tag within the window regardless of how many times they posted it.
"""

from __future__ import annotations

import sys
from collections import defaultdict

# --------------------------------------------------------------------------- Part 1
def top_k_hashtags(events: list[tuple[str, str]], k: int) -> list[tuple[str, int]]:
    """events: (user_id, hashtag) pairs. Popularity = number of distinct users per hashtag.
    Returns up to k (hashtag, popularity), sorted popularity desc then hashtag asc.
    ValueError if k < 0."""
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k!r}")
    users_by_tag: dict[str, set[str]] = defaultdict(set)
    for user, tag in events:
        users_by_tag[tag].add(user)
    ranked = sorted(users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(tag, len(users)) for tag, users in ranked[:k]]


# --------------------------------------------------------------------------- Part 2
class HashtagCounter:
    """Part2 (reconstructed): streaming add(user, tag) + frequent top(k) queries.

    State: `users_by_tag: dict[tag -> set[user]]`, size O(number of distinct (user, tag) pairs
    ever added) -- this is the minimum state any correct implementation needs, since "distinct
    users per tag" cannot be answered from counts alone (you must be able to tell whether a user
    has already been counted for a tag).

    top(k) complexity: O(T log T) where T = number of distinct tags seen, because we re-sort tags
    by (-popularity, tag) on every call. This is NOT the asymptotically optimal design -- a
    proper solution keeps tags in a balanced structure ordered by (popularity, tag) and updates it
    in O(log T) per add() (e.g. a sorted-list/skiplist with a popularity change = remove + insert,
    or a Fenwick-tree-of-buckets by popularity for top(k) in O(k + log T)). We keep the simple
    re-sort here because interview time rarely allows building an order-statistics tree from
    scratch, and the drill's tests never simulate the query volume where the difference matters;
    problem.md's follow-ups section states the O(log T) design in words for when it's asked."""

    def __init__(self) -> None:
        self._users_by_tag: dict[str, set[str]] = defaultdict(set)

    def add(self, user: str, tag: str) -> None:
        self._users_by_tag[tag].add(user)

    def top(self, k: int) -> list[tuple[str, int]]:
        if k < 0:
            raise ValueError(f"k must be >= 0, got {k!r}")
        ranked = sorted(self._users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        return [(tag, len(users)) for tag, users in ranked[:k]]


# --------------------------------------------------------------------------- Part 3
def top_k_hashtags_windowed(
    events: list[tuple[int, str, str]], k: int, window_seconds: int
) -> list[tuple[str, int]]:
    """events: (timestamp, user_id, hashtag), NOT necessarily sorted by timestamp. Only events
    with timestamp >= max_ts - window_seconds count (max_ts = the latest timestamp across all
    events): a CLOSED trailing window [max_ts - window_seconds, max_ts], so window_seconds == 0
    keeps exactly the event(s) at max_ts. A user counts at most once per tag within the window.
    Returns up to k (hashtag, popularity) sorted popularity desc, hashtag asc. ValueError if
    k < 0 or window_seconds < 0."""
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k!r}")
    if window_seconds < 0:
        raise ValueError(f"window_seconds must be >= 0, got {window_seconds!r}")
    if not events:
        return []
    max_ts = max(ts for ts, _, _ in events)
    cutoff = max_ts - window_seconds
    users_by_tag: dict[str, set[str]] = defaultdict(set)
    for ts, user, tag in events:
        if ts >= cutoff:
            users_by_tag[tag].add(user)
    ranked = sorted(users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(tag, len(users)) for tag, users in ranked[:k]]


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _fmt_ranked(ranked: list[tuple[str, int]]) -> list[str]:
    return [f"{tag} {count}" for tag, count in ranked] if ranked else ["-"]


def part1(lines: list[str]) -> list[str]:
    """'N n' / n 'user,tag' lines / 'K k' -> up to k 'tag count' lines, or '-'."""
    records, idx = _read_n_lines(lines, 0)
    tag_line, k = lines[idx].split()
    if tag_line != "K":
        raise ValueError(f"expected 'K <k>', got {lines[idx]!r}")
    events = []
    for rec in records:
        user, tag = rec.split(",")
        events.append((user, tag))
    return _fmt_ranked(top_k_hashtags(events, int(k)))


def part2(lines: list[str]) -> list[str]:
    """'N n' / n lines, each 'ADD user,tag' or 'TOP k' -> per TOP (in order): 'Q count' then
    up to k 'tag count' lines. '-' if no TOP was ever issued."""
    ops, _ = _read_n_lines(lines, 0)
    counter = HashtagCounter()
    snapshots: list[list[tuple[str, int]]] = []
    for op in ops:
        parts = op.split(maxsplit=1)
        if parts[0] == "ADD":
            user, tag = parts[1].split(",")
            counter.add(user, tag)
        elif parts[0] == "TOP":
            snapshots.append(counter.top(int(parts[1])))
        else:
            raise ValueError(f"unknown op {op!r}")
    if not snapshots:
        return ["-"]
    out: list[str] = []
    for snap in snapshots:
        out.append(f"Q {len(snap)}")
        out.extend(f"{tag} {count}" for tag, count in snap)
    return out


def part3(lines: list[str]) -> list[str]:
    """'N n' / n 'ts,user,tag' lines / 'K k W window' -> up to k 'tag count' lines, or '-'."""
    records, idx = _read_n_lines(lines, 0)
    header = lines[idx].split()
    if header[0] != "K" or header[2] != "W":
        raise ValueError(f"expected 'K <k> W <window>', got {lines[idx]!r}")
    k, window = int(header[1]), int(header[3])
    events = []
    for rec in records:
        ts, user, tag = rec.split(",")
        events.append((int(ts), user, tag))
    return _fmt_ranked(top_k_hashtags_windowed(events, k, window))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
