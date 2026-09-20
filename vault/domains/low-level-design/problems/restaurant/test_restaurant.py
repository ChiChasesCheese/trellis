import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

NOW = datetime(2026, 9, 20, 18, 0, tzinfo=UTC)


def make_service(now=NOW, tables=(("T1", 2), ("T2", 2), ("T4", 4)), grace=timedelta(minutes=30)):
    clock = {"now": now}
    floor = impl.FloorManager(clock=lambda: clock["now"], grace=grace)
    for table_id, capacity in tables:
        floor.add_table(impl.Table(table_id, capacity))
    kitchen = impl.Kitchen()
    service = impl.RestaurantService(clock=lambda: clock["now"], floor=floor, kitchen=kitchen)
    service.add_menu_item(impl.MenuItem("starter", "沙拉", 1800, impl.Course.STARTER))
    service.add_menu_item(impl.MenuItem("main", "牛排", 6800, impl.Course.MAIN))
    service.add_menu_item(impl.MenuItem("dessert", "布丁", 1200, impl.Course.DESSERT))
    return service, floor, kitchen, clock


# ---- 第 1 关：入座、预订、候位 ------------------------------------------------


def test_seat_walk_in_picks_smallest_fitting_free_table():
    service, floor, kitchen, clock = make_service()
    order, waitlist_id = service.seat_walk_in(2)
    assert order is not None and waitlist_id is None
    assert order.table_id == "T1"  # T1 和 T2 都装得下 2 人，T1 先注册、id 更小


def test_seat_walk_in_waitlists_when_nothing_fits():
    service, floor, kitchen, clock = make_service(tables=(("T1", 2),))
    order, waitlist_id = service.seat_walk_in(5)
    assert order is None and waitlist_id is not None
    assert floor.waitlist_length == 1


def test_reservation_binds_smallest_fitting_table_and_seats_on_arrival():
    service, floor, kitchen, clock = make_service()
    reservation = service.reserve(4, NOW + timedelta(hours=1), timedelta(hours=1))
    assert reservation.table_id == "T4"
    order = service.seat_reservation(reservation.id)
    assert order.table_id == "T4"
    assert floor.table("T4").status is impl.TableStatus.OCCUPIED


def test_reservation_raises_when_no_table_ever_fits():
    service, floor, kitchen, clock = make_service(tables=(("T1", 2),))
    with pytest.raises(impl.NoTableAvailableError):
        service.reserve(6, NOW, timedelta(hours=1))


def test_reservation_overlap_is_rejected_for_the_only_fitting_table():
    service, floor, kitchen, clock = make_service(tables=(("T4", 4),))
    service.reserve(4, NOW, timedelta(hours=1))
    with pytest.raises(impl.NoTableAvailableError):
        service.reserve(4, NOW + timedelta(minutes=30), timedelta(hours=1))
    # 不重叠的时段可以正常订到同一张桌
    later = service.reserve(4, NOW + timedelta(hours=2), timedelta(hours=1))
    assert later.table_id == "T4"


def test_reseat_from_waitlist_skips_a_party_too_big_and_seats_the_next_that_fits():
    service, floor, kitchen, clock = make_service(tables=(("T1", 2),))
    first_order, _ = service.seat_walk_in(2)
    assert first_order.table_id == "T1"
    _, too_big_id = service.seat_walk_in(4)   # 永远坐不下 T1，排在候位队首
    _, fits_id = service.seat_walk_in(2)      # 坐得下，但排在队伍第二位
    floor.clear_table("T1")
    reseated = service.reseat_waitlist("T1")
    assert reseated is not None and reseated.table_id == "T1"
    assert floor.waitlist_length == 1   # 队首那个太大的一批仍然在等


def test_unclaimed_reservation_holds_the_table_until_the_grace_period():
    service, floor, kitchen, clock = make_service(tables=(("T4", 4),), grace=timedelta(minutes=30))
    service.reserve(4, NOW, timedelta(hours=1))
    order, waitlist_id = service.seat_walk_in(4)   # 宽限期内，T4 被预订占着，散客坐不进去
    assert order is None and waitlist_id is not None


def test_reservation_expires_after_grace_and_frees_the_table_for_walk_ins():
    service, floor, kitchen, clock = make_service(tables=(("T4", 4),), grace=timedelta(minutes=30))
    service.reserve(4, NOW, timedelta(hours=1))
    assert floor.reservation_count == 1
    clock["now"] = NOW + timedelta(minutes=31)   # 过了宽限期，还没人来认领
    order, waitlist_id = service.seat_walk_in(4)
    assert order is not None and order.table_id == "T4"
    assert waitlist_id is None
    assert floor.reservation_count == 0          # 过期的预订被清掉了，不会永远占着这个时段


def test_reservation_expiry_gives_the_waitlist_a_chance_at_the_table():
    service, floor, kitchen, clock = make_service(tables=(("T4", 4),), grace=timedelta(minutes=30))
    service.reserve(4, NOW, timedelta(hours=1))
    order, waitlist_id = service.seat_walk_in(2)   # 宽限期内坐不进去，进候位
    assert order is None and waitlist_id is not None
    clock["now"] = NOW + timedelta(minutes=31)
    assert floor.waitlist_length == 0   # 单是查询也会先把世界推到当前时刻，候位的人被顶上去了


def test_seating_an_expired_reservation_raises():
    service, floor, kitchen, clock = make_service(tables=(("T4", 4),), grace=timedelta(minutes=30))
    reservation = service.reserve(4, NOW, timedelta(hours=1))
    clock["now"] = NOW + timedelta(minutes=31)
    with pytest.raises(impl.UnknownReservationError):
        service.seat_reservation(reservation.id)


# ---- 第 2 关：点单、拆账 -----------------------------------------------------


def test_submit_items_orders_lines_in_ordered_state():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    lines = service.submit_items(order.id, [("starter", 1), ("main", 1)])
    assert all(l.state is impl.LineState.ORDERED for l in lines)
    assert {l.menu_item_id for l in lines} == {"starter", "main"}


def test_line_illegal_transition_is_rejected():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    (line,) = service.submit_items(order.id, [("starter", 1)])
    with pytest.raises(impl.IllegalLineTransitionError):
        line.transition_to(impl.LineState.SERVED)  # 不能跳过 PREPARING/READY


def test_served_total_counts_only_served_lines():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    a, b = service.submit_items(order.id, [("starter", 1), ("dessert", 1)])
    assert order.served_total == 0
    a.transition_to(impl.LineState.PREPARING)
    a.transition_to(impl.LineState.READY)
    service.serve(order.id, a.id)
    assert order.served_total == 1800
    assert b.state is impl.LineState.ORDERED  # 没上桌的不计入账单


def test_partial_payment_then_more_items_grows_balance_again():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    (a,) = service.submit_items(order.id, [("starter", 1)])
    a.transition_to(impl.LineState.PREPARING)
    a.transition_to(impl.LineState.READY)
    service.serve(order.id, a.id)
    service.record_payment(order.id, 1800)
    assert order.balance_due == 0
    (b,) = service.submit_items(order.id, [("dessert", 1)])
    b.transition_to(impl.LineState.PREPARING)
    b.transition_to(impl.LineState.READY)
    service.serve(order.id, b.id)
    assert order.balance_due == 1200  # 加的菜上桌后，余额重新变大


def test_split_even_gives_the_remainder_to_the_first_payers_in_order():
    assert impl.split_even(100, 3) == (34, 33, 33)
    assert impl.split_even(90, 3) == (30, 30, 30)


def test_split_by_share_sums_to_amount_and_is_deterministic():
    shares = [1, 1, 2]
    result = impl.split_by_share(101, shares)
    assert sum(result) == 101
    assert impl.split_by_share(101, shares) == result  # 同样输入永远同样输出


def test_split_by_item_requires_exact_coverage_of_served_lines():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    a, b = service.submit_items(order.id, [("starter", 1), ("dessert", 1)])
    for line in (a, b):
        line.transition_to(impl.LineState.PREPARING)
        line.transition_to(impl.LineState.READY)
        service.serve(order.id, line.id)
    result = impl.split_by_item(order.lines, {"alice": (a.id,), "bob": (b.id,)})
    assert result == {"alice": 1800, "bob": 1200}
    with pytest.raises(impl.SplitMismatchError):
        impl.split_by_item(order.lines, {"alice": (a.id,)})  # 漏了 b


def test_close_order_requires_settlement_and_frees_the_table():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    (a,) = service.submit_items(order.id, [("starter", 1)])
    with pytest.raises(impl.SettlementError):
        service.close_order(order.id)
    a.transition_to(impl.LineState.PREPARING)
    a.transition_to(impl.LineState.READY)
    service.serve(order.id, a.id)
    service.record_payment(order.id, 1800)
    service.close_order(order.id)
    assert floor.table(order.table_id).status is impl.TableStatus.FREE


def test_close_order_forgets_it_in_the_kitchen_so_the_index_does_not_grow_forever():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    (a,) = service.submit_items(order.id, [("starter", 1)])
    assert kitchen.known_order_count == 1
    a.transition_to(impl.LineState.PREPARING)
    a.transition_to(impl.LineState.READY)
    service.serve(order.id, a.id)
    service.record_payment(order.id, 1800)
    service.close_order(order.id)
    assert kitchen.known_order_count == 0


# ---- 第 3 关：后厨队列、课程门禁、缺货 -----------------------------------------


def test_main_is_not_eligible_until_starter_is_ready():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    service.submit_items(order.id, [("starter", 1), ("main", 1)])
    started = service.start_next_in_kitchen()
    assert started.menu_item_id == "starter"   # 主菜还没资格开始做
    assert service.start_next_in_kitchen() is None


def test_main_becomes_eligible_once_starter_is_ready():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    service.submit_items(order.id, [("starter", 1), ("main", 1)])
    starter = service.start_next_in_kitchen()
    service.mark_ready(order.id, starter.id)
    main = service.start_next_in_kitchen()
    assert main.menu_item_id == "main"


def test_mark_unavailable_cancels_queued_lines_and_blocks_new_orders():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    (a,) = service.submit_items(order.id, [("main", 1)])
    kitchen.mark_unavailable("main")
    assert a.state is impl.LineState.UNAVAILABLE
    with pytest.raises(impl.ItemUnavailableError):
        service.submit_items(order.id, [("main", 1)])


def test_mark_unavailable_rolls_back_the_whole_batch_leaving_no_partial_lines():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    kitchen.mark_unavailable("main")
    with pytest.raises(impl.ItemUnavailableError):
        service.submit_items(order.id, [("starter", 1), ("main", 1)])
    assert order.lines == ()   # 缺货一道，整批一行都不留


def test_floor_status_reports_pending_lines_per_table():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(2)
    service.submit_items(order.id, [("starter", 1)])
    status = service.floor_status()
    assert order.table_id in status
    assert len(status[order.table_id]) == 1


# ---- 第 4 关：外带/外送不碰桌位 -----------------------------------------------


def test_takeaway_order_does_not_touch_any_table():
    service, floor, kitchen, clock = make_service()
    order = service.open_takeaway_order()
    assert order.table_id is None
    service.submit_items(order.id, [("starter", 1)])
    assert all(t.status is impl.TableStatus.FREE for t in
              (floor.table("T1"), floor.table("T2"), floor.table("T4")))


def test_delivery_order_shares_the_same_kitchen_pipeline():
    service, floor, kitchen, clock = make_service()
    order = service.open_delivery_order()
    (line,) = service.submit_items(order.id, [("starter", 1)])
    started = service.start_next_in_kitchen()
    assert started.id == line.id


# ---- 并发：不变量而不是计时 ---------------------------------------------------


def test_concurrent_walk_ins_never_double_seat_the_same_table():
    service, floor, kitchen, clock = make_service(
        tables=[(f"T{i}", 2) for i in range(8)])
    barrier = threading.Barrier(8)
    seated_tables: list[str] = []
    lock = threading.Lock()

    def worker():
        barrier.wait()
        order, _ = service.seat_walk_in(2)
        if order is not None:
            with lock:
                seated_tables.append(order.table_id)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(seated_tables) == 8
    assert len(set(seated_tables)) == 8   # 每张桌子只坐进去一拨人


def test_concurrent_kitchen_start_next_never_returns_the_same_line_twice():
    service, floor, kitchen, clock = make_service()
    order, _ = service.seat_walk_in(4)
    requests = [("starter", 1)] * 6
    service.submit_items(order.id, requests)
    barrier = threading.Barrier(6)
    started: list[object] = []
    lock = threading.Lock()

    def worker():
        barrier.wait()
        line = service.start_next_in_kitchen()
        if line is not None:
            with lock:
                started.append(line)

    threads = [threading.Thread(target=worker) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(started) == 6
    assert len({id(l) for l in started}) == 6


def test_table_cannot_be_occupied_or_freed_twice():
    table = impl.Table("T1", 2)
    table.occupy()
    with pytest.raises(impl.TableOccupiedError):
        table.occupy()
    table.free()
    with pytest.raises(impl.TableOccupiedError):
        table.free()
