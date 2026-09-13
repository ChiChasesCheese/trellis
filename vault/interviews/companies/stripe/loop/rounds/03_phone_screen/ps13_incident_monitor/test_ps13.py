import random

import pytest

# ---------------------------------------------------------------- Part 1: confirmed real examples
P1_EX1_PARAMS = "WINDOW=3 THRESHOLD=4"
P1_EX1_LOGS = ["1,m1,500,2", "2,m1,500,2", "5,m1,500,1", "6,m1,500,1"]
P1_EX1_OUT = ["2,m1,500,TRIGGER", "5,m1,500,RESOLVE"]

P1_EX2_PARAMS = "WINDOW=3 THRESHOLD=3"
P1_EX2_LOGS = ["1,A,404,2", "1,A,404,1", "2,B,500,3", "3,A,404,1", "4,B,500,1"]
P1_EX2_OUT = ["1,A,404,TRIGGER", "2,B,500,TRIGGER"]


@pytest.mark.part1
def test_example_trigger_then_resolve(impl):
    assert impl.part1([P1_EX1_PARAMS] + P1_EX1_LOGS) == P1_EX1_OUT


@pytest.mark.part1
def test_example_two_independent_pairs_same_timestamp_tie(impl):
    assert impl.part1([P1_EX2_PARAMS] + P1_EX2_LOGS) == P1_EX2_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_window_boundary_closed_inclusive(impl):
    # exactly WINDOW-1 seconds earlier is IN range; one second further back is OUT
    assert impl.part1(["WINDOW=3 THRESHOLD=5", "1,m,e,3", "3,m,e,2"]) == ["3,m,e,TRIGGER"]
    assert impl.part1(["WINDOW=3 THRESHOLD=5", "1,m,e,3", "4,m,e,2"]) == []  # 1 is now out of [2,4]


@pytest.mark.part1
@pytest.mark.edge
def test_count_exactly_equal_to_threshold_triggers(impl):
    assert impl.part1(["WINDOW=1 THRESHOLD=5", "1,m,e,5"]) == ["1,m,e,TRIGGER"]


@pytest.mark.part1
@pytest.mark.edge
def test_pair_that_never_crosses_threshold_has_no_events(impl):
    assert impl.part1(["WINDOW=10 THRESHOLD=1000", "1,m,e,1", "2,m,e,1"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_pair_triggered_and_never_resolved_by_end_of_input(impl):
    assert impl.part1(["WINDOW=100 THRESHOLD=1", "1,m,e,1"]) == ["1,m,e,TRIGGER"]


@pytest.mark.part1
@pytest.mark.edge
def test_no_duplicate_consecutive_triggers_while_staying_above(impl):
    # sum stays >= threshold across several more records -- only ONE TRIGGER, no re-firing
    lines = ["1,m,e,10", "2,m,e,10", "3,m,e,10", "4,m,e,10"]
    assert impl.part1(["WINDOW=100 THRESHOLD=5"] + lines) == ["1,m,e,TRIGGER"]


@pytest.mark.part1
@pytest.mark.edge
def test_independent_pairs_do_not_share_state(impl):
    # two different (merchant,status_code) pairs must not share a running sum or deque
    lines = ["1,m1,e1,3", "1,m2,e2,3"]
    assert impl.part1(["WINDOW=10 THRESHOLD=5"] + lines) == []  # neither pair alone reaches 5


@pytest.mark.part1
def test_zero_log_lines(impl):
    assert impl.part1(["WINDOW=1 THRESHOLD=1"]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_output_line_format_no_extra_spaces(impl):
    out = impl.part1(["WINDOW=1 THRESHOLD=1", "1,merchantA,404,1"])
    assert out == ["1,merchantA,404,TRIGGER"]  # exact CSV, no spaces around commas


# ---------------------------------------------------------------- Part 2: out-of-order arrival
@pytest.mark.part2
def test_shuffled_input_matches_sorted_result(impl):
    shuffled = ["6,m1,500,1", "1,m1,500,2", "5,m1,500,1", "2,m1,500,2"]
    assert impl.part2([P1_EX1_PARAMS] + shuffled) == P1_EX1_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_reverse_sorted_input_still_produces_chronological_output(impl):
    reversed_logs = list(reversed(P1_EX2_LOGS))
    assert impl.part2([P1_EX2_PARAMS] + reversed_logs) == P1_EX2_OUT


@pytest.mark.part2
@pytest.mark.fmt
def test_tie_broken_by_input_order_not_merchant_id(impl):
    order1 = impl.part2(["WINDOW=5 THRESHOLD=5", "1,B,500,5", "1,A,404,5"])
    assert order1 == ["1,B,500,TRIGGER", "1,A,404,TRIGGER"]  # B first in input -> B first out
    order2 = impl.part2(["WINDOW=5 THRESHOLD=5", "1,A,404,5", "1,B,500,5"])
    assert order2 == ["1,A,404,TRIGGER", "1,B,500,TRIGGER"]  # swapped input -> swapped output


@pytest.mark.part2
def test_already_sorted_input_still_works(impl):
    assert impl.part2([P1_EX1_PARAMS] + P1_EX1_LOGS) == P1_EX1_OUT


# ---------------------------------------------------------------- Part 3: per-merchant overrides
P3_PARAMS = "DEFAULT_WINDOW=3 DEFAULT_THRESHOLD=4 RULES=1"
P3_RULE = "m2,2,3"
P3_LOGS = ["1,m1,500,2", "2,m1,500,2", "5,m1,500,1", "6,m1,500,1", "1,m2,404,3", "2,m2,404,1"]
P3_OUT = ["1,m2,404,TRIGGER", "2,m1,500,TRIGGER", "5,m1,500,RESOLVE"]


@pytest.mark.part3
def test_example_default_plus_override_merge_chronologically(impl):
    assert impl.part3([P3_PARAMS, P3_RULE] + P3_LOGS) == P3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_rules_zero_every_merchant_uses_default(impl):
    out = impl.part3(["DEFAULT_WINDOW=3 DEFAULT_THRESHOLD=4 RULES=0"] + P1_EX1_LOGS)
    assert out == P1_EX1_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_override_looser_than_default_never_triggers(impl):
    # default threshold=1 would trigger immediately; m1's override threshold=100 does not
    params = "DEFAULT_WINDOW=10 DEFAULT_THRESHOLD=1 RULES=1"
    rule = "m1,10,100"
    assert impl.part3([params, rule, "1,m1,e,5"]) == []


@pytest.mark.part3
def test_two_merchants_different_window_sizes_interleave_correctly(impl):
    params = "DEFAULT_WINDOW=100 DEFAULT_THRESHOLD=5 RULES=1"
    rule = "fast,1,5"  # fast's window is only 1 second (no accumulation across records)
    logs = ["1,fast,e,5", "1,slow,e,3", "2,slow,e,2"]
    out = impl.part3([params, rule] + logs)
    # fast triggers immediately at t=1 (single record already >= 5); slow needs both records
    # (window=100 accumulates 3+2=5) and only reaches threshold at t=2.
    assert out == ["1,fast,e,TRIGGER", "2,slow,e,TRIGGER"]


# ---------------------------------------------------------------- Part 4: two-severity ladder
P4_PARAMS = "WARN=3 CRIT=6 WINDOW=3"
P4_LOGS = ["1,m1,500,2", "2,m1,500,2", "3,m1,500,3", "5,m1,500,1", "7,m1,500,1"]
P4_OUT = ["2,m1,500,TRIGGER", "3,m1,500,ESCALATE", "5,m1,500,DEESCALATE", "7,m1,500,RESOLVE"]


@pytest.mark.part4
def test_example_full_escalation_deescalation_cycle(impl):
    assert impl.part4([P4_PARAMS] + P4_LOGS) == P4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_single_record_jumps_two_levels_up(impl):
    out = impl.part4(["WARN=3 CRIT=10 WINDOW=2", "1,m1,500,1", "2,m1,500,20"])
    assert out == ["2,m1,500,TRIGGER", "2,m1,500,ESCALATE"]


@pytest.mark.part4
@pytest.mark.edge
def test_single_record_jumps_two_levels_down(impl):
    lines = ["1,m1,500,1", "2,m1,500,20", "10,m1,500,1"]
    out = impl.part4(["WARN=3 CRIT=10 WINDOW=2"] + lines)
    assert out == ["2,m1,500,TRIGGER", "2,m1,500,ESCALATE", "10,m1,500,DEESCALATE", "10,m1,500,RESOLVE"]


@pytest.mark.part4
@pytest.mark.edge
def test_count_exactly_on_warn_and_crit_boundaries(impl):
    # WARN=3 -> total==3 is level 1 (not 0); CRIT=6 -> total==6 is level 2 (not 1)
    assert impl.part4(["WARN=3 CRIT=6 WINDOW=1", "1,m,e,3"]) == ["1,m,e,TRIGGER"]
    assert impl.part4(["WARN=3 CRIT=6 WINDOW=1", "1,m,e,6"]) == ["1,m,e,TRIGGER", "1,m,e,ESCALATE"]


@pytest.mark.part4
@pytest.mark.edge
def test_reaches_warn_only_never_crit_no_escalate(impl):
    lines = ["1,m,e,4", "10,m,e,1"]  # window=3: t=1 total=4 (level1); t=10 window empties -> level0
    out = impl.part4(["WARN=3 CRIT=100 WINDOW=3"] + lines)
    assert out == ["1,m,e,TRIGGER", "10,m,e,RESOLVE"]


@pytest.mark.part4
def test_zero_log_lines_part4(impl):
    assert impl.part4(["WARN=1 CRIT=2 WINDOW=1"]) == []


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n" + P1_EX1_PARAMS + "\n" + "\n".join(P1_EX1_LOGS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_EX1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n" + P3_PARAMS + "\n" + P3_RULE + "\n" + "\n".join(P3_LOGS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_OUT) + "\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    r = run_script("PART 4\n" + P4_PARAMS + "\n" + "\n".join(P4_LOGS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_200k_logs_out_of_order(run_script):
    rng = random.Random(0)
    merchants = [f"m{i}" for i in range(100)]
    statuses = ["404", "500", "502", "503"]
    n = 200_000
    lines = [
        f"{rng.randrange(0, 500_000)},{rng.choice(merchants)},{rng.choice(statuses)},{rng.randrange(1, 50)}"
        for _ in range(n)
    ]
    rng.shuffle(lines)  # deliberately out of timestamp order -- this is part2's whole point
    stdin_text = "PART 2\nWINDOW=60 THRESHOLD=200\n" + "\n".join(lines) + "\n"
    r = run_script(stdin_text, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
