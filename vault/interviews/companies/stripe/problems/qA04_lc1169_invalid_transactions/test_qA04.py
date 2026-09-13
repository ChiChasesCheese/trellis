import random
import time

import pytest

EX1 = ["alice,20,800,mtv", "alice,50,100,beijing"]
EX2 = ["alice,20,800,mtv", "alice,50,1200,mtv"]
EX3 = ["alice,20,800,mtv", "bob,50,1200,mtv"]


def brute(transactions):
    """O(n^2) oracle in input order."""
    rows = [t.split(",") for t in transactions]
    out = []
    for i, (n, t, a, c) in enumerate(rows):
        bad = int(a) > 1000
        for j, (n2, t2, a2, c2) in enumerate(rows):
            if j != i and n2 == n and c2 != c and abs(int(t) - int(t2)) <= 60:
                bad = True
        if bad:
            out.append(transactions[i])
    return out


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.invalid_transactions(EX1) == EX1
    assert impl.invalid_transactions(EX2) == ["alice,50,1200,mtv"]
    assert impl.invalid_transactions(EX3) == ["bob,50,1200,mtv"]


@pytest.mark.part1
@pytest.mark.edge
def test_amount_boundary(impl):
    assert impl.invalid_transactions(["a,0,1000,x"]) == []
    assert impl.invalid_transactions(["a,0,1001,x"]) == ["a,0,1001,x"]
    assert impl.invalid_transactions(["a,0,0,x"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_time_boundary_inclusive_and_symmetric(impl):
    assert impl.invalid_transactions(["a,0,1,x", "a,60,1,y"]) == ["a,0,1,x", "a,60,1,y"]
    assert impl.invalid_transactions(["a,0,1,x", "a,61,1,y"]) == []
    assert impl.invalid_transactions(["a,61,1,y", "a,0,1,x"]) == []
    assert impl.invalid_transactions(["a,100,1,y", "a,40,1,x"]) == ["a,100,1,y", "a,40,1,x"]  # input order kept


@pytest.mark.part1
@pytest.mark.edge
def test_same_city_and_duplicates_never_conflict(impl):
    assert impl.invalid_transactions(["a,0,1,x", "a,10,1,x", "a,20,1,x"]) == []
    assert impl.invalid_transactions(["a,0,1,x", "a,0,1,x"]) == []
    # duplicates of an invalid transaction are each reported
    assert impl.invalid_transactions(["a,0,1,x", "a,0,1,x", "a,5,1,y"]) == ["a,0,1,x", "a,0,1,x", "a,5,1,y"]
    assert impl.invalid_transactions(["a,0,2000,x", "a,0,2000,x"]) == ["a,0,2000,x", "a,0,2000,x"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_single_and_other_names(impl):
    assert impl.invalid_transactions([]) == []
    assert impl.invalid_transactions(["a,0,1,x"]) == []
    assert impl.invalid_transactions(["a,0,1,x", "b,0,1,y"]) == []
    assert impl.invalid_transactions([" a , 0 , 1 , x ", "a,30,1,y"]) == ["a , 0 , 1 , x", "a,30,1,y"]


@pytest.mark.part1
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randrange(0, 15)
        txs = [f"{rng.choice('ab')},{rng.randrange(0, 200)},{rng.choice([1, 1000, 1001])},{rng.choice('xyz')}" for _ in range(n)]
        assert impl.invalid_transactions(txs) == brute(txs)


@pytest.mark.part1
@pytest.mark.edge
def test_dense_same_minute_group_is_not_quadratic(impl):
    # 20,000 transactions, one name, one minute, two cities: all invalid; O(n^2) pair scan would stall
    txs = [f"a,5,1,{'x' if i % 2 else 'y'}" for i in range(20_000)] + ["a,5,1,x"] * 0
    t0 = time.perf_counter()
    assert impl.invalid_transactions(txs) == txs
    assert time.perf_counter() - t0 < 1.0
    # and one city only -> none, still fast
    same = ["a,5,1,x"] * 20_000
    assert impl.invalid_transactions(same) == []


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_reasons_examples(impl):
    v = impl.invalid_reasons(EX1)
    assert [tuple(x) for x in v] == [
        (0, "alice,20,800,mtv", ["city:alice,50,100,beijing"]),
        (1, "alice,50,100,beijing", ["city:alice,20,800,mtv"]),
    ]
    v = impl.invalid_reasons(["alice,20,1500,mtv", "alice,80,100,sf", "alice,81,100,la"])
    assert [x.reasons for x in v] == [
        ["amount>1000", "city:alice,80,100,sf"],
        ["city:alice,20,1500,mtv", "city:alice,81,100,la"],
        ["city:alice,80,100,sf"],
    ]
    assert [x.index for x in v] == [0, 1, 2]


@pytest.mark.part2
@pytest.mark.edge
def test_reasons_order_and_valid_omitted(impl):
    # conflicts ordered by (time, index) of the other, not by input order
    v = impl.invalid_reasons(["a,50,1,x", "a,60,1,z", "a,10,1,y", "b,50,1,x"])
    assert v[0].reasons == ["city:a,10,1,y", "city:a,60,1,z"]
    assert [x.transaction for x in v] == ["a,50,1,x", "a,60,1,z", "a,10,1,y"]
    assert impl.invalid_reasons(["a,0,1000,x"]) == []
    assert impl.invalid_reasons(["a,0,1001,x"])[0].reasons == ["amount>1000"]


@pytest.mark.part2
def test_reasons_consistent_with_part1(impl):
    rng = random.Random(1)
    for _ in range(100):
        txs = [f"{rng.choice('ab')},{rng.randrange(0, 150)},{rng.choice([1, 1001])},{rng.choice('xy')}" for _ in range(rng.randrange(0, 12))]
        assert [v.transaction for v in impl.invalid_reasons(txs)] == impl.invalid_transactions(txs)
        for v in impl.invalid_reasons(txs):
            assert v.reasons and all(r == "amount>1000" or r.startswith("city:") for r in v.reasons)


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_stream_example(impl):
    s = impl.TransactionStream()
    assert s.add("alice,20,800,mtv") == []
    assert s.add("alice,50,100,beijing") == ["alice,20,800,mtv", "alice,50,100,beijing"]
    assert s.add("alice,60,100,mtv") == ["alice,60,100,mtv"]
    assert s.add("bob,70,2000,sf") == ["bob,70,2000,sf"]
    assert s.add("alice,121,5,beijing") == []
    with pytest.raises(ValueError):
        s.add("alice,120,5,la")
    assert s.flagged == ["alice,20,800,mtv", "alice,50,100,beijing", "alice,60,100,mtv", "bob,70,2000,sf"]


@pytest.mark.part3
@pytest.mark.edge
def test_stream_eviction_boundary_and_no_double_report(impl):
    s = impl.TransactionStream()
    assert s.add("a,0,1,x") == []
    assert s.add("a,60,1,y") == ["a,0,1,x", "a,60,1,y"]      # exactly 60 apart -> still in window
    assert s.add("a,60,1,y") == ["a,60,1,y"]                 # duplicate arrival still conflicts with x@0 itself
    assert s.add("a,120,1,x") == ["a,120,1,x"]               # conflicts with y@60; y already reported
    assert s.add("a,181,1,z") == []                          # x@120 is 61 away -> evicted/out of window
    assert s.add("a,181,1001,z") == ["a,181,1001,z"]         # amount alone
    assert s.flagged == ["a,0,1,x", "a,60,1,y", "a,60,1,y", "a,120,1,x", "a,181,1001,z"]


@pytest.mark.part3
def test_stream_matches_batch_when_sorted(impl):
    rng = random.Random(2)
    for _ in range(100):
        txs = sorted(
            (f"{rng.choice('ab')},{rng.randrange(0, 150)},{rng.choice([1, 1001])},{rng.choice('xy')}" for _ in range(rng.randrange(0, 12))),
            key=lambda t: int(t.split(",")[1]),
        )
        s = impl.TransactionStream()
        for t in txs:
            s.add(t)
        assert sorted(s.flagged) == sorted(impl.invalid_transactions(txs))


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\nalice,20,800,mtv\nalice,50,100,beijing\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "alice,20,800,mtv\nalice,50,100,beijing\n"
    assert run_script("PART 1\nalice,20,800,mtv\n").stdout == ""
    r = run_script("PART 2\nalice,20,1500,mtv\nalice,80,100,sf\nalice,81,100,la\n\n")
    assert r.stdout == (
        "alice,20,1500,mtv | amount>1000 ; city:alice,80,100,sf\n"
        "alice,80,100,sf | city:alice,20,1500,mtv ; city:alice,81,100,la\n"
        "alice,81,100,la | city:alice,80,100,sf\n"
    )
    r = run_script("PART 3\nalice,20,800,mtv\nalice,50,100,beijing\nalice,60,100,mtv\nalice,121,5,beijing\n")
    assert r.stdout == "alice,50,100,beijing => alice,20,800,mtv ; alice,50,100,beijing\nalice,60,100,mtv => alice,60,100,mtv\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max_and_stress(impl, run_script):
    rng = random.Random(0)
    # LC max: 1000 transactions, times 0..1000, 10 names -> dense windows
    lc = [f"{rng.choice('abcdefghij')},{rng.randrange(0, 1001)},{rng.randrange(0, 2001)},{rng.choice(['mtv', 'sf', 'la'])}" for _ in range(1000)]
    t0 = time.perf_counter()
    for _ in range(20):
        impl.invalid_transactions(lc)
    # stress: 10^5 transactions, 200 names, times up to 10^6 -> O(n log n) required
    big = [f"n{rng.randrange(200)},{rng.randrange(0, 10**6)},{rng.randrange(0, 2001)},{rng.choice(['mtv', 'sf', 'la'])}" for _ in range(100_000)]
    impl.invalid_transactions(big)
    assert time.perf_counter() - t0 < 2.0
    r = run_script("PART 1\n" + "\n".join(lc) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == brute(lc)
    assert r.seconds < 2.0 and r.max_rss_mb < 256
