import random
import threading

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_basic(impl):
    out = impl.part1(["1 ADD a", "2 IN a", "3 REMOVE a", "4 IN a"])
    assert out == ["false", "true"]


@pytest.mark.part1
@pytest.mark.edge
def test_tie_break_mutation_before_input_same_timestamp(impl):
    out = impl.part1(["5 ADD b", "5 IN b"])
    assert out == ["false"]


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_order_events_sorted_by_timestamp(impl):
    out = impl.part1(["3 IN a", "1 ADD a", "2 REMOVE a"])
    assert out == ["true"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_event_list(impl):
    assert impl.process_events([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_remove_never_added_is_noop(impl):
    f = impl.BlacklistFilter()
    f.remove("ghost")  # must not raise
    assert f.offer("ghost") is True


@pytest.mark.part1
@pytest.mark.edge
def test_no_input_events_returns_empty(impl):
    assert impl.process_events([(1, "ADD", "a"), (2, "REMOVE", "a")]) == []


@pytest.mark.part1
def test_class_api_directly(impl):
    f = impl.BlacklistFilter()
    assert f.offer("a") is True
    f.add("a")
    assert f.offer("a") is False
    f.remove("a")
    assert f.offer("a") is True


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_refcount(impl):
    out = impl.part2(
        [
            "1 ADD u1 a",
            "2 ADD u2 a",
            "3 IN a",
            "4 REMOVE u1 a",
            "5 IN a",
            "6 REMOVE u2 a",
            "7 IN a",
        ]
    )
    assert out == ["false", "false", "true"]


@pytest.mark.part2
def test_worked_example_wildcard(impl):
    out = impl.part2(
        ["1 ADD u1 10.0.*", "2 IN 10.0.9.9", "3 IN 10.1.0.0", "4 REMOVE u1 10.0.*", "5 IN 10.0.9.9"]
    )
    assert out == ["false", "true", "true"]


@pytest.mark.part2
@pytest.mark.edge
def test_repeated_add_by_same_owner_is_idempotent(impl):
    out = impl.part2(["1 ADD u1 a", "2 ADD u1 a", "3 REMOVE u1 a", "4 IN a"])
    assert out == ["true"]  # a single remove undoes the repeated add


@pytest.mark.part2
@pytest.mark.edge
def test_remove_by_owner_who_never_added_is_noop(impl):
    out = impl.part2(["1 ADD u1 a", "2 REMOVE u2 a", "3 IN a"])
    assert out == ["false"]  # u1's block is still active


@pytest.mark.part2
@pytest.mark.edge
def test_exact_and_prefix_rules_coexist(impl):
    out = impl.part2(["1 ADD u1 abc", "2 ADD u2 ab*", "3 IN abc", "4 IN abz", "5 IN xyz"])
    assert out == ["false", "false", "true"]


@pytest.mark.part2
@pytest.mark.edge
def test_wildcard_does_not_match_unrelated_prefix(impl):
    out = impl.part2(["1 ADD u1 10.0.*", "2 IN 10.100.0.0"])
    assert out == ["true"]  # "10.0." is not a prefix of "10.100.0.0"


@pytest.mark.part2
def test_class_api_directly_multi_owner(impl):
    f = impl.RefCountedPatternFilter()
    f.add("u1", "x")
    f.add("u2", "x")
    assert f.offer("x") is False
    f.remove("u1", "x")
    assert f.offer("x") is False
    f.remove("u2", "x")
    assert f.offer("x") is True


# ------------------------------------------------------------------------ Part 3 (concurrency)
@pytest.mark.part3
def test_replay_sequential_matches_direct_calls(impl):
    f = impl.ThreadSafeBlacklistFilter()
    f.add("u1", "a")
    r1 = f.offer("a")
    f.remove("u1", "a")
    r2 = f.offer("a")
    log = f.linearization_log()
    replayed = impl.replay_sequential(log)
    assert replayed == [r1, r2] == [False, True]


@pytest.mark.part3
@pytest.mark.edge
def test_concurrent_add_remove_final_state_matches_sequential_replay(impl):
    """Many threads hammer add/remove concurrently on overlapping owner/pattern pairs (no offer()
    calls while racing, so the check below is unambiguous). linearization_log() records every
    mutation in the exact order it actually took effect (each append happens inside the same lock
    as the mutation itself, so seq order == real linearized order). Replaying that log
    sequentially through a fresh filter must reproduce the exact same final blocked/allowed state
    that the real, concurrently-built filter ends up in -- this is what "thread-safe" means here."""
    f = impl.ThreadSafeBlacklistFilter()
    owners = [f"owner{i}" for i in range(5)]
    values = [f"v{i}" for i in range(8)]

    def worker(seed: int):
        rng = random.Random(seed)
        for _ in range(200):
            owner = rng.choice(owners)
            value = rng.choice(values)
            if rng.random() < 0.5:
                f.add(owner, value)
            else:
                f.remove(owner, value)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    log = f.linearization_log()
    mirror = impl.RefCountedPatternFilter()
    for _seq, kind, owner, value in log:
        if kind == "ADD":
            mirror.add(owner, value)
        elif kind == "REMOVE":
            mirror.remove(owner, value)

    for value in values:
        assert f.offer(value) == mirror.offer(value), f"mismatch for {value!r}"


@pytest.mark.part3
@pytest.mark.edge
def test_concurrent_offer_calls_never_crash_and_are_boolean(impl):
    """A read-heavy mix of add/remove/offer must never raise and offer() must always return a
    plain bool, even while other threads are mutating concurrently."""
    f = impl.ThreadSafeBlacklistFilter()
    values = [f"v{i}" for i in range(6)]
    errors: list[BaseException] = []
    results: list[bool] = []
    lock = threading.Lock()

    def worker(seed: int):
        rng = random.Random(seed)
        try:
            for _ in range(200):
                action = rng.choice(["add", "remove", "offer"])
                value = rng.choice(values)
                if action == "add":
                    f.add(f"owner{seed}", value)
                elif action == "remove":
                    f.remove(f"owner{seed}", value)
                else:
                    r = f.offer(value)
                    with lock:
                        results.append(r)
        except BaseException as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert errors == []
    assert all(isinstance(r, bool) for r in results)


@pytest.mark.part3
@pytest.mark.edge
def test_concurrent_disjoint_owners_all_take_effect(impl):
    f = impl.ThreadSafeBlacklistFilter()
    n = 32

    def worker(i: int):
        f.add(f"owner{i}", f"val{i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    for i in range(n):
        assert f.offer(f"val{i}") is False


# ------------------------------------------------------------------------ fmt / perf / io
@pytest.mark.part1
@pytest.mark.fmt
def test_output_is_lowercase_true_false_strings(impl):
    out = impl.part1(["1 ADD a", "2 IN a", "2 IN b"])
    assert out == ["false", "true"]
    assert all(o in ("true", "false") for o in out)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_100000_unordered_events(run_script):
    rng = random.Random(0)
    values = [f"v{i}" for i in range(2000)]
    lines = ["PART 1"]
    for i in range(100_000):
        ts = rng.randint(0, 1_000_000)  # deliberately unsorted
        kind = rng.choice(["ADD", "REMOVE", "IN"])
        lines.append(f"{ts} {kind} {rng.choice(values)}")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"
    assert r.max_rss_mb < 256


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n1 ADD a\n2 IN a\n3 REMOVE a\n4 IN a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\ntrue\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script(
        "PART 2\n1 ADD u1 10.0.*\n2 IN 10.0.9.9\n3 IN 10.1.0.0\n4 REMOVE u1 10.0.*\n5 IN 10.0.9.9\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\ntrue\ntrue\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n0 ADD u1 a\n1 IN a\n2 REMOVE u1 a\n3 IN a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\ntrue\n"
