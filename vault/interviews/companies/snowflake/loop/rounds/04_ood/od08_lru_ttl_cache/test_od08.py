import random

import pytest


# ------------------------------------------------------------------ Part 1: classic LRU
@pytest.mark.part1
def test_worked_example_1(impl):
    c = impl.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    results = [c.get(1)]
    c.put(3, 3)
    results.append(c.get(2))
    c.put(4, 4)
    results.append(c.get(1))
    results.append(c.get(3))
    results.append(c.get(4))
    assert results == [1, -1, -1, 3, 4]


@pytest.mark.part1
@pytest.mark.edge
def test_capacity_zero_never_retains_anything(impl):
    c = impl.LRUCache(0)
    c.put("a", 1)
    assert c.get("a") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_missing_key_returns_minus_one(impl):
    c = impl.LRUCache(2)
    assert c.get("ghost") == -1


@pytest.mark.part1
@pytest.mark.edge
def test_put_existing_key_updates_value_and_marks_mru(impl):
    c = impl.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 100)  # update -- also marks "a" MRU
    c.put("c", 3)  # capacity exceeded -> evict LRU, which is now "b", not "a"
    assert c.get("b") == -1
    assert c.get("a") == 100
    assert c.get("c") == 3


@pytest.mark.part1
@pytest.mark.edge
def test_get_marks_mru(impl):
    c = impl.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")  # a is now MRU, b is LRU
    c.put("c", 3)  # evicts b
    assert c.get("b") == -1
    assert c.get("a") == 1


# ------------------------------------------------------------------ Part 2: TTL expiry
@pytest.mark.part2
def test_worked_example_2a_lru_eviction_not_expiry(impl):
    c = impl.TTLCache(1)
    c.put("x", 1, now=0, ttl=5)
    c.put("y", 2, now=3, ttl=100)  # x not yet expired (3 < 5) -- pure LRU eviction
    assert c.get("x", now=4) == -1
    assert c.get("y", now=4) == 2


@pytest.mark.part2
def test_worked_example_2b_expiry_frees_space_without_lru_eviction(impl):
    c = impl.TTLCache(1)
    c.put("p", 1, now=0, ttl=2)
    c.put("q", 2, now=5, ttl=100)  # p already expired (5 >= 2) -- no valid entry evicted
    assert c.get("p", now=5) == -1
    assert c.get("q", now=5) == 2


@pytest.mark.part2
@pytest.mark.edge
def test_ttl_half_open_boundary(impl):
    c = impl.TTLCache(5)
    c.put("a", 1, now=0, ttl=10)
    assert c.get("a", now=9) == 1  # one before expiry -- still valid
    assert c.get("a", now=10) == -1  # exactly at expiry -- expired


@pytest.mark.part2
@pytest.mark.edge
def test_repeated_put_overwrites_ttl_and_value(impl):
    c = impl.TTLCache(5)
    c.put("a", 1, now=0, ttl=2)  # would expire at 2
    c.put("a", 2, now=0, ttl=100)  # overwrite -- now expires at 100, value 2
    assert c.get("a", now=50) == 2


@pytest.mark.part2
@pytest.mark.edge
def test_missing_key_returns_minus_one_ttl(impl):
    c = impl.TTLCache(5)
    assert c.get("ghost", now=0) == -1


# ------------------------------------------------------------------ Part 3: two-tier hot/cold (reconstructed)
@pytest.mark.part3
def test_worked_example_3_full_chain(impl):
    c = impl.TwoTierCache(hot_capacity=1, cold_capacity=1)
    c.put("a", 1)
    c.put("b", 2)  # a demoted to cold
    r1 = c.get("a")  # promotes a; demotes b to cold
    r2 = c.get("b")  # promotes b; demotes a to cold
    c.put("c", 3)  # demotes b to cold; cold overflow discards a
    r3 = c.get("a")
    assert [r1, r2, r3] == [1, 2, -1]


@pytest.mark.part3
@pytest.mark.edge
def test_missing_from_both_tiers(impl):
    c = impl.TwoTierCache(hot_capacity=2, cold_capacity=2)
    assert c.get("ghost") == -1


@pytest.mark.part3
@pytest.mark.edge
def test_hot_capacity_zero_everything_lands_in_cold(impl):
    c = impl.TwoTierCache(hot_capacity=0, cold_capacity=2)
    c.put("a", 1)
    assert c.get("a") == 1  # found via cold (promotion bounces right back out of hot)


@pytest.mark.part3
@pytest.mark.edge
def test_both_capacities_zero_retains_nothing(impl):
    c = impl.TwoTierCache(hot_capacity=0, cold_capacity=0)
    c.put("a", 1)
    assert c.get("a") == -1


@pytest.mark.part3
@pytest.mark.edge
def test_key_never_in_both_tiers_simultaneously(impl):
    c = impl.TwoTierCache(hot_capacity=1, cold_capacity=1)
    c.put("a", 1)
    c.put("b", 2)  # a demoted to cold
    c.get("a")  # promote a back to hot; b demoted to cold
    # whichever internal structure holds "b", a fresh put on "b" must not create a duplicate
    c.put("b", 20)
    assert c.get("b") == 20
    assert c.get("a") == 1


@pytest.mark.part3
@pytest.mark.edge
def test_put_on_existing_cold_key_promotes_and_updates(impl):
    c = impl.TwoTierCache(hot_capacity=1, cold_capacity=1)
    c.put("a", 1)
    c.put("b", 2)  # a demoted to cold
    c.put("a", 999)  # update while in cold -> must promote AND update value
    assert c.get("a") == 999


# ------------------------------------------------------------------ fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_output_strings_exact(impl):
    out = impl.part1(["CAPACITY 2", "PUT a 1", "GET a", "GET ghost"])
    assert out == ["1", "-1"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["CAPACITY 2", "PUT 1 1", "PUT 2 2", "GET 1", "PUT 3 3", "GET 2", "PUT 4 4", "GET 1", "GET 3", "GET 4"]
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n-1\n-1\n3\n4\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["CAPACITY 1", "PUT x 1 0 5", "PUT y 2 3 100", "GET x 4", "GET y 4"]
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "-1\n2\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    body = [
        "CAPACITY 1,1",
        "PUT a 1",
        "PUT b 2",
        "GET a",
        "GET b",
        "PUT c 3",
        "GET a",
    ]
    r = run_script("PART 3\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n2\n-1\n"


@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_ops_lru(run_script):
    rng = random.Random(0)
    body = ["CAPACITY 1000"]
    for i in range(100_000):
        if rng.random() < 0.5:
            body.append(f"PUT k{rng.randrange(5000)} {i}")
        else:
            body.append(f"GET k{rng.randrange(5000)}")
    result = run_script("PART 1\n" + "\n".join(body) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_ops_ttl(run_script):
    rng = random.Random(0)
    body = ["CAPACITY 100"]
    now = 0
    for i in range(100_000):
        now += rng.randrange(0, 2)
        if rng.random() < 0.5:
            body.append(f"PUT k{rng.randrange(500)} {i} {now} {rng.randrange(1, 50)}")
        else:
            body.append(f"GET k{rng.randrange(500)} {now}")
    result = run_script("PART 2\n" + "\n".join(body) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
