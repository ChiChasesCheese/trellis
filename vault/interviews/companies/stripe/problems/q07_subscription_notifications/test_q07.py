import random

import pytest

EX1 = ["Alice,basic,0,30", "Bob,pro,10,30"]
EX1_OUT = [
    "0: Alice - Welcome to basic",
    "10: Bob - Welcome to pro",
    "15: Alice - Upcoming expiry",
    "25: Bob - Upcoming expiry",
    "30: Alice - Subscription expired",
    "40: Bob - Subscription expired",
]
EX2 = EX1 + ["CHANGE,Alice,premium,5", "CHANGE,Bob,enterprise,10"]
EX2_OUT = [
    "0: Alice - Welcome to basic",
    "5: [Changed] Alice - basic -> premium",
    "10: [Changed] Bob - pro -> enterprise",
    "10: Bob - Welcome to enterprise",
    "15: Alice - Upcoming expiry",
    "25: Bob - Upcoming expiry",
    "30: Alice - Subscription expired",
    "40: Bob - Subscription expired",
]
EX3 = ["Alice,basic,0,30", "RENEW,Alice,30,20"]
EX3_OUT = [
    "0: Alice - Welcome to basic",
    "15: Alice - Upcoming expiry",
    "20: [Renewed] Alice - 30 -> 60",
    "45: Alice - Upcoming expiry",
    "60: Alice - Subscription expired",
]
EX4 = ["Alice,basic,0,30", "Bob,pro,0,30", "RENEW,Alice,10,30", "RENEW,Bob,10,31"]
EX4_OUT = [
    "0: Alice - Welcome to basic",
    "0: Bob - Welcome to pro",
    "15: Alice - Upcoming expiry",
    "15: Bob - Upcoming expiry",
    "30: [Renewed] Alice - 30 -> 40",
    "30: Bob - Subscription expired",
    "31: [Renewed] Bob - 30 -> 40",
    "40: Alice - Subscription expired",
    "40: Bob - Subscription expired",
]
EX5 = [
    "30",
    "ACCOUNT,acc_1,0,30",
    "ACCOUNT,acc_2,30,60",
    "ACCOUNT,acc_3,0,45",
    "RULE,welcome,on_create,0,Welcome aboard",
    "RULE,warn,days_before_expiration,15,Your plan expires in 15 days",
    "RULE,bye,after_expiration,0,Your plan has expired",
]
EX5_OUT = [
    "acc_1 bye Your plan has expired",
    "acc_2 welcome Welcome aboard",
    "acc_3 warn Your plan expires in 15 days",
]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_warning_never_before_start_day(impl):
    # duration 10: warning day -5 -> dropped
    assert impl.part1(["u,p,0,10"]) == ["0: u - Welcome to p", "10: u - Subscription expired"]
    # duration 15: warning lands on the start day, after the welcome
    assert impl.part1(["u,p,5,15"]) == ["5: u - Welcome to p", "5: u - Upcoming expiry", "20: u - Subscription expired"]
    # duration 14: warning day = start - 1 -> dropped
    assert impl.part1(["u,p,5,14"]) == ["5: u - Welcome to p", "19: u - Subscription expired"]
    # duration 0: welcome and expiry on the same day
    assert impl.part1(["u,p,3,0"]) == ["3: u - Welcome to p", "3: u - Subscription expired"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_single(impl):
    assert impl.part1([]) == []
    assert impl.part1(["solo,gold,7,30"]) == ["7: solo - Welcome to gold", "22: solo - Upcoming expiry", "37: solo - Subscription expired"]


@pytest.mark.part1
@pytest.mark.fmt
def test_same_day_ties_follow_user_input_order(impl):
    out = impl.part1(["A,x,0,20", "B,y,0,20"])
    assert out == ["0: A - Welcome to x", "0: B - Welcome to y", "5: A - Upcoming expiry",
                   "5: B - Upcoming expiry", "20: A - Subscription expired", "20: B - Subscription expired"]
    # chronological across users, not grouped by user
    out = impl.part1(["A,x,10,20", "B,y,0,20"])
    assert out == ["0: B - Welcome to y", "5: B - Upcoming expiry", "10: A - Welcome to x",
                   "15: A - Upcoming expiry", "20: B - Subscription expired", "30: A - Subscription expired"]


@pytest.mark.part1
def test_whitespace_and_blank_lines(impl):
    assert impl.part1(["  Alice , basic , 0 , 30 ", "", "   "]) == impl.part1(["Alice,basic,0,30"])


@pytest.mark.part1
def test_custom_send_schedule(impl):
    sched = (("start", "Hi {plan}"), (-7, "Soon"), ("end", "Bye"))
    assert impl.part1(["u,p,0,30"], schedule=sched) == ["0: u - Hi p", "23: u - Soon", "30: u - Bye"]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_name_later_record_wins_and_takes_later_position(impl):
    out = impl.part1(["A,x,0,30", "B,y,0,30", "A,z,0,30"])
    assert out == ["0: B - Welcome to y", "0: A - Welcome to z", "15: B - Upcoming expiry",
                   "15: A - Upcoming expiry", "30: B - Subscription expired", "30: A - Subscription expired"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_change_before_on_after_start(impl):
    # before the start: welcome names the new plan
    assert impl.part2(["u,basic,10,30", "CHANGE,u,pro,3"]) == [
        "3: [Changed] u - basic -> pro", "10: u - Welcome to pro", "25: u - Upcoming expiry", "40: u - Subscription expired"]
    # after the start: only the [Changed] line is visible, dates unchanged, no extra expiry
    assert impl.part2(["u,basic,10,30", "CHANGE,u,pro,12"]) == [
        "10: u - Welcome to basic", "12: [Changed] u - basic -> pro", "25: u - Upcoming expiry", "40: u - Subscription expired"]
    # same plan is still printed
    assert "12: [Changed] u - basic -> basic" in impl.part2(["u,basic,10,30", "CHANGE,u,basic,12"])


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_user_and_unsupported_event_are_ignored(impl):
    assert impl.part2(EX1 + ["CHANGE,ghost,pro,5"]) == EX1_OUT
    assert impl.part2(EX1 + ["RENEW,Alice,10,5"]) == EX1_OUT  # RENEW is a Part 3 event
    assert impl.part1(EX2) == EX1_OUT  # Part 1 ignores CHANGE


@pytest.mark.part2
@pytest.mark.edge
def test_events_out_of_order_and_same_day_same_user(impl):
    # events are applied in day order regardless of input order; the day-15 warning sits between them
    out = impl.part2(["u,a,0,30", "CHANGE,u,c,20", "CHANGE,u,b,5"])
    assert out == ["0: u - Welcome to a", "5: [Changed] u - a -> b", "15: u - Upcoming expiry",
                   "20: [Changed] u - b -> c", "30: u - Subscription expired"]
    out = impl.part2(["u,a,0,30", "CHANGE,u,b,5", "CHANGE,u,c,5"])
    assert out[1:3] == ["5: [Changed] u - a -> b", "5: [Changed] u - b -> c"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
def test_example4_renew_on_end_day_and_after_expiry(impl):
    assert impl.part3(EX4) == EX4_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_renew_before_or_on_warning_day_replaces_pending_warning(impl):
    assert impl.part3(["Alice,basic,0,30", "RENEW,Alice,30,10"]) == [
        "0: Alice - Welcome to basic", "10: [Renewed] Alice - 30 -> 60",
        "45: Alice - Upcoming expiry", "60: Alice - Subscription expired"]
    # on the warning day itself: the warning is pending (>= day) so it is replaced
    assert impl.part3(["u,p,0,30", "RENEW,u,30,15"]) == [
        "0: u - Welcome to p", "15: [Renewed] u - 30 -> 60", "45: u - Upcoming expiry", "60: u - Subscription expired"]
    # one day later the warning is already sent and stays
    assert impl.part3(["u,p,0,30", "RENEW,u,30,16"]) == [
        "0: u - Welcome to p", "15: u - Upcoming expiry", "16: [Renewed] u - 30 -> 60",
        "45: u - Upcoming expiry", "60: u - Subscription expired"]


@pytest.mark.part3
@pytest.mark.edge
def test_zero_extension_and_late_short_renewal(impl):
    assert impl.part3(["u,p,0,30", "RENEW,u,0,20"]) == [
        "0: u - Welcome to p", "15: u - Upcoming expiry", "20: [Renewed] u - 30 -> 30", "30: u - Subscription expired"]
    # renewal after expiry with new_end < renewal day: no second expiry, no warning
    assert impl.part3(["u,p,0,30", "RENEW,u,5,40"]) == [
        "0: u - Welcome to p", "15: u - Upcoming expiry", "30: u - Subscription expired", "40: [Renewed] u - 30 -> 35"]


@pytest.mark.part3
@pytest.mark.fmt
def test_mixed_change_and_renew_same_day_input_order(impl):
    assert impl.part3(["u,basic,0,30", "CHANGE,u,pro,5", "RENEW,u,30,5"]) == [
        "0: u - Welcome to basic", "5: [Changed] u - basic -> pro", "5: [Renewed] u - 30 -> 60",
        "45: u - Upcoming expiry", "60: u - Subscription expired"]
    assert impl.part3(EX1) == EX1_OUT  # superset of Part 1


# ---------------------------------------------------------------- Part 4 (rule-driven variant)
@pytest.mark.part4
def test_example5_rules(impl):
    assert impl.part4(EX5) == EX5_OUT
    assert impl.schedule_by_rules(
        30, [("acc_1", 0, 30), ("acc_2", 30, 60), ("acc_3", 0, 45)],
        [("welcome", "on_create", 0, "Welcome aboard"),
         ("warn", "days_before_expiration", 15, "Your plan expires in 15 days"),
         ("bye", "after_expiration", 0, "Your plan has expired")]) == EX5_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_rules_offsets_order_and_no_match(impl):
    accounts = [("a", 7, 10), ("b", 10, 10), ("c", 0, 5)]
    rules = [("r1", "on_create", 3, "T1"), ("r2", "after_expiration", 5, "T2"), ("r3", "days_before_expiration", 0, "T3")]
    assert impl.schedule_by_rules(10, accounts, rules) == ["a r1 T1", "a r3 T3", "b r3 T3", "c r2 T2"]
    assert impl.schedule_by_rules(99, accounts, rules) == []
    assert impl.schedule_by_rules(10, [], rules) == [] and impl.schedule_by_rules(10, accounts, []) == []
    # template keeps spaces and commas
    assert impl.part4(["0", "ACCOUNT,x,0,9", "RULE,w,on_create,0,Hello, friend"]) == ["x w Hello, friend"]


@pytest.mark.part4
@pytest.mark.edge
def test_unknown_trigger_raises(impl):
    with pytest.raises(ValueError):
        impl.schedule_by_rules(0, [("a", 0, 1)], [("r", "on_delete", 0, "T")])


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
    r = run_script("PART 4\n" + "\n".join(EX5) + "\n")
    assert r.stdout == "\n".join(EX5_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin_and_missing_part_header(run_script):
    assert run_script("").stdout == ""
    assert run_script("PART 1\n").stdout == ""
    r = run_script("\n".join(EX3) + "\n")  # no header -> full rule set
    assert r.stdout == "\n".join(EX3_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_users_and_events(run_script):
    rng = random.Random(0)
    n = 100_000
    lines = [f"user{i},plan{rng.randrange(5)},{rng.randrange(10000)},{rng.randrange(0, 400)}" for i in range(n)]
    for _ in range(n):
        u = rng.randrange(n)
        if rng.random() < 0.5:
            lines.append(f"CHANGE,user{u},plan{rng.randrange(5)},{rng.randrange(10500)}")
        else:
            lines.append(f"RENEW,user{u},{rng.randrange(1, 400)},{rng.randrange(10500)}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= 2 * n  # every user has >= welcome + expired, plus n events
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_rules_variant_is_not_quadratic(run_script):
    rng = random.Random(1)
    lines = ["500000"]
    for i in range(100_000):
        c = rng.randrange(1_000_000)
        lines.append(f"ACCOUNT,acc{i},{c},{c + rng.randrange(1, 1000)}")
    for i in range(100_000):
        t = rng.choice(["on_create", "days_before_expiration", "after_expiration"])
        lines.append(f"RULE,r{i},{t},{rng.randrange(0, 500_000)},Template {i}")
    r = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
