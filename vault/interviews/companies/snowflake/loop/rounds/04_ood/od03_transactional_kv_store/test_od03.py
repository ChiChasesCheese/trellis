import threading
import time

import pytest

EX1 = [
    "PUT a 1",
    "BEGIN",
    "PUT a 2",
    "GET a",
    "BEGIN",
    "DELETE a",
    "GET a",
    "ROLLBACK",
    "GET a",
    "COMMIT",
    "GET a",
]
EX1_OUT = ["2", "None", "True", "2", "True", "2"]

EX2 = ["GET a", "COMMIT", "ROLLBACK", "PUT a 5", "GET a"]
EX2_OUT = ["None", "False", "False", "5"]

EX3 = [
    "BEGIN",
    "PUT k 10",
    "BEGIN",
    "PUT k 20",
    "COMMIT",
    "GET k",
    "ROLLBACK",
    "GET k",
]
EX3_OUT = ["True", "20", "True", "None"]


# ------------------------------------------------------------------ Part 1: single transaction
@pytest.mark.part1
def test_worked_example_2_no_transaction(impl):
    assert impl.part1(EX2) == EX2_OUT


@pytest.mark.part1
def test_single_transaction_commit(impl):
    s = impl.TransactionalKVStore()
    s.put("a", 1)
    s.begin()
    s.put("a", 2)
    assert s.get("a") == 2
    assert s.commit() is True
    assert s.get("a") == 2


@pytest.mark.part1
def test_single_transaction_rollback(impl):
    s = impl.TransactionalKVStore()
    s.put("a", 1)
    s.begin()
    s.put("a", 2)
    assert s.rollback() is True
    assert s.get("a") == 1


@pytest.mark.part1
@pytest.mark.edge
def test_commit_rollback_without_transaction_return_false(impl):
    s = impl.TransactionalKVStore()
    assert s.commit() is False
    assert s.rollback() is False


@pytest.mark.part1
@pytest.mark.edge
def test_get_missing_or_deleted_key_returns_none(impl):
    s = impl.TransactionalKVStore()
    assert s.get("ghost") is None
    s.put("a", 1)
    s.delete("a")
    assert s.get("a") is None


# ------------------------------------------------------------------ Part 2: nested transactions
@pytest.mark.part2
def test_worked_example_1(impl):
    assert impl.part2(EX1) == EX1_OUT


@pytest.mark.part2
def test_worked_example_3_nested_commit_merges_up(impl):
    assert impl.part2(EX3) == EX3_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_rollback_inner_restores_outer_uncommitted_put(impl):
    s = impl.TransactionalKVStore()
    s.begin()
    s.put("a", 1)
    s.begin()
    s.delete("a")  # inner deletes a key the OUTER transaction (not yet committed) just put
    assert s.get("a") is None
    assert s.rollback() is True
    assert s.get("a") == 1  # restored to the outer transaction's own uncommitted value
    assert s.rollback() is True
    assert s.get("a") is None  # outer never committed -> global untouched


@pytest.mark.part2
@pytest.mark.edge
def test_deep_nesting_rollback_middle_does_not_touch_outer(impl):
    s = impl.TransactionalKVStore()
    s.begin()
    s.put("outer", "O")
    s.begin()
    s.put("mid", "M")
    s.begin()
    s.put("inner", "I")
    assert s.rollback() is True  # discard innermost only
    assert s.get("inner") is None
    assert s.get("mid") == "M"
    assert s.get("outer") == "O"
    assert s.commit() is True  # commit mid into outer
    assert s.commit() is True  # commit outer into global
    assert s.get("outer") == "O"
    assert s.get("mid") == "M"


@pytest.mark.part2
@pytest.mark.edge
def test_repeated_writes_to_same_key_in_one_transaction_rollback_once(impl):
    s = impl.TransactionalKVStore()
    s.put("a", 0)
    s.begin()
    for v in range(1, 21):
        s.put("a", v)
    s.delete("a")
    s.put("a", 999)
    assert s.rollback() is True
    assert s.get("a") == 0  # a single rollback undoes the whole transaction, not step by step


# ------------------------------------------------------------------ Part 3: per-thread stacks, concurrency
@pytest.mark.part3
def test_uncommitted_writes_invisible_to_other_threads(impl):
    s = impl.TransactionalKVStore()
    s.put("shared", 0)
    saw_uncommitted = []

    def writer():
        s.begin()
        s.put("shared", 999)
        time.sleep(0.05)  # hold the transaction open long enough for the read below
        s.commit()

    t = threading.Thread(target=writer)
    t.start()
    # while writer's transaction is open, this thread's own (uninvolved) read must see the old
    # global value -- it has no transaction of its own, so it reads straight from global state
    time.sleep(0.01)
    saw_uncommitted.append(s.get("shared"))
    t.join(timeout=2)
    assert saw_uncommitted == [0]  # never 999 before the writer's commit
    assert s.get("shared") == 999  # visible after commit


@pytest.mark.part3
def test_concurrent_disjoint_key_transactions_all_land(impl):
    s = impl.TransactionalKVStore()
    n_threads = 16

    def worker(i: int):
        s.begin()
        s.put(f"k{i}", i * 10)
        s.begin()
        s.put(f"k{i}b", i * 10 + 1)
        assert s.commit() is True
        assert s.commit() is True

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    for i in range(n_threads):
        assert s.get(f"k{i}") == i * 10
        assert s.get(f"k{i}b") == i * 10 + 1


@pytest.mark.part3
@pytest.mark.edge
def test_per_thread_stacks_are_independent(impl):
    s = impl.TransactionalKVStore()
    barrier = threading.Barrier(2)
    results = {}

    def thread_a():
        s.begin()
        s.put("x", "A")
        barrier.wait()
        results["a_sees"] = s.get("x")  # must see its own write, not thread b's

    def thread_b():
        s.begin()
        s.put("x", "B")
        barrier.wait()
        results["b_sees"] = s.get("x")

    ta, tb = threading.Thread(target=thread_a), threading.Thread(target=thread_b)
    ta.start()
    tb.start()
    ta.join(timeout=5)
    tb.join(timeout=5)
    assert results["a_sees"] == "A"
    assert results["b_sees"] == "B"


# ------------------------------------------------------------------ fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_output_strings_exact(impl):
    out = impl.part1(["GET a", "PUT a 3", "GET a", "BEGIN", "COMMIT", "ROLLBACK"])
    assert out == ["None", "3", "True", "False"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + "\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_body_stdin(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_mixed_ops(run_script):
    import random

    rng = random.Random(0)
    lines = ["PART 1"]
    depth = 0
    for i in range(100_000):
        r = rng.random()
        if r < 0.4:
            lines.append(f"PUT k{i % 500} {i}")
        elif r < 0.6:
            lines.append(f"GET k{i % 500}")
        elif r < 0.75 and depth < 20:
            lines.append("BEGIN")
            depth += 1
        elif r < 0.9 and depth > 0:
            lines.append("COMMIT")
            depth -= 1
        elif depth > 0:
            lines.append("ROLLBACK")
            depth -= 1
        else:
            lines.append(f"DELETE k{i % 500}")
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
