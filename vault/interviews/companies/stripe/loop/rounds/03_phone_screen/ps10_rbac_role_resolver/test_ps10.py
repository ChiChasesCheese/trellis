import pytest

ACCOUNTS = [
    {"account_id": "platform", "parent_id": None},
    {"account_id": "connected", "parent_id": "platform"},
    {"account_id": "submerchant", "parent_id": "connected"},
]

ROLES = [
    {"role_id": "viewer", "permissions": ["payouts:read", "charges:read"]},  # deliberately unsorted
    {"role_id": "admin", "permissions": ["charges:read", "charges:write", "payouts:read", "payouts:write"]},
]

ASSIGNMENTS = [
    {"user_id": "alice", "account_id": "platform", "role_id": "viewer"},
    {"user_id": "alice", "account_id": "connected", "role_id": "admin"},
    {"user_id": "bob", "account_id": "submerchant", "role_id": "viewer"},
]

ADMIN_PERMS = ["charges:read", "charges:write", "payouts:read", "payouts:write"]
VIEWER_PERMS = ["charges:read", "payouts:read"]

# Part 3/4 shared extension: adds a "manager" role and carol, holding it at the topmost account,
# to exercise inheritance reaching two levels down (see problem.md worked examples).
ROLES_34 = ROLES + [{"role_id": "manager", "permissions": ["charges:read", "charges:write"]}]
ASSIGNMENTS_34 = ASSIGNMENTS + [{"user_id": "carol", "account_id": "platform", "role_id": "manager"}]


def _accounts_lines(accounts):
    return ["ACCOUNTS", "account_id,parent_id"] + [
        f"{a['account_id']},{a['parent_id'] or ''}" for a in accounts
    ]


def _roles_lines(roles):
    return ["ROLES", "role_id,permissions"] + [f"{r['role_id']},{';'.join(r['permissions'])}" for r in roles]


def _assignments_lines(assignments):
    return ["ASSIGNMENTS", "user_id,account_id,role_id"] + [
        f"{a['user_id']},{a['account_id']},{a['role_id']}" for a in assignments
    ]


def _stdin(part, accounts, roles, assignments, query_header, query_lines):
    lines = [f"PART {part}"]
    lines += _accounts_lines(accounts)
    lines += _roles_lines(roles)
    lines += _assignments_lines(assignments)
    lines += ["QUERY", query_header] + query_lines
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- Part 1: flat, no hierarchy
@pytest.mark.part1
def test_direct_role_at_own_account(impl):
    assert impl.part1(ACCOUNTS, ROLES, ASSIGNMENTS, "alice", "connected") == ADMIN_PERMS


@pytest.mark.part1
def test_no_inheritance_from_ancestor(impl):
    # alice's role is at platform/connected, not at submerchant itself -- Part 1 has no inheritance
    assert impl.part1(ACCOUNTS, ROLES, ASSIGNMENTS, "alice", "submerchant") == []


@pytest.mark.part1
def test_no_role_anywhere_returns_empty(impl):
    assert impl.part1(ACCOUNTS, ROLES, ASSIGNMENTS, "zoe", "platform") == []


@pytest.mark.part1
@pytest.mark.fmt
def test_permissions_are_sorted_even_though_role_lists_them_unsorted(impl):
    # ROLES['viewer'] lists payouts:read before charges:read
    assert impl.part1(ACCOUNTS, ROLES, ASSIGNMENTS, "alice", "platform") == VIEWER_PERMS


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin_text = _stdin(1, ACCOUNTS, ROLES, ASSIGNMENTS, "user_id,account_id", ["alice,connected"])
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == ",".join(ADMIN_PERMS) + "\n"


# ---------------------------------------------------------------- Part 2: hierarchy (union, no wildcards)
@pytest.mark.part2
def test_inherits_union_of_ancestor_permissions(impl):
    # alice: viewer@platform + admin@connected, nothing at submerchant itself -> union of both
    assert impl.part2(ACCOUNTS, ROLES, ASSIGNMENTS, "alice", "submerchant") == ADMIN_PERMS


@pytest.mark.part2
def test_own_level_role_with_no_ancestors_assigned(impl):
    assert impl.part2(ACCOUNTS, ROLES, ASSIGNMENTS, "bob", "submerchant") == VIEWER_PERMS


@pytest.mark.part2
def test_no_role_anywhere_in_chain_returns_empty(impl):
    assert impl.part2(ACCOUNTS, ROLES, ASSIGNMENTS, "zoe", "submerchant") == []


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_account_id_raises(impl):
    with pytest.raises(ValueError):
        impl.part2(ACCOUNTS, ROLES, ASSIGNMENTS, "alice", "does-not-exist")


@pytest.mark.part2
@pytest.mark.edge
def test_duplicate_assignment_same_user_account_raises(impl):
    bad = ASSIGNMENTS + [{"user_id": "alice", "account_id": "platform", "role_id": "admin"}]
    with pytest.raises(ValueError):
        impl.part2(ACCOUNTS, ROLES, bad, "alice", "platform")


@pytest.mark.part2
@pytest.mark.edge
def test_two_node_cycle_raises(impl):
    cyclic = [{"account_id": "x", "parent_id": "y"}, {"account_id": "y", "parent_id": "x"}]
    with pytest.raises(ValueError):
        impl.part2(cyclic, ROLES, [], "anyone", "x")


@pytest.mark.part2
@pytest.mark.edge
def test_self_parent_cycle_raises(impl):
    cyclic = [{"account_id": "x", "parent_id": "x"}]
    with pytest.raises(ValueError):
        impl.part2(cyclic, ROLES, [], "anyone", "x")


@pytest.mark.part2
@pytest.mark.fmt
def test_union_deduplicates_permission_appearing_at_two_levels(impl):
    accounts = [{"account_id": "p", "parent_id": None}, {"account_id": "c", "parent_id": "p"}]
    roles = [
        {"role_id": "r1", "permissions": ["charges:read"]},
        {"role_id": "r2", "permissions": ["charges:read"]},
    ]
    assignments = [
        {"user_id": "u", "account_id": "p", "role_id": "r1"},
        {"user_id": "u", "account_id": "c", "role_id": "r2"},
    ]
    assert impl.part2(accounts, roles, assignments, "u", "c") == ["charges:read"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin_text = _stdin(2, ACCOUNTS, ROLES, ASSIGNMENTS, "user_id,account_id", ["alice,submerchant"])
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == ",".join(ADMIN_PERMS) + "\n"


# ---------------------------------------------------------------- Part 3: reverse -- permission -> users
@pytest.mark.part3
def test_direct_and_inherited_holders_at_a_middle_level(impl):
    # at "connected": alice has admin directly; carol's platform-level manager role reaches down
    # one level; bob's only assignment is at submerchant, a DESCENDANT of connected, not an
    # ancestor -- he must not appear here at all.
    assert impl.part3(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "connected", "charges:read") == ["alice", "carol"]


@pytest.mark.part3
def test_same_permission_one_level_lower_adds_the_local_holder(impl):
    # at "submerchant": same permission now also picks up bob's own direct role there, and
    # carol's platform-level role now reaches two levels down instead of one.
    assert impl.part3(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "submerchant", "charges:read") == [
        "alice",
        "bob",
        "carol",
    ]


@pytest.mark.part3
def test_permission_only_one_role_grants(impl):
    # payouts:write is only in admin -- only alice's chain includes admin
    assert impl.part3(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "submerchant", "payouts:write") == ["alice"]


@pytest.mark.part3
@pytest.mark.edge
def test_permission_nobody_grants_returns_empty_not_error(impl):
    assert impl.part3(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "submerchant", "invoices:void") == []


@pytest.mark.part3
@pytest.mark.edge
def test_sibling_branch_assignment_never_counted(impl):
    # "other" is a sibling of "connected" (both children of platform), not an ancestor of
    # "submerchant" -- dave's role there must never leak into a submerchant query even though it
    # grants the same permission.
    accounts = ACCOUNTS + [{"account_id": "other", "parent_id": "platform"}]
    assignments = ASSIGNMENTS_34 + [{"user_id": "dave", "account_id": "other", "role_id": "admin"}]
    assert impl.part3(accounts, ROLES_34, assignments, "submerchant", "charges:read") == [
        "alice",
        "bob",
        "carol",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_unknown_query_account_raises(impl):
    with pytest.raises(ValueError):
        impl.part3(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "does-not-exist", "charges:read")


@pytest.mark.part3
@pytest.mark.edge
def test_cycle_in_chain_still_raises_in_part3(impl):
    cyclic = [{"account_id": "x", "parent_id": "y"}, {"account_id": "y", "parent_id": "x"}]
    with pytest.raises(ValueError):
        impl.part3(cyclic, ROLES_34, [], "x", "charges:read")


@pytest.mark.part3
@pytest.mark.fmt
def test_holder_ids_sorted_as_plain_strings(impl):
    accounts = [{"account_id": "root", "parent_id": None}]
    roles = [{"role_id": "r", "permissions": ["x:read"]}]
    assignments = [
        {"user_id": "zack", "account_id": "root", "role_id": "r"},
        {"user_id": "amy", "account_id": "root", "role_id": "r"},
        {"user_id": "mo", "account_id": "root", "role_id": "r"},
    ]
    assert impl.part3(accounts, roles, assignments, "root", "x:read") == ["amy", "mo", "zack"]


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    stdin_text = _stdin(
        3, ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "account_id,permission", ["connected,charges:read"]
    )
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "alice,carol\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_reverse_query_ignores_unrelated_users(run_script):
    # A deep chain (depth D) is the query target; a separate, much larger population of users
    # (N) is scattered on an UNRELATED branch of the tree. A naive "check every user" answer to
    # part3 costs O(N x D); a reverse index keyed by account only ever touches the D accounts on
    # the queried chain (and whatever handful of assignments actually sit on it) -- this input is
    # sized so the former would blow the time budget and the latter comfortably will not.
    depth = 3000
    n_scattered_users = 10_000
    n_target_holders = 5

    accounts = [{"account_id": "chain0", "parent_id": ""}]
    for i in range(1, depth):
        accounts.append({"account_id": f"chain{i}", "parent_id": f"chain{i - 1}"})
    leaf = f"chain{depth - 1}"
    target_level = f"chain{depth // 2}"

    accounts.append({"account_id": "side_root", "parent_id": ""})
    for i in range(n_scattered_users):
        accounts.append({"account_id": f"leaf{i}", "parent_id": "side_root"})

    roles = [
        {"role_id": "target_role", "permissions": ["target:perm"]},
        {"role_id": "noise_role", "permissions": ["noise:perm"]},
    ]
    assignments = [
        {"user_id": f"scattered{i}", "account_id": f"leaf{i}", "role_id": "noise_role"}
        for i in range(n_scattered_users)
    ]
    assignments += [
        {"user_id": f"holder{i}", "account_id": target_level, "role_id": "target_role"}
        for i in range(n_target_holders)
    ]

    stdin_text = _stdin(3, accounts, roles, assignments, "account_id,permission", [f"{leaf},target:perm"])
    r = run_script(stdin_text, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().split(",") == sorted(f"holder{i}" for i in range(n_target_holders))
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"


# ---------------------------------------------------------------- Part 4: reverse -- role -> users
@pytest.mark.part4
def test_role_held_by_two_different_users_at_two_accounts(impl):
    assert impl.part4(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "viewer") == ["alice", "bob"]


@pytest.mark.part4
def test_role_held_by_a_single_user_unaffected_by_their_other_roles(impl):
    # alice also holds "viewer" elsewhere -- that must not remove or duplicate her under "admin"
    assert impl.part4(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "admin") == ["alice"]


@pytest.mark.part4
def test_identical_permissions_different_role_id_not_conflated(impl):
    # clone_of_manager grants the exact same permissions as manager, but is a different role_id --
    # dave must not appear under "manager", and carol must not appear under "clone_of_manager".
    roles = ROLES_34 + [{"role_id": "clone_of_manager", "permissions": ["charges:read", "charges:write"]}]
    assignments = ASSIGNMENTS_34 + [
        {"user_id": "dave", "account_id": "platform", "role_id": "clone_of_manager"}
    ]
    assert impl.part4(ACCOUNTS, roles, assignments, "manager") == ["carol"]
    assert impl.part4(ACCOUNTS, roles, assignments, "clone_of_manager") == ["dave"]


@pytest.mark.part4
@pytest.mark.edge
def test_valid_role_nobody_holds_returns_empty(impl):
    roles = ROLES_34 + [{"role_id": "billing", "permissions": ["invoices:read"]}]
    assert impl.part4(ACCOUNTS, roles, ASSIGNMENTS_34, "billing") == []


@pytest.mark.part4
@pytest.mark.edge
def test_unknown_role_id_raises(impl):
    with pytest.raises(ValueError):
        impl.part4(ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "does-not-exist")


@pytest.mark.part4
@pytest.mark.edge
def test_same_role_at_two_accounts_listed_once(impl):
    accounts = [
        {"account_id": "a", "parent_id": None},
        {"account_id": "b", "parent_id": None},
    ]
    roles = [{"role_id": "r", "permissions": ["x:read"]}]
    assignments = [
        {"user_id": "u", "account_id": "a", "role_id": "r"},
        {"user_id": "u", "account_id": "b", "role_id": "r"},
    ]
    assert impl.part4(accounts, roles, assignments, "r") == ["u"]


@pytest.mark.part4
@pytest.mark.fmt
def test_role_holder_ids_sorted_as_plain_strings(impl):
    accounts = [{"account_id": "root", "parent_id": None}]
    roles = [{"role_id": "r", "permissions": ["x:read"]}]
    assignments = [
        {"user_id": "u10", "account_id": "root", "role_id": "r"},
        {"user_id": "u2", "account_id": "root", "role_id": "r"},
    ]
    # plain string order: "u10" < "u2"
    assert impl.part4(accounts, roles, assignments, "r") == ["u10", "u2"]


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    stdin_text = _stdin(4, ACCOUNTS, ROLES_34, ASSIGNMENTS_34, "role_id", ["viewer"])
    r = run_script(stdin_text)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "alice,bob\n"
