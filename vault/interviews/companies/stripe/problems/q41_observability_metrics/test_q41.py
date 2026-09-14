"""q41 Observability Metrics — tests. RECONSTRUCTED TRAINING PROBLEM (see problem.md's warning
block). Every literal expected value below was produced by running solution.py on the exact
input shown and transcribed, not hand-derived (same discipline as ps11's tests).
"""

import random

import pytest

# ---------------------------------------------------------------- shared examples

P1_EXAMPLE = [
    "EVENTS",
    "0,latency,region=us,120",
    "5,latency,us=1;region=us,80",
    "10,latency,region=eu,300",
    "not,a,valid,row,extra",
]
P1_EXAMPLE_OUT = [
    "latency,region=eu count=1 sum=300.00 avg=300.00",
    "latency,region=us count=1 sum=120.00 avg=120.00",
    "latency,region=us;us=1 count=1 sum=80.00 avg=80.00",
    "MALFORMED 1",
]

P3_HYSTERESIS_LINES = ["WINDOW", "10 10", "RULES", "errors,-,count,gte,3,2,2", "EVENTS"]
_counts_by_window = [5, 4, 1, 1, 0, 0, 5, 5]
for _w, _c in enumerate(_counts_by_window):
    for _i in range(_c):
        P3_HYSTERESIS_LINES.append(f"{_w * 10 + 1 + _i},errors,-,1")
P3_HYSTERESIS_OUT = [
    "errors,- ALERT_ON window=1",
    "errors,- ALERT_OFF window=3",
    "errors,- ALERT_ON window=7",
    "MALFORMED 0",
]


# ---------------------------------------------------------------- Part 1: parse + aggregate
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(P1_EXAMPLE) == P1_EXAMPLE_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_zero_events(impl):
    assert impl.part1(["EVENTS"]) == ["MALFORMED 0"]


@pytest.mark.part1
@pytest.mark.edge
def test_label_reordering_merges_same_series(impl):
    lines = ["EVENTS", "0,m,a=1;b=2,10", "1,m,b=2;a=1,20"]
    assert impl.part1(lines) == ["m,a=1;b=2 count=2 sum=30.00 avg=15.00", "MALFORMED 0"]


@pytest.mark.part1
@pytest.mark.edge
def test_every_malformed_reason_tallied(impl):
    lines = [
        "EVENTS",
        "1,m,-,10,extra",  # wrong field count
        "abc,m,-,10",  # bad timestamp
        "1,m,-,notanumber",  # bad value
        "1,m,badlabels,10",  # malformed labels (no '=')
        "1,m,-,20",  # the one well-formed row
    ]
    assert impl.part1(lines) == ["m,- count=1 sum=20.00 avg=20.00", "MALFORMED 4"]


@pytest.mark.part1
@pytest.mark.fmt
def test_avg_two_decimal_rounding(impl):
    lines = ["EVENTS", "0,m,-,1", "1,m,-,1", "2,m,-,2"]
    assert impl.part1(lines) == ["m,- count=3 sum=4.00 avg=1.33", "MALFORMED 0"]


# ---------------------------------------------------------------- Part 2: windowed buckets
@pytest.mark.part2
def test_tumbling_window(impl):
    lines = [
        "WINDOW",
        "10 10",
        "EVENTS",
        "0,lat,region=us,1",
        "3,lat,region=us,2",
        "5,lat,region=us,3",
        "9,lat,region=us,4",
        "12,lat,region=us,10",
    ]
    assert impl.part2(lines) == [
        "lat,region=us,window=0 count=4 avg=2.50 p50=2.00 p90=4.00",
        "lat,region=us,window=1 count=1 avg=10.00 p50=10.00 p90=10.00",
        "MALFORMED 0",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_sliding_window_overlap(impl):
    lines = [
        "WINDOW",
        "10 5",
        "EVENTS",
        "0,lat,region=us,1",
        "3,lat,region=us,2",
        "5,lat,region=us,3",
        "9,lat,region=us,4",
    ]
    assert impl.part2(lines) == [
        "lat,region=us,window=0 count=4 avg=2.50 p50=2.00 p90=4.00",
        "lat,region=us,window=1 count=2 avg=3.50 p50=3.00 p90=4.00",
        "MALFORMED 0",
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_percentile_nearest_rank_even_length_window(impl):
    lines = ["WINDOW", "100 100", "EVENTS", "1,m,-,10", "2,m,-,20", "3,m,-,30", "4,m,-,40"]
    assert impl.part2(lines) == ["m,-,window=0 count=4 avg=25.00 p50=20.00 p90=40.00", "MALFORMED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_malformed_rows_excluded_but_tallied(impl):
    lines = ["WINDOW", "10 10", "EVENTS", "1,m,-,10", "bad,row"]
    assert impl.part2(lines) == ["m,-,window=0 count=1 avg=10.00 p50=10.00 p90=10.00", "MALFORMED 1"]


@pytest.mark.part2
@pytest.mark.edge
def test_sort_order_metric_then_labels_then_window(impl):
    lines = ["WINDOW", "10 10", "EVENTS", "15,z,-,1", "1,a,region=b,1", "1,a,region=a,1"]
    out = impl.part2(lines)
    assert out == [
        "a,region=a,window=0 count=1 avg=1.00 p50=1.00 p90=1.00",
        "a,region=b,window=0 count=1 avg=1.00 p50=1.00 p90=1.00",
        "z,-,window=1 count=1 avg=1.00 p50=1.00 p90=1.00",
        "MALFORMED 0",
    ]


# ---------------------------------------------------------------- Part 3: alerting hysteresis
@pytest.mark.part3
def test_trigger_clear_retrigger_hysteresis(impl):
    assert impl.part3(P3_HYSTERESIS_LINES) == P3_HYSTERESIS_OUT


@pytest.mark.part3
def test_rate_rule_count_vs_ratio(impl):
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "lat,-,rate,gt,0.5,1,1,100",
        "EVENTS",
        "1,lat,-,50",
        "2,lat,-,200",
        "3,lat,-,300",
        "11,lat,-,10",
        "12,lat,-,20",
    ]
    assert impl.part3(lines) == [
        "lat,- ALERT_ON window=0",
        "lat,- ALERT_OFF window=1",
        "MALFORMED 0",
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_gt_vs_gte_strict_boundary(impl):
    lines = ["WINDOW", "10 10", "RULES", "m,-,count,gt,2,1,1", "EVENTS", "1,m,-,1", "2,m,-,1"]
    # exactly 2 events, gt 2 is false -> never fires
    assert impl.part3(lines) == ["MALFORMED 0"]
    lines_gte = ["WINDOW", "10 10", "RULES", "m,-,count,gte,2,1,1", "EVENTS", "1,m,-,1", "2,m,-,1"]
    # gte 2 is true -> fires immediately at window 0
    assert impl.part3(lines_gte) == ["m,- ALERT_ON window=0", "MALFORMED 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_rule_on_metric_with_no_data_still_evaluates_zero_windows(impl):
    # 'ghost' never appears in EVENTS; count is always 0, so 'lte 0' fires on window 0 immediately
    # (max_k comes from the 'other' metric's events, which the rule's own series must still walk).
    lines = ["WINDOW", "10 10", "RULES", "ghost,-,count,lte,0,1,1", "EVENTS", "5,other,-,1", "25,other,-,1"]
    assert impl.part3(lines) == ["ghost,- ALERT_ON window=0", "MALFORMED 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_rate_zero_denominator_is_defined_as_zero(impl):
    # window has zero matching events -> rate is 0.0, never satisfies a 'gt' rule
    lines = ["WINDOW", "10 10", "RULES", "ghost,-,rate,gt,0.0,1,1,50", "EVENTS", "5,other,-,1"]
    assert impl.part3(lines) == ["MALFORMED 0"]


# ---------------------------------------------------------------- Part 4: lateness watermark
@pytest.mark.part4
def test_late_event_within_tolerance_is_kept(impl):
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "errors,-,count,gte,1,1,1",
        "LATENESS",
        "2",
        "EVENTS",
        "25,errors,-,1",
        "5,errors,-,1",
    ]
    assert impl.part4(lines) == [
        "errors,- ALERT_ON window=0",
        "errors,- ALERT_OFF window=1",
        "errors,- ALERT_ON window=2",
        "DROPPED 0",
        "MALFORMED 0",
    ]


@pytest.mark.part4
def test_late_event_beyond_tolerance_is_dropped(impl):
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "errors,-,count,gte,1,1,1",
        "LATENESS",
        "1",
        "EVENTS",
        "25,errors,-,1",
        "5,errors,-,1",
    ]
    assert impl.part4(lines) == ["errors,- ALERT_ON window=2", "DROPPED 1", "MALFORMED 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_lateness_boundary_is_not_dropped_at_exact_equality(impl):
    # primary(0) < max_primary_seen(2) - L(2) == 0 is FALSE (strict <) -> kept, not dropped
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "errors,-,count,gte,1,1,1",
        "LATENESS",
        "2",
        "EVENTS",
        "25,errors,-,1",
        "5,errors,-,1",
    ]
    out = impl.part4(lines)
    assert "DROPPED 0" in out and "errors,- ALERT_ON window=0" in out


@pytest.mark.part4
@pytest.mark.edge
def test_dropped_events_actually_change_alert_outcome(impl):
    base = ["WINDOW", "10 10", "RULES", "errors,-,count,gte,2,1,1"]
    events = ["EVENTS", "25,errors,-,1", "26,errors,-,1", "5,errors,-,1", "6,errors,-,1"]
    keep_late = impl.part4(base + ["LATENESS", "5"] + events)
    drop_late = impl.part4(base + ["LATENESS", "0"] + events)
    assert "errors,- ALERT_ON window=0" in keep_late
    assert "errors,- ALERT_ON window=0" not in drop_late
    assert drop_late == ["errors,- ALERT_ON window=2", "DROPPED 2", "MALFORMED 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_lateness_zero_drops_any_out_of_order_arrival(impl):
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "errors,-,count,gte,1,1,1",
        "LATENESS",
        "0",
        "EVENTS",
        "10,errors,-,1",
        "11,errors,-,1",  # same primary bucket (1) as the first -> NOT behind it, kept
        "5,errors,-,1",  # primary 0 < max_primary_seen(1) - 0 -> dropped
    ]
    out = impl.part4(lines)
    assert out[-2:] == ["DROPPED 1", "MALFORMED 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_malformed_still_tallied_in_part4(impl):
    lines = [
        "WINDOW",
        "10 10",
        "RULES",
        "errors,-,count,gte,1,1,1",
        "LATENESS",
        "0",
        "EVENTS",
        "1,errors,-,1",
        "not,valid",
    ]
    assert impl.part4(lines) == ["errors,- ALERT_ON window=0", "DROPPED 0", "MALFORMED 1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_EXAMPLE_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    r = run_script("PART 3\n" + "\n".join(P3_HYSTERESIS_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_HYSTERESIS_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_1e5_events(run_script):
    rng = random.Random(0)
    n = 100_000
    metrics = [f"m{i}" for i in range(20)]
    regions = ["us", "eu", "ap"]
    lines = [
        "WINDOW",
        "300 300",
        "RULES",
        "m0,region=us,count,gte,50,3,3",
        "m1,-,rate,gt,0.8,2,2,100",
        "EVENTS",
    ]
    for i in range(n):
        ts = rng.randrange(0, 50_000)
        m = rng.choice(metrics)
        label = f"region={rng.choice(regions)}"
        value = rng.uniform(0, 200)
        lines.append(f"{ts},{m},{label},{value:.2f}")
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.endswith("MALFORMED 0\n")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
