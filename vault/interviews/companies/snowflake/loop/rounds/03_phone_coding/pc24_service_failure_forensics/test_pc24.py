import random

import pytest

LOGS = [
    "2026-09-01T00:00:00 auth INFO started",
    "2026-09-01T00:01:00 auth WARN slow_response",
    "2026-09-01T00:02:00 db ERROR connection_refused",
    "2026-09-01T00:03:00 auth ERROR timeout",
    "2026-09-01T00:04:00 cache INFO ok",
]


def _brute_first_error_at_or_after(logs, ts):
    for i, line in enumerate(logs):
        line_ts, _, level, _ = (line.split(" ", 3) + [""])[:4]
        if line_ts >= ts and level == "ERROR":
            return i
    return -1


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_examples_part1(impl):
    assert impl.first_error_at_or_after(LOGS, "2026-09-01T00:00:00") == 2
    assert impl.first_error_at_or_after(LOGS, "2026-09-01T00:01:30") == 2
    assert impl.first_error_at_or_after(LOGS, "2026-09-01T00:04:30") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_no_errors_at_all(impl):
    logs = [l for l in LOGS if " ERROR " not in l]
    assert impl.first_error_at_or_after(logs, "2026-09-01T00:00:00") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_ts_before_everything(impl):
    assert impl.first_error_at_or_after(LOGS, "2020-01-01T00:00:00") == 2


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_timestamps(impl):
    logs = [
        "2026-01-01T00:00:00 a INFO x",
        "2026-01-01T00:00:00 b INFO y",
        "2026-01-01T00:00:00 c ERROR z",
        "2026-01-01T00:00:01 d INFO w",
    ]
    assert impl.first_error_at_or_after(logs, "2026-01-01T00:00:00") == 2


@pytest.mark.part1
@pytest.mark.edge
def test_bad_level_raises(impl):
    with pytest.raises(ValueError):
        impl.first_error_at_or_after(["2026-01-01T00:00:00 a BAD msg"], "2026-01-01T00:00:00")


@pytest.mark.part1
@pytest.mark.edge
def test_agrees_with_brute_force_random(impl):
    rng = random.Random(0)
    levels = ["INFO", "WARN", "ERROR"]
    logs = []
    for i in range(500):
        ts = f"2026-01-01T{i:06d}"
        logs.append(f"{ts} svc{i % 7} {rng.choice(levels)} msg {i}")
    for _ in range(200):
        q = f"2026-01-01T{rng.randint(-50, 550):06d}"
        assert impl.first_error_at_or_after(logs, q) == _brute_first_error_at_or_after(logs, q), q


# ------------------------------------------------------------------------ Part 2
EDGES = ["auth db", "cache auth", "api auth"]


@pytest.mark.part2
def test_worked_examples_part2(impl):
    assert impl.services_that_will_fail(EDGES, "db") == ["db", "auth", "cache", "api"]
    assert impl.services_that_will_fail(EDGES, "auth") == ["auth", "cache", "api"]


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_initial_failure_raises(impl):
    with pytest.raises(ValueError):
        impl.services_that_will_fail(EDGES, "nope")


@pytest.mark.part2
@pytest.mark.edge
def test_diamond_dependency_no_duplicates(impl):
    edges = ["a b", "c b", "d a", "d c"]  # d depends on a and c; both depend on b
    result = impl.services_that_will_fail(edges, "b")
    assert sorted(result) == ["a", "b", "c", "d"]
    assert len(result) == len(set(result))
    assert result[0] == "b"


@pytest.mark.part2
@pytest.mark.edge
def test_self_dependency_terminates(impl):
    result = impl.services_that_will_fail(["a a"], "a")
    assert result == ["a"]


@pytest.mark.part2
@pytest.mark.edge
def test_leaf_failure_does_not_affect_upstream(impl):
    # api and cache depend on auth, which depends on db. failing "api" (a leaf) affects only api.
    assert impl.services_that_will_fail(EDGES, "api") == ["api"]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_examples_part3(impl):
    edges = ["auth db", "cache auth", "api auth", "billing api"]
    assert impl.longest_failure_chain(edges) == ["db", "auth", "api", "billing"]


@pytest.mark.part3
@pytest.mark.edge
def test_cycle_raises(impl):
    with pytest.raises(ValueError):
        impl.longest_failure_chain(["a b", "b c", "c a"])


@pytest.mark.part3
@pytest.mark.edge
def test_self_loop_is_a_cycle(impl):
    with pytest.raises(ValueError):
        impl.longest_failure_chain(["a a"])


@pytest.mark.part3
@pytest.mark.edge
def test_empty_edges_raises(impl):
    with pytest.raises(ValueError):
        impl.longest_failure_chain([])


@pytest.mark.part3
@pytest.mark.edge
def test_tie_break_lexicographic(impl):
    # two length-2 chains from independent roots: a->x and b->y. "a x" < "b y" lexicographically.
    edges = ["x a", "y b"]
    assert impl.longest_failure_chain(edges) == ["a", "x"]


@pytest.mark.part3
def test_longest_chain_against_brute_force_dag(impl):
    import itertools

    rng = random.Random(1)
    for _ in range(60):
        nodes = [f"s{i}" for i in range(rng.randint(2, 7))]
        order = nodes[:]
        rng.shuffle(order)
        # build a random DAG respecting `order` (edges only go from later to earlier in `order`,
        # i.e. b (earlier) -> a (later) meaning a depends on b)
        edges = []
        for i in range(1, len(order)):
            for j in range(i):
                if rng.random() < 0.35:
                    edges.append(f"{order[i]} {order[j]}")  # order[i] depends on order[j]
        if not edges:
            edges = [f"{order[1]} {order[0]}"]
        graph = {}
        for e in edges:
            a, b = e.split()
            graph.setdefault(b, []).append(a)
            graph.setdefault(a, [])

        best = [0]
        best_chain = [None]

        def dfs(node, chain):
            if len(chain) > best[0] or (len(chain) == best[0] and chain < best_chain[0]):
                best[0], best_chain[0] = len(chain), list(chain)
            for nxt in graph.get(node, []):
                dfs(nxt, chain + [nxt])

        for n in sorted(graph):
            dfs(n, [n])

        assert impl.longest_failure_chain(edges) == best_chain[0], edges


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_log(run_script):
    rng = random.Random(0)
    lines = []
    for i in range(200_000):
        ts = f"2026-01-01T{i:08d}"
        level = "ERROR" if i == 199_999 else "INFO"
        lines.append(f"{ts} svc{i % 11} {level} msg")
    body = "\n".join(lines)
    stdin = f"PART 1\nN 200000\n{body}\nQ 2026-01-01T00000000\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "199999"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    body = "\n".join(LOGS)
    r = run_script(f"PART 1\nN 5\n{body}\nQ 2026-09-01T00:01:30\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    body = "\n".join(EDGES)
    r = run_script(f"PART 2\nN 3\n{body}\nS db\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "db auth cache api\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    edges = ["auth db", "cache auth", "api auth", "billing api"]
    body = "\n".join(edges)
    r = run_script(f"PART 3\nN 4\n{body}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "db auth api billing\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3_cycle(run_script):
    r = run_script("PART 3\nN 3\na b\nb c\nc a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "CYCLE a\n"
