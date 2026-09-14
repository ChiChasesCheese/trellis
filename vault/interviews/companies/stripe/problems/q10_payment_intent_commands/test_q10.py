import random

import pytest

EX1 = ["INIT m1 0", "INIT m2 10", "CREATE p1 m1 50", "ATTEMPT p1", "SUCCEED p1",
       "CREATE p2 m2 100", "ATTEMPT p2"]
EX1_OUT = ["m1 50", "m2 10"]
EX2 = ["INIT m1 100", "CREATE p1 m1 50", "UPDATE p1 80", "ATTEMPT p1", "UPDATE p1 999",
       "SUCCEED p1", "UPDATE p1 -5"]
EX3 = ["INIT m1 0", "INIT m1 500", "CREATE p1 m1 40", "ATTEMPT p1", "FAIL p1", "UPDATE p1 60",
       "ATTEMPT p1", "SUCCEED p1", "REFUND p1", "REFUND p1", "CREATE p2 m1 25", "REFUND p2"]
EX4 = ["1 INIT m1 1000 10", "2 CREATE p1 m1 200", "5 REFUND p1", "15 REFUND p1"]
EX5 = ["1 INIT a 0 5", "1 INIT b 0 0", "1 INIT c 0", "2 CREATE pa a 100", "2 CREATE pb b 100",
       "2 CREATE pc c 100", "7 REFUND pa", "7 REFUND pb", "99 REFUND pc"]
EX5_OUT = ["a 0", "b 100", "c 0"]

SUCCEEDED = ["INIT m 0", "CREATE p m 50", "ATTEMPT p", "SUCCEED p"]  # -> m 50


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1_verbatim(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_init_keeps_first_balance(impl):
    assert impl.part1(["INIT m 5", "INIT m 999"]) == ["m 5"]


@pytest.mark.part1
@pytest.mark.edge
def test_create_ignore_paths(impl):
    # duplicate payment id keeps the first amount
    assert impl.part1(["INIT m 0", "CREATE p m 50", "CREATE p m 70", "ATTEMPT p", "SUCCEED p"]) == ["m 50"]
    # unknown merchant: payment never exists, later commands on it are no-ops
    assert impl.part1(["INIT m 0", "CREATE p x 50", "ATTEMPT p", "SUCCEED p"]) == ["m 0"]
    # negative amount ignored; zero and one accepted
    assert impl.part1(["INIT m 0", "CREATE p m -1", "ATTEMPT p", "SUCCEED p"]) == ["m 0"]
    assert impl.part1(["INIT m 0", "CREATE p m 0", "ATTEMPT p", "SUCCEED p"]) == ["m 0"]
    assert impl.part1(["INIT m 0", "CREATE p m 1", "ATTEMPT p", "SUCCEED p"]) == ["m 1"]


@pytest.mark.part1
@pytest.mark.edge
def test_transition_ignore_paths(impl):
    # SUCCEED without ATTEMPT
    assert impl.part1(["INIT m 0", "CREATE p m 50", "SUCCEED p"]) == ["m 0"]
    # SUCCEED twice credits once; ATTEMPT on COMPLETED and re-SUCCEED are no-ops
    assert impl.part1(SUCCEEDED + ["SUCCEED p", "ATTEMPT p", "SUCCEED p"]) == ["m 50"]
    # ATTEMPT twice is a no-op (already PROCESSING) but SUCCEED still works
    assert impl.part1(["INIT m 0", "CREATE p m 50", "ATTEMPT p", "ATTEMPT p", "SUCCEED p"]) == ["m 50"]
    # unknown payment ids
    assert impl.part1(["INIT m 7", "ATTEMPT zz", "SUCCEED zz"]) == ["m 7"]


@pytest.mark.part1
@pytest.mark.fmt
def test_output_sorted_as_strings_and_zero_printed(impl):
    lines = ["INIT m2 0", "INIT m10 0", "INIT B 0", "INIT a -3"]
    assert impl.part1(lines) == ["B 0", "a -3", "m10 0", "m2 0"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_malformed_lines(impl):
    assert impl.part1([]) == []
    assert impl.part1(["INIT m x", "INIT m", "CREATE p m", "BOGUS m 1", "INIT n 1 2 3", "INIT k 4"]) == ["k 4"]


@pytest.mark.part1
@pytest.mark.edge
def test_later_part_commands_ignored_in_part1(impl):
    # UPDATE / FAIL / REFUND do not exist yet
    assert impl.part1(["INIT m 0", "CREATE p m 50", "UPDATE p 80", "ATTEMPT p", "SUCCEED p", "REFUND p"]) == ["m 50"]


@pytest.mark.part1
@pytest.mark.edge
def test_init_with_extra_argument_is_ignored_in_parts_1_to_3(impl):
    # Parts 1-3: INIT takes exactly 2 arguments; a 3rd token (Part 4's refund_limit) is a wrong
    # argument count and the whole command is ignored
    assert impl.part1(["INIT m 5 10"]) == []
    assert impl.part2(["INIT m 5 10", "INIT m 7"]) == ["m 7"]
    # regression: the stray "0" used to be read as refund_limit 0 and silently blocked the REFUND
    assert impl.part3(["INIT m 5 0", "INIT m 5", "CREATE p m 10", "ATTEMPT p", "SUCCEED p", "REFUND p"]) == ["m 5"]
    assert impl.part4(["1 INIT m 5 0", "2 CREATE p m 10", "3 REFUND p"]) == ["m 15"]  # Part 4 keeps the 3-arg form


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2_verbatim(impl):
    assert impl.part2(EX2) == ["m1 180"]


@pytest.mark.part2
@pytest.mark.edge
def test_update_only_in_requires_action(impl):
    assert impl.part2(["INIT m 0", "CREATE p m 50", "ATTEMPT p", "UPDATE p 80", "SUCCEED p"]) == ["m 50"]
    assert impl.part2(SUCCEEDED + ["UPDATE p 80"]) == ["m 50"]
    assert impl.part2(["INIT m 0", "UPDATE p 80"]) == ["m 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_update_negative_ignored_zero_allowed(impl):
    assert impl.part2(["INIT m 0", "CREATE p m 50", "UPDATE p -1", "ATTEMPT p", "SUCCEED p"]) == ["m 50"]
    assert impl.part2(["INIT m 0", "CREATE p m 50", "UPDATE p 0", "ATTEMPT p", "SUCCEED p"]) == ["m 0"]
    # last valid update wins
    assert impl.part2(["INIT m 0", "CREATE p m 50", "UPDATE p 10", "UPDATE p 20", "ATTEMPT p", "SUCCEED p"]) == ["m 20"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_still_ignores_part3_commands(impl):
    assert impl.part2(SUCCEEDED + ["REFUND p"]) == ["m 50"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3_verbatim(impl):
    assert impl.part3(EX3) == ["m1 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_fail_reopens_and_only_from_processing(impl):
    # FAIL then UPDATE then full cycle again
    assert impl.part3(["INIT m 0", "CREATE p m 50", "ATTEMPT p", "FAIL p", "UPDATE p 5", "ATTEMPT p", "SUCCEED p"]) == ["m 5"]
    # FAIL on REQUIRES_ACTION / COMPLETED / unknown -> ignored
    assert impl.part3(["INIT m 0", "CREATE p m 50", "FAIL p", "ATTEMPT p", "SUCCEED p"]) == ["m 50"]
    assert impl.part3(SUCCEEDED + ["FAIL p", "REFUND p"]) == ["m 0"]  # still COMPLETED, refund works
    assert impl.part3(["INIT m 1", "FAIL p"]) == ["m 1"]
    # after FAIL a SUCCEED without a fresh ATTEMPT is ignored
    assert impl.part3(["INIT m 0", "CREATE p m 50", "ATTEMPT p", "FAIL p", "SUCCEED p"]) == ["m 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_refund_paths(impl):
    assert impl.part3(SUCCEEDED + ["REFUND p"]) == ["m 0"]
    assert impl.part3(SUCCEEDED + ["REFUND p", "REFUND p"]) == ["m 0"]          # once only
    assert impl.part3(["INIT m 0", "CREATE p m 50", "REFUND p"]) == ["m 0"]      # REQUIRES_ACTION
    assert impl.part3(["INIT m 0", "CREATE p m 50", "ATTEMPT p", "REFUND p", "SUCCEED p"]) == ["m 50"]  # PROCESSING
    assert impl.part3(["INIT m 0", "REFUND nope"]) == ["m 0"]
    # refund uses the credited (updated) amount and may drive the balance negative
    assert impl.part3(["INIT m 0", "CREATE p m 50", "UPDATE p 70", "ATTEMPT p", "SUCCEED p", "INIT m 999", "REFUND p"]) == ["m 0"]
    assert impl.part3(["INIT m 10", "CREATE p m 50", "ATTEMPT p", "SUCCEED p", "REFUND p"]) == ["m 10"]


@pytest.mark.part3
def test_many_merchants_and_payments_independent(impl):
    lines = ["INIT b 0", "INIT a 0", "CREATE p1 a 5", "CREATE p2 b 7", "ATTEMPT p1", "ATTEMPT p2",
             "SUCCEED p2", "FAIL p1", "ATTEMPT p1", "SUCCEED p1", "REFUND p2"]
    assert impl.part3(lines) == ["a 5", "b 0"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example4_verbatim(impl):
    assert impl.part4(EX4) == ["m1 1000"]


@pytest.mark.part4
def test_example5_verbatim(impl):
    assert impl.part4(EX5) == EX5_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_create_credits_immediately_no_succeed_needed(impl):
    assert impl.part4(["1 INIT m1 1000", "2 CREATE p1 m1 500"]) == ["m1 1500"]
    # state-machine commands are harmless no-ops here
    assert impl.part4(["1 INIT m 0", "2 CREATE p m 5", "3 ATTEMPT p", "4 SUCCEED p", "5 UPDATE p 9"]) == ["m 5"]


@pytest.mark.part4
@pytest.mark.edge
def test_refund_window_boundaries(impl):
    base = ["1 INIT m 0 10", "5 CREATE p m 100"]
    assert impl.part4(base + ["15 REFUND p"]) == ["m 0"]      # 15-5 == 10 -> allowed
    assert impl.part4(base + ["16 REFUND p"]) == ["m 100"]    # one above -> refused
    assert impl.part4(base + ["14 REFUND p"]) == ["m 0"]      # one below
    # a refused refund does not "use up" the refund: a later in-window one is impossible, but an
    # earlier-timestamp line (out-of-order input) still works
    assert impl.part4(base + ["16 REFUND p", "10 REFUND p"]) == ["m 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_limit_zero_absent_and_duplicate_init(impl):
    assert impl.part4(["1 INIT m 0 0", "1 CREATE p m 100", "1 REFUND p"]) == ["m 100"]   # 0 -> never
    assert impl.part4(["1 INIT m 0", "1 CREATE p m 100", "1000000 REFUND p"]) == ["m 0"]  # absent -> always
    # duplicate INIT cannot change the window either
    assert impl.part4(["1 INIT m 0 0", "2 INIT m 0", "3 CREATE p m 100", "4 REFUND p"]) == ["m 100"]
    # ignore paths carry over: dup id, unknown merchant, negative, double refund
    assert impl.part4(["1 INIT m 0", "2 CREATE p m 5", "2 CREATE p m 50", "2 CREATE q x 5",
                       "2 CREATE r m -5", "3 REFUND p", "4 REFUND p"]) == ["m 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_part4_malformed_timestamp_and_bad_limit(impl):
    assert impl.part4(["INIT m 0", "1 INIT m 0", "x CREATE p m 5", "2 INIT n 1 abc", "2 CREATE q m 5"]) == ["m 5"]


@pytest.mark.part4
def test_version_b_variant_keeps_state_machine(impl):
    lines = ["1 INIT m 0 10", "2 CREATE p m 100", "3 REFUND p", "4 ATTEMPT p", "5 SUCCEED p",
             "13 REFUND p"]
    # refund at t=3 fails (not COMPLETED); SUCCEED credits 100; refund at 13: 13-2 = 11 > 10 -> refused
    assert impl.part4(lines, immediate_credit=False) == ["m 100"]
    lines[-1] = "12 REFUND p"
    assert impl.part4(lines, immediate_credit=False) == ["m 0"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_no_header_and_with_header(run_script):
    r = run_script("\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "m1 50\nm2 10\n"
    r = run_script("PART 4\n" + "\n".join(EX5) + "\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a 0\nb 100\nc 0\n"
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.stdout == "m1 180\n"
    assert run_script("").stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_200k_commands(run_script):
    rng = random.Random(0)
    lines = [f"INIT m{i} {rng.randrange(1000)}" for i in range(2000)]
    words = ["ATTEMPT", "SUCCEED", "FAIL", "REFUND", "UPDATE"]
    for i in range(198_000):
        if i % 4 == 0:
            lines.append(f"CREATE p{i // 4} m{rng.randrange(2000)} {rng.randrange(10000)}")
        else:
            w = rng.choice(words)
            arg = f" {rng.randrange(10000)}" if w == "UPDATE" else ""
            lines.append(f"{w} p{rng.randrange(i // 4 + 1)}{arg}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 2000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
