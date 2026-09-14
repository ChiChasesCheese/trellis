import random

import pytest

EX1 = [
    "2026-01-01,alice,subscribe,monthly",
    "2026-01-10,bob,subscribe,annual",
    "2026-01-01..2026-12-31",
]
EX1_OUT = [
    "2026-01-01 alice welcome",
    "2026-01-10 bob welcome",
    "2026-01-24 alice expiring",
    "2026-01-30 alice expiring",
    "2026-01-31 alice expired",
]
EX2 = [
    "2026-01-01,alice,subscribe,monthly",
    "2026-01-11,alice,change,annual",
    "2026-01-01..2026-12-31",
]
EX2_OUT = [
    "2026-01-01 alice welcome",
    "2026-09-04 alice expiring",
    "2026-09-10 alice expiring",
    "2026-09-11 alice expired",
]
EX3 = [
    "2026-02-01,bob,subscribe,monthly",
    "2026-02-20,bob,renew",
    "2026-01-01,carol,subscribe,monthly",
    "2026-02-15,carol,renew",
    "2026-01-01,dave,subscribe,monthly",
    "2026-01-15,dave,cancel",
    "2026-01-01..2026-12-31",
]
EX3_OUT = [
    "2026-01-01 carol welcome",
    "2026-01-01 dave welcome",
    "2026-01-15 dave canceled",
    "2026-01-24 carol expiring",
    "2026-01-30 carol expiring",
    "2026-01-31 carol expired",
    "2026-02-01 bob welcome",
    "2026-02-15 carol welcome",
    "2026-02-20 bob renewed",
    "2026-03-10 carol expiring",
    "2026-03-16 carol expiring",
    "2026-03-17 carol expired",
    "2026-03-26 bob expiring",
    "2026-04-01 bob expiring",
    "2026-04-02 bob expired",
]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
def test_single_monthly_subscription(impl):
    out = impl.part1(["2026-03-01,u,subscribe,monthly", "2026-01-01..2026-12-31"])
    assert out == [
        "2026-03-01 u welcome",
        "2026-03-24 u expiring",
        "2026-03-30 u expiring",
        "2026-03-31 u expired",
    ]


@pytest.mark.part1
def test_empty_input(impl):
    assert impl.part1([]) == []
    assert impl.part1(["2026-01-01..2026-12-31"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_part1_ignores_change_renew_cancel_lines(impl):
    lines = EX1[:2] + [
        "2026-01-05,alice,change,annual",
        "2026-01-05,alice,renew",
        "2026-01-05,alice,cancel",
        "2026-01-01..2026-12-31",
    ]
    assert impl.part1(lines) == EX1_OUT


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_by_date_user_then_fixed_type_priority(impl):
    # same date, two users -> string order; then within one date/user, welcome < expiring < expired
    out = impl.part1(
        ["2026-06-01,b,subscribe,monthly", "2026-06-01,a,subscribe,monthly", "2026-06-01..2026-12-31"]
    )
    assert out[0] == "2026-06-01 a welcome"
    assert out[1] == "2026-06-01 b welcome"


@pytest.mark.part1
def test_whitespace_and_blank_lines_tolerated(impl):
    a = impl.part1(["  2026-01-01 , alice , subscribe , monthly  ", "", "   ", "2026-01-01..2026-01-31"])
    b = impl.part1(["2026-01-01,alice,subscribe,monthly", "2026-01-01..2026-01-31"])
    assert a == b


@pytest.mark.part1
@pytest.mark.edge
def test_query_window_boundaries_inclusive(impl):
    lines = ["2026-01-01,u,subscribe,monthly"]  # expire 2026-01-31, expiring 01-24/01-30
    assert impl.part1(lines + ["2026-01-24..2026-01-30"]) == [
        "2026-01-24 u expiring",
        "2026-01-30 u expiring",
    ]
    assert impl.part1(lines + ["2026-01-25..2026-01-29"]) == []  # one day inside on each side: nothing left
    assert impl.part1(lines + ["2026-01-01..2026-01-01"]) == ["2026-01-01 u welcome"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2_proration(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_change_ignored_for_unknown_user(impl):
    lines = EX1[:-1] + ["2026-01-05,ghost,change,annual", EX1[-1]]
    assert impl.part2(lines) == EX1_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_change_ignored_exactly_at_expire_boundary(impl):
    lines = ["2026-01-01,u,subscribe,monthly", "2026-01-31,u,change,annual", "2026-01-01..2026-12-31"]
    assert impl.part2(lines) == [
        "2026-01-01 u welcome",
        "2026-01-24 u expiring",
        "2026-01-30 u expiring",
        "2026-01-31 u expired",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_change_same_day_as_subscribe_is_exact_no_floor_loss(impl):
    # remaining_old == period_days(old) -> remaining_new == period_days(new) exactly
    out = impl.part2(
        ["2026-01-01,u,subscribe,monthly", "2026-01-01,u,change,annual", "2026-01-01..2027-12-31"]
    )
    assert out == [
        "2026-01-01 u welcome",
        "2026-12-25 u expiring",
        "2026-12-31 u expiring",
        "2027-01-01 u expired",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_change_causing_immediate_expiry_keeps_same_day_old_emails(impl):
    # annual sub with exactly 1 day left; change to monthly floors the reprorated remainder to 0
    # -> new_expire == event date. The OLD expiring emails dated <= the event date are NOT revoked
    # (only strictly-future dates are), so the output keeps them alongside the new same-day expiry.
    lines = ["2026-01-01,u,subscribe,annual", "2026-12-31,u,change,monthly", "2026-01-01..2027-12-31"]
    assert impl.part2(lines) == [
        "2026-01-01 u welcome",
        "2026-12-25 u expiring",  # from the ORIGINAL annual schedule, untouched (dated <= event day)
        "2026-12-31 u expiring",  # also from the ORIGINAL schedule, dated == event day, untouched
        "2026-12-31 u expired",  # NEW: immediate expiry from the change (remaining floors to 0)
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_events_applied_in_date_order_not_file_order(impl):
    lines = ["2026-01-11,alice,change,annual", "2026-01-01,alice,subscribe,monthly", "2026-01-01..2026-12-31"]
    assert impl.part2(lines) == EX2_OUT


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3_renew_and_cancel(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
def test_part3_is_superset_of_part1_on_subscribe_only_input(impl):
    assert impl.part3(EX1) == EX1_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_renew_ignored_after_cancel_and_double_cancel_is_noop(impl):
    lines = [
        "2026-01-01,u,subscribe,monthly",
        "2026-01-05,u,cancel",
        "2026-01-06,u,cancel",
        "2026-01-10,u,renew",
        "2026-01-01..2026-12-31",
    ]
    assert impl.part3(lines) == ["2026-01-01 u welcome", "2026-01-05 u canceled"]


@pytest.mark.part3
@pytest.mark.edge
def test_resubscribe_while_active_wipes_pending_schedule(impl):
    lines = ["2026-01-01,u,subscribe,monthly", "2026-01-05,u,subscribe,annual", "2026-01-01..2026-12-31"]
    assert impl.part3(lines) == ["2026-01-01 u welcome", "2026-01-05 u welcome", "2026-12-29 u expiring"]


@pytest.mark.part3
@pytest.mark.edge
def test_same_day_cancel_then_resubscribe_orders_by_type_not_event_order(impl):
    lines = [
        "2026-01-01,u,subscribe,monthly",
        "2026-01-05,u,cancel",
        "2026-01-05,u,subscribe,monthly",
        "2026-01-01..2026-12-31",
    ]
    assert impl.part3(lines) == [
        "2026-01-01 u welcome",
        "2026-01-05 u welcome",  # welcome (priority 0) sorts before canceled (priority 4)
        "2026-01-05 u canceled",  # even though cancel was processed first (same-day -> not revoked)
        "2026-01-28 u expiring",
        "2026-02-03 u expiring",
        "2026-02-04 u expired",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_duplicate_subscribe_lines_are_not_deduplicated(impl):
    lines = ["2026-01-01,u,subscribe,monthly", "2026-01-01,u,subscribe,monthly", "2026-01-01..2026-12-31"]
    out = impl.part3(lines)
    assert out.count("2026-01-01 u welcome") == 2
    assert out == [
        "2026-01-01 u welcome",
        "2026-01-01 u welcome",
        "2026-01-24 u expiring",
        "2026-01-30 u expiring",
        "2026-01-31 u expired",
    ]


@pytest.mark.part3
@pytest.mark.fmt
def test_renew_before_and_after_expiry_message_types_differ(impl):
    # renew strictly before expiry -> "renewed"; on/after expiry -> treated as fresh "welcome"
    before = impl.part3(["2026-01-01,u,subscribe,monthly", "2026-01-20,u,renew", "2026-01-01..2027-12-31"])
    assert any(line.endswith("renewed") for line in before)
    after = impl.part3(["2026-01-01,u,subscribe,monthly", "2026-01-31,u,renew", "2026-01-01..2027-12-31"])
    assert any(line == "2026-01-31 u welcome" for line in after)
    assert not any(line.endswith("renewed") for line in after)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r2 = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r2.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin_and_missing_part_header(run_script):
    assert run_script("").stdout == ""
    r = run_script("\n".join(EX2) + "\n")  # no PART header -> full rule set (part3), still handles change
    assert r.stdout == "\n".join(EX2_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_events(run_script):
    rng = random.Random(0)
    n_users = 20_000
    lines = []

    def rand_date(lo_ord, span):
        import datetime

        return (datetime.date.fromordinal(lo_ord) + datetime.timedelta(days=rng.randrange(span))).isoformat()

    base = 738_000  # ~2021-11-01 as an ordinal, arbitrary stable anchor
    for i in range(n_users):
        plan = rng.choice(["monthly", "annual"])
        lines.append(f"{rand_date(base, 200)},user{i},subscribe,{plan}")
    while len(lines) < 100_000:
        u = rng.randrange(n_users)
        action = rng.choice(["change", "renew", "cancel"])
        d = rand_date(base + 200, 1200)
        if action == "change":
            lines.append(f"{d},user{u},change,{rng.choice(['monthly', 'annual'])}")
        else:
            lines.append(f"{d},user{u},{action}")
    rng.shuffle(lines)  # exercise the "not guaranteed in date order" contract too
    lines.append("2000-01-01..2100-01-01")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= n_users  # at least one welcome per user
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
