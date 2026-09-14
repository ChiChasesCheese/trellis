import random

import pytest

WORKERS = ["WORKERS", "w1,python;go,10", "w2,python,5", "w3,go,3"]
TASKS = ["TASKS", "t1,python,5", "t2,go,3", "t3,python,4", "t4,go,1"]
EX = WORKERS + TASKS
EX1_OUT = ["t1 -> w1", "t2 -> w2", "t3 -> w3", "t4 -> w2", "w1 5", "w2 4", "w3 4"]
EX2_OUT = ["t1 -> w1", "t2 -> w3", "t3 -> w2", "t4 -> w3", "w1 5", "w2 4", "w3 4"]
EX3_OUT = ["t1 -> w2", "t2 -> w3", "t3 -> w1", "t4 -> w3", "w1 4", "w2 5", "w3 4"]
EX4 = EX + ["t5,rust,1", "t6,go,9"]
EX4_OUT = ["t1 -> w2", "t2 -> w3", "t3 -> w1", "t4 -> w1", "t5 -> UNASSIGNED", "t6 -> UNASSIGNED",
           "w1 5", "w2 5", "w3 3"]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(EX) == EX1_OUT


@pytest.mark.part1
@pytest.mark.fmt
def test_ties_are_string_order_and_load_updates(impl):
    lines = ["WORKERS", "w2,a,100", "w10,a,100", "w1,a,100", "TASKS", "t1,a,1", "t2,a,1", "t3,a,1", "t4,a,5", "t5,a,1"]
    assert impl.part1(lines) == ["t1 -> w1", "t2 -> w10", "t3 -> w2", "t4 -> w1", "t5 -> w10",
                                 "w1 6", "w10 2", "w2 1"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_ignores_skills_and_capacity_zero_cost_and_empties(impl):
    assert impl.part1(["WORKERS", "w,none,0", "TASKS", "t,python,7", "u,go,0"]) == ["t -> w", "u -> w", "w 7"]
    assert impl.part1(["WORKERS", "b,x,1", "a,x,1", "TASKS"]) == ["a 0", "b 0"]
    assert impl.part1(["WORKERS", "TASKS", "t,x,1"]) == ["t -> UNASSIGNED"]
    assert impl.part1([]) == []


@pytest.mark.part1
def test_whitespace_tolerance(impl):
    lines = ["", " WORKERS ", " w1 , python ; go , 10 ", "TASKS", " t1 , go , 2 ", ""]
    assert impl.part1(lines) == ["t1 -> w1", "w1 2"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(EX) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_skill_unassigned_and_case_sensitive(impl):
    lines = ["WORKERS", "w1,Python,10", "w2,python,10", "TASKS", "t1,python,1", "t2,rust,1", "t3,Python,1", "t4,python,1"]
    assert impl.part2(lines) == ["t1 -> w2", "t2 -> UNASSIGNED", "t3 -> w1", "t4 -> w2", "w1 1", "w2 2"]


@pytest.mark.part2
@pytest.mark.edge
def test_skill_filter_then_least_load_and_ties(impl):
    lines = ["WORKERS", "gen,a;b;c,99", "spec,a,99", "TASKS", "t1,b,4", "t2,a,1", "t3,a,1", "t4,a,3", "t5,c,1"]
    # t1 -> gen (only b). t2 -> spec (0<4). t3 -> spec (1<4). t4 -> spec (2<4). t5 -> gen.
    assert impl.part2(lines) == ["t1 -> gen", "t2 -> spec", "t3 -> spec", "t4 -> spec", "t5 -> gen",
                                 "gen 5", "spec 5"]
    # equal load -> id order regardless of skill count in Part 2
    lines = ["WORKERS", "b,a,9", "a,a;x;y,9", "TASKS", "t,a,1"]
    assert impl.part2(lines) == ["t -> a", "a 1", "b 0"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(EX) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_specialist_only_breaks_equal_load_and_duplicate_skills_count_once(impl):
    lines = ["WORKERS", "a,x;y;z,9", "b,x,9", "TASKS", "t1,x,1", "t2,x,5", "t3,x,1"]
    # t1: both 0 -> b (1 skill). t2: a 0 < b 1 -> a. t3: b 1 < a 5 -> b
    assert impl.part3(lines) == ["t1 -> b", "t2 -> a", "t3 -> b", "a 5", "b 2"]
    lines = ["WORKERS", "a,x;x;x,9", "b,x;y,9", "TASKS", "t1,x,1"]
    assert impl.part3(lines) == ["t1 -> a", "a 1", "b 0"]        # a has 1 distinct skill


@pytest.mark.part3
@pytest.mark.edge
def test_specialist_tie_then_id(impl):
    lines = ["WORKERS", "z,x,9", "y,x,9", "m,x;q,9", "TASKS", "t1,x,0", "t2,x,0", "t3,x,0"]
    assert impl.part3(lines) == ["t1 -> y", "t2 -> y", "t3 -> y", "m 0", "y 0", "z 0"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_part4(impl):
    assert impl.part4(EX4) == EX4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_capacity_boundary_exact_one_over_and_zero(impl):
    lines = ["WORKERS", "w,x,10", "TASKS", "t1,x,10", "t2,x,0", "t3,x,1"]
    assert impl.part4(lines) == ["t1 -> w", "t2 -> w", "t3 -> UNASSIGNED", "w 10"]   # == ok, +1 not
    lines = ["WORKERS", "w,x,0", "TASKS", "t1,x,1", "t2,x,0"]
    assert impl.part4(lines) == ["t1 -> UNASSIGNED", "t2 -> w", "w 0"]


@pytest.mark.part4
@pytest.mark.edge
def test_least_loaded_does_not_fit_but_busier_does(impl):
    lines = ["WORKERS", "small,x,3", "big,x,100", "TASKS", "t1,x,3", "t2,x,3", "t3,x,50", "t4,x,50", "t5,x,1"]
    # t1: both load 0, 1 skill each -> id order -> big (3). t2: small 0 < big 3 -> small (3).
    # t3: small is least loaded but 3+50 > 3 -> big (53). t4: big 53+50 > 100, small no -> UNASSIGNED.
    # t5: big 53 vs small 3 -> small? 3+1 > 3 -> does not fit -> big (54).
    assert impl.part4(lines) == ["t1 -> big", "t2 -> small", "t3 -> big", "t4 -> UNASSIGNED", "t5 -> big",
                                 "big 54", "small 3"]


@pytest.mark.part4
@pytest.mark.edge
def test_unassigned_keeps_pool_intact_for_later_tasks(impl):
    lines = ["WORKERS", "a,x,5", "b,x,5", "TASKS", "t1,x,6", "t2,x,5", "t3,x,5", "t4,x,1"]
    assert impl.part4(lines) == ["t1 -> UNASSIGNED", "t2 -> a", "t3 -> b", "t4 -> UNASSIGNED", "a 5", "b 5"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 4\n" + "\n".join(EX4) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX4_OUT) + "\n"
    r = run_script("PART 1\n" + "\n".join(EX) + "\n")
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_tasks_1000_workers(run_script):
    rng = random.Random(0)
    skills = [f"s{i}" for i in range(20)]
    workers = [f"w{i},{';'.join(rng.sample(skills, rng.randrange(1, 4)))},{rng.randrange(10 ** 6, 10 ** 7)}" for i in range(1000)]
    tasks = [f"t{i},{rng.choice(skills)},{rng.randrange(0, 100)}" for i in range(100_000)]
    text = "PART 4\nWORKERS\n" + "\n".join(workers) + "\nTASKS\n" + "\n".join(tasks) + "\n"
    r = run_script(text, timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 101_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256
