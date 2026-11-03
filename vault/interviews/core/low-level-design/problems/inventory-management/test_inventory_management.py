"""库存管理的测试：`-k part1` 选第 1 关，依此类推。时间用假时钟，线程用屏障对齐，不靠 sleep 估时间。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Status = impl.Status

T = 5.0


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make(stock=(("A", 10), ("B", 5)), sku="widget"):
    clock = Clock()
    inv = impl.Inventory(clock=clock)
    for warehouse, quantity in stock:
        inv.add_stock(warehouse, sku, quantity)
    return inv, clock


def alloc(reservation):
    return [(a.warehouse, a.quantity) for a in reservation.allocations]


def run_threads(n, target):
    barrier = threading.Barrier(n)

    def wrapped(i):
        barrier.wait(T)
        target(i)

    threads = [threading.Thread(target=wrapped, args=(i,), daemon=True) for i in range(n)]
    [t.start() for t in threads]
    [t.join(T * 2) for t in threads]
    assert not any(t.is_alive() for t in threads)


# ---- 第 1 关：多仓库存、预留、确认、取消 ---------------------------------------


def test_part1_stock_is_tracked_per_warehouse_and_in_total():
    inv, _ = make()
    assert inv.on_hand("widget") == 15 and inv.available("widget") == 15
    assert inv.on_hand("widget", "A") == 10 and inv.on_hand("widget", "B") == 5
    assert inv.on_hand("widget", "Z") == 0 and inv.on_hand("nothing") == 0 and inv.available("nothing") == 0
    inv.add_stock("A", "widget", 3)
    assert inv.on_hand("widget", "A") == 13


@pytest.mark.parametrize("bad", [0, -1, 1.5, "3", None, True])
def test_part1_quantities_must_be_positive_integers(bad):
    inv, _ = make()
    with pytest.raises(impl.InvalidQuantity):
        inv.add_stock("A", "widget", bad)
    with pytest.raises(impl.InvalidQuantity):
        inv.reserve("widget", bad)
    assert issubclass(impl.InvalidQuantity, ValueError) and issubclass(impl.InvalidQuantity, impl.InventoryError)


def test_part1_reserve_takes_from_the_warehouse_with_the_most_available_stock():
    inv, _ = make()
    r = inv.reserve("widget", 4)
    assert alloc(r) == [("A", 4)] and r.sku == "widget" and r.quantity == 4
    assert r.status is Status.ACTIVE and r.expires_at is None
    assert inv.available("widget", "A") == 6 and inv.available("widget") == 11
    assert inv.on_hand("widget") == 15                                # 预留只占用，不减在架


def test_part1_a_reservation_may_span_warehouses_and_ties_go_to_the_smaller_name():
    inv, _ = make()
    assert alloc(inv.reserve("widget", 12)) == [("A", 10), ("B", 2)]
    inv2, _ = make(stock=(("B", 5), ("A", 5)))
    assert alloc(inv2.reserve("widget", 7)) == [("A", 5), ("B", 2)]  # 一样多：仓库名小的先


def test_part1_allocation_follows_what_is_still_free():
    inv, _ = make()
    inv.reserve("widget", 8)                                          # A 剩 2，B 剩 5
    assert alloc(inv.reserve("widget", 6)) == [("B", 5), ("A", 1)]    # 现在 B 可售最多


def test_part1_out_of_stock_is_all_or_nothing_and_reports_what_was_available():
    inv, _ = make()
    inv.reserve("widget", 10)
    with pytest.raises(impl.OutOfStock) as e:
        inv.reserve("widget", 6)
    assert (e.value.sku, e.value.requested, e.value.available) == ("widget", 6, 5)
    assert inv.available("widget") == 5                               # 没有先占走一部分
    with pytest.raises(impl.OutOfStock) as e2:
        inv.reserve("ghost", 1)
    assert e2.value.available == 0


def test_part1_the_whole_stock_can_be_reserved_exactly():
    inv, _ = make()
    r = inv.reserve("widget", 15)
    assert sum(q for _, q in alloc(r)) == 15 and inv.available("widget") == 0
    with pytest.raises(impl.OutOfStock):
        inv.reserve("widget", 1)


def test_part1_cancel_returns_stock_and_is_idempotent():
    inv, _ = make()
    r = inv.reserve("widget", 12)
    inv.cancel(r.id)
    assert inv.available("widget") == 15 and inv.get(r.id).status is Status.CANCELLED
    inv.cancel(r.id)
    assert inv.available("widget") == 15                              # 重复取消不会多放回
    assert alloc(inv.reserve("widget", 12)) == [("A", 10), ("B", 2)]


def test_part1_confirm_ships_the_stock_and_is_idempotent():
    inv, _ = make()
    r = inv.reserve("widget", 12)
    inv.confirm(r.id)
    assert inv.on_hand("widget") == 3 and inv.available("widget") == 3
    assert (inv.on_hand("widget", "A"), inv.on_hand("widget", "B")) == (0, 3)
    assert inv.get(r.id).status is Status.CONFIRMED
    inv.confirm(r.id)
    assert inv.on_hand("widget") == 3                                 # 重复确认不会再扣


def test_part1_confirmed_and_cancelled_reservations_cannot_switch_sides():
    inv, _ = make()
    a, b = inv.reserve("widget", 1), inv.reserve("widget", 1)
    inv.confirm(a.id)
    inv.cancel(b.id)
    with pytest.raises(impl.InvalidState):
        inv.cancel(a.id)                                              # 已经发货了
    with pytest.raises(impl.InvalidState):
        inv.confirm(b.id)                                             # 已经取消了
    assert inv.on_hand("widget") == 14 and inv.available("widget") == 14


def test_part1_unknown_reservations_raise():
    inv, _ = make()
    for call in (inv.confirm, inv.cancel, inv.get):
        with pytest.raises(impl.UnknownReservation):
            call("nope")
    assert issubclass(impl.UnknownReservation, LookupError)


def test_part1_skus_are_independent_and_reservation_ids_unique():
    inv, _ = make()
    inv.add_stock("A", "gadget", 2)
    a, b, c = inv.reserve("widget", 1), inv.reserve("gadget", 2), inv.reserve("widget", 1)
    assert len({a.id, b.id, c.id}) == 3
    assert inv.available("gadget") == 0 and inv.available("widget") == 13


def test_part1_reservation_is_an_immutable_snapshot():
    inv, _ = make()
    r = inv.reserve("widget", 3)
    with pytest.raises(AttributeError):
        r.quantity = 99
    inv.cancel(r.id)
    assert r.status is Status.ACTIVE and inv.get(r.id).status is Status.CANCELLED   # 旧快照不会变


# ---- 第 2 关：过期、延期 -------------------------------------------------------


def test_part2_reservation_expires_exactly_at_its_deadline():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=10)
    assert r.expires_at == 110.0
    clock.advance(9.99)
    assert inv.available("widget") == 10 and inv.get(r.id).status is Status.ACTIVE
    clock.advance(0.01)                                               # 恰好到点：已经过期
    assert inv.available("widget") == 15 and inv.get(r.id).status is Status.EXPIRED


def test_part2_expired_stock_is_immediately_available_to_the_next_reservation():
    inv, clock = make()
    inv.reserve("widget", 15, ttl=5)
    with pytest.raises(impl.OutOfStock):
        inv.reserve("widget", 1)
    clock.advance(5)
    assert sum(q for _, q in alloc(inv.reserve("widget", 15))) == 15


def test_part2_confirm_after_expiry_fails_and_cancel_is_a_no_op():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=10)
    clock.advance(10)
    with pytest.raises(impl.ReservationExpired):
        inv.confirm(r.id)
    inv.cancel(r.id)
    assert inv.available("widget") == 15 and inv.on_hand("widget") == 15
    assert issubclass(impl.ReservationExpired, impl.InventoryError)


def test_part2_confirm_before_the_deadline_works_and_later_time_changes_nothing():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=10)
    clock.advance(9)
    inv.confirm(r.id)
    clock.advance(1000)
    assert inv.get(r.id).status is Status.CONFIRMED
    assert inv.on_hand("widget") == 10 and inv.available("widget") == 10


def test_part2_cancelled_reservations_are_not_released_twice_when_their_time_comes():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=10)
    inv.cancel(r.id)
    other = inv.reserve("widget", 5)                                  # 占住同样多的库存
    clock.advance(1000)
    assert inv.get(r.id).status is Status.CANCELLED
    assert inv.available("widget") == 10 and inv.get(other.id).status is Status.ACTIVE


def test_part2_reservations_without_ttl_never_expire():
    inv, clock = make()
    r = inv.reserve("widget", 5)
    clock.advance(10 ** 9)
    assert inv.get(r.id).status is Status.ACTIVE and inv.available("widget") == 10


def test_part2_extend_counts_from_now_and_the_old_deadline_no_longer_applies():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=10)                              # 到 110
    clock.advance(5)
    r2 = inv.extend(r.id, 10)                                         # 到 115，不是 120
    assert r2.expires_at == 115.0 and r2.status is Status.ACTIVE
    clock.advance(5)                                                  # 110：原来的期限到了，但已经延期
    assert inv.get(r.id).status is Status.ACTIVE and inv.available("widget") == 10
    clock.advance(4.99)
    assert inv.get(r.id).status is Status.ACTIVE
    clock.advance(0.01)
    assert inv.get(r.id).status is Status.EXPIRED and inv.available("widget") == 15


def test_part2_extend_can_also_shorten_and_can_add_an_expiry():
    inv, clock = make()
    r = inv.reserve("widget", 5, ttl=100)
    inv.extend(r.id, 1)
    clock.advance(1)
    assert inv.get(r.id).status is Status.EXPIRED
    forever = inv.reserve("widget", 5)
    inv.extend(forever.id, 10)
    clock.advance(10)
    assert inv.get(forever.id).status is Status.EXPIRED


def test_part2_extend_rejects_finished_reservations_and_bad_ttl():
    inv, clock = make()
    a, b, c = inv.reserve("widget", 1, ttl=5), inv.reserve("widget", 1), inv.reserve("widget", 1)
    inv.confirm(b.id)
    inv.cancel(c.id)
    clock.advance(5)
    with pytest.raises(impl.ReservationExpired):
        inv.extend(a.id, 10)
    for done in (b, c):
        with pytest.raises(impl.InvalidState):
            inv.extend(done.id, 10)
    with pytest.raises(impl.UnknownReservation):
        inv.extend("nope", 10)
    live = inv.reserve("widget", 1)
    for ttl in (0, -3):
        with pytest.raises(ValueError):
            inv.extend(live.id, ttl)
        with pytest.raises(ValueError):
            inv.reserve("widget", 1, ttl=ttl)


def test_part2_many_reservations_expire_in_deadline_order_in_one_step():
    inv, clock = make(stock=(("A", 100),))
    ids = [inv.reserve("widget", 10, ttl=t).id for t in (30, 10, 20, 40, 50)]
    clock.advance(25)                                                 # 10 和 20 已到点
    assert [inv.get(i).status for i in ids] == [Status.ACTIVE, Status.EXPIRED, Status.EXPIRED,
                                                Status.ACTIVE, Status.ACTIVE]
    assert inv.available("widget") == 100 - 30
    clock.advance(100)
    assert inv.available("widget") == 100


def test_part2_expiry_releases_exactly_the_allocated_warehouses():
    inv, clock = make()
    inv.reserve("widget", 12, ttl=5)                                  # A 10 + B 2
    clock.advance(5)
    assert (inv.available("widget", "A"), inv.available("widget", "B")) == (10, 5)


# ---- 第 3 关：并发不超卖、多件商品的原子预留 ------------------------------------


def test_part3_concurrent_reservations_never_oversell():
    inv, _ = make(stock=(("A", 60), ("B", 40)))
    wins, errors = [], []
    lock = threading.Lock()

    def worker(i):
        for _ in range(10):
            try:
                r = inv.reserve("widget", 1)
                with lock:
                    wins.append(r)
            except impl.OutOfStock as e:
                with lock:
                    errors.append(e)

    run_threads(16, worker)
    assert len(wins) == 100 and len(errors) == 60                     # 160 次尝试，正好 100 件
    assert len({r.id for r in wins}) == 100
    assert inv.available("widget") == 0 and inv.on_hand("widget") == 100
    per_warehouse = {"A": 0, "B": 0}
    for r in wins:
        for a in r.allocations:
            per_warehouse[a.warehouse] += a.quantity
    assert per_warehouse == {"A": 60, "B": 40}


def test_part3_big_concurrent_reservations_split_the_stock_without_overlap():
    inv, _ = make(stock=(("A", 30), ("B", 30)))
    got = []
    lock = threading.Lock()

    def worker(i):
        try:
            r = inv.reserve("widget", 25)
            with lock:
                got.append(r)
        except impl.OutOfStock:
            pass

    run_threads(8, worker)
    assert len(got) == 2                                              # 60 件最多满足两个 25，第三个只剩 10
    assert inv.available("widget") == 10
    assert sum(a.quantity for r in got for a in r.allocations) == 50


def test_part3_reserve_and_cancel_churn_leaves_the_books_balanced():
    inv, _ = make(stock=(("A", 4), ("B", 4)))

    def worker(i):
        for _ in range(100):
            try:
                r = inv.reserve("widget", 2)
            except impl.OutOfStock:
                continue
            inv.cancel(r.id)

    run_threads(8, worker)
    assert inv.available("widget") == 8 and inv.on_hand("widget") == 8
    assert inv.available("widget", "A") == 4 and inv.available("widget", "B") == 4


def test_part3_concurrent_confirms_of_one_reservation_ship_once():
    inv, _ = make()
    r = inv.reserve("widget", 7)
    run_threads(8, lambda i: inv.confirm(r.id))
    assert inv.on_hand("widget") == 8 and inv.available("widget") == 8


def test_part3_reserve_many_is_all_or_nothing():
    inv, _ = make()
    inv.add_stock("A", "gadget", 1)
    with pytest.raises(impl.OutOfStock) as e:
        inv.reserve_many({"widget": 3, "gadget": 2})
    assert e.value.sku == "gadget" and e.value.available == 1
    assert inv.available("widget") == 15 and inv.available("gadget") == 1    # widget 没有被先占走
    rs = inv.reserve_many({"gadget": 1, "widget": 3})
    assert [r.sku for r in rs] == ["gadget", "widget"]                        # 按 sku 排序
    assert inv.available("widget") == 12 and inv.available("gadget") == 0


def test_part3_reserve_many_reports_the_first_missing_sku_in_sorted_order_and_validates_input():
    inv, _ = make()
    with pytest.raises(impl.OutOfStock) as e:
        inv.reserve_many({"zeta": 1, "alpha": 1, "widget": 1})
    assert e.value.sku == "alpha"
    with pytest.raises(ValueError):
        inv.reserve_many({})
    with pytest.raises(impl.InvalidQuantity):
        inv.reserve_many({"widget": 0})
    with pytest.raises(ValueError):
        inv.reserve_many({"widget": 1}, ttl=0)
    assert inv.available("widget") == 15


def test_part3_reserve_many_applies_the_ttl_to_every_line():
    inv, clock = make()
    inv.add_stock("A", "gadget", 5)
    rs = inv.reserve_many({"widget": 2, "gadget": 2}, ttl=10)
    assert {r.expires_at for r in rs} == {110.0}
    clock.advance(10)
    assert inv.available("widget") == 15 and inv.available("gadget") == 5


def test_part3_failed_reserve_many_attempts_never_leak_stock_under_concurrency():
    inv, _ = make()
    inv.add_stock("A", "gadget", 1)                                   # gadget 只有一件，widget 有十五件
    wins = []
    lock = threading.Lock()

    def worker(i):
        try:
            rs = inv.reserve_many({"widget": 1, "gadget": 1} if i % 2 else {"gadget": 1, "widget": 1})
            with lock:
                wins.append(rs)
        except impl.OutOfStock:
            pass

    run_threads(12, worker)
    assert len(wins) == 1
    assert inv.available("gadget") == 0 and inv.available("widget") == 14   # 失败的 11 次没有占走任何 widget


def test_part3_reserve_many_in_opposite_orders_cannot_deadlock_and_stays_consistent():
    inv, _ = make(stock=(("A", 20),))
    inv.add_stock("A", "gadget", 20)
    wins = []
    lock = threading.Lock()

    def worker(i):
        for _ in range(5):
            lines = {"widget": 1, "gadget": 1} if i % 2 else {"gadget": 1, "widget": 1}
            try:
                inv.reserve_many(lines)
                with lock:
                    wins.append(1)
            except impl.OutOfStock:
                pass

    run_threads(8, worker)
    assert len(wins) == 20                                            # 两种商品各 20 件：恰好 20 次成功
    assert inv.available("widget") == inv.available("gadget") == 0


# ---- 第 4 关（选做）：仓间调拨、库存快照 ---------------------------------------


def test_part4_transfer_moves_free_stock_between_warehouses():
    inv, _ = make()
    inv.transfer("widget", "A", "B", 4)
    assert (inv.on_hand("widget", "A"), inv.on_hand("widget", "B")) == (6, 9)
    inv.transfer("widget", "A", "C", 1)                               # 目标仓库可以是新的
    assert inv.on_hand("widget", "C") == 1 and inv.on_hand("widget") == 15


def test_part4_transfer_never_moves_reserved_stock():
    inv, _ = make()
    r = inv.reserve("widget", 8)                                      # A 被占 8，A 可售 2
    with pytest.raises(impl.OutOfStock) as e:
        inv.transfer("widget", "A", "B", 3)
    assert e.value.available == 2
    inv.transfer("widget", "A", "B", 2)
    assert inv.get(r.id).allocations == (impl.Allocation("A", 8),)    # 已有预留的分配不变
    inv.confirm(r.id)                                                 # 仍然能从 A 发货
    assert inv.on_hand("widget", "A") == 0 and inv.on_hand("widget", "B") == 7


def test_part4_expired_reservations_free_their_stock_for_transfer():
    inv, clock = make()
    inv.reserve("widget", 10, ttl=5)
    with pytest.raises(impl.OutOfStock):
        inv.transfer("widget", "A", "B", 1)
    clock.advance(5)
    inv.transfer("widget", "A", "B", 10)
    assert inv.on_hand("widget", "B") == 15


def test_part4_transfer_validates_its_arguments():
    inv, _ = make()
    with pytest.raises(ValueError):
        inv.transfer("widget", "A", "A", 1)
    with pytest.raises(impl.InvalidQuantity):
        inv.transfer("widget", "A", "B", 0)
    with pytest.raises(impl.OutOfStock):
        inv.transfer("widget", "Z", "B", 1)
    with pytest.raises(impl.OutOfStock):
        inv.transfer("ghost", "A", "B", 1)
    assert inv.on_hand("widget") == 15


def test_part4_snapshot_is_sorted_and_immutable():
    inv, _ = make()
    inv.add_stock("A", "gadget", 2)
    inv.reserve("widget", 4)
    rows = inv.snapshot()
    assert [(r.sku, r.warehouse, r.on_hand, r.reserved) for r in rows] == [
        ("gadget", "A", 2, 0), ("widget", "A", 10, 4), ("widget", "B", 5, 0)]
    inv.add_stock("B", "widget", 100)
    assert rows[2].on_hand == 5
    with pytest.raises(AttributeError):
        rows[0].on_hand = 0


def test_part4_snapshots_taken_during_transfers_are_consistent():
    inv, _ = make(stock=(("A", 10), ("B", 5)))
    stop = threading.Event()
    bad = []

    def mover():
        try:
            for i in range(300):
                inv.transfer("widget", "A", "B", 1)
                inv.transfer("widget", "B", "A", 1)
        finally:
            stop.set()

    def reader():
        while not stop.is_set():
            total = sum(r.on_hand for r in inv.snapshot() if r.sku == "widget")
            if total != 15:                                           # 调拨是原子的：总量任何时刻都是 15
                bad.append(total)

    run_threads(3, lambda i: mover() if i == 0 else reader())
    assert bad == []
