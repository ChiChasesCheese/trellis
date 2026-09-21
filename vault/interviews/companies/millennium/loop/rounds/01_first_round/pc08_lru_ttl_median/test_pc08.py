import random

import pytest


def _brute_median(values: list[float]) -> float:
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_lru_cache(impl):
    c = impl.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)  # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)  # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


@pytest.mark.part1
def test_worked_example_lru_cache_linked(impl):
    c = impl.LRUCacheLinked(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


@pytest.mark.part1
@pytest.mark.edge
def test_two_impls_agree_random(impl):
    rng = random.Random(0)
    for _ in range(20):
        capacity = rng.randint(1, 5)
        a = impl.LRUCache(capacity)
        b = impl.LRUCacheLinked(capacity)
        for _ in range(200):
            key = rng.randint(0, 7)
            if rng.random() < 0.5:
                value = rng.randint(0, 100)
                a.put(key, value)
                b.put(key, value)
            else:
                assert a.get(key) == b.get(key), (capacity, key)


@pytest.mark.part1
@pytest.mark.edge
def test_get_miss_returns_minus_one_not_error(impl):
    c = impl.LRUCache(2)
    assert c.get(99) == -1
    cl = impl.LRUCacheLinked(2)
    assert cl.get(99) == -1


@pytest.mark.part1
@pytest.mark.edge
def test_update_existing_key_does_not_consume_extra_capacity(impl):
    c = impl.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 100)  # update, not a new entry
    c.put(3, 3)  # capacity still 2 -> evicts LRU (2), not 1
    assert c.get(1) == 100
    assert c.get(2) == -1
    assert c.get(3) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_capacity_one(impl):
    c = impl.LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_capacity_raises(impl):
    with pytest.raises(ValueError):
        impl.LRUCache(0)
    with pytest.raises(ValueError):
        impl.LRUCache(-1)
    with pytest.raises(ValueError):
        impl.LRUCacheLinked(True)  # bool is an int subclass -- must not silently pass


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_key_or_value_raises(impl):
    c = impl.LRUCache(2)
    with pytest.raises(ValueError):
        c.put("1", 1)
    with pytest.raises(ValueError):
        c.put(1, "one")
    with pytest.raises(ValueError):
        c.get(1.5)


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = (
        "PART 1\nCAPACITY 2\nPUT 1 1\nPUT 2 2\nGET 1\nPUT 3 3\nGET 2\n"
        "PUT 4 4\nGET 1\nGET 3\nGET 4\n"
    )
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n-1\n-1\n3\n4\n"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_ttl_worked_example(impl):
    now = [0.0]
    tc = impl.LRUCacheTTL(2, clock=lambda: now[0])
    tc.put(1, 100, ttl=5)
    tc.put(2, 200)
    assert tc.get(1) == 100
    now[0] = 6
    assert tc.get(1) == -1
    assert tc.get(2) == 200


@pytest.mark.part2
def test_capacity_eviction_independent_of_ttl(impl):
    now = [0.0]
    tc = impl.LRUCacheTTL(2, clock=lambda: now[0])
    tc.put(1, 1, ttl=1000)
    tc.put(2, 2, ttl=1000)
    tc.get(1)  # 1 becomes most-recently-used
    tc.put(3, 3)  # evicts LRU (2), even though its TTL is far off
    assert tc.get(2) == -1
    assert tc.get(1) == 1
    assert tc.get(3) == 3


@pytest.mark.part2
@pytest.mark.edge
def test_get_does_not_postpone_expiry(impl):
    now = [0.0]
    tc = impl.LRUCacheTTL(2, clock=lambda: now[0])
    tc.put(1, 1, ttl=5)
    now[0] = 4
    assert tc.get(1) == 1  # touched, but deadline stays at 5
    now[0] = 5
    assert tc.get(1) == -1  # still expires at the original deadline


@pytest.mark.part2
@pytest.mark.edge
def test_ttl_none_never_expires(impl):
    now = [0.0]
    tc = impl.LRUCacheTTL(1, clock=lambda: now[0])
    tc.put(1, 1)
    now[0] = 10_000
    assert tc.get(1) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_ttl_raises(impl):
    tc = impl.LRUCacheTTL(2)
    with pytest.raises(ValueError):
        tc.put(1, 1, ttl=0)
    with pytest.raises(ValueError):
        tc.put(1, 1, ttl=-5)


@pytest.mark.part2
@pytest.mark.edge
def test_expired_key_reinsertable(impl):
    now = [0.0]
    tc = impl.LRUCacheTTL(2, clock=lambda: now[0])
    tc.put(1, 1, ttl=1)
    now[0] = 2
    assert tc.get(1) == -1  # expired
    tc.put(1, 42, ttl=100)  # fresh insert after expiry
    assert tc.get(1) == 42


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\nCAPACITY 2\nPUT 1 100 5\nPUT 2 200 -\nGET 1\nTICK 6\nGET 1\nGET 2\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "100\n-1\n200\n"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_median_worked_example(impl):
    m = impl.MedianStream()
    m.add(5)
    assert m.median() == 5
    m.add(15)
    assert m.median() == 10
    m.add(1)
    assert m.median() == 5
    m.add(3)
    assert m.median() == 4


@pytest.mark.part3
@pytest.mark.edge
def test_median_single_element(impl):
    m = impl.MedianStream()
    m.add(7)
    assert m.median() == 7


@pytest.mark.part3
@pytest.mark.edge
def test_median_empty_raises(impl):
    with pytest.raises(ValueError):
        impl.MedianStream().median()


@pytest.mark.part3
@pytest.mark.edge
def test_median_negatives_and_duplicates(impl):
    m = impl.MedianStream()
    for x in [-5, -5, 0, 5, 5]:
        m.add(x)
    assert m.median() == 0


@pytest.mark.part3
@pytest.mark.edge
def test_median_rejects_bool(impl):
    m = impl.MedianStream()
    with pytest.raises(ValueError):
        m.add(True)
    with pytest.raises(ValueError):
        m.add("5")


@pytest.mark.part3
@pytest.mark.edge
def test_median_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(20):
        m = impl.MedianStream()
        values: list[float] = []
        for _ in range(rng.randint(1, 40)):
            x = rng.randint(-50, 50)
            m.add(x)
            values.append(x)
            assert m.median() == _brute_median(values), values


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    stdin = "PART 3\nADD 5\nMEDIAN\nADD 15\nMEDIAN\nADD 1\nMEDIAN\nADD 3\nMEDIAN\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n10\n5\n4\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_large_stream(run_script):
    rng = random.Random(0)
    nums = [rng.randint(-1_000_000, 1_000_000) for _ in range(100_000)]
    body = "\n".join(f"ADD {n}" for n in nums) + "\nMEDIAN\n"
    r = run_script("PART 3\n" + body, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"
