"""ps09 Matching Contacts — reference solution.

Records ``{id, name, email, company}``. Two records are *linked* (undirected) when the sum of the
weights of the fields where they are exactly, non-emptily equal is >= ``threshold``. Part 1
returns direct (1-hop) links, Part 2 returns everything within 2 hops (direct links, plus their
direct links), Part 3 returns the full connected component (any number of hops). All three share
one adjacency-building step (``_adjacency``); only the traversal depth differs.
"""

from __future__ import annotations

import sys
from collections import defaultdict, deque
from itertools import combinations


def _validate(rows: list[dict]) -> dict[str, dict]:
    """id -> row, raising on a duplicate id (ambiguous which row 'wins')."""
    by_id: dict[str, dict] = {}
    for row in rows:
        rid = row["id"]
        if rid in by_id:
            raise ValueError(f"duplicate record id: {rid!r}")
        by_id[rid] = row
    return by_id


def _require_target(by_id: dict[str, dict], target_user_id: str) -> None:
    if target_user_id not in by_id:
        raise ValueError(f"unknown target_user_id: {target_user_id!r}")


def _score(a: dict, b: dict, weights: dict[str, float]) -> float:
    """Sum weights[field] for every field where both values are non-empty and exactly equal.

    An empty field never contributes, even when both sides are empty — "no data" is not a match.
    """
    total = 0.0
    for field, weight in weights.items():
        va, vb = a.get(field, ""), b.get(field, "")
        if va and vb and va == vb:
            total += weight
    return total


def _adjacency(by_id: dict[str, dict], weights: dict[str, float], threshold: float) -> dict[str, set[str]]:
    """Build the undirected link graph over all records.

    Candidate pairs are records that share an exact value on *any single* field (grouped per
    field); each candidate pair's full score (summed across *all* fields, not just the one that
    made it a candidate) is then computed once. This avoids an O(n^2) all-pairs scan when
    duplicate field values are sparse, while still scoring every pair correctly — a pair that
    shares two different fields is still found (via either field's group) and scored with both
    weights counted.
    """
    groups: dict[str, dict[str, list[str]]] = {field: defaultdict(list) for field in weights}
    for rid, row in by_id.items():
        for field in weights:
            value = row.get(field, "")
            if value:
                groups[field][value].append(rid)
    candidates: set[tuple[str, str]] = set()
    for field_groups in groups.values():
        for ids in field_groups.values():
            if len(ids) > 1:
                for a, b in combinations(sorted(ids), 2):
                    candidates.add((a, b))
    adj: dict[str, set[str]] = defaultdict(set)
    for a, b in candidates:
        if _score(by_id[a], by_id[b], weights) >= threshold:
            adj[a].add(b)
            adj[b].add(a)
    return adj


# ---------------------------------------------------------------- Part 1
def part1(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """Record ids directly linked (1 hop) to target_user_id, ascending, excluding the target."""
    by_id = _validate(rows)
    _require_target(by_id, target_user_id)
    adj = _adjacency(by_id, weights, threshold)
    return sorted(adj.get(target_user_id, set()))


# ---------------------------------------------------------------- Part 2
def part2(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """Record ids within <= 2 hops of target_user_id (direct links, plus links of those links),
    ascending, excluding the target itself. A record reachable at both 1 and 2 hops is listed once.
    """
    by_id = _validate(rows)
    _require_target(by_id, target_user_id)
    adj = _adjacency(by_id, weights, threshold)
    hop1 = adj.get(target_user_id, set())
    within_two: set[str] = set(hop1)
    for neighbor in hop1:
        within_two.update(adj.get(neighbor, set()))
    within_two.discard(target_user_id)
    return sorted(within_two)


# ---------------------------------------------------------------- Part 3
def part3(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """Every record id in target_user_id's connected component (any number of hops), ascending,
    excluding the target itself."""
    by_id = _validate(rows)
    _require_target(by_id, target_user_id)
    adj = _adjacency(by_id, weights, threshold)
    seen = {target_user_id}
    queue = deque([target_user_id])
    while queue:
        node = queue.popleft()
        for neighbor in adj.get(node, set()):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    seen.discard(target_user_id)
    return sorted(seen)


# ---------------------------------------------------------------- I/O
PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3}


def _parse_weights(line: str) -> dict[str, float]:
    """'name=0.2,email=0.5,company=0.3' -> {'name': 0.2, 'email': 0.5, 'company': 0.3}."""
    weights: dict[str, float] = {}
    for chunk in line.split(","):
        field, _, value = chunk.strip().partition("=")
        weights[field.strip()] = float(value)
    return weights


def _parse_rows(lines: list[str]) -> list[dict]:
    rows = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        rid, name, email, company = (p.strip() for p in raw.split(","))
        rows.append({"id": rid, "name": name, "email": email, "company": company})
    return rows


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """Stdin protocol:
        PART <n>
        <target_user_id>
        <threshold>
        <field=weight,field=weight,...>
        id,name,email,company            <- header row, always present, always skipped
        <data rows...>
    Output: one line — the matched ids joined by ',' (ascending, plain string order), or the
    literal 'NONE' when the result is empty.
    """
    lines = stdin.read().splitlines()
    if not lines:
        return
    header = lines[0].strip()
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    target = lines[1].strip()
    threshold = float(lines[2].strip())
    weights = _parse_weights(lines[3])
    rows = _parse_rows(lines[5:])  # lines[4] is the 'id,name,email,company' header, skipped
    out_ids = PARTS[header](rows, weights, threshold, target)
    stdout.write((",".join(out_ids) if out_ids else "NONE") + "\n")


if __name__ == "__main__":
    main()
