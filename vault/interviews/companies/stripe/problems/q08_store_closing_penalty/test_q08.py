import random

import pytest

EX3_IN = "PART 3\nBEGIN\nY Y N Y N N N Y Y N\nEND\nGARBAGE\nBEGIN\nN N Y Y Y N Y Y\nEND\n"
EX3_OUT = ["2", "8"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1_lines(impl):
    lines = ["Y Y N Y|0", "Y Y N Y|1", "Y Y N Y|2", "Y Y N Y|4", "N Y N Y|2", "Y Y Y N N N N|3", "|0"]
    assert impl.part1(lines) == ["3", "2", "1", "1", "2", "0", "0"]


@pytest.mark.part1
@pytest.mark.parametrize("log,t,want", [
    ("Y Y N Y", 0, 3), ("N Y N Y", 2, 2), ("Y Y N Y", 4, 1), ("", 0, 0), ("Y Y N", 0, 2), ("Y Y N Y", 1, 2),
    ("Y Y Y N N N N", 0, 3), ("Y Y Y N N N N", 7, 4), ("Y Y Y N N N N", 3, 0), ("Y N Y N N N N", 3, 1),
])
def test_compute_penalty_yingw787_vectors(impl, log, t, want):
    assert impl.compute_penalty(log, t) == want


@pytest.mark.part1
@pytest.mark.edge
def test_compute_penalty_ends_and_single_hour(impl):
    assert impl.compute_penalty("Y", 0) == 1 and impl.compute_penalty("Y", 1) == 0
    assert impl.compute_penalty("N", 0) == 0 and impl.compute_penalty("N", 1) == 1
    assert impl.compute_penalty("N N N N", 4) == 4 and impl.compute_penalty("Y Y Y Y", 0) == 4


@pytest.mark.part1
@pytest.mark.edge
def test_compute_penalty_unspaced_and_extra_whitespace(impl):
    assert impl.compute_penalty("YYNY", 2) == 1
    assert impl.compute_penalty("  Y   Y\tN Y ", 2) == 1
    assert impl.part1(["YYNY|2", " Y Y N Y |3"]) == ["1", "2"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2_lines(impl):
    lines = ["Y Y N Y", "Y Y N N", "N N N N", "Y Y Y Y",
             "N Y Y Y Y N N N Y N N Y Y N N N N Y Y N N Y N N N", "Y Y N N N Y Y N Y Y N N N Y Y N N Y Y Y N Y N Y Y"]
    assert impl.part2(lines) == ["2", "2", "0", "4", "5", "25"]


@pytest.mark.part2
@pytest.mark.parametrize("log,want", [
    ("Y Y N N", 2), ("Y Y Y N N N N", 3), ("", 0), ("Y", 1), ("N N N N", 0), ("Y Y Y Y", 4),
    ("N Y Y Y Y N N N Y N N Y Y N N N N Y Y N N Y N N N", 5),
    ("N N N N N Y Y Y N N N N Y Y Y N N N Y N Y Y N Y N", 0),
    ("Y Y N N N Y Y N Y Y N N N Y Y N N Y Y Y N Y N Y Y", 25),
])
def test_find_best_yingw787_vectors(impl, log, want):
    assert impl.find_best_closing_time(log) == want


@pytest.mark.part2
@pytest.mark.edge
def test_tie_goes_to_smallest_time(impl):
    assert impl.find_best_closing_time("N Y") == 0      # penalties 1,2,1 -> 0
    assert impl.find_best_closing_time("Y N") == 1      # penalties 1,0,1 -> 1
    assert impl.find_best_closing_time("N") == 0        # 0 vs 1
    assert impl.find_best_closing_time("Y N Y N") == 1  # penalties 2,1,2,1,2 -> first min at 1
    assert impl.find_best_closing_time("YYNY") == 2     # Hazeera example: 3,2,1,2,1 -> 2


@pytest.mark.part2
@pytest.mark.edge
def test_best_matches_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        hours = [rng.choice("YN") for _ in range(rng.randint(0, 12))]
        log = " ".join(hours)
        pens = [impl.compute_penalty(log, t) for t in range(len(hours) + 1)]
        assert impl.find_best_closing_time(log) == pens.index(min(pens)), log


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3_verbatim_sample(impl):
    assert impl.part3(["BEGIN", "Y Y N Y N N N Y Y N", "END", "GARBAGE", "BEGIN", "N N Y Y Y N Y Y", "END"]) == EX3_OUT


@pytest.mark.part3
def test_example4_restart_and_stray_end(impl):
    assert impl.get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END") == [2]
    assert impl.get_best_closing_times("BEGIN Y Y END \nBEGIN N N END") == [2, 0]


@pytest.mark.part3
def test_example5_invalid_empty_unfinished(impl):
    assert impl.get_best_closing_times("BEGIN Y X N END BEGIN END BEGIN Y Y END BEGIN N") == [0, 2]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_edge_tokens(impl):
    assert impl.get_best_closing_times("") == []
    assert impl.get_best_closing_times("END END Y N BEGIN") == []
    assert impl.get_best_closing_times("BEGIN END") == [0]
    assert impl.get_best_closing_times("BEGIN y n END BEGIN begin Y END BEGIN YYNY END") == [2]  # lowercase is garbage
    assert impl.get_best_closing_times("BEGIN Y END BEGIN N END junk BEGIN Y Y END") == [1, 0, 2]
    assert impl.get_best_closing_times("BEGIN Y Y END END BEGIN N BEGIN Y END") == [2, 1]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_logs_span_lines_and_share_lines(impl):
    lines = ["BEGIN Y Y", "N Y END BEGIN N N END BEGIN", "Y", "END"]
    assert impl.part3(lines) == ["2", "0", "1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script(EX3_IN)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n8\n"
    assert run_script("PART 1\nY Y N Y|2\n").stdout == "1\n"
    assert run_script("PART 2\nY Y N Y\n\nN N\n").stdout == "2\n0\n"
    assert run_script("PART 3\nBEGIN Y X END\n").stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_million_hours(run_script):
    rng = random.Random(0)
    one_log = " ".join(rng.choice("YN") for _ in range(1_000_000))
    r = run_script("PART 2\n" + one_log + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().isdigit()
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_aggregate_million_tokens(run_script):
    rng = random.Random(1)
    chunks = []
    for _ in range(2000):
        chunks.append("BEGIN " + " ".join(rng.choice("YN") for _ in range(500)) + " END" + rng.choice(["", " GARBAGE", " END"]))
    r = run_script("PART 3\n" + "\n".join(chunks) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 2000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
