import random

import pytest

AGG = "BEGIN BEGIN \nBEGIN 1 1 BEGIN 0 0\n END 1 1 BEGIN"


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_verbatim(impl):
    assert impl.compute_penalty("0 0 1 0", 0) == 3
    assert impl.compute_penalty("0 0 1 0", 4) == 1
    assert [impl.compute_penalty("0 0 1 0", t) for t in range(5)] == [3, 2, 1, 2, 1]


@pytest.mark.part1
@pytest.mark.edge
def test_penalty_edges(impl):
    assert impl.compute_penalty("", 0) == 0
    assert impl.compute_penalty("1", 0) == 0 and impl.compute_penalty("1", 1) == 1
    assert impl.compute_penalty("0", 0) == 1 and impl.compute_penalty("0", 1) == 0
    assert impl.compute_penalty("1 1 1 1", 4) == 4 and impl.compute_penalty("0 0 0 0", 0) == 4
    assert impl.compute_penalty("0010", 2) == impl.compute_penalty("0 0 1 0", 2) == 1


@pytest.mark.part1
def test_part1_lines(impl):
    assert impl.part1(["0 0 1 0|0", "0 0 1 0|4", "|0"]) == ["3", "1", "0"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_best_removal(impl):
    assert impl.find_best_removal_time("0 0 1 1") == 2
    assert impl.find_best_removal_time("0 0 1 0") == 2


@pytest.mark.part2
@pytest.mark.edge
def test_best_removal_edges_and_ties(impl):
    assert impl.find_best_removal_time("") == 0
    assert impl.find_best_removal_time("0 0 0") == 3
    assert impl.find_best_removal_time("1 1 1") == 0
    assert impl.find_best_removal_time("0 1") == 1       # penalties 1,0,1 -> 1
    assert impl.find_best_removal_time("1 0") == 0       # 1,2,1 -> tie, smallest -> 0
    assert impl.find_best_removal_time("0 1 0 1") == 1   # 2,1,2,1,2 -> min 1 first at 1


@pytest.mark.part2
def test_best_removal_agrees_with_brute_force(impl):
    rng = random.Random(1)
    for _ in range(200):
        log = " ".join(rng.choice("01") for _ in range(rng.randrange(0, 12)))
        n = len(log.split())
        pens = [impl.compute_penalty(log, t) for t in range(n + 1)]
        assert impl.find_best_removal_time(log) == pens.index(min(pens))


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_aggregate_verbatim(impl):
    assert impl.get_best_removal_times(AGG) == [2]
    assert impl.get_best_removal_times("BEGIN BEGIN BEGIN 1 1 BEGIN 0 0 END 1 1 BEGIN") == [2]


@pytest.mark.part3
@pytest.mark.edge
def test_aggregate_edges(impl):
    assert impl.get_best_removal_times("") == []
    assert impl.get_best_removal_times("END 0 0 BEGIN") == []           # END without BEGIN, unfinished BEGIN
    assert impl.get_best_removal_times("BEGIN END") == [0]              # empty valid log
    assert impl.get_best_removal_times("BEGIN 0 0\n1 1 END BEGIN 1 END BEGIN 0 END") == [2, 0, 1]
    assert impl.get_best_removal_times("BEGIN 1 1 BEGIN 0 END END") == [1]  # restart; 2nd END ignored


@pytest.mark.part3
def test_part3_joins_lines(impl):
    assert impl.part3(AGG.splitlines()) == ["2"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_k_removals(impl):
    assert impl.min_penalty_k("0 1 0", 0) == 1
    assert impl.min_penalty_k("0 1 0", 1) == 0
    assert [impl.min_penalty_k("1 0 1 0 1", k) for k in (1, 2, 3)] == [2, 1, 0]


@pytest.mark.part4
@pytest.mark.edge
def test_k_edges(impl):
    assert impl.min_penalty_k("", 0) == 0 and impl.min_penalty_k("", 3) == 0
    assert impl.min_penalty_k("1 1 1", 0) == 3 and impl.min_penalty_k("1 1 1", 1) == 0
    assert impl.min_penalty_k("0 0 0", 5) == 0
    assert impl.min_penalty_k("1 0 1 0 1", 10) == 0    # k larger than needed


@pytest.mark.part4
def test_k1_never_worse_than_part2(impl):
    rng = random.Random(2)
    for _ in range(200):
        log = " ".join(rng.choice("01") for _ in range(rng.randrange(0, 12)))
        best = impl.compute_penalty(log, impl.find_best_removal_time(log))
        assert impl.min_penalty_k(log, 1) <= best
        assert impl.min_penalty_k(log, 0) == log.split().count("1")


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + AGG + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"
    assert run_script("PART 1\n0 0 1 0|0\n\n0 0 1 0|4\n").stdout == "3\n1\n"
    assert run_script("PART 4\n1 0 1 0 1|2\n").stdout == "1\n"
    assert run_script("").stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_million_hours(run_script):
    rng = random.Random(0)
    log = " ".join(rng.choice("01") for _ in range(1_000_000))
    r = run_script("PART 2\n" + log + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().isdigit()
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    agg = "\n".join("BEGIN " + " ".join(rng.choice("01") for _ in range(100)) + " END" for _ in range(5000))
    r = run_script("PART 3\n" + agg + "\n", timeout=30)
    assert r.stdout.count("\n") == 5000 and r.seconds < 2.0
