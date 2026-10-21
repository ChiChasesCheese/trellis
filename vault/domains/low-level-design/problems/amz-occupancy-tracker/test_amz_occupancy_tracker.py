import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def office():
    """a 进@10, b 进@20, c 进@30, a 出@40, d 进@40, b 出@50, c 出@60"""
    t = impl.OccupancyTracker()
    t.enter("a", 10)
    t.enter("b", 20)
    t.enter("c", 30)
    t.leave("a", 40)
    t.enter("d", 40)
    t.leave("b", 50)
    t.leave("c", 60)
    return t


# ---- 第 1 关：进出事件，现在的人数 ----

def test_empty_office_is_zero_everywhere():
    t = impl.OccupancyTracker()
    assert t.current() == 0 and t.count_at(100) == 0 and t.max_in(0, 100) == 0


def test_current_is_enters_minus_leaves():
    t = office()
    assert t.current() == 1
    t.enter("e", 70)
    assert t.current() == 2


def test_entering_twice_without_leaving_is_rejected():
    t = office()
    with pytest.raises(impl.AlreadyInside):
        t.enter("d", 70)


def test_leaving_without_entering_is_rejected():
    t = office()
    with pytest.raises(impl.NotInside):
        t.leave("zz", 70)


def test_a_rejected_event_changes_nothing():
    t = office()
    before = (t.current(), t.events, t.count_at(1000))
    for bad in (lambda: t.enter("d", 70), lambda: t.leave("zz", 70), lambda: t.enter("e", 55)):
        with pytest.raises(impl.OccupancyError):
            bad()
    assert (t.current(), t.events, t.count_at(1000)) == before


# ---- 第 2 关：任意时刻的人数 ----

def test_count_at_is_zero_before_first_event_inclusive_at_event_and_holds_after():
    t = office()
    got = [t.count_at(x) for x in (5, 10, 15, 20, 29, 30, 39, 40, 45, 50, 59, 60, 1000)]
    assert got == [0, 1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1, 1]


def test_same_second_events_apply_in_arrival_order_and_the_second_ends_at_three():
    t = office()
    assert t.count_at(40) == 3


def test_events_may_not_go_back_in_time():
    t = office()
    with pytest.raises(impl.OutOfOrder):
        t.enter("e", 55)


def test_equal_timestamps_are_allowed():
    t = impl.OccupancyTracker()
    t.enter("a", 5)
    t.enter("b", 5)
    assert t.count_at(5) == 2


def test_max_in_counts_people_already_inside_when_the_range_starts():
    t = office()
    assert t.max_in(41, 100) == 3
    assert t.max_in(35, 39) == 3  # 区间内没有事件，取开始时的人数
    assert t.max_in(50, 100) == 2


def test_max_in_has_closed_ends_and_sees_the_peak():
    t = office()
    assert t.max_in(10, 10) == 1
    assert t.max_in(0, 5) == 0
    assert t.max_in(0, 1000) == 3
    assert t.max_in(61, 100) == 1


def test_max_in_rejects_a_reversed_range():
    with pytest.raises(ValueError):
        office().max_in(10, 5)


def test_who_is_inside_at_replays_the_log():
    t = office()
    assert t.who_is_inside_at(45) == {"b", "c", "d"}
    assert t.who_is_inside_at(1000) == {"d"}
    assert t.who_is_inside_at(5) == frozenset()


# ---- 第 3 关：楼层、重复与迟到事件 ----

def floors():
    t = impl.OccupancyTracker()
    t.enter("a", 1, zone="f1")
    t.enter("b", 2, zone="f2")
    t.enter("c", 3, zone="f2")
    t.leave("b", 4, zone="f2")
    return t


def test_counts_per_zone_and_for_the_whole_office():
    t = floors()
    assert (t.count_at(3, "f1"), t.count_at(3, "f2"), t.count_at(3)) == (1, 2, 3)
    assert (t.count_at(4, "f2"), t.count_at(4)) == (1, 2)
    assert t.current("f2") == 1 and t.current() == 2
    assert t.count_at(10, "nowhere") == 0 and t.current("nowhere") == 0


def test_max_in_per_zone_is_not_the_sum_of_zone_peaks():
    t = impl.OccupancyTracker()
    t.enter("a", 1, "f1")
    t.leave("a", 2, "f1")
    t.enter("b", 3, "f2")
    assert t.max_in(0, 10, "f1") == 1 and t.max_in(0, 10, "f2") == 1
    assert t.max_in(0, 10) == 1


def test_moving_floors_is_a_leave_then_an_enter():
    t = floors()
    t.leave("a", 5, "f1")
    t.enter("a", 5, "f2")
    assert (t.count_at(5, "f1"), t.count_at(5, "f2"), t.count_at(5)) == (0, 2, 2)


def test_leaving_a_different_floor_than_entered_is_rejected():
    t = floors()
    with pytest.raises(impl.NotInside):
        t.leave("a", 5, "f2")


def test_an_identical_retry_is_ignored_not_an_error():
    t = impl.OccupancyTracker()
    assert t.enter("a", 10) is True
    assert t.enter("a", 10) is False
    assert t.leave("a", 20) is True
    assert t.leave("a", 20) is False
    assert t.count_at(15) == 1 and t.current() == 0 and len(t.events) == 2


def test_a_late_event_is_rejected_even_when_it_is_valid_for_that_person():
    t = impl.OccupancyTracker()
    t.enter("a", 100)
    with pytest.raises(impl.OutOfOrder):
        t.enter("b", 99)
    assert t.who_is_inside_at(100) == {"a"}


def test_events_property_is_a_snapshot():
    t = office()
    snap = t.events
    t.enter("e", 70)
    assert len(snap) == 7 and len(t.events) == 8


# ---- 第 4 关：线段树、SQL、并发 ----

def random_office(seed, n=400):
    rng = random.Random(seed)
    t = impl.OccupancyTracker()
    now, inside = 0, {}
    for i in range(n):
        now += rng.choice([0, 0, 1, 2, 5])
        if inside and rng.random() < 0.45:
            person = rng.choice(sorted(inside))
            t.leave(person, now, inside.pop(person))
        else:
            zone = rng.choice(["f1", "f2", "f3"])
            t.enter(f"p{i}", now, zone)
            inside[f"p{i}"] = zone
    return t, now


def brute_count(events, ts, zone):
    return sum(e.delta for e in events if e.ts <= ts and zone in (None, e.zone))


def brute_max(events, a, b, zone):
    best, cur = brute_count(events, a, zone), 0
    for e in events:
        if zone in (None, e.zone):
            cur += e.delta
            if a <= e.ts <= b:
                best = max(best, cur)
    return best


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_memory_version_matches_brute_force_and_sql(seed):
    t, now = random_office(seed)
    db = impl.load_sqlite(t.events)
    rng = random.Random(seed + 100)
    for _ in range(150):
        a = rng.randrange(-3, now + 3)
        b = a + rng.randrange(0, 60)
        zone = rng.choice([None, "f1", "f2", "f3"])
        params = {"t": a, "a": a, "b": b, "zone": zone}
        assert t.count_at(a, zone) == brute_count(t.events, a, zone) == db.execute(impl.SQL_COUNT_AT, params).fetchone()[0]
        assert t.max_in(a, b, zone) == brute_max(t.events, a, b, zone) == db.execute(impl.SQL_MAX_IN, params).fetchone()[0]


def test_the_tree_survives_many_growth_steps():
    t = impl.OccupancyTracker()
    for i in range(1100):
        t.enter(f"p{i}", i)
    assert t.max_in(0, 2000) == 1100 and t.max_in(500, 520) == 521 and t.count_at(1099) == 1100


def test_concurrent_gates_keep_counts_consistent():
    t = impl.OccupancyTracker()
    barrier = threading.Barrier(8)

    def gate(k):
        barrier.wait()
        for i in range(50):
            t.enter(f"g{k}-{i}", 0)

    threads = [threading.Thread(target=gate, args=(k,)) for k in range(8)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert t.current() == 400 and len(t.events) == 400 and t.max_in(0, 0) == 400
