import random
import time

import pytest

EX1 = [
    "RECORD q1 10 orders orders.id",
    "RECORD q2 20 orders -",
    "RECORD q3 15 customers -",
    "RANGE orders 0 100",
    "RANGE orders 11 100",
    "RANGE orders.id 0 100",
    "RANGE customers 0 12",
]
EX1_OUT = ["['q1', 'q2']", "['q2']", "['q1']", "[]"]

EX2 = [
    "RECORD q1 10 a -",
    "RECORD q2 20 b -",
    "RECORD q3 25 a -",
    "UNSINCE 15",
    "UNSINCE 21",
    "UNSINCE 26",
]
EX2_OUT = ["[]", "['b']", "['a', 'b']"]


# ------------------------------------------------------------------ Part 1: record + range query
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_never_accessed_name_returns_empty(impl):
    log = impl.QueryAuditLog()
    assert log.accessed_in_range("ghost", 0, 100) == []


@pytest.mark.part1
@pytest.mark.edge
def test_repeated_access_same_name_appears_multiple_times(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 5, {"a"}, set())
    log.record_access("q1", 6, {"a"}, set())
    assert log.accessed_in_range("a", 0, 10) == ["q1", "q1"]


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_order_ts_still_sorted_in_result(impl):
    log = impl.QueryAuditLog()
    log.record_access("late", 30, {"a"}, set())
    log.record_access("early", 5, {"a"}, set())
    log.record_access("mid", 15, {"a"}, set())
    assert log.accessed_in_range("a", 0, 100) == ["early", "mid", "late"]


@pytest.mark.part1
@pytest.mark.edge
def test_ties_broken_by_query_id_lexicographic(impl):
    log = impl.QueryAuditLog()
    log.record_access("zeta", 10, {"a"}, set())
    log.record_access("alpha", 10, {"a"}, set())
    assert log.accessed_in_range("a", 10, 10) == ["alpha", "zeta"]


@pytest.mark.part1
@pytest.mark.edge
def test_range_boundaries_inclusive(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 10, {"a"}, set())
    assert log.accessed_in_range("a", 10, 10) == ["q1"]
    assert log.accessed_in_range("a", 0, 9) == []
    assert log.accessed_in_range("a", 11, 20) == []


@pytest.mark.part1
@pytest.mark.edge
def test_inverted_range_returns_empty_no_exception(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 10, {"a"}, set())
    assert log.accessed_in_range("a", 20, 5) == []


# ------------------------------------------------------------------ Part 2: unaccessed_since + efficiency
@pytest.mark.part2
def test_worked_example_2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_never_accessed_name_excluded_from_unaccessed(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 5, {"a"}, set())
    assert "ghost" not in log.unaccessed_since(1000)


@pytest.mark.part2
@pytest.mark.edge
def test_unaccessed_since_strict_less_than(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 10, {"a"}, set())
    assert log.unaccessed_since(10) == set()  # ts == t does not count as "before t"
    assert log.unaccessed_since(11) == {"a"}


@pytest.mark.part2
@pytest.mark.edge
def test_unaccessed_since_uses_most_recent_access(impl):
    log = impl.QueryAuditLog()
    log.record_access("q1", 5, {"a"}, set())
    log.record_access("q2", 50, {"a"}, set())  # a's most recent access is now 50
    assert log.unaccessed_since(10) == set()  # not stale -- most recent (50) is way past 10
    assert log.unaccessed_since(51) == {"a"}


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.perf
def test_perf_100k_records_10k_queries(run_script):
    rng = random.Random(0)
    n_names = 2000
    lines = ["PART 2"]
    for i in range(100_000):
        name = f"t{rng.randrange(n_names)}"
        lines.append(f"RECORD q{i} {i} {name} -")
    for i in range(10_000):
        name = f"t{rng.randrange(n_names)}"
        if i % 2 == 0:
            lo = rng.randrange(0, 100_000)
            hi = lo + rng.randrange(0, 1000)
            lines.append(f"RANGE {name} {lo} {hi}")
        else:
            lines.append(f"UNSINCE {rng.randrange(0, 100_000)}")
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 10_000
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"


@pytest.mark.part2
@pytest.mark.perf
def test_direct_api_perf_is_not_a_full_scan(impl):
    # sanity: a single unaccessed_since call after many records shouldn't be O(total records)
    log = impl.QueryAuditLog()
    for i in range(50_000):
        log.record_access(f"q{i}", i, {f"name{i % 500}"}, set())
    t0 = time.perf_counter()
    result = log.unaccessed_since(49_999)
    elapsed = time.perf_counter() - t0
    # 500 distinct names (i % 500), each hit 100 times; name{499}'s last access is exactly
    # 49999 (== t, not < t, so excluded); every other name's last access is < 49999
    assert len(result) == 499
    assert elapsed < 1.0, f"too slow for a single query: {elapsed:.3f}s"


# ------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_range_output_is_python_list_repr(impl):
    out = impl.part1(["RECORD q1 1 a -", "RANGE a 0 5"])
    assert out == ["['q1']"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX2_OUT) + "\n"
