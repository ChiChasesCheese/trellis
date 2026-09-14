"""pc01 RBAC / DAG Permissions -- reference solution.

Four parts, all sharing one DP-over-a-DAG core (`_toposort` + `_dp_union`):

1. `get_effective_privileges` -- plain inheritance: value(v) = own(v) union value(p) for every
   direct parent p, folded in topological order (parents before children, so a node's DP value
   is fully settled before any child reads it).
2. `get_effective_access` -- same DP run twice (once over allow lists, once over deny lists);
   deny is inherited from every ancestor exactly like allow, and wins on conflict.
3. `get_effective_access_local_deny` -- allow is still inherited the same way, but deny is
   NOT propagated: only a node's own deny list can remove one of ITS privileges.
4. Reverse queries over a role DAG + a flat (user, role) assignment table: which users hold a
   privilege (via their assigned role's effective privileges), and which users are assigned a
   given role directly (no hierarchy walk -- this one is a plain filter).

All four validate node/role indices and reject cycles with a documented `ValueError` -- callers
must not assume a broken input silently degrades to empty results.
"""

from __future__ import annotations

import sys
from collections import deque


def _toposort(n: int, edges: list[list[int]]) -> tuple[list[int], list[list[int]]]:
    """Kahn's algorithm over `edges` = [ancestor, descendant] pairs on n nodes [0, n).

    Returns (topo_order, children) where children[a] lists a's direct descendants, in the
    order edges were given. Raises ValueError if an edge references a node outside [0, n), or
    if the edges do not form a DAG (a cycle exists) -- both are documented, non-silent failures.
    """
    children: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for a, d in edges:
        if not (0 <= a < n) or not (0 <= d < n):
            raise ValueError(f"edge ({a}, {d}) references a node outside [0, {n})")
        children[a].append(d)
        indeg[d] += 1
    order: list[int] = []
    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        u = q.popleft()
        order.append(u)
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != n:
        raise ValueError("cycle detected in role/permission DAG")
    return order, children


def _parents_from_children(n: int, children: list[list[int]]) -> list[list[int]]:
    parents: list[list[int]] = [[] for _ in range(n)]
    for a in range(n):
        for d in children[a]:
            parents[d].append(a)
    return parents


def _dp_union(
    n: int, order: list[int], parents: list[list[int]], own: list[list[str]]
) -> list[set[str]]:
    """value(v) = own(v) unioned with value(p) for every direct parent p. `order` must be a
    topological order (parents before children) so each value(p) is final when a child reads
    it -- correct for multi-parent DAGs because value(p) already includes p's own ancestors."""
    value: list[set[str]] = [set() for _ in range(n)]
    for u in order:
        value[u].update(own[u])
        for p in parents[u]:
            value[u].update(value[p])
    return value


# --------------------------------------------------------------------------- Part 1
def get_effective_privileges(
    privileges: list[list[str]], grants: list[list[int]]
) -> list[list[str]]:
    """Effective privileges of every role = its own privileges plus every ancestor's (over the
    grants DAG, `grants[i] = [ancestor_role, descendant_role]`)."""
    n = len(privileges)
    order, children = _toposort(n, grants)
    parents = _parents_from_children(n, children)
    value = _dp_union(n, order, parents, privileges)
    return [sorted(v) for v in value]


# --------------------------------------------------------------------------- Part 2
def get_effective_access(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]:
    """Deny-overrides-allow, both inherited from every ancestor. `edges[i] = [ancestor, child]`."""
    n = len(allow_lists)
    order, children = _toposort(n, edges)
    parents = _parents_from_children(n, children)
    allowset = _dp_union(n, order, parents, allow_lists)
    denyset = _dp_union(n, order, parents, deny_lists)
    return [sorted(allowset[i] - denyset[i]) for i in range(n)]


# --------------------------------------------------------------------------- Part 3
def get_effective_access_local_deny(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]:
    """Same inherited allow as Part 2, but deny is LOCAL ONLY: a node's own deny list can only
    remove one of its own (possibly inherited) privileges -- it never blocks a descendant."""
    n = len(allow_lists)
    order, children = _toposort(n, edges)
    parents = _parents_from_children(n, children)
    allowset = _dp_union(n, order, parents, allow_lists)
    return [sorted(allowset[i] - set(deny_lists[i])) for i in range(n)]


# --------------------------------------------------------------------------- Part 4
def users_with_privilege(
    effective_privileges: list[list[str]], assignments: list[tuple[str, int]], privilege: str
) -> list[str]:
    """Users who hold `privilege` through ANY role assigned to them. `role_id` is a declared
    index into `effective_privileges` -- an assignment referencing an out-of-range role_id is a
    data error and raises, matching Parts 1-3's error discipline."""
    n = len(effective_privileges)
    holders: set[str] = set()
    for user_id, role_id in assignments:
        if not (0 <= role_id < n):
            raise ValueError(f"assignment references unknown role_id {role_id}")
        if privilege in effective_privileges[role_id]:
            holders.add(user_id)
    return sorted(holders)


def filter_users_by_role(assignments: list[tuple[str, int]], role_id: int) -> list[str]:
    """Users DIRECTLY assigned `role_id` -- a plain filter over the assignment table, no
    hierarchy walk. Unlike `users_with_privilege`, an unrecognised role_id is not an error here:
    role_id is a free-form filter key (there is no separate "role catalog" argument to check
    against), so it simply yields no matches."""
    return sorted({user_id for user_id, r in assignments if r == role_id})


# --------------------------------------------------------------------------- line-driven wrappers
def _parse_str_list(token: str) -> list[str]:
    return [] if token == "-" else token.split(",")


def _fmt_str_list(items: list[str]) -> str:
    return ",".join(items) if items else "-"


def _read_edges(lines: list[str], idx: int) -> tuple[list[list[int]], int]:
    e = int(lines[idx])
    idx += 1
    edges = []
    for _ in range(e):
        a, d = lines[idx].split()
        edges.append([int(a), int(d)])
        idx += 1
    return edges, idx


def part1(lines: list[str]) -> list[str]:
    """n / n own-privilege lines ("-" or comma-separated) / e / e "ancestor descendant" lines."""
    idx = 0
    n = int(lines[idx])
    idx += 1
    privileges = []
    for _ in range(n):
        privileges.append(_parse_str_list(lines[idx]))
        idx += 1
    grants, idx = _read_edges(lines, idx)
    result = get_effective_privileges(privileges, grants)
    return [_fmt_str_list(r) for r in result]


def _read_access_block(lines: list[str], idx: int):
    n = int(lines[idx])
    idx += 1
    allow = []
    for _ in range(n):
        allow.append(_parse_str_list(lines[idx]))
        idx += 1
    deny = []
    for _ in range(n):
        deny.append(_parse_str_list(lines[idx]))
        idx += 1
    edges, idx = _read_edges(lines, idx)
    return allow, deny, edges, idx


def part2(lines: list[str]) -> list[str]:
    """n / n allow lines / n deny lines / e / e "ancestor descendant" lines."""
    allow, deny, edges, _ = _read_access_block(lines, 0)
    result = get_effective_access(allow, deny, edges)
    return [_fmt_str_list(r) for r in result]


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2, local-only deny semantics."""
    allow, deny, edges, _ = _read_access_block(lines, 0)
    result = get_effective_access_local_deny(allow, deny, edges)
    return [_fmt_str_list(r) for r in result]


def part4(lines: list[str]) -> list[str]:
    """n / n own-privilege lines / e / e grant edges / m / m "user role_id" lines / q /
    q query lines ("PRIV <privilege>" or "ROLE <role_id>")."""
    idx = 0
    n = int(lines[idx])
    idx += 1
    privileges = []
    for _ in range(n):
        privileges.append(_parse_str_list(lines[idx]))
        idx += 1
    grants, idx = _read_edges(lines, idx)
    effective = get_effective_privileges(privileges, grants)

    m = int(lines[idx])
    idx += 1
    assignments = []
    for _ in range(m):
        user_id, role_id = lines[idx].split()
        assignments.append((user_id, int(role_id)))
        idx += 1

    q = int(lines[idx])
    idx += 1
    out = []
    for _ in range(q):
        query = lines[idx]
        idx += 1
        kind, arg = query.split(" ", 1)
        if kind == "PRIV":
            out.append(_fmt_str_list(users_with_privilege(effective, assignments, arg)))
        elif kind == "ROLE":
            out.append(_fmt_str_list(filter_users_by_role(assignments, int(arg))))
        else:
            raise ValueError(f"unknown query kind {kind!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
