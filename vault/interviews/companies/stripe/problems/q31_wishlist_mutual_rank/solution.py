"""q31 Wishlist / Mutual Rank — reference solution.

`lists[u]` is u's ordered wishlist; `pos[u][v]` is the 0-based rank of v in u's list (built once so
every rank lookup is O(1)).  Unknown users behave as having an empty list.  All ranks are 0-based.
"""
from __future__ import annotations

import sys


class Wishlists:
    def __init__(self, data: dict[str, list[str]]) -> None:
        self.lists: dict[str, list[str]] = {u: [w for w in ws if w != u] for u, ws in data.items()}  # self-wishes ignored
        self.pos: dict[str, dict[str, int]] = {u: {w: i for i, w in enumerate(ws)} for u, ws in self.lists.items()}

    def entry(self, user: str, rank: int) -> str | None:
        """list[user][rank] or None when the user/rank does not exist."""
        ws = self.lists.get(user, [])
        return ws[rank] if 0 <= rank < len(ws) else None

    # ---- Part 1 ----------------------------------------------------------------------------
    def has_mutual_pair_for_rank(self, user: str, rank: int) -> bool:
        other = self.entry(user, rank)
        return other is not None and self.entry(other, rank) == user   # same rank on both sides

    def has_mutual_first_choice(self, user: str) -> bool:
        return self.has_mutual_pair_for_rank(user, 0)

    # ---- Part 2 ----------------------------------------------------------------------------
    def changed_pairings(self, user: str, rank: int) -> list[str]:
        if rank <= 0 or self.entry(user, rank) is None:
            return []                                   # nothing above rank 0 / rank out of range
        up, down = self.entry(user, rank), self.entry(user, rank - 1)   # up moves to rank-1, down to rank
        changed = []
        # `up`: currently mutual iff list[up][rank] == user; after the swap iff list[up][rank-1] == user
        if (self.entry(up, rank) == user) != (self.entry(up, rank - 1) == user):
            changed.append(up)
        # `down`: currently mutual iff list[down][rank-1] == user; after iff list[down][rank] == user
        if (self.entry(down, rank - 1) == user) != (self.entry(down, rank) == user):
            changed.append(down)
        return changed

    # ---- Part 3 ----------------------------------------------------------------------------
    def mutual_pairs(self) -> list[tuple[str, str, int]]:
        out = []
        for u, ws in self.lists.items():
            for ru, v in enumerate(ws):
                rv = self.pos.get(v, {}).get(u)
                if rv is not None and u < v:            # each pair once, smaller name first
                    out.append((u, v, ru + rv))
        return sorted(out, key=lambda t: (t[2], t[0], t[1]))   # score, then names

    def best_match(self, user: str) -> tuple[str, int] | None:
        best = None
        for ru, v in enumerate(self.lists.get(user, [])):
            rv = self.pos.get(v, {}).get(user)
            if rv is None:
                continue
            key = (ru + rv, ru, v)                       # score, then my own rank, then name
            if best is None or key < best:
                best = key
        return (best[2], best[0]) if best else None

    # ---- Part 4 ----------------------------------------------------------------------------
    def cycles(self, k: int) -> list[list[str]]:
        found: list[list[str]] = []

        def walk(start: str, path: list[str]) -> None:
            last = path[-1]
            if len(path) == k:
                if start in self.pos.get(last, {}):
                    found.append(list(path))
                return
            for nxt in self.lists.get(last, []):
                if nxt > start and nxt not in path:      # start is the smallest name -> each cycle once
                    path.append(nxt)
                    walk(start, path)
                    path.pop()

        if k >= 2:
            for start in self.lists:
                walk(start, [start])
        return sorted(found)


def parse(lines: list[str]) -> tuple[Wishlists, list[list[str]]]:
    data: dict[str, list[str]] = {}
    queries: list[list[str]] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if ":" in line:
            user, _, rest = line.partition(":")
            data[user.strip()] = rest.split()
        else:
            queries.append(line.split())
    return Wishlists(data), queries


def fmt_list(names: list[str]) -> str:
    return " ".join(names) if names else "NONE"


def answer(w: Wishlists, q: list[str], part: int) -> list[str]:
    cmd = q[0].upper()
    if cmd == "FIRST":
        return [str(w.has_mutual_first_choice(q[1])).lower()]
    if cmd == "RANK":
        return [str(w.has_mutual_pair_for_rank(q[1], int(q[2]))).lower()]
    if cmd == "BUMP" and part >= 2:
        return [fmt_list(w.changed_pairings(q[1], int(q[2])))]
    if cmd == "PAIRS" and part >= 3:
        return [f"{u} {v} {s}" for u, v, s in w.mutual_pairs()] or ["NONE"]
    if cmd == "BEST" and part >= 3:
        b = w.best_match(q[1])
        return [f"{b[0]} {b[1]}" if b else "NONE"]
    if cmd == "CYCLES" and part >= 4:
        return [" ".join(c) for c in w.cycles(int(q[1]))] or ["NONE"]
    return []   # unknown command for this part: ignored


def run(lines: list[str], part: int) -> list[str]:
    w, queries = parse(lines)
    out: list[str] = []
    for q in queries:
        out.extend(answer(w, q, part))
    return out


def part1(lines: list[str]) -> list[str]:
    """FIRST u / RANK u r -> 'true' | 'false'."""
    return run(lines, 1)


def part2(lines: list[str]) -> list[str]:
    """+ BUMP u r -> affected users or 'NONE'."""
    return run(lines, 2)


def part3(lines: list[str]) -> list[str]:
    """+ PAIRS -> 'u v score' lines; BEST u -> 'v score' | 'NONE'."""
    return run(lines, 3)


def part4(lines: list[str]) -> list[str]:
    """+ CYCLES k -> 'u1 u2 ... uk' lines | 'NONE'."""
    return run(lines, 4)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
