import random

import pytest

THREE = ["tokyo,+9,09:00,17:00", "london,0,09:00,17:00", "us-west,-8,09:00,17:00"]
EX1 = ["2026-03-02", "tokyo,+9,09:00,17:00", "india,+5.5,09:00,17:00", "london,0,09:00,17:00",
       "us-west,-8,09:00,17:00", "sydney,+11,09:00,17:00"]
EX1_OUT = [
    "tokyo 2026-03-02T00:00..2026-03-02T08:00",
    "india 2026-03-02T03:30..2026-03-02T11:30",
    "london 2026-03-02T09:00..2026-03-02T17:00",
    "us-west 2026-03-02T17:00..2026-03-03T01:00",
    "sydney 2026-03-01T22:00..2026-03-02T06:00",
]
EX2 = ["2026-03-02"] + THREE
EX2_OUT = ["2026-03-02T08:00..09:00"]
EX3 = ["2026-03-02T08:30,30,3", "blackout,2026-03-03"] + THREE
EX3_OUT = ["2026-03-02T08:30..09:00", "2026-03-04T08:00..09:00", "2026-03-05T08:00..09:00"]
EX4 = ["2026-03-02,60", "tokyo,+9,Mon-Fri,09:00,17:00", "london,0,Mon-Fri,09:00,17:00",
       "us-west,-8,Mon-Fri,09:00,17:00"]
EX4_OUT = ["2026-03-02T08:00..09:00", "2026-03-03T08:00..09:00", "2026-03-04T08:00..09:00",
           "2026-03-05T08:00..09:00", "2026-03-06T08:00..09:00", "2026-03-07T01:00..24:00",
           "2026-03-08T00:00..24:00"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_fractional_and_negative_offsets(impl):
    assert impl.part1(["2026-01-31", "kabul,+4.5,08:00,16:00"]) == ["kabul 2026-01-31T03:30..2026-01-31T11:30"]
    assert impl.part1(["2026-01-31", "nfld,-3.5,09:00,17:00"]) == ["nfld 2026-01-31T12:30..2026-01-31T20:30"]
    assert impl.part1(["2026-01-31", "np,5.75,00:00,01:00"]) == ["np 2026-01-30T18:15..2026-01-30T19:15"]


@pytest.mark.part1
@pytest.mark.edge
def test_wrap_and_full_day_windows(impl):
    # 22:00 -> 06:00 next local day; offset 0 so UTC = local
    assert impl.part1(["2026-12-31", "ops,0,22:00,06:00"]) == ["ops 2026-12-31T22:00..2027-01-01T06:00"]
    # start == end -> the whole day is busy
    assert impl.part1(["2026-02-28", "all,+1,09:00,09:00"]) == ["all 2026-02-28T08:00..2026-03-01T08:00"]


@pytest.mark.part1
@pytest.mark.fmt
def test_part1_whitespace_and_empty(impl):
    assert impl.part1(["2026-03-02", "  a , +9 , 09:00 , 17:00  ", ""]) == ["a 2026-03-02T00:00..2026-03-02T08:00"]
    assert impl.part1(["2026-03-02"]) == []


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_free_day_and_busy_day(impl):
    assert impl.part2(["2026-03-02"]) == ["2026-03-02T00:00..24:00"]
    assert impl.part2(["2026-03-02", "x,0,00:00,00:00"]) == []
    # two 12-hour shifts that touch exactly at 12:00 cover the day, no zero-length window
    assert impl.part2(["2026-03-02", "a,0,00:00,12:00", "b,0,12:00,00:00"]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_spill_from_previous_and_next_local_day(impl):
    # +14: local 2026-03-03 00:00 is 2026-03-02 10:00 UTC -> busy 10:00..18:00 comes from local D+1
    assert impl.part2(["2026-03-02", "kir,+14,00:00,08:00"]) == ["2026-03-02T00:00..10:00", "2026-03-02T18:00..24:00"]
    # -8 with a wrapping 20:00..04:00 local shift: Sunday's shift spills to Mon 04:00..12:00 UTC,
    # Monday's own spills 04:00 Tue -> busy Mon [04:00,12:00] only
    assert impl.part2(["2026-03-02", "sea,-8,20:00,04:00"]) == ["2026-03-02T00:00..04:00", "2026-03-02T12:00..24:00"]


@pytest.mark.part2
@pytest.mark.fmt
def test_merge_touching_overlapping_and_duplicates(impl):
    lines = ["2026-03-02", "a,0,09:00,12:00", "b,0,12:00,13:00", "c,0,11:00,14:00", "a,0,09:00,12:00"]
    assert impl.part2(lines) == ["2026-03-02T00:00..09:00", "2026-03-02T14:00..24:00"]


@pytest.mark.part2
@pytest.mark.edge
def test_windows_split_at_midnight_and_minute_granularity(impl):
    # one minute free at 23:59 and one at 00:00 -> two separate one-minute windows on two days
    rules = ["a,0,00:01,23:59"]
    assert impl.part2(["2026-03-02"] + rules) == ["2026-03-02T00:00..00:01", "2026-03-02T23:59..24:00"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_min_length_boundary_exact_below_above(impl):
    base = ["blackout,2026-03-03"] + THREE
    assert impl.part3(["2026-03-02T08:30,30,1"] + base) == ["2026-03-02T08:30..09:00"]   # == L
    assert impl.part3(["2026-03-02T08:30,31,1"] + base) == ["2026-03-04T08:00..09:00"]   # one above -> skip day 1
    assert impl.part3(["2026-03-02T08:30,29,1"] + base) == ["2026-03-02T08:30..09:00"]   # one below
    assert impl.part3(["2026-03-02T08:30,45,3"] + base) == ["2026-03-04T08:00..09:00", "2026-03-05T08:00..09:00", "2026-03-06T08:00..09:00"]


@pytest.mark.part3
@pytest.mark.edge
def test_now_inside_busy_at_window_start_and_at_window_end(impl):
    assert impl.part3(["2026-03-02T10:00,60,1"] + THREE) == ["2026-03-03T08:00..09:00"]   # now inside busy
    assert impl.part3(["2026-03-02T08:00,60,1"] + THREE) == ["2026-03-02T08:00..09:00"]   # exactly at start
    assert impl.part3(["2026-03-02T09:00,1,1"] + THREE) == ["2026-03-03T08:00..09:00"]    # exactly at end: no window


@pytest.mark.part3
@pytest.mark.edge
def test_k_zero_k_too_large_blackout_on_start_day_and_no_windows(impl):
    assert impl.part3(["2026-03-02T00:00,1,0"] + THREE) == []
    assert impl.part3(["2026-03-02T00:00,1,2", "blackout,2026-03-02"] + THREE) == ["2026-03-03T08:00..09:00", "2026-03-04T08:00..09:00"]
    # 24 h coverage -> nothing within the 366-day horizon
    assert impl.part3(["2026-03-02T00:00,1,5", "x,+3,10:00,10:00"]) == []
    # only a week of windows exists before a permanent freeze? no — fewer than K returns what exists:
    out = impl.part3(["2026-03-02T00:00,1440,3", "a,0,00:00,00:00", "blackout,2026-03-02"])
    assert out == []


@pytest.mark.part3
def test_no_rules_gives_full_days_and_crosses_month_end(impl):
    assert impl.part3(["2026-02-27T12:00,600,3", "blackout,2026-02-28"]) == [
        "2026-02-27T12:00..24:00", "2026-03-01T00:00..24:00", "2026-03-02T00:00..24:00"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_part4(impl):
    assert impl.part4(EX4) == EX4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_weekday_is_local_and_day_specs(impl):
    # -8 Friday shift 09:00-17:00 local => Fri 17:00 .. Sat 01:00 UTC; Sat/Sun off
    out = impl.part4(["2026-03-06,60", "us-west,-8,Fri,09:00,17:00"])
    assert out[:2] == ["2026-03-06T00:00..17:00", "2026-03-07T01:00..24:00"]
    assert len(out) == 7
    # Mon-Wed/Fri: Thursday free; Sat/Sun free; ranges + slash lists
    out = impl.part4(["2026-03-02,1440", "l,0,Mon-Wed/Fri,00:00,00:00"])
    assert out == ["2026-03-05T00:00..24:00", "2026-03-07T00:00..24:00", "2026-03-08T00:00..24:00"]
    # Sat/Sun busy, week wrap of a range Sat-Mon
    out = impl.part4(["2026-03-02,1440", "w,0,Sat-Mon,00:00,00:00"])
    assert out == ["2026-03-03T00:00..24:00", "2026-03-04T00:00..24:00", "2026-03-05T00:00..24:00", "2026-03-06T00:00..24:00"]


@pytest.mark.part4
@pytest.mark.edge
def test_part4_multiple_lines_per_region_blackout_and_four_field_rule(impl):
    lines = ["2026-03-02,60", "blackout,2026-03-04",
             "r,0,Mon-Fri,09:00,17:00", "r,0,Sat/Sun,10:00,12:00", "z,0,00:00,01:00"]
    assert impl.part4(lines) == [
        "2026-03-02T01:00..09:00", "2026-03-02T17:00..24:00",
        "2026-03-03T01:00..09:00", "2026-03-03T17:00..24:00",
        "2026-03-05T01:00..09:00", "2026-03-05T17:00..24:00",
        "2026-03-06T01:00..09:00", "2026-03-06T17:00..24:00",
        "2026-03-07T01:00..10:00", "2026-03-07T12:00..24:00",
        "2026-03-08T01:00..10:00", "2026-03-08T12:00..24:00",
    ]


# ---------------------------------------------------------------- variant
@pytest.mark.part1
def test_variant_week_intervals_prachub_examples(impl):
    assert impl.variant_week_intervals(["540,600,allowed", "570,585,freeze"]) == [[540, 570], [585, 600]]
    assert impl.variant_week_intervals(["0,20,allowed", "10,30,allowed", "5,8,freeze", "20,25,freeze"]) == [[0, 5], [8, 20], [25, 30]]
    assert impl.variant_week_intervals(["0,10,allowed", "0,10,freeze"]) == []
    assert impl.variant_week_intervals([]) == []


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"
    r = run_script("PART 4\n" + "\n".join(EX4) + "\n")
    assert r.stdout == "\n".join(EX4_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_1000_regions_366_day_scan(run_script):
    rng = random.Random(0)
    offsets = ["-12", "-8", "-5", "-3.5", "0", "+1", "+5.5", "+8", "+9", "+14"]
    rules = [f"r{i},{rng.choice(offsets)},{rng.randrange(24):02d}:{rng.randrange(60):02d},{rng.randrange(24):02d}:{rng.randrange(60):02d}"
             for i in range(1000)]
    # random 1000 rules cover the clock -> forces the full 366-day scan; then a realistic P4 week
    r = run_script("PART 3\n2026-03-02T00:00,1,5\n" + "\n".join(rules) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256
    week = [f"r{i},{rng.choice(offsets)},{rng.choice(['Mon-Fri', 'Sat/Sun', 'Mon-Wed/Fri'])},09:00,09:30" for i in range(5000)]
    r = run_script("PART 4\n2026-03-02,1\n" + "\n".join(week) + "\n", timeout=30)
    assert r.returncode == 0 and r.seconds < 2.0
