import random

import pytest

EX1 = (4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3)
EX2_FLIGHTS = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
ROUTES = ["US:UK:FedEx:5", "UK:CA:FedEx:5", "US:CA:UPS:7", "US:UK:UPS:3", "UK:CA:UPS:9"]


def both(impl):
    return [impl.find_cheapest_price, impl.find_cheapest_price_bfs]


# ---------------------------------------------------------------- Part 1: Bellman-Ford
@pytest.mark.part1
def test_lc_examples(impl):
    n, fl, s, d = EX1
    assert impl.find_cheapest_price(n, fl, s, d, 1) == 700
    assert impl.find_cheapest_price(3, EX2_FLIGHTS, 0, 2, 1) == 200
    assert impl.find_cheapest_price(3, EX2_FLIGHTS, 0, 2, 0) == 500


@pytest.mark.part1
@pytest.mark.edge
def test_k_boundaries_ex1(impl):
    n, fl, s, d = EX1
    # k=0: no direct 0->3 ; k=1: 700 ; k=2: 0-1-2-3 = 400 ; k=3: still 400
    assert impl.find_cheapest_price(n, fl, s, d, 0) == -1
    assert impl.find_cheapest_price(n, fl, s, d, 2) == 400
    assert impl.find_cheapest_price(n, fl, s, d, 3) == 400


@pytest.mark.part1
@pytest.mark.edge
def test_in_place_relaxation_would_fail(impl):
    # chain 0-1-2-3-4 each 1, direct 0-4 costs 10, k=1: in-place relaxation returns 4, correct is 10
    fl = [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]]
    assert impl.find_cheapest_price(5, fl, 0, 4, 1) == 10
    assert impl.find_cheapest_price(5, fl, 0, 4, 2) == 10
    assert impl.find_cheapest_price(5, fl, 0, 4, 3) == 4


@pytest.mark.part1
@pytest.mark.edge
def test_unreachable_empty_and_same_city(impl):
    assert impl.find_cheapest_price(2, [], 0, 1, 0) == -1
    assert impl.find_cheapest_price(3, [[1, 2, 5]], 0, 2, 2) == -1
    assert impl.find_cheapest_price(3, [[0, 1, 5]], 0, 0, 0) == 0
    assert impl.find_cheapest_price(1, [], 0, 0, 0) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_cycle_does_not_help(impl):
    fl = [[0, 1, 1], [1, 0, 1], [1, 2, 100]]
    assert impl.find_cheapest_price(3, fl, 0, 2, 5) == 101


# ---------------------------------------------------------------- Part 2: BFS by hops
@pytest.mark.part2
def test_bfs_lc_examples(impl):
    n, fl, s, d = EX1
    assert impl.find_cheapest_price_bfs(n, fl, s, d, 1) == 700
    assert impl.find_cheapest_price_bfs(3, EX2_FLIGHTS, 0, 2, 1) == 200
    assert impl.find_cheapest_price_bfs(3, EX2_FLIGHTS, 0, 2, 0) == 500


@pytest.mark.part2
@pytest.mark.edge
def test_bfs_pruning_must_use_global_best(impl):
    # 0->1 cost 1 (1 hop) and 0->2->1 cost 1 (2 hops): second reach of 1 is NOT better -> pruned;
    # 1->3 cost 1: answer 2 with k=1, and 0->2->1->3 would need k=2 anyway
    fl = [[0, 1, 1], [0, 2, 1], [2, 1, 1], [1, 3, 1]]
    assert impl.find_cheapest_price_bfs(4, fl, 0, 3, 1) == 2
    assert impl.find_cheapest_price_bfs(4, fl, 0, 3, 0) == -1
    assert impl.find_cheapest_price_bfs(5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]], 0, 4, 1) == 10


@pytest.mark.part2
@pytest.mark.edge
def test_bfs_edge_cases(impl):
    assert impl.find_cheapest_price_bfs(2, [], 0, 1, 0) == -1
    assert impl.find_cheapest_price_bfs(3, [[0, 1, 5]], 0, 0, 0) == 0
    assert impl.find_cheapest_price_bfs(3, [[0, 1, 1], [1, 0, 1], [1, 2, 100]], 0, 2, 5) == 101


@pytest.mark.part2
def test_bf_and_bfs_agree_on_random_graphs(impl):
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randrange(2, 9)
        pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
        fl = [[u, v, rng.randrange(1, 20)] for u, v in rng.sample(pairs, rng.randrange(0, len(pairs) + 1))]
        s, d = rng.sample(range(n), 2)
        k = rng.randrange(0, n)
        assert impl.find_cheapest_price(n, fl, s, d, k) == impl.find_cheapest_price_bfs(n, fl, s, d, k)


# ---------------------------------------------------------------- Part 3: path
@pytest.mark.part3
def test_path_examples(impl):
    n, fl, s, d = EX1
    assert impl.cheapest_path(n, fl, s, d, 1) == [0, 1, 3]
    assert impl.cheapest_path(n, fl, s, d, 2) == [0, 1, 2, 3]
    assert impl.cheapest_path(3, EX2_FLIGHTS, 0, 2, 0) == [0, 2]
    assert impl.cheapest_path(3, EX2_FLIGHTS, 0, 2, 1) == [0, 1, 2]


@pytest.mark.part3
@pytest.mark.fmt
def test_path_tie_breaks(impl):
    fl = [[0, 1, 5], [1, 3, 5], [0, 2, 5], [2, 3, 5], [0, 3, 10]]
    assert impl.cheapest_path(4, fl, 0, 3, 1) == [0, 3]          # fewer flights wins the 10-10 tie
    fl2 = [f for f in fl if f != [0, 3, 10]]
    assert impl.cheapest_path(4, fl2, 0, 3, 1) == [0, 1, 3]      # lexicographic beats [0, 2, 3]
    fl3 = [[0, 2, 5], [2, 3, 5], [0, 1, 5], [1, 3, 5]]           # edge order must not matter
    assert impl.cheapest_path(4, fl3, 0, 3, 1) == [0, 1, 3]


@pytest.mark.part3
@pytest.mark.edge
def test_path_none_and_trivial(impl):
    assert impl.cheapest_path(2, [], 0, 1, 0) is None
    assert impl.cheapest_path(4, EX1[1], 0, 3, 0) is None
    assert impl.cheapest_path(2, [[0, 1, 1]], 0, 0, 0) == [0]


@pytest.mark.part3
def test_path_cost_matches_part1(impl):
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randrange(2, 8)
        pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
        fl = [[u, v, rng.randrange(1, 6)] for u, v in rng.sample(pairs, rng.randrange(0, len(pairs) + 1))]
        s, d = rng.sample(range(n), 2)
        k = rng.randrange(0, n)
        path = impl.cheapest_path(n, fl, s, d, k)
        price = impl.find_cheapest_price(n, fl, s, d, k)
        if price == -1:
            assert path is None
        else:
            w = {(u, v): c for u, v, c in fl}
            assert path[0] == s and path[-1] == d and len(path) - 2 <= k
            assert sum(w[(path[i], path[i + 1])] for i in range(len(path) - 1)) == price


# ---------------------------------------------------------------- Part 4: carriers
@pytest.mark.part4
def test_carrier_examples(impl):
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 1, "FedEx") == 10
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 1, "UPS") == 7
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 1, "*") == 7
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 1) == 7
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 0, "FedEx") == -1


@pytest.mark.part4
@pytest.mark.edge
def test_carrier_unknown_and_mixing(impl):
    assert impl.cheapest_with_carrier(ROUTES, "US", "CA", 1, "DHL") == -1
    assert impl.cheapest_with_carrier(ROUTES, "US", "MX", 1, "*") == -1
    assert impl.cheapest_with_carrier(ROUTES, "US", "US", 1, "*") == 0
    assert impl.cheapest_with_carrier([], "US", "CA", 3, "*") == -1
    # mixing: US:UK on UPS (3) + UK:CA on FedEx (5) = 8 only with '*', and only if cheaper than direct 7
    routes = ["US:UK:UPS:3", "UK:CA:FedEx:5", "US:CA:UPS:20"]
    assert impl.cheapest_with_carrier(routes, "US", "CA", 1, "*") == 8
    assert impl.cheapest_with_carrier(routes, "US", "CA", 1, "UPS") == 20
    assert impl.cheapest_with_carrier(routes, "US", "CA", 1, "FedEx") == -1


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    ex1 = "4 0 3 1\n0 1 100\n1 2 100\n2 0 100\n1 3 600\n2 3 200\n"
    assert run_script("PART 1\n" + ex1).stdout == "700\n"
    assert run_script("PART 2\n" + ex1).stdout == "700\n"
    assert run_script("PART 3\n" + ex1).stdout == "0 -> 1 -> 3 (700)\n"
    assert run_script("PART 3\n4 0 3 0\n0 1 100\n").stdout == "-1\n"
    r = run_script("PART 4\nUS CA 1 FedEx\n" + "\n".join(ROUTES) + "\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "10\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    # LC max: n=100, all 4950 (u<v) flights plus a few back edges, k=99
    rng = random.Random(0)
    n = 100
    fl = [[u, v, rng.randrange(1, 10_001)] for u in range(n) for v in range(u + 1, n)]
    import time
    t0 = time.perf_counter()
    a = impl.find_cheapest_price(n, fl, 0, n - 1, n - 1)
    b = impl.find_cheapest_price_bfs(n, fl, 0, n - 1, n - 1)
    p = impl.cheapest_path(n, fl, 0, n - 1, n - 1)
    assert a == b != -1 and p[0] == 0 and p[-1] == n - 1
    assert time.perf_counter() - t0 < 2.0
    text = f"PART 3\n{n} 0 {n - 1} {n - 1}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in fl) + "\n"
    r = run_script(text)
    assert r.returncode == 0, r.stderr
    assert r.stdout.endswith(f"({a})\n")
    assert r.seconds < 2.0 and r.max_rss_mb < 256
