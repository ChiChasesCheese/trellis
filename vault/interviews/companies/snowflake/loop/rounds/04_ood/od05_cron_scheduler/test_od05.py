import threading

import pytest

EX1 = [
    "SCHEDULE a */15 * * * *",
    "SCHEDULE b 30 9 * * *",
    "TICK 0",
    "TICK 15",
    "TICK 570",
    "TICK 571",
]
EX1_OUT = ["['a']", "['a']", "['a', 'b']", "[]"]


# ------------------------------------------------------------------ Part 1: API + tick loop
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_pause_resume_unknown_job_silently_ignored(impl):
    s = impl.CronScheduler()
    s.pause("ghost")  # must not raise
    s.resume("ghost")


@pytest.mark.part1
@pytest.mark.edge
def test_paused_job_never_fires(impl):
    s = impl.CronScheduler()
    s.schedule("a", "*/1 * * * *")
    s.pause("a")
    assert s.tick(0) == []
    s.resume("a")
    assert s.tick(1) == ["a"]  # a fresh, not-yet-claimed minute


@pytest.mark.part1
@pytest.mark.edge
def test_same_minute_not_reclaimed_on_repeated_tick(impl):
    s = impl.CronScheduler()
    s.schedule("a", "*/1 * * * *")
    assert s.tick(0) == ["a"]
    assert s.tick(0) == []  # already claimed for minute 0
    assert s.tick(1) == ["a"]  # a new minute is a fresh claim


@pytest.mark.part1
@pytest.mark.edge
def test_star_slash_1_equals_star(impl):
    s = impl.CronScheduler()
    s.schedule("a", "*/1 * * * *")
    for now in range(5):
        assert s.tick(now) == ["a"]


@pytest.mark.part1
@pytest.mark.edge
def test_star_slash_60_only_matches_top_of_hour(impl):
    s = impl.CronScheduler()
    s.schedule("a", "*/60 * * * *")
    assert s.tick(0) == ["a"]  # minute 0
    assert s.tick(30) == []  # minute 30
    assert s.tick(60) == ["a"]  # minute 0 again (next hour)


@pytest.mark.part1
@pytest.mark.edge
def test_reschedule_resets_pause_state(impl):
    s = impl.CronScheduler()
    s.schedule("a", "*/1 * * * *")
    s.pause("a")
    s.schedule("a", "*/1 * * * *")  # re-registering -> unpaused per problem.md
    assert s.tick(100) == ["a"]


# ------------------------------------------------------------------ Part 2: pause-vs-claim race
@pytest.mark.part2
def test_concurrent_tick_claims_job_exactly_once(impl):
    s = impl.CronScheduler()
    s.schedule("job", "*/1 * * * *")
    n_threads = 20
    all_results: list[str] = []
    lock = threading.Lock()

    def worker():
        r = s.tick(100)
        with lock:
            all_results.extend(r)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    assert all_results.count("job") == 1


@pytest.mark.part2
@pytest.mark.edge
def test_concurrent_tick_across_many_minutes_no_duplicate_claims(impl):
    s = impl.CronScheduler()
    s.schedule("job", "*/1 * * * *")
    claims: list[tuple[int, str]] = []
    lock = threading.Lock()

    def worker(minute: int):
        for _ in range(5):  # each thread re-ticks the same minute several times
            for job_id in s.tick(minute):
                with lock:
                    claims.append((minute, job_id))

    minutes = list(range(10))
    threads = [threading.Thread(target=worker, args=(m,)) for m in minutes for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    assert sorted(claims) == [(m, "job") for m in minutes]  # each minute claimed exactly once


# ------------------------------------------------------------------ Part 3: multi-instance lease
@pytest.mark.part3
def test_two_instances_share_lease_store_never_double_fire(impl):
    shared = impl.LeaseStore()
    s1 = impl.CronScheduler(lease_store=shared)
    s2 = impl.CronScheduler(lease_store=shared)
    s1.schedule("job", "*/1 * * * *")
    s2.schedule("job", "*/1 * * * *")

    results: list[str] = []
    lock = threading.Lock()

    def run(scheduler):
        r = scheduler.tick(200)
        with lock:
            results.extend(r)

    t1 = threading.Thread(target=run, args=(s1,))
    t2 = threading.Thread(target=run, args=(s2,))
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)

    assert results.count("job") == 1


@pytest.mark.part3
@pytest.mark.edge
def test_two_instances_many_ticks_each_minute_fired_once_total(impl):
    shared = impl.LeaseStore()
    schedulers = [impl.CronScheduler(lease_store=shared) for _ in range(3)]
    for s in schedulers:
        s.schedule("job", "*/1 * * * *")

    claims: list[tuple[int, str]] = []
    lock = threading.Lock()

    def worker(scheduler, minute):
        for job_id in scheduler.tick(minute):
            with lock:
                claims.append((minute, job_id))

    threads = [
        threading.Thread(target=worker, args=(s, m)) for m in range(5) for s in schedulers
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    assert sorted(claims) == [(m, "job") for m in range(5)]


@pytest.mark.part3
def test_lease_store_independent_of_pause_state_per_instance(impl):
    # a job paused on one instance can still be claimed via the other instance's tick
    shared = impl.LeaseStore()
    s1 = impl.CronScheduler(lease_store=shared)
    s2 = impl.CronScheduler(lease_store=shared)
    s1.schedule("job", "*/1 * * * *")
    s2.schedule("job", "*/1 * * * *")
    s1.pause("job")
    assert s1.tick(0) == []
    assert s2.tick(0) == ["job"]


# ------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_tick_output_is_sorted_python_list_repr(impl):
    out = impl.part1(
        ["SCHEDULE b */1 * * * *", "SCHEDULE a */1 * * * *", "TICK 0"]
    )
    assert out == ["['a', 'b']"]  # sorted regardless of schedule order


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


@pytest.mark.part1
@pytest.mark.perf
def test_perf_many_jobs_many_ticks(run_script):
    n_jobs = 2000
    lines = ["PART 1"] + [f"SCHEDULE j{i} */{(i % 30) + 1} * * * *" for i in range(n_jobs)]
    lines += [f"TICK {t}" for t in range(200)]
    result = run_script("\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n") == 200
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
