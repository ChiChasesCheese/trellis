"""ps10 RBAC Role Resolver — reference solution.

RECONSTRUCTED problem (see problem.md's warning block) — Stripe-style account hierarchy
(platform -> connected account -> ... -> user) where a user's *effective* permission at some
account is resolved by walking that account's ancestor chain and combining every role the user
holds along the way. Each part deliberately breaks the previous part's data structure or flips the
direction of the query:

  Part 1 - flat lookup, no hierarchy at all (a linear scan is fine).
  Part 2 - hierarchy is introduced: a flat scan can no longer answer "does this user have any
            role *anywhere in the chain*" -- needs an indexed graph walk, with cycle protection.
  Part 3 - the query direction reverses: "account + permission -> users" instead of "user +
            account -> permissions". Reusing Part 2 once per user is O(U x D); a reverse index
            (assignments grouped by account_id) answers it in O(D + matches) instead.
  Part 4 - the query direction reverses again ("role -> users"), but this time there is no
            hierarchy to walk at all -- a role's identity is direct-only (see problem.md). A
            role-keyed reverse index over `assignments`, built once, answers every query in O(1).
"""

from __future__ import annotations

import sys


# ------------------------------------------------------------------ Part 1: flat, no hierarchy
def part1(
    accounts: list[dict], roles: list[dict], assignments: list[dict], user_id: str, account_id: str
) -> list[str]:
    """Happy path, no hierarchy: the permissions of the role (if any) the user is DIRECTLY
    assigned at account_id itself. No inheritance, no validation -- assume well-formed input."""
    roles_by_id = {r["role_id"]: r for r in roles}
    for a in assignments:
        if a["user_id"] == user_id and a["account_id"] == account_id:
            return sorted(roles_by_id[a["role_id"]]["permissions"])
    return []


# ------------------------------------------------------------------ shared indexing (Part 2+)
def _index(accounts: list[dict], roles: list[dict], assignments: list[dict]):
    """Build every lookup structure Parts 2-4 need, and validate structural integrity, in one
    pass over the input. Raises ValueError on: a duplicate account_id or role_id, an assignment
    referencing an unknown account or role, or two assignments for the same (user_id, account_id)
    pair (ambiguous -- which role applies?).

    Returns (accounts_by_id, roles_by_id, assignment_by_user_account, assignments_by_account,
    assignments_by_role):
      - assignment_by_user_account: (user_id, account_id) -> role_id -- Part 2/3's per-user,
        per-level lookup while walking an ancestor chain.
      - assignments_by_account: account_id -> list of (user_id, role_id) assigned there -- Part
        3's reverse index: "who is assigned anything at this one account level", so a chain walk
        only ever touches the accounts actually on the chain, never every user in the system.
      - assignments_by_role: role_id -> set of user_id directly holding it anywhere -- Part 4's
        reverse index, built once and reused for O(1) lookups.
    """
    accounts_by_id: dict[str, dict] = {}
    for acc in accounts:
        aid = acc["account_id"]
        if aid in accounts_by_id:
            raise ValueError(f"duplicate account_id: {aid!r}")
        accounts_by_id[aid] = acc

    roles_by_id: dict[str, dict] = {}
    for role in roles:
        rid = role["role_id"]
        if rid in roles_by_id:
            raise ValueError(f"duplicate role_id: {rid!r}")
        roles_by_id[rid] = role

    assignment_by_user_account: dict[tuple[str, str], str] = {}
    assignments_by_account: dict[str, list[tuple[str, str]]] = {}
    assignments_by_role: dict[str, set[str]] = {}
    for a in assignments:
        key = (a["user_id"], a["account_id"])
        if key in assignment_by_user_account:
            raise ValueError(f"duplicate assignment for user {a['user_id']!r} at account {a['account_id']!r}")
        if a["account_id"] not in accounts_by_id:
            raise ValueError(f"assignment references unknown account: {a['account_id']!r}")
        if a["role_id"] not in roles_by_id:
            raise ValueError(f"assignment references unknown role: {a['role_id']!r}")
        assignment_by_user_account[key] = a["role_id"]
        assignments_by_account.setdefault(a["account_id"], []).append((a["user_id"], a["role_id"]))
        assignments_by_role.setdefault(a["role_id"], set()).add(a["user_id"])

    return (
        accounts_by_id,
        roles_by_id,
        assignment_by_user_account,
        assignments_by_account,
        assignments_by_role,
    )


def _ancestor_chain(
    accounts_by_id: dict[str, dict], account_id: str, cache: dict[str, list[str]]
) -> list[str]:
    """Root-first list of account ids from the topmost ancestor down to account_id (inclusive).
    Memoized in `cache` (shared across a whole batch, fresh per call otherwise), so an account
    whose chain was already resolved is O(1) on every later lookup. Raises ValueError on an
    unknown account_id anywhere in the chain, or a parent_id cycle (including a self-referencing
    account_id == parent_id)."""
    if account_id in cache:
        return cache[account_id]
    path: list[str] = []
    visiting: set[str] = set()
    current: str | None = account_id
    while current not in cache:
        if current in visiting:
            raise ValueError(f"cycle detected in account hierarchy at {current!r}")
        if current not in accounts_by_id:
            raise ValueError(f"unknown account: {current!r}")
        visiting.add(current)
        path.append(current)
        parent = accounts_by_id[current].get("parent_id")
        if not parent:
            current = None
            break
        current = parent
    path.reverse()  # was leaf -> ... -> topmost; now topmost -> ... -> leaf
    prefix = cache[current] if current is not None else []
    full = prefix + path
    cache[account_id] = full
    return full


def _effective_permissions(
    accounts_by_id: dict[str, dict],
    roles_by_id: dict[str, dict],
    assignment_by_user_account: dict[tuple[str, str], str],
    chain_cache: dict[str, list[str]],
    user_id: str,
    account_id: str,
) -> set[str]:
    """Union of literal permissions from every role the user holds anywhere along account_id's
    ancestor chain (their own assignments only -- another user's role never contributes). A level
    where the user has no assignment simply contributes nothing."""
    chain = _ancestor_chain(accounts_by_id, account_id, chain_cache)
    perms: set[str] = set()
    for level in chain:
        role_id = assignment_by_user_account.get((user_id, level))
        if role_id is not None:
            perms.update(roles_by_id[role_id]["permissions"])
    return perms


# ------------------------------------------------------------------ Part 2: hierarchy (union)
def part2(
    accounts: list[dict], roles: list[dict], assignments: list[dict], user_id: str, account_id: str
) -> list[str]:
    """Effective permissions at account_id, inheriting (union, not override) every role the user
    holds at any ancestor level, root down to account_id itself."""
    accounts_by_id, roles_by_id, assignment_by_user_account, _by_acct, _by_role = _index(
        accounts, roles, assignments
    )
    perms = _effective_permissions(
        accounts_by_id, roles_by_id, assignment_by_user_account, {}, user_id, account_id
    )
    return sorted(perms)


# ------------------------------------------------------------------ Part 3: reverse -- permission -> users
def part3(
    accounts: list[dict], roles: list[dict], assignments: list[dict], account_id: str, permission: str
) -> list[str]:
    """Every user_id who effectively has `permission` at account_id (their own direct role there,
    or a role inherited from their own assignment at any ancestor -- Part 2's rule, run in
    reverse). Walks account_id's ancestor chain once (O(D)); at each level, looks up ONLY the
    assignments recorded at that one account (assignments_by_account), never every user in the
    system -- see problem.md's "why the obvious approach doesn't scale"."""
    accounts_by_id, roles_by_id, _by_pair, assignments_by_account, _by_role = _index(
        accounts, roles, assignments
    )
    chain = _ancestor_chain(accounts_by_id, account_id, {})
    holders: set[str] = set()
    for level in chain:
        for user_id, role_id in assignments_by_account.get(level, ()):
            if permission in roles_by_id[role_id]["permissions"]:
                holders.add(user_id)
    return sorted(holders)


# ------------------------------------------------------------------ Part 4: reverse -- role -> users
def part4(accounts: list[dict], roles: list[dict], assignments: list[dict], role_id: str) -> list[str]:
    """Every user_id directly assigned role_id, at any account (see problem.md for why
    direct-only is not just simpler but provably the same set as "counting inheritance" would
    be). O(1) after _index's one-time O(assignments) build of assignments_by_role."""
    _by_id, roles_by_id, _by_pair, _by_acct, assignments_by_role = _index(accounts, roles, assignments)
    if role_id not in roles_by_id:
        raise ValueError(f"unknown role: {role_id!r}")
    return sorted(assignments_by_role.get(role_id, ()))


# ------------------------------------------------------------------ I/O
SECTION_NAMES = ("ACCOUNTS", "ROLES", "ASSIGNMENTS", "QUERY")


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {name: [] for name in SECTION_NAMES}
    current: str | None = None
    for raw in lines:
        if raw.strip() in SECTION_NAMES:
            current = raw.strip()
            continue
        if current is not None:
            sections[current].append(raw)
    return sections


def _drop_header(lines: list[str]) -> list[str]:
    """Every section's own field-header row (e.g. 'account_id,parent_id') is always present and
    always skipped -- see problem.md Input."""
    return lines[1:] if lines else []


def _parse_accounts(lines: list[str]) -> list[dict]:
    out = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        account_id, parent_id = (p.strip() for p in raw.split(","))
        out.append({"account_id": account_id, "parent_id": parent_id or None})
    return out


def _parse_roles(lines: list[str]) -> list[dict]:
    out = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        role_id, perms = raw.split(",", 1)
        permissions = [p.strip() for p in perms.split(";") if p.strip()]
        out.append({"role_id": role_id.strip(), "permissions": permissions})
    return out


def _parse_assignments(lines: list[str]) -> list[dict]:
    out = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        user_id, account_id, role_id = (p.strip() for p in raw.split(","))
        out.append({"user_id": user_id, "account_id": account_id, "role_id": role_id})
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """Stdin protocol (see problem.md Input for the full spec):
        PART <n>
        ACCOUNTS
        account_id,parent_id
        ...
        ROLES
        role_id,permissions          <- ';'-joined literal permission strings
        ...
        ASSIGNMENTS
        user_id,account_id,role_id
        ...
        QUERY
        <header row, ignored>
        <one query row -- shape depends on n, see below>
    Part 1/2 query row: "user_id,account_id"        -> output: sorted perms, ',' joined, or 'NONE'
    Part 3    query row: "account_id,permission"     -> output: sorted user ids, ',' joined, or 'NONE'
    Part 4    query row: "role_id"                   -> output: sorted user ids, ',' joined, or 'NONE'
    """
    lines = stdin.read().splitlines()
    if not lines:
        return
    header = lines[0].strip()
    if not header.startswith("PART "):
        raise ValueError(f"unknown header: {header!r}")
    part_num = int(header.split()[1])

    sections = _split_sections(lines[1:])
    accounts = _parse_accounts(_drop_header(sections["ACCOUNTS"]))
    roles = _parse_roles(_drop_header(sections["ROLES"]))
    assignments = _parse_assignments(_drop_header(sections["ASSIGNMENTS"]))
    query_lines = [ln.strip() for ln in _drop_header(sections["QUERY"]) if ln.strip()]

    if part_num in (1, 2):
        user_id, account_id = (p.strip() for p in query_lines[0].split(","))
        fn = part1 if part_num == 1 else part2
        perms = fn(accounts, roles, assignments, user_id, account_id)
        stdout.write((",".join(perms) if perms else "NONE") + "\n")
    elif part_num == 3:
        account_id, permission = (p.strip() for p in query_lines[0].split(","))
        result = part3(accounts, roles, assignments, account_id, permission)
        stdout.write((",".join(result) if result else "NONE") + "\n")
    elif part_num == 4:
        role_id = query_lines[0].strip()
        result = part4(accounts, roles, assignments, role_id)
        stdout.write((",".join(result) if result else "NONE") + "\n")
    else:
        raise ValueError(f"unknown header: {header!r}")


if __name__ == "__main__":
    main()
