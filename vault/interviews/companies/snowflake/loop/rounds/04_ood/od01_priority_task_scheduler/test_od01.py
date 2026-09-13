import random
import threading

import pytest

EX1 = [
    "ADD 101 2 100",
    "ADD 102 5 50",
    "EXEC",
    "ADD 103 5 30",
    "EXEC",
    "EXEC",
    "EXEC",
]
EX1_OUT = ["102", "103", "101", ""]

EX2 = ["ADD a 1 0", "ADD a 5 10", "EXEC", "ADD a 9 0", "EXEC"]
EX2_OUT = ["a", ""]

EX3 = [
    "ADD x 1 0",
    "ADD y 1 1",
    "ADD x 9 5",
    "EXEC",
    "ADD x 100 0",
    "EXEC",
    "EXEC",
]
EX3_OUT = ["x", "y", ""]

EX4 = [
    "ADD a 1 0",
    "ADD b 5 0",
    "EXEC",
    "SNAPSHOT",
    "ADD c 9 0",
    "EXEC",
    "EXEC",
]
EX4_OUT = ["b", "c", "a"]


# ------------------------------------------------------------------ Part 1: priority + tie-break
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
def test_single_task(impl):
    s = impl.TaskScheduler()
    s.add("a", 1, 1)
    assert s.execute() == "a"


@pytest.mark.part1
@pytest.mark.edge
def test_empty_pool_returns_empty_string(impl):
    s = impl.TaskScheduler()
    assert s.execute() == ""


@pytest.mark.part1
@pytest.mark.edge
def test_tie_priority_breaks_on_timestamp(impl):
    s = impl.TaskScheduler()
    s.add("a", 5, 10)
    s.add("b", 5, 3)
    assert s.execute() == "b"  # earlier timestamp wins
    assert s.execute() == "a"


@pytest.mark.part1
@pytest.mark.edge
def test_tie_priority_and_timestamp_breaks_on_id_lexicographic(impl):
    s = impl.TaskScheduler()
    s.add("10", 1, 0)
    s.add("9", 1, 0)
    # lexicographic, not numeric: "10" < "9"
    assert s.execute() == "10"
    assert s.execute() == "9"


@pytest.mark.part1
@pytest.mark.edge
def test_negative_priority_and_timestamp(impl):
    s = impl.TaskScheduler()
    s.add("a", -5, -100)
    s.add("b", -1, -50)
    assert s.execute() == "b"  # -1 > -5
    assert s.execute() == "a"


@pytest.mark.part1
@pytest.mark.edge
def test_readd_before_execution_replaces_entry(impl):
    s = impl.TaskScheduler()
    s.add("a", 1, 100)
    s.add("a", 9, 0)  # replaces; a is now (priority=9, ts=0)
    s.add("b", 2, 0)
    assert s.execute() == "a"  # 9 > 2, proves the replacement took effect
    assert s.execute() == "b"


# ------------------------------------------------------------------ Part 2: duplicate-ID suppression
@pytest.mark.part2
def test_worked_example_2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
def test_worked_example_3(impl):
    assert impl.part2(EX3) == EX3_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_readd_after_execution_is_permanently_ineligible(impl):
    s = impl.TaskScheduler()
    s.add("a", 1, 0)
    assert s.execute() == "a"
    s.add("a", 1000, 0)  # highest possible priority -- must still never be selected again
    s.add("b", 1, 0)
    assert s.execute() == "b"
    assert s.execute() == ""


@pytest.mark.part2
@pytest.mark.edge
def test_queued_duplicate_becomes_ineligible_once_any_copy_executes(impl):
    s = impl.TaskScheduler()
    s.add("dup", 1, 0)
    # dup's only pending entry executes...
    assert s.execute() == "dup"
    # ...so a fresh submission of the same id must never come back
    s.add("dup", 1000, 0)
    s.add("other", 1, 0)
    assert s.execute() == "other"
    assert s.execute() == ""


# ------------------------------------------------------------------ Part 3: concurrency
@pytest.mark.part3
def test_concurrent_execute_never_double_returns_and_never_loses_a_task(impl):
    n = 500
    sched = impl.TaskScheduler()
    for i in range(n):
        sched.add(f"t{i}", priority=random.Random(i).randrange(1, 5), timestamp=i)

    results: list[str] = []
    lock = threading.Lock()

    def worker():
        while True:
            r = sched.execute()
            if r == "":
                return
            with lock:
                results.append(r)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    # exactly-once: every id appears at most once, and every submitted id was eventually claimed
    assert len(results) == len(set(results)) == n
    assert set(results) == {f"t{i}" for i in range(n)}


@pytest.mark.part3
@pytest.mark.edge
def test_concurrent_add_and_execute_no_crash_and_consistent_total(impl):
    sched = impl.TaskScheduler()
    n_add = 300
    claimed: list[str] = []
    lock = threading.Lock()

    def adder(start):
        for i in range(start, start + n_add):
            sched.add(f"c{i}", priority=i % 7, timestamp=i)

    def executor():
        misses = 0
        while misses < 50:
            r = sched.execute()
            if r == "":
                misses += 1
                continue
            misses = 0
            with lock:
                claimed.append(r)

    adders = [threading.Thread(target=adder, args=(i * n_add,)) for i in range(4)]
    executors = [threading.Thread(target=executor) for _ in range(4)]
    for t in adders + executors:
        t.start()
    for t in adders:
        t.join(timeout=10)
    for t in executors:
        t.join(timeout=10)

    # drain anything left (executors may have given up early on transient empties)
    while True:
        r = sched.execute()
        if r == "":
            break
        claimed.append(r)

    assert len(claimed) == len(set(claimed)) == 4 * n_add


# ------------------------------------------------------------------ Part 4: persistence (reconstructed)
@pytest.mark.part4
def test_worked_example_4_snapshot_replay_is_invisible(impl):
    assert impl.part4(EX4) == EX4_OUT


@pytest.mark.part4
def test_replay_empty_log(impl):
    s = impl.TaskScheduler.replay([])
    assert s.execute() == ""


@pytest.mark.part4
@pytest.mark.edge
def test_replay_preserves_executed_suppression(impl):
    s = impl.TaskScheduler()
    s.add("a", 1, 0)
    assert s.execute() == "a"
    s.add("b", 1, 0)
    log = s.snapshot()

    replayed = impl.TaskScheduler.replay(log)
    replayed.add("a", 1000, 0)  # a already executed in the log -> must stay dead
    assert replayed.execute() == "b"
    assert replayed.execute() == ""


@pytest.mark.part4
@pytest.mark.edge
def test_replayed_and_original_diverge_identically_from_shared_history(impl):
    original = impl.TaskScheduler()
    original.add("a", 3, 0)
    original.add("b", 3, 1)
    # replay the same history independently and confirm both agree on remaining behaviour
    log = ["ADD a 3 0", "ADD b 3 1"]
    replayed = impl.TaskScheduler.replay(log)
    assert original.execute() == replayed.execute() == "a"


# ------------------------------------------------------------------ fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_output_strings_exact(impl):
    out = impl.part1(["ADD a 1 0", "EXEC", "EXEC"])
    assert out == ["a", ""]  # bare id or empty string, no extra formatting


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_body_stdin(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    r = run_script("PART 4\n" + "\n".join(EX4) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_mixed_ops(run_script):
    rng = random.Random(0)
    lines = ["PART 1"]
    live_ids = []
    for i in range(100_000):
        if not live_ids or rng.random() < 0.6:
            tid = f"id{i}"
            live_ids.append(tid)
            lines.append(f"ADD {tid} {rng.randrange(1, 1000)} {i}")
        else:
            lines.append("EXEC")
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
