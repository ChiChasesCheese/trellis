import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

LO, HI = -50, 200


def make_index(kind: str):
    return impl.SortedListIndex() if kind == "sorted" else impl.FenwickIndex(LO, HI)


@pytest.fixture(params=["sorted", "fenwick"])
def store(request):
    return impl.NumberStore(make_index(request.param))


def brute_closest(values, target, lower_wins=True):
    best = min(abs(v - target) for v in values)
    tied = sorted(v for v in values if abs(v - target) == best)
    return tied[0] if lower_wins else tied[-1]


# ---- 第 1 关：排序一次，二分找最近 ----

def test_closest_picks_the_nearest_value(store):
    for v in (10, 40, 70):
        store.add(v)
    assert store.closest(44) == 40
    assert store.closest(60) == 70


def test_closest_target_below_all_and_above_all(store):
    for v in (10, 40):
        store.add(v)
    assert store.closest(-30) == 10
    assert store.closest(199) == 40


def test_exact_match_wins(store):
    for v in (10, 40, 70):
        store.add(v)
    assert store.closest(40) == 40


def test_tie_goes_to_the_lower_value_by_default(store):
    store.add(10)
    store.add(20)
    assert store.closest(15) == 10


def test_tie_policy_higher_is_a_constructor_argument():
    for kind in ("sorted", "fenwick"):
        s = impl.NumberStore(make_index(kind), tie=impl.Tie.HIGHER)
        s.add(10)
        s.add(20)
        assert s.closest(15) == 20


def test_closest_on_empty_store_raises(store):
    with pytest.raises(impl.EmptyStoreError):
        store.closest(5)


# ---- 第 2 关：增删与重复值 ----

def test_add_then_remove_changes_the_answer(store):
    store.add(10)
    store.add(100)
    assert store.closest(90) == 100
    store.remove(100)
    assert store.closest(90) == 10


def test_duplicates_are_counted_and_removed_one_at_a_time(store):
    store.add(30)
    store.add(30)
    assert store.count(30) == 2 and len(store) == 2
    store.remove(30)
    assert store.count(30) == 1 and 30 in store
    store.remove(30)
    assert 30 not in store and len(store) == 0


def test_remove_missing_value_raises_and_changes_nothing(store):
    store.add(30)
    with pytest.raises(impl.ValueNotFoundError):
        store.remove(31)
    assert store.values() == (30,)


def test_non_integers_are_rejected(store):
    for bad in (1.5, "3", None, True):
        with pytest.raises(impl.InvalidValueError):
            store.add(bad)
    with pytest.raises(impl.InvalidValueError):
        store.closest(2.5)


def test_values_is_a_sorted_snapshot(store):
    for v in (5, 1, 5, 3):
        store.add(v)
    snap = store.values()
    store.add(2)
    assert snap == (1, 3, 5, 5)
    assert store.values() == (1, 2, 3, 5, 5)


# ---- 第 3 关：值域约束，树状数组 ----

def test_fenwick_rejects_values_outside_its_range():
    s = impl.NumberStore(impl.FenwickIndex(0, 9))
    with pytest.raises(impl.OutOfRangeError):
        s.add(10)
    with pytest.raises(impl.OutOfRangeError):
        s.add(-1)
    assert len(s) == 0


def test_fenwick_query_outside_range_still_answers():
    s = impl.NumberStore(impl.FenwickIndex(0, 9))
    s.add(0)
    s.add(9)
    assert s.closest(1000) == 9
    assert s.closest(-1000) == 0


def test_fenwick_rejects_empty_or_huge_range():
    with pytest.raises(impl.InvalidValueError):
        impl.FenwickIndex(5, 4)
    with pytest.raises(impl.InvalidValueError):
        impl.FenwickIndex(0, 10**9)


def test_single_value_range():
    s = impl.NumberStore(impl.FenwickIndex(7, 7))
    s.add(7)
    assert s.closest(-100) == 7 and s.k_closest(7, 3) == (7,)
    s.remove(7)
    with pytest.raises(impl.EmptyStoreError):
        s.closest(7)


@pytest.mark.parametrize("seed", range(5))
@pytest.mark.parametrize("lower_wins", [True, False])
def test_both_indexes_agree_with_brute_force(seed, lower_wins):
    rng = random.Random(seed)
    tie = impl.Tie.LOWER if lower_wins else impl.Tie.HIGHER
    stores = [impl.NumberStore(make_index(k), tie=tie) for k in ("sorted", "fenwick")]
    shadow: list[int] = []
    for _ in range(300):
        op = rng.choice("aar")
        if op == "a" or not shadow:
            v = rng.randint(LO, HI)
            shadow.append(v)
            for s in stores:
                s.add(v)
        else:
            v = rng.choice(shadow)
            shadow.remove(v)
            for s in stores:
                s.remove(v)
        if shadow:
            t = rng.randint(LO - 20, HI + 20)
            want = brute_closest(shadow, t, lower_wins)
            assert [s.closest(t) for s in stores] == [want, want]
    assert all(s.values() == tuple(sorted(shadow)) for s in stores)


# ---- 第 4 关：k 个最近值与线程安全 ----

def test_k_closest_counts_duplicates_and_returns_ascending(store):
    for v in (5, 20, 20, 42):
        store.add(v)
    assert store.k_closest(21, 3) == (5, 20, 20)
    assert store.k_closest(21, 1) == (20,)
    assert store.k_closest(21, 0) == ()
    assert store.k_closest(21, 99) == (5, 20, 20, 42)


def test_k_closest_tie_between_sides_follows_policy():
    for tie, want in ((impl.Tie.LOWER, (10,)), (impl.Tie.HIGHER, (20,))):
        s = impl.NumberStore(tie=tie)
        s.add(10)
        s.add(20)
        assert s.k_closest(15, 1) == want


def test_k_closest_matches_brute_force_by_distance():
    rng = random.Random(7)
    s = impl.NumberStore(impl.FenwickIndex(LO, HI))
    shadow = [rng.randint(LO, HI) for _ in range(60)]
    for v in shadow:
        s.add(v)
    for t in range(LO, HI, 17):
        got = s.k_closest(t, 8)
        want_dists = sorted(abs(v - t) for v in shadow)[:8]
        assert sorted(abs(v - t) for v in got) == want_dists


def test_k_closest_rejects_negative_k(store):
    with pytest.raises(impl.InvalidValueError):
        store.k_closest(1, -1)


@pytest.mark.parametrize("kind", ["sorted", "fenwick"])
def test_concurrent_adds_lose_nothing(kind):
    s = impl.NumberStore(make_index(kind))
    barrier = threading.Barrier(8)

    def work(base):
        barrier.wait()
        for i in range(20):
            s.add(base * 20 + i)

    threads = [threading.Thread(target=work, args=(b,)) for b in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(s) == 160 and s.values() == tuple(range(160))


@pytest.mark.parametrize("kind", ["sorted", "fenwick"])
def test_concurrent_removes_succeed_exactly_as_many_times_as_copies(kind):
    s = impl.NumberStore(make_index(kind))
    for _ in range(5):
        s.add(42)
    barrier = threading.Barrier(12)
    results: list[bool] = []

    def work():
        barrier.wait()
        try:
            s.remove(42)
            results.append(True)
        except impl.ValueNotFoundError:
            results.append(False)

    threads = [threading.Thread(target=work) for _ in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results.count(True) == 5 and results.count(False) == 7
    assert len(s) == 0
