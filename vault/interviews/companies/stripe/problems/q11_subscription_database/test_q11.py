import random

import pytest

EX1 = ["1,start,Michael", "5,check,Michael", "7,end,Michael", "8,check,Michael", "9,check,Alice"]
EX1_OUT = ["active", "inactive", "inactive"]
EX2 = [
    "1,start,Michael,9", "10,check,Michael", "11,check,Michael", "12,start,Michael",
    "20,check,Michael", "21,start,Michael,2", "24,check,Michael",
]
EX2_OUT = ["active", "inactive", "active", "inactive"]
EX3 = [
    "1,start,Michael,10", "2,start,Michael,4", "15,check,Michael", "16,check,Michael",
    "1,start,Alice", "3,start,Alice,2", "100,check,Alice",
]
EX3_OUT = ["active", "inactive", "active"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_check_before_start_and_unknown_user(impl):
    assert impl.part1(["1,check,A", "2,start,A", "3,check,B", "4,check,A"]) == ["inactive", "inactive", "active"]


@pytest.mark.part1
@pytest.mark.edge
def test_end_is_idempotent_and_noop_for_unknown(impl):
    assert impl.part1(["1,end,A", "2,check,A", "3,start,A", "4,end,A", "5,end,A", "6,check,A"]) == ["inactive", "inactive"]


@pytest.mark.part1
@pytest.mark.edge
def test_same_timestamp_input_order(impl):
    assert impl.part1(["5,start,A", "5,check,A"]) == ["active"]
    assert impl.part1(["5,start,A", "5,end,A", "5,check,A"]) == ["inactive"]
    assert impl.part1(["5,check,A", "5,start,A"]) == ["inactive"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_no_checks(impl):
    assert impl.part1([]) == []
    assert impl.part1(["1,start,A", "2,end,A"]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_whitespace_and_case_sensitive_users(impl):
    assert impl.part1([" 1 , start , Michael ", "", "2,check,michael", "3,check,Michael"]) == ["inactive", "active"]


@pytest.mark.part1
@pytest.mark.edge
def test_events_processed_in_given_order_not_sorted(impl):
    # timestamps go backwards; we still apply them in the order given
    assert impl.part1(["9,start,A", "3,check,A", "1,end,A", "8,check,A"]) == ["active", "inactive"]


@pytest.mark.part1
def test_part1_ignores_durations(impl):
    assert impl.part1(["1,start,A,2", "100,check,A"]) == ["active"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_inclusive_boundary(impl):
    # 1 + 9 = 10: active at 9, 10; inactive at 11
    assert impl.part2(["1,start,M,9", "9,check,M", "10,check,M", "11,check,M"]) == ["active", "active", "inactive"]


@pytest.mark.part2
@pytest.mark.edge
def test_zero_duration_active_only_at_start(impl):
    assert impl.part2(["5,start,M,0", "5,check,M", "6,check,M"]) == ["active", "inactive"]


@pytest.mark.part2
@pytest.mark.edge
def test_new_start_replaces_old(impl):
    # finite replaces finite: expiry becomes 2 + 4 = 6 (not 11, not 15)
    assert impl.part2(["1,start,M,10", "2,start,M,4", "6,check,M", "7,check,M"]) == ["active", "inactive"]
    # finite replaces unlimited
    assert impl.part2(["1,start,M", "2,start,M,1", "3,check,M", "4,check,M"]) == ["active", "inactive"]
    # unlimited replaces finite
    assert impl.part2(["1,start,M,1", "2,start,M", "1000,check,M"]) == ["active"]


@pytest.mark.part2
@pytest.mark.edge
def test_end_cancels_remaining_time_and_restart(impl):
    assert impl.part2(["1,start,M,100", "2,end,M", "3,check,M", "4,start,M,1", "5,check,M", "6,check,M"]) == [
        "inactive", "active", "inactive"]


@pytest.mark.part2
def test_multiple_users_independent(impl):
    lines = ["1,start,A,5", "1,start,B", "6,check,A", "7,check,A", "7,check,B", "8,end,B", "8,check,B"]
    assert impl.part2(lines) == ["active", "inactive", "active", "inactive"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_accumulate_extends_from_current_expiry(impl):
    # expiry 11, +4 -> 15 (NOT 2 + 4 = 6 and NOT 11 + 4 measured from the second start)
    assert impl.part3(["1,start,M,10", "2,start,M,4", "15,check,M", "16,check,M"]) == ["active", "inactive"]
    # same input under part2 gives the replace answer
    assert impl.part2(["1,start,M,10", "2,start,M,4", "7,check,M"]) == ["inactive"]
    assert impl.part3(["1,start,M,10", "2,start,M,4", "7,check,M"]) == ["active"]


@pytest.mark.part3
@pytest.mark.edge
def test_three_starts_chain(impl):
    # 1+10=11, +4=15, +5=20
    assert impl.part3(["1,start,M,10", "2,start,M,4", "3,start,M,5", "20,check,M", "21,check,M"]) == ["active", "inactive"]


@pytest.mark.part3
@pytest.mark.edge
def test_start_exactly_on_expiry_extends(impl):
    # expiry 10; a start at t=10 is still "active" (inclusive) -> extends to 15; a start at t=11 restarts -> 11+5=16
    assert impl.part3(["1,start,M,9", "10,start,M,5", "15,check,M", "16,check,M"]) == ["active", "inactive"]
    assert impl.part3(["1,start,M,9", "11,start,M,5", "16,check,M", "17,check,M"]) == ["active", "inactive"]


@pytest.mark.part3
@pytest.mark.edge
def test_expired_or_ended_subscription_restarts_fresh(impl):
    assert impl.part3(["1,start,M,2", "10,start,M,5", "15,check,M", "16,check,M"]) == ["active", "inactive"]
    assert impl.part3(["1,start,M,100", "2,end,M", "3,start,M,1", "4,check,M", "5,check,M"]) == ["active", "inactive"]


@pytest.mark.part3
@pytest.mark.edge
def test_unlimited_unaffected_and_no_duration_upgrades(impl):
    # unlimited + later finite start: still unlimited
    assert impl.part3(["1,start,M", "2,start,M,1", "1000,check,M"]) == ["active"]
    # finite + later start without duration: becomes unlimited
    assert impl.part3(["1,start,M,1", "2,start,M", "1000,check,M"]) == ["active"]


@pytest.mark.part3
def test_part3_example_part1_and_part2_inputs_unchanged(impl):
    assert impl.part3(EX1) == EX1_OUT
    # EX2 under part3: the unlimited start at 12 is NOT shortened by 21,start,Michael,2 -> last check active
    assert impl.part3(EX2) == ["active", "inactive", "active", "active"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.stdout == "\n".join(EX3_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_200k_events(run_script):
    rng = random.Random(0)
    lines, t = [], 0
    for _ in range(200_000):
        t += rng.randrange(0, 3)
        u = f"u{rng.randrange(20_000)}"
        op = rng.choice(["start", "start", "check", "check", "check", "end"])
        if op == "start" and rng.random() < 0.8:
            lines.append(f"{t},start,{u},{rng.randrange(0, 50)}")
        else:
            lines.append(f"{t},{op},{u}")
    n_checks = sum(1 for ln in lines if ",check," in ln)
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == n_checks
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
