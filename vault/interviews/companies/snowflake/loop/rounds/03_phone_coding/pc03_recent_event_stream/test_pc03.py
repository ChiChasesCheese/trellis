import random

import pytest

EX1_OPS = [
    ("record", 1, "a"),
    ("record", 2, "b"),
    ("record", 3, "a"),
    ("count", 10),
    ("top",),
    ("record", 4, "a"),
    ("count", 10),
    ("top",),
]
EX1_OUT = ["2", "a", "2", "a"]

EX3_OPS = [
    ("record", 0, "a"),
    ("record", 1, "b"),
    ("record", 5, "c"),
    ("count", 10),
    ("top",),
]
EX3_OUT = ["2", "b"]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.process_recent_event_stream(EX1_OPS, m=3) == EX1_OUT


@pytest.mark.part1
def test_worked_example_2_count_based_eviction(impl):
    stream = impl.RecentEventStream(m=2)
    stream.record(1, "a")
    stream.record(2, "b")
    stream.record(3, "c")
    assert stream.top() == "b"


@pytest.mark.part1
@pytest.mark.edge
def test_empty_window_top_is_empty_string(impl):
    assert impl.RecentEventStream(m=5).top() == ""


@pytest.mark.part1
@pytest.mark.edge
def test_empty_window_count_is_zero(impl):
    assert impl.RecentEventStream(m=5).count(100) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_count_is_strictly_before(impl):
    stream = impl.RecentEventStream(m=5)
    stream.record(10, "a")
    assert stream.count(10) == 0  # not strictly before
    assert stream.count(11) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_top_tie_break_is_lexicographic_not_recency(impl):
    stream = impl.RecentEventStream(m=10)
    stream.record(1, "z")
    stream.record(2, "a")
    # both appear once -- lexicographically smallest ("a") wins, not the most-recently-added ("a"
    # happens to also be most recent here, so also test the reverse order below)
    assert stream.top() == "a"
    stream2 = impl.RecentEventStream(m=10)
    stream2.record(1, "a")
    stream2.record(2, "z")
    assert stream2.top() == "a"


@pytest.mark.part1
@pytest.mark.edge
def test_m_one_keeps_only_latest(impl):
    stream = impl.RecentEventStream(m=1)
    stream.record(1, "a")
    stream.record(2, "b")
    assert stream.top() == "b"
    assert stream.count(3) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_empty_operations(impl):
    assert impl.process_recent_event_stream([], m=3) == []


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_3_time_based_eviction(impl):
    assert impl.process_recent_event_stream_by_time(EX3_OPS, window_seconds=5) == EX3_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_time_window_boundary_is_half_open(impl):
    stream = impl.RecentEventStreamByTime(window_seconds=5)
    stream.record(0, "a")
    stream.record(5, "b")  # window (0, 5] -- ts=0 must be purged exactly at the boundary
    assert stream.count(100) == 1  # only "b" remains


@pytest.mark.part2
@pytest.mark.edge
def test_time_window_unbounded_count(impl):
    stream = impl.RecentEventStreamByTime(window_seconds=1000)
    for i in range(20):
        stream.record(i, f"k{i}")
    # all 20 fit within the window -- unlike Part1, there is no cap on event COUNT
    assert stream.count(1000) == 20


@pytest.mark.part2
@pytest.mark.edge
def test_window_zero_purges_even_same_timestamp_predecessors(impl):
    # window_seconds=0 -> boundary (ts - 0, ts] is as tight as it gets: a NEW record at the same
    # timestamp as an existing one still purges it (half-open, same "<=" convention as od04's
    # RateLimiter), and a record at any later timestamp purges everything before it.
    stream = impl.RecentEventStreamByTime(window_seconds=0)
    stream.record(5, "a")
    stream.record(5, "b")  # purges "a": window[0][0]=5 <= 5-0=5
    assert stream.count(100) == 1
    stream.record(6, "c")  # purges "b": window[0][0]=5 <= 6-0=6
    assert stream.count(100) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_empty_operations(impl):
    assert impl.process_recent_event_stream_by_time([], window_seconds=5) == []


@pytest.mark.part2
@pytest.mark.edge
def test_count_vs_time_based_divergence_from_count_based(impl):
    # same records fed to both variants can retain different sets: a tight COUNT cap can evict
    # an event a wide TIME window would still keep
    ops = [
        ("record", 0, "a"),
        ("record", 1, "b"),
        ("record", 2, "c"),
        ("count", 100),
    ]
    count_based = impl.process_recent_event_stream(ops, m=1)  # only "c" survives
    time_based = impl.process_recent_event_stream_by_time(ops, window_seconds=1000)  # all 3 survive
    assert count_based == ["1"]
    assert time_based == ["3"]


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_strings_exact(impl):
    out = impl.part1(["M 3", "RECORD 1 a", "COUNT 2", "TOP"])
    assert out == ["1", "a"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["M 3"] + [
        "RECORD 1 a",
        "RECORD 2 b",
        "RECORD 3 a",
        "COUNT 10",
        "TOP",
        "RECORD 4 a",
        "COUNT 10",
        "TOP",
    ]
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["WINDOW 5", "RECORD 0 a", "RECORD 1 b", "RECORD 5 c", "COUNT 10", "TOP"]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"


# ------------------------------------------------------------------------ perf
@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_mixed_operations(run_script):
    rng = random.Random(0)
    m = 500
    lines = [f"M {m}"]
    ts = 0
    for _ in range(100_000):
        ts += rng.randrange(0, 2)
        r = rng.random()
        if r < 0.7:
            lines.append(f"RECORD {ts} k{rng.randrange(0, 50)}")
        elif r < 0.85:
            lines.append(f"COUNT {ts + 1}")
        else:
            lines.append("TOP")
    result = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
