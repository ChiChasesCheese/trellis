import random

import pytest

EXAMPLE = [
    "alice,10.00,1030",
    "bob,5.00,2000",
    "alice,12.00,1000",
    "alice,8.00,1050",
    "bob,5.00,2000",
    "alice,9.00,1015",
    "carol,1.00,3000",
    "bob,5.00,2000",
    "bob,5.00,2000",
]
EXAMPLE_PART1_OUT = ["alice", "bob"]
EXAMPLE_PART2_OUT = ["alice: 4 in [1000, 1050]", "bob: 4 in [2000, 2000]"]

DAVE = ["dave,1.00,0", "dave,1.00,20", "dave,1.00,40", "dave,1.00,101"]


# ---------------------------------------------------------------- Part 1: naive detection
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EXAMPLE) == EXAMPLE_PART1_OUT


@pytest.mark.part1
def test_exactly_3_not_suspicious(impl):
    # 3 transactions spanning 40s, then a 4th too far away to ever join a 4-in-a-row window
    assert impl.part1(DAVE) == []


@pytest.mark.part1
def test_exactly_60s_apart_is_suspicious(impl):
    lines = ["u,1.00,0", "u,1.00,20", "u,1.00,40", "u,1.00,60"]
    assert impl.part1(lines) == ["u"]


@pytest.mark.part1
@pytest.mark.edge
def test_span_61s_excludes_boundary_and_stays_not_suspicious(impl):
    lines = ["u,1.00,0", "u,1.00,20", "u,1.00,40", "u,1.00,61"]
    assert impl.part1(lines) == []


@pytest.mark.part1
@pytest.mark.edge
def test_fewer_than_4_total_never_suspicious(impl):
    lines = ["u,1.00,0", "u,1.00,1", "u,1.00,2"]
    assert impl.part1(lines) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input(impl):
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_order_within_single_user(impl):
    shuffled = ["u,1.00,40", "u,1.00,0", "u,1.00,30", "u,1.00,10"]
    assert impl.part1(shuffled) == ["u"]


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_is_plain_string_order(impl):
    lines = []
    for user in ["user2", "user10", "B", "a"]:
        for t in (0, 10, 20, 30):
            lines.append(f"{user},1.00,{t}")
    assert impl.part1(lines) == ["B", "a", "user10", "user2"]


# ---------------------------------------------------------------- Part 2: O(n log n), window report
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EXAMPLE) == EXAMPLE_PART2_OUT


@pytest.mark.part2
def test_not_suspicious_matches_part1_on_dave(impl):
    assert impl.part2(DAVE) == []


@pytest.mark.part2
@pytest.mark.edge
def test_duplicate_timestamps_collapse_to_point_window(impl):
    lines = ["u,1.00,500" for _ in range(5)]  # 5 transactions, all at t=500
    # first trigger fires as soon as the 4th one is seen -> count 4, not 5
    assert impl.part2(lines) == ["u: 4 in [500, 500]"]


@pytest.mark.part2
@pytest.mark.edge
def test_first_trigger_not_largest_or_last(impl):
    early = ["u,1.00,0", "u,1.00,10", "u,1.00,20", "u,1.00,30"]
    later_denser = [f"u,1.00,{1000 + i * 10}" for i in range(5)]
    lines = early + later_denser
    # the early, smaller burst triggers first (t=30) -- report that, not the later 5-in-a-row
    assert impl.part2(lines) == ["u: 4 in [0, 30]"]


@pytest.mark.part2
@pytest.mark.edge
def test_span_61s_never_triggers_in_part2_either(impl):
    lines = ["u,1.00,0", "u,1.00,20", "u,1.00,40", "u,1.00,61"]
    assert impl.part2(lines) == []


@pytest.mark.part2
@pytest.mark.fmt
def test_exact_output_format_string(impl):
    lines = ["z,1.00,0", "z,1.00,10", "z,1.00,20", "z,1.00,30"]
    assert impl.part2(lines) == ["z: 4 in [0, 30]"]


@pytest.mark.part2
def test_multiple_users_independent_and_sorted(impl):
    lines = (
        ["b,1.00,0", "b,1.00,10", "b,1.00,20", "b,1.00,30"]
        + ["a,1.00,0", "a,1.00,10", "a,1.00,20", "a,1.00,30"]
        + ["c,1.00,0"]
    )
    assert impl.part2(lines) == ["a: 4 in [0, 30]", "b: 4 in [0, 30]"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + "\n".join(EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EXAMPLE_PART2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_empty_when_none_suspicious(run_script):
    r = run_script("PART 1\n" + "\n".join(DAVE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_1m_rows(run_script):
    rng = random.Random(0)
    n_users = 200_000
    lines = []
    for _ in range(1_000_000):
        user = f"user{rng.randrange(n_users)}"
        ts = rng.randrange(0, 10_000_000)
        amount = f"{rng.randrange(1, 10000) / 100:.2f}"
        lines.append(f"{user},{amount},{ts}")
    # a deterministic marker burst mixed into the random noise: proves the scan actually ran and
    # found the right answer at scale, not just "didn't crash" (a broken always-[] stub would also
    # pass a timing/memory-only perf check)
    lines += [f"perf_marker,1.00,{t}" for t in (0, 10, 20, 30)]
    r = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert "perf_marker: 4 in [0, 30]" in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
