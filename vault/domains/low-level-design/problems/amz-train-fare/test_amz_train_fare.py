import importlib
import os
import random
import threading
from datetime import datetime

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

SATURDAY = datetime(2026, 10, 17, 9, 0)
SUNDAY = datetime(2026, 10, 18, 9, 0)
MONDAY = datetime(2026, 10, 19, 9, 0)
MONDAY_RUSH = datetime(2026, 10, 19, 8, 30)


def line():
    return impl.Route(["G", "U", "H", "K", "I"])


def calc_at(when, *rules, route=None):
    return impl.FareCalculator(route or line(), rules, clock=lambda: when)


# ---- 第 1 关：固定线路上的 calculateFare ----

def test_each_hop_costs_one_unit_so_g_to_i_is_four():
    assert calc_at(MONDAY).calculate_fare("G", "I") == impl.Money(400)


def test_fare_is_the_number_of_hops_between_stations():
    c = calc_at(MONDAY)
    assert c.calculate_fare("U", "K") == impl.Money(200)
    assert c.calculate_fare("H", "K") == impl.Money(100)


def test_fare_is_the_same_in_both_directions():
    c = calc_at(MONDAY)
    assert c.calculate_fare("I", "G") == c.calculate_fare("G", "I")


def test_same_station_costs_nothing():
    assert calc_at(MONDAY).calculate_fare("H", "H") == impl.ZERO


def test_unknown_station_is_rejected():
    c = calc_at(MONDAY)
    with pytest.raises(impl.UnknownStationError):
        c.calculate_fare("G", "Z")
    with pytest.raises(LookupError):
        c.calculate_fare("Z", "G")


def test_money_is_a_value_that_prints_in_units_and_cents():
    assert str(impl.Money(450)) == "4.50" and str(impl.Money(5)) == "0.05"
    assert impl.Money(100) + impl.Money(250) == impl.Money(350)
    assert min(impl.Money(100), impl.Money(90)) == impl.Money(90)


# ---- 第 2 关：线路数据从哪来，动态加站 ----

def test_appending_a_station_extends_the_route_and_prices_it():
    route = line()
    c = calc_at(MONDAY, route=route)
    assert "X" not in route
    route.append("X")
    assert route.stations == ("G", "U", "H", "K", "I", "X") and len(route) == 6
    assert c.calculate_fare("G", "X") == impl.Money(500)
    assert c.calculate_fare("G", "I") == impl.Money(400)


def test_appending_a_station_with_its_own_segment_price():
    route = line()
    route.append("X", impl.Money(250))
    c = calc_at(MONDAY, route=route)
    assert c.calculate_fare("I", "X") == impl.Money(250)
    assert c.calculate_fare("G", "X") == impl.Money(650)


def test_duplicate_station_is_rejected_and_route_unchanged():
    route = line()
    with pytest.raises(impl.DuplicateStationError):
        route.append("H")
    with pytest.raises(impl.DuplicateStationError):
        route.insert_after("G", "K")
    assert route.stations == ("G", "U", "H", "K", "I")


def test_stations_is_a_snapshot_not_the_internal_list():
    route = line()
    snap = route.stations
    route.append("X")
    assert snap == ("G", "U", "H", "K", "I")


def test_route_can_start_empty_and_grow():
    route = impl.Route()
    route.append("A")
    route.append("B")
    assert calc_at(MONDAY, route=route).calculate_fare("A", "B") == impl.Money(100)


def test_inserting_in_the_middle_makes_fares_across_it_larger_and_others_unchanged():
    route = line()
    c = calc_at(MONDAY, route=route)
    route.insert_after("U", "N")
    assert route.stations == ("G", "U", "N", "H", "K", "I")
    assert c.calculate_fare("G", "U") == impl.Money(100)       # 在插入点之前的不变
    assert c.calculate_fare("H", "I") == impl.Money(200)       # 在插入点之后的不变
    assert c.calculate_fare("G", "I") == impl.Money(500)       # 跨过插入点的多一个区间
    assert c.calculate_fare("U", "H") == impl.Money(200)


def test_insert_after_the_last_station_is_an_append():
    route = line()
    route.insert_after("I", "X")
    assert route.stations[-1] == "X"


@pytest.mark.parametrize("seed", range(5))
def test_fares_are_additive_along_the_line_after_random_edits(seed):
    rng = random.Random(seed)
    route = impl.Route(["s0"])
    for i in range(1, 25):
        if rng.random() < 0.5:
            route.append(f"s{i}", impl.Money(rng.randint(0, 300)))
        else:
            route.insert_after(rng.choice(route.stations), f"s{i}")
    names, c = route.stations, calc_at(MONDAY, route=route)
    for _ in range(100):
        a, b, d = sorted(rng.sample(range(len(names)), 3))
        ab, bd, ad = (c.calculate_fare(names[x], names[y]) for x, y in ((a, b), (b, d), (a, d)))
        assert ab + bd == ad
        assert c.calculate_fare(names[d], names[a]) == ad


# ---- 第 3 关：周末封顶 ----

def test_weekend_fare_is_capped_for_a_single_trip():
    weekend = impl.WeekendCap(impl.Money(300))
    assert calc_at(SATURDAY, weekend).calculate_fare("G", "I") == impl.Money(300)
    assert calc_at(SUNDAY, weekend).calculate_fare("G", "I") == impl.Money(300)


def test_weekend_cap_does_not_raise_cheap_fares():
    assert calc_at(SATURDAY, impl.WeekendCap(impl.Money(300))).calculate_fare("G", "U") == impl.Money(100)


def test_weekday_ignores_the_weekend_cap():
    assert calc_at(MONDAY, impl.WeekendCap(impl.Money(300))).calculate_fare("G", "I") == impl.Money(400)


def test_cap_applies_after_the_route_grows():
    route = line()
    c = calc_at(SATURDAY, impl.WeekendCap(impl.Money(300)), route=route)
    route.append("X")
    assert c.calculate_fare("G", "X") == impl.Money(300)


# ---- 第 4 关：高峰加价、每日封顶与线程安全 ----

def test_peak_surcharge_only_on_weekdays_inside_the_window():
    peak = impl.PeakSurcharge(7, 10, 50)
    assert calc_at(MONDAY_RUSH, peak).calculate_fare("G", "I") == impl.Money(600)
    assert calc_at(datetime(2026, 10, 19, 10, 0), peak).calculate_fare("G", "I") == impl.Money(400)
    assert calc_at(datetime(2026, 10, 17, 8, 30), peak).calculate_fare("G", "I") == impl.Money(400)


def test_rules_apply_in_list_order():
    peak, cap = impl.PeakSurcharge(7, 10, 50), impl.WeekendCap(impl.Money(300))
    assert calc_at(MONDAY_RUSH, peak, cap).calculate_fare("G", "I") == impl.Money(600)
    assert calc_at(SATURDAY, peak, cap).calculate_fare("G", "I") == impl.Money(300)


def test_daily_cap_charges_only_the_remaining_room():
    ledger = impl.DailyCapLedger(calc_at(MONDAY), impl.Money(600))
    assert ledger.charge("ann", "G", "I", MONDAY) == impl.Money(400)
    assert ledger.charge("ann", "I", "G", MONDAY) == impl.Money(200)
    assert ledger.charge("ann", "G", "U", MONDAY) == impl.ZERO
    assert ledger.paid_today("ann", MONDAY.date()) == impl.Money(600)


def test_daily_cap_is_per_rider_and_per_day():
    ledger = impl.DailyCapLedger(calc_at(MONDAY), impl.Money(500))
    assert ledger.charge("ann", "G", "I", MONDAY) == impl.Money(400)
    assert ledger.charge("bob", "G", "I", MONDAY) == impl.Money(400)
    assert ledger.charge("ann", "G", "I", datetime(2026, 10, 20, 9, 0)) == impl.Money(400)


def test_daily_cap_uses_the_injected_clock_when_no_time_is_given():
    ledger = impl.DailyCapLedger(calc_at(MONDAY), impl.Money(500))
    assert ledger.charge("ann", "G", "I") == impl.Money(400)
    assert ledger.paid_today("ann", MONDAY.date()) == impl.Money(400)


def test_ledger_forgets_old_days_so_memory_stays_bounded():
    ledger = impl.DailyCapLedger(calc_at(MONDAY), impl.Money(500))
    for day in range(1, 29):
        ledger.charge("ann", "G", "U", datetime(2026, 9, day, 9, 0))
    assert ledger.tracked_days == 2


def test_concurrent_trips_never_exceed_the_daily_cap():
    ledger = impl.DailyCapLedger(calc_at(MONDAY), impl.Money(1000))
    barrier = threading.Barrier(16)
    charged: list[impl.Money] = []

    def ride():
        barrier.wait()
        charged.append(ledger.charge("ann", "G", "I", MONDAY))

    threads = [threading.Thread(target=ride) for _ in range(16)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(m.cents for m in charged) == 1000
    assert ledger.paid_today("ann", MONDAY.date()) == impl.Money(1000)


def test_concurrent_appends_and_quotes_stay_consistent():
    route = impl.Route(["s0"])
    c = calc_at(MONDAY, route=route)
    barrier = threading.Barrier(5)

    def grow(base):
        barrier.wait()
        for i in range(20):
            route.append(f"t{base}-{i}")

    threads = [threading.Thread(target=grow, args=(b,)) for b in range(4)]
    for t in threads:
        t.start()
    barrier.wait()
    for _ in range(200):
        snap = route.stations  # 站点只增不减，快照里每一站的位置以后不会变
        assert c.calculate_fare("s0", snap[-1]) == impl.Money(100 * (len(snap) - 1))
    for t in threads:
        t.join()
    assert len(route) == 81
    assert c.calculate_fare("s0", route.stations[-1]) == impl.Money(8000)
