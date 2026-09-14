import random

import pytest

EX1_SERVICES = ["db", "cache", "api", "auth"]
EX1_DEPS = [("api", "db"), ("api", "cache"), ("cache", "db"), ("auth", "db")]


def _valid_topo_order(services, deps, order):
    if sorted(order) != sorted(services):
        return False
    pos = {s: i for i, s in enumerate(order)}
    return all(pos[s] > pos[d] for s, d in deps)


def _has_cycle_brute(services, deps):
    requires = {s: set() for s in services}
    for s, d in deps:
        requires[s].add(d)
    color = {s: 0 for s in services}

    def dfs(u):
        color[u] = 1
        for v in requires[u]:
            if color[v] == 1:
                return True
            if color[v] == 0 and dfs(v):
                return True
        color[u] = 2
        return False

    return any(dfs(s) for s in services if color[s] == 0)


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.startup_order(EX1_SERVICES, EX1_DEPS) == ["db", "auth", "cache", "api"]


@pytest.mark.part1
def test_worked_example_3_no_deps_lexicographic(impl):
    assert impl.startup_order(["zeta", "alpha", "beta"], []) == ["alpha", "beta", "zeta"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_services(impl):
    assert impl.startup_order([], []) == []


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_services_raises(impl):
    with pytest.raises(ValueError):
        impl.startup_order(["a", "a"], [])


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_dependency_raises(impl):
    with pytest.raises(ValueError):
        impl.startup_order(["a", "b"], [("a", "x")])


@pytest.mark.part1
@pytest.mark.edge
def test_self_dependency_raises(impl):
    with pytest.raises(ValueError):
        impl.startup_order(["a"], [("a", "a")])


@pytest.mark.part1
@pytest.mark.edge
def test_simple_cycle_reports_exact_members(impl):
    with pytest.raises(impl.CycleError) as exc:
        impl.startup_order(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    assert sorted(exc.value.cycle) == ["a", "b", "c"]


@pytest.mark.part1
@pytest.mark.edge
def test_cycle_excludes_services_merely_waiting_on_it(impl):
    services = ["a", "b", "c", "d", "e"]
    deps = [("b", "c"), ("c", "d"), ("d", "b"), ("e", "d")]
    with pytest.raises(impl.CycleError) as exc:
        impl.startup_order(services, deps)
    assert set(exc.value.cycle) == {"b", "c", "d"}
    assert "a" not in exc.value.cycle
    assert "e" not in exc.value.cycle


@pytest.mark.part1
@pytest.mark.edge
def test_random_dag_produces_valid_deterministic_order(impl):
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(0, 7)
        services = [f"s{i}" for i in range(n)]
        deps = [(services[i], services[j]) for i in range(n) for j in range(i) if rng.random() < 0.4]
        order = impl.startup_order(services, deps)
        assert _valid_topo_order(services, deps, order), (services, deps, order)
        # determinism: same input, same output
        assert impl.startup_order(services, deps) == order


@pytest.mark.part1
@pytest.mark.edge
def test_random_graphs_cycle_detection_matches_brute_force(impl):
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(1, 6)
        services = [f"s{i}" for i in range(n)]
        deps = [(services[i], services[j]) for i in range(n) for j in range(n) if i != j and rng.random() < 0.25]
        has_cycle = _has_cycle_brute(services, deps)
        if has_cycle:
            with pytest.raises(impl.CycleError):
                impl.startup_order(services, deps)
        else:
            order = impl.startup_order(services, deps)
            assert _valid_topo_order(services, deps, order)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_5000_services(run_script):
    rng = random.Random(0)
    n = 5000
    services = [f"s{i}" for i in range(n)]
    deps = []
    for i in range(1, n):
        for j in rng.sample(range(i), min(i, 3)):
            deps.append((services[i], services[j]))
    lines = [f"S {n}", *services, f"D {len(deps)}", *[f"{a} {b}" for a, b in deps]]
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    assert impl.startup_waves(EX1_SERVICES, EX1_DEPS) == [["db"], ["auth", "cache"], ["api"]]


@pytest.mark.part2
def test_part2_no_deps_single_wave(impl):
    assert impl.startup_waves(["zeta", "alpha", "beta"], []) == [["alpha", "beta", "zeta"]]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_cycle_raises(impl):
    with pytest.raises(impl.CycleError):
        impl.startup_waves(["a", "b"], [("a", "b"), ("b", "a")])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_waves_partition_and_respect_deps(impl):
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(0, 7)
        services = [f"s{i}" for i in range(n)]
        deps = [(services[i], services[j]) for i in range(n) for j in range(i) if rng.random() < 0.4]
        waves = impl.startup_waves(services, deps)
        flat = [s for wave in waves for s in wave]
        assert sorted(flat) == sorted(services)
        wave_of = {s: i for i, wave in enumerate(waves) for s in wave}
        assert all(wave_of[s] > wave_of[d] for s, d in deps)
        assert all(wave == sorted(wave) for wave in waves)


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    lines = ["S 4", *EX1_SERVICES, "D 4", "api db", "api cache", "cache db", "auth db"]
    assert impl.part2(lines) == ["db", "auth cache", "api"]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_example(impl):
    services = ["db", "cache", "api"]
    deps = [("api", "db"), ("api", "cache"), ("cache", "db")]
    duration = {"db": 5, "cache": 3, "api": 2}
    assert impl.startup_times(services, deps, duration) == ({"db": 0, "cache": 5, "api": 8}, 10)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_deps_all_start_at_zero(impl):
    services = ["a", "b"]
    start, overall = impl.startup_times(services, [], {"a": 3, "b": 7})
    assert start == {"a": 0, "b": 0}
    assert overall == 7


@pytest.mark.part3
@pytest.mark.edge
def test_part3_duration_mismatch_raises(impl):
    with pytest.raises(ValueError):
        impl.startup_times(["a", "b"], [], {"a": 1})
    with pytest.raises(ValueError):
        impl.startup_times(["a"], [], {"a": 1, "b": 2})


@pytest.mark.part3
@pytest.mark.edge
def test_part3_negative_duration_raises(impl):
    with pytest.raises(ValueError):
        impl.startup_times(["a"], [], {"a": -1})


@pytest.mark.part3
@pytest.mark.edge
def test_part3_cycle_raises(impl):
    with pytest.raises(impl.CycleError):
        impl.startup_times(["a", "b"], [("a", "b"), ("b", "a")], {"a": 1, "b": 1})


@pytest.mark.part3
@pytest.mark.edge
def test_part3_empty(impl):
    assert impl.startup_times([], [], {}) == ({}, 0)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_random_matches_brute_force_finish(impl):
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 6)
        services = [f"s{i}" for i in range(n)]
        deps = [(services[i], services[j]) for i in range(n) for j in range(i) if rng.random() < 0.4]
        duration = {s: rng.randint(0, 9) for s in services}
        start, overall = impl.startup_times(services, deps, duration)
        requires = {s: [] for s in services}
        for s, d in deps:
            requires[s].append(d)
        memo = {}

        def finish(s):
            if s in memo:
                return memo[s]
            st = max((finish(d) for d in requires[s]), default=0)
            memo[s] = st + duration[s]
            return memo[s]

        expected_overall = max((finish(s) for s in services), default=0)
        assert overall == expected_overall
        for s in services:
            assert start[s] == max((finish(d) for d in requires[s]), default=0)


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nS 4\ndb\ncache\napi\nauth\nD 4\napi db\napi cache\ncache db\nauth db\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "db\nauth\ncache\napi\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1_cycle(run_script):
    r = run_script("PART 1\nS 3\na\nb\nc\nD 3\na b\nb c\nc a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "CYCLE a b c\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script(
        "PART 3\nS 3\ndb\ncache\napi\nD 3\napi db\napi cache\ncache db\nT 3\ndb 5\ncache 3\napi 2\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "10\napi 8\ncache 5\ndb 0\n"
