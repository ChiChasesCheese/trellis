import random
import time

import pytest

EX1 = ([["a", "b"], ["b", "c"]], [2.0, 3.0], [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]])
EX2 = ([["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0], [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]])
EX3 = ([["a", "b"]], [0.5], [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]])
INCONSISTENT = ([["a", "b"], ["b", "c"], ["a", "c"]], [2.0, 3.0, 7.0])


def _consistent_case(rng, n_vars, n_eq, n_q):
    """Hidden potentials -> every derivable ratio is exact; a spanning-ish random graph."""
    names = [f"v{i}" for i in range(n_vars)]
    pot = {v: rng.uniform(0.1, 10.0) for v in names}
    eqs, vals = [], []
    for _ in range(n_eq):
        a, b = rng.sample(names, 2)
        eqs.append([a, b])
        vals.append(pot[a] / pot[b])
    queries = [rng.sample(names, 2) for _ in range(n_q)] + [["zz", "v0"], ["v0", "v0"]]
    return eqs, vals, queries, pot


# ---------------------------------------------------------------- Part 1: BFS
@pytest.mark.part1
def test_lc_examples_bfs(impl):
    assert impl.calc_equation(*EX1) == pytest.approx([6.0, 0.5, -1.0, 1.0, -1.0])
    assert impl.calc_equation(*EX2) == pytest.approx([3.75, 0.4, 5.0, 0.2])
    assert impl.calc_equation(*EX3) == pytest.approx([0.5, 2.0, -1.0, -1.0])


@pytest.mark.part1
@pytest.mark.edge
def test_self_inverse_disconnected(impl):
    eqs, vals = [["a", "b"], ["c", "d"]], [4.0, 0.25]
    q = [["a", "a"], ["d", "d"], ["b", "a"], ["d", "c"], ["a", "d"], ["a", "q"], ["q", "q"]]
    assert impl.calc_equation(eqs, vals, q) == pytest.approx([1.0, 1.0, 0.25, 4.0, -1.0, -1.0, -1.0])


@pytest.mark.part1
@pytest.mark.edge
def test_twenty_equation_chain(impl):
    eqs = [[f"x{i}", f"x{i+1}"] for i in range(20)]
    vals = [2.0] * 20
    r = impl.calc_equation(eqs, vals, [["x0", "x20"], ["x20", "x0"], ["x5", "x15"]])
    assert r == pytest.approx([2.0**20, 2.0**-20, 2.0**10], rel=1e-9)


@pytest.mark.part1
def test_bfs_matches_hidden_potentials(impl):
    rng = random.Random(0)
    for _ in range(100):
        eqs, vals, queries, pot = _consistent_case(rng, rng.randint(2, 8), rng.randint(1, 12), 10)
        got = impl.calc_equation(eqs, vals, queries)
        uf = impl.calc_equation_union_find(eqs, vals, queries)
        for (s, d), g, u in zip(queries, got, uf):
            assert g == pytest.approx(u, rel=1e-9)
            if g != -1.0:
                assert g == pytest.approx(pot[s] / pot[d], rel=1e-9)


# ---------------------------------------------------------------- Part 2: union-find
@pytest.mark.part2
def test_lc_examples_union_find(impl):
    assert impl.calc_equation_union_find(*EX1) == pytest.approx([6.0, 0.5, -1.0, 1.0, -1.0])
    assert impl.calc_equation_union_find(*EX2) == pytest.approx([3.75, 0.4, 5.0, 0.2])
    assert impl.calc_equation_union_find(*EX3) == pytest.approx([0.5, 2.0, -1.0, -1.0])


@pytest.mark.part2
@pytest.mark.edge
def test_union_find_merging_two_trees_and_compression(impl):
    # two components built separately, then joined by a late equation between non-roots
    eqs = [["a", "b"], ["b", "c"], ["d", "e"], ["e", "f"], ["c", "d"]]
    vals = [2.0, 3.0, 5.0, 7.0, 11.0]
    q = [["a", "f"], ["f", "a"], ["b", "e"], ["c", "c"]]
    assert impl.calc_equation_union_find(eqs, vals, q) == pytest.approx([2 * 3 * 11 * 5 * 7, 1 / (2 * 3 * 11 * 5 * 7), 3 * 11 * 5, 1.0], rel=1e-9)
    # querying twice must give the same answers (path compression must keep weights right)
    assert impl.calc_equation_union_find(eqs, vals, q + q)[4:] == pytest.approx(impl.calc_equation_union_find(eqs, vals, q), rel=1e-9)


@pytest.mark.part2
@pytest.mark.edge
def test_union_find_duplicate_and_reversed_equations(impl):
    eqs = [["a", "b"], ["b", "a"], ["a", "b"]]
    vals = [2.0, 0.5, 2.0]
    assert impl.calc_equation_union_find(eqs, vals, [["a", "b"], ["b", "a"]]) == pytest.approx([2.0, 0.5])


# ---------------------------------------------------------------- Part 3: best rate
@pytest.mark.part3
def test_best_rate_examples(impl):
    eqs, vals = INCONSISTENT
    assert impl.best_rate_path(eqs, vals, "a", "c") == (pytest.approx(7.0), ["a", "c"])
    r = impl.best_rate_path(eqs, vals, "c", "a")
    assert r[0] == pytest.approx(1 / 6) and r[1] == ["c", "b", "a"]
    assert impl.best_rate_path(eqs, vals, "b", "b") == (1.0, ["b"])
    assert impl.best_rate_path(eqs, vals, "a", "z") is None
    assert impl.best_rate_path(EX1[0], EX1[1], "a", "c") == (pytest.approx(6.0), ["a", "b", "c"])


@pytest.mark.part3
@pytest.mark.fmt
def test_best_rate_ties_and_no_cycles(impl):
    # two 2-hop paths with equal product: lexicographically smaller wins
    eqs = [["a", "m"], ["m", "z"], ["a", "b"], ["b", "z"]]
    vals = [2.0, 3.0, 3.0, 2.0]
    assert impl.best_rate_path(eqs, vals, "a", "z") == (pytest.approx(6.0), ["a", "b", "z"])
    # a direct quote equal to the 2-hop product: fewer hops wins
    eqs2, vals2 = eqs + [["a", "z"]], vals + [6.0]
    assert impl.best_rate_path(eqs2, vals2, "a", "z") == (pytest.approx(6.0), ["a", "z"])
    # inconsistent triangle with product > 1 around the loop must not be exploited
    eqs3, vals3 = [["a", "b"], ["b", "c"], ["c", "a"]], [2.0, 2.0, 2.0]
    r = impl.best_rate_path(eqs3, vals3, "a", "b")
    assert r[0] == pytest.approx(2.0) and r[1] == ["a", "b"]  # a->c->b = (1/2)*(1/2) is worse
    assert impl.best_rate_path(eqs3, vals3, "a", "a") == (1.0, ["a"])
    assert impl.best_rate_path([], [], "a", "a") is None


@pytest.mark.part3
def test_best_rate_equals_bfs_when_consistent(impl):
    rng = random.Random(1)
    for _ in range(60):
        eqs, vals, queries, pot = _consistent_case(rng, rng.randint(2, 6), rng.randint(1, 8), 5)
        for s, d in queries:
            r = impl.best_rate_path(eqs, vals, s, d)
            bfs = impl.calc_equation(eqs, vals, [[s, d]])[0]
            if bfs == -1.0:
                assert r is None
            else:
                assert r[0] == pytest.approx(bfs, rel=1e-9) and r[1][0] == s and r[1][-1] == d


# ---------------------------------------------------------------- Part 4: conflicts
@pytest.mark.part4
def test_conflict_examples(impl):
    C = impl.Conflict
    eqs, vals = INCONSISTENT
    assert impl.find_conflicts(eqs, vals) == [C(2, "a", "c", 7.0, pytest.approx(6.0))]
    assert impl.find_conflicts(eqs, [2.0, 3.0, 6.0]) == []
    assert impl.find_conflicts([["a", "b"], ["b", "a"], ["a", "b"]], [2.0, 0.5, 2.0000000001]) == []
    got = impl.find_conflicts([["a", "b"], ["a", "b"], ["b", "c"], ["a", "c"]], [2.0, 2.1, 3.0, 6.3])
    assert got == [C(1, "a", "b", 2.1, pytest.approx(2.0)), C(3, "a", "c", 6.3, pytest.approx(6.0))]


@pytest.mark.part4
@pytest.mark.edge
def test_conflict_tolerance_boundary(impl):
    eqs = [["a", "b"], ["a", "b"]]
    assert impl.find_conflicts(eqs, [2.0, 2.0 * (1 + 5e-10)]) == []            # inside 1e-9
    assert len(impl.find_conflicts(eqs, [2.0, 2.0 * (1 + 5e-9)])) == 1        # outside
    assert impl.find_conflicts(eqs, [2.0, 2.0 * (1 + 5e-9)], rel_tol=1e-6) == []  # looser tolerance
    assert impl.find_conflicts([], []) == []
    assert impl.find_conflicts([["a", "a"]], [1.0]) == []                     # a/a = 1 is fine
    assert len(impl.find_conflicts([["a", "a"]], [2.0])) == 1                 # a/a = 2 conflicts


@pytest.mark.part4
def test_conflicts_only_on_perturbed_quotes(impl):
    rng = random.Random(4)
    for _ in range(60):
        eqs, vals, _, pot = _consistent_case(rng, rng.randint(2, 7), rng.randint(2, 12), 0)
        assert impl.find_conflicts(eqs, vals, rel_tol=1e-9) == []
        # perturb one quote that is derivable from the others (a duplicate of equation 0, appended)
        eqs2, vals2 = eqs + [eqs[0]], vals + [vals[0] * 1.01]
        got = impl.find_conflicts(eqs2, vals2, rel_tol=1e-6)
        assert [c.index for c in got] == [len(eqs)]
        assert got[0].implied == pytest.approx(vals[0], rel=1e-9) and got[0].given == vals2[-1]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\na/b=2.0\nb/c=3.0\n?\na/c\nb/a\na/e\na/a\nx/x\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6.00000\n0.50000\n-1.00000\n1.00000\n-1.00000\n"
    assert run_script("PART 2\na / b = 2.0\n\nb/c=3.0\n?\na/c\n").stdout == "6.00000\n"
    assert run_script("PART 3\na/b=2\nb/c=3\na/c=7\n?\nc a\n").stdout == "0.16667 c -> b -> a\n"
    assert run_script("PART 3\na/b=2\n?\na z\n").stdout == "N/A\n"
    assert run_script("PART 4\na/b=2\nb/c=3\na/c=7\n?\n").stdout == "2: a/c given=7.00000 implied=6.00000\n"
    assert run_script("PART 4\na/b=2\nb/c=3\n").stdout == "consistent\n"
    assert run_script("").stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_many_queries(impl, run_script):
    rng = random.Random(0)
    # LC max is tiny (20/20); stress: 20 equations x 10^4 BFS queries, then 2*10^4 eq / 2*10^4 UF queries
    eqs, vals, _, pot = _consistent_case(rng, 21, 20, 0)
    queries = [rng.sample(list(pot), 2) for _ in range(10_000)]
    t0 = time.perf_counter()
    a = impl.calc_equation(eqs, vals, queries)
    b = impl.calc_equation_union_find(eqs, vals, queries)
    assert a == pytest.approx(b, rel=1e-9)
    big_eqs, big_vals, big_q, _ = _consistent_case(rng, 20_000, 20_000, 20_000)
    impl.calc_equation_union_find(big_eqs, big_vals, big_q)
    assert impl.find_conflicts(big_eqs, big_vals, rel_tol=1e-6) == []
    assert time.perf_counter() - t0 < 2.0
    text = "PART 2\n" + "\n".join(f"{x}/{y}={v!r}" for (x, y), v in zip(big_eqs, big_vals)) + "\n?\n" + "\n".join(f"{x}/{y}" for x, y in big_q) + "\n"
    r = run_script(text)
    assert r.returncode == 0 and r.seconds < 2.0 and r.max_rss_mb < 256
