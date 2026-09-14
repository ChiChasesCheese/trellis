"""pc01 RBAC / DAG Permissions -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: plain DAG inheritance (Part1), deny-overrides-allow both
inherited from every ancestor (Part2), local-only deny (Part3), and reverse queries over a flat
(user, role) assignment table (Part4). Cycles and out-of-range node/role indices must raise
ValueError -- do not let them silently produce wrong-but-plausible output.
"""

from __future__ import annotations

import sys


def get_effective_privileges(
    privileges: list[list[str]], grants: list[list[int]]
) -> list[list[str]]:
    """Effective privileges of every role = its own privileges plus every ancestor's, over the
    grants DAG (`grants[i] = [ancestor_role, descendant_role]`). Sorted per role. Raise
    ValueError on an out-of-range node index or a cycle."""
    # TODO
    return []


def get_effective_access(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]:
    """Deny-overrides-allow, both inherited from every ancestor. `edges[i] = [ancestor, child]`."""
    # TODO
    return []


def get_effective_access_local_deny(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]:
    """Same inherited allow as Part2, but deny is LOCAL ONLY: a node's own deny list only
    removes one of its own privileges -- it never blocks a descendant."""
    # TODO
    return []


def users_with_privilege(
    effective_privileges: list[list[str]], assignments: list[tuple[str, int]], privilege: str
) -> list[str]:
    """Users who hold `privilege` through ANY role assigned to them (sorted, deduplicated).
    Raise ValueError if an assignment references a role_id outside range(len(effective_privileges))."""
    # TODO
    return []


def filter_users_by_role(assignments: list[tuple[str, int]], role_id: int) -> list[str]:
    """Users DIRECTLY assigned role_id -- a plain filter, no hierarchy walk. Unknown role_id is
    not an error: it simply yields no matches."""
    # TODO
    return []


def _parse_str_list(token: str) -> list[str]:
    return [] if token == "-" else token.split(",")


def _fmt_str_list(items: list[str]) -> str:
    return ",".join(items) if items else "-"


def part1(lines: list[str]) -> list[str]:
    """n / n own-privilege lines ("-" or comma-separated) / e / e "ancestor descendant" lines."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """n / n allow lines / n deny lines / e / e "ancestor descendant" lines."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2, local-only deny semantics."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """n / n own-privilege lines / e / e grant edges / m / m "user role_id" lines / q /
    q query lines ("PRIV <privilege>" or "ROLE <role_id>")."""
    # TODO
    return []


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
