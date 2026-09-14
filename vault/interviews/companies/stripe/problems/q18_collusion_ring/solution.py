"""q18 Six Degrees of Collusion — reference solution.

Link graph: customers sharing an identifier value at the same field position are linked.
Parts 1–3 use union-find over (position, value) keys; Part 4 is the weighted record-linking
variant. All ordering is deterministic (sorted names / first-appearance order of rings).
"""
from __future__ import annotations

import sys
from collections import defaultdict

DEFAULT_WEIGHTS = {"name": 0.2, "email": 0.5, "company": 0.3}
FIELDS4 = ["user_id", "name", "email", "company"]


def parse(records: list[str]) -> list[list[str]]:
    """':'-separated, trimmed fields; blank lines dropped. rows[i][0] is the customer."""
    rows = []
    for raw in records:
        raw = raw.strip()
        if raw:
            rows.append([f.strip() for f in raw.split(":")])
    return rows


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def _ident_map(rows: list[list[str]]) -> dict[tuple[int, str], list[str]]:
    """(field position, value) -> customers (in input order, may repeat)."""
    owners: dict[tuple[int, str], list[str]] = defaultdict(list)
    for row in rows:
        for pos, val in enumerate(row[1:], start=1):
            if val:  # empty identifiers link nothing
                owners[(pos, val)].append(row[0])
    return owners


# ---------------------------------------------------------------- Part 1
def direct_links(records: list[str], target: str) -> list[str]:
    rows = parse(records)
    owners = _ident_map(rows)
    linked: set[str] = set()
    for row in rows:
        if row[0] != target:
            continue
        for pos, val in enumerate(row[1:], start=1):
            if val:
                linked.update(owners[(pos, val)])
    linked.discard(target)  # never list the target itself
    return sorted(linked)


# ---------------------------------------------------------------- Part 2
def groups(records: list[str]) -> list[set[str]]:
    rows = parse(records)
    dsu = DSU()
    order: list[str] = []  # customers in first-appearance order
    seen: set[str] = set()
    for row in rows:
        if row[0] not in seen:
            seen.add(row[0])
            order.append(row[0])
        dsu.find(row[0])
    for custs in _ident_map(rows).values():
        for other in custs[1:]:
            dsu.union(custs[0], other)
    comps: dict[str, set[str]] = {}
    result: list[set[str]] = []
    for c in order:  # ring order = first-appearing member
        root = dsu.find(c)
        if root not in comps:
            comps[root] = set()
            result.append(comps[root])
        comps[root].add(c)
    return result


def ring_size(records: list[str], target: str) -> int:
    for g in groups(records):
        if target in g:
            return len(g)  # includes the target itself
    return 0


def largest_ring(records: list[str]) -> int:
    return max((len(g) for g in groups(records)), default=0)


def should_block(records: list[str], target: str, k: int) -> bool:
    return ring_size(records, target) >= k  # non-strict: size == K blocks


# ---------------------------------------------------------------- Part 3
def ring_risks(records: list[str]) -> list[float]:
    rows = parse(records)
    risk: dict[str, int] = {}
    for row in rows:
        risk[row[0]] = int(row[-1])  # last record wins (chronological input)
    ident_records = [":".join(row[:-1]) for row in rows]  # risk column is not an identifier
    out = []
    for g in groups(ident_records):
        scored = [risk[c] for c in g if risk[c] != 0]  # rule: drop zero-risk members BEFORE averaging
        out.append(sum(scored) / len(scored) if scored else 0.0)
    return out


# ---------------------------------------------------------------- Part 4
def weighted_links(records: list[str], target: str, weights: dict[str, float] = DEFAULT_WEIGHTS,
                   threshold: float = 0.5) -> list[str]:
    users: dict[str, dict[str, str]] = {}
    for raw in records:
        raw = raw.strip()
        if not raw:
            continue
        vals = [v.strip() for v in raw.split(",")]
        vals += [""] * (len(FIELDS4) - len(vals))
        users[vals[0]] = {f: v.lower() for f, v in zip(FIELDS4[1:], vals[1:])}
    if target not in users:
        return []
    w_int = {f: round(w * 1000) for f, w in weights.items()}  # integer thousandths: no float drift
    need = round(threshold * 1000)
    t = users[target]
    out = []
    for uid, u in users.items():
        if uid == target:
            continue
        score = sum(w for f, w in w_int.items() if t.get(f) and t.get(f) == u.get(f))
        if score >= need:  # non-strict threshold
            out.append(uid)
    return sorted(out)


# ---------------------------------------------------------------- stdin protocol
def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    if part == 1:
        out = direct_links(lines[2:], lines[1]) or ["NONE"]
    elif part == 2:
        target, k = lines[1].split()
        out = [f"{ring_size(lines[2:], target)} {'BLOCK' if should_block(lines[2:], target, int(k)) else 'ALLOW'}"]
    elif part == 3:
        rings = groups([":".join(r[:-1]) for r in parse(lines[1:])])
        out = [f"{','.join(sorted(g))} {risk:.2f}" for g, risk in zip(rings, ring_risks(lines[1:]))]
    elif part == 4:
        target, thr = lines[1].split()
        out = weighted_links(lines[2:], target, threshold=float(thr)) or ["NONE"]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
