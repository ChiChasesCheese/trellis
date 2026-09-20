"""外卖配送参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 9, 20, 11, 30, tzinfo=UTC)
MENU = (("m1", "主菜", 3800, 12), ("m2", "米饭", 300, 2))


def make_clock(start: datetime = T0):
    """一个可以手动拨动的假时钟：`clock()` 读当前值，`advance()` 往前拨。"""
    state = {"now": start}

    def clock() -> datetime:
        return state["now"]

    def advance(delta: timedelta) -> None:
        state["now"] += delta

    return clock, advance


def build(clock, couriers=(("c1", 0.0, 0.0),), max_courier_wait=2, max_added_delay=5,
          max_batch=3, speed=0.4):
    """造一个平台，返回 (service, pool)。骑手默认就停在 R1 门口，路程为 0。"""
    pool = impl.CourierPool()
    for courier_id, x, y in couriers:
        pool.go_online(courier_id, impl.Location(x, y))
    service = impl.DeliveryService(
        clock=clock, couriers=pool, speed_km_per_minute=speed,
        max_courier_wait=timedelta(minutes=max_courier_wait),
        max_added_delay=timedelta(minutes=max_added_delay), max_batch_size=max_batch)
    return service, pool


def add_restaurant(service, restaurant_id="R1", at=(0.0, 0.0), base=5, menu=MENU):
    r = impl.Restaurant(restaurant_id, restaurant_id, impl.Location(*at),
                        base_prep=timedelta(minutes=base))
    for item_id, name, price, prep in menu:
        r.add_item(impl.MenuItem(item_id, name, price, prep_minutes=prep))
    service.register(r)
    return r


def place(service, customer="u1", restaurant_id="R1", wanted=None, drop=(0.0, 2.0), **kw):
    return service.place_order(customer, restaurant_id, wanted or {"m1": 1, "m2": 2},
                               impl.Location(*drop), **kw)


# ---- 第 1 关：菜单、下单、三方状态机 -----------------------------------------


def test_placing_an_order_snapshots_the_price_at_that_moment():
    """事后改价不追溯已下的单——订单行抄下的是下单那一刻的价格。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    restaurant = add_restaurant(service)
    order = place(service)
    assert order.subtotal == 3800 + 2 * 300
    assert order.total == order.subtotal + 500
    restaurant.add_item(impl.MenuItem("m1", "主菜", 9900, prep_minutes=12))
    assert order.subtotal == 3800 + 2 * 300


def test_a_sold_out_item_fails_the_whole_order_not_part_of_it():
    """不做部分履约：三道菜缺一道就整单失败，少送一道的配送成本一分不少。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    restaurant = add_restaurant(service)
    restaurant.set_sold_out("m1")
    with pytest.raises(impl.ItemUnavailableError):
        place(service)
    assert [i.id for i in restaurant.available_items()] == ["m2"]
    restaurant.set_sold_out("m1", False)
    assert place(service).subtotal == 3800 + 600


def test_a_closed_restaurant_takes_no_new_order():
    clock, _ = make_clock()
    service, _ = build(clock)
    restaurant = add_restaurant(service)
    restaurant.set_open(False)
    with pytest.raises(impl.RestaurantClosedError):
        place(service)


def test_accepting_computes_ready_time_from_the_slowest_dish_not_the_sum():
    """后厨是并行的：出餐时间 = 基础准备 + 最慢的那道菜，不是所有菜相加。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service, base=5)
    order = service.accept(place(service).id)
    assert order.ready_at == T0 + timedelta(minutes=17)
    assert order.state is impl.OrderState.ACCEPTED


def test_the_happy_path_records_who_did_every_step():
    clock, advance = make_clock()
    service, pool = build(clock)
    add_restaurant(service)
    order = place(service)
    service.accept(order.id)
    advance(timedelta(minutes=15))
    service.dispatch_due()
    service.mark_ready(order.id)
    service.pick_up(order.id)
    service.deliver(order.id)
    assert order.state is impl.OrderState.DELIVERED
    assert [(c.current, c.by) for c in order.history] == [
        (impl.OrderState.ACCEPTED, impl.Actor.RESTAURANT),
        (impl.OrderState.READY, impl.Actor.RESTAURANT),
        (impl.OrderState.PICKED_UP, impl.Actor.COURIER),
        (impl.OrderState.DELIVERED, impl.Actor.COURIER)]
    assert pool.idle_count == 1
    assert service.open_batch_count == 0


def test_an_impossible_edge_and_an_unauthorised_edge_raise_different_errors():
    """这道题的设计核心：边不存在和边存在但越权，是两种错误。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    order = place(service)
    with pytest.raises(impl.IllegalTransitionError):
        order.transition_to(impl.OrderState.PICKED_UP, T0, impl.Actor.COURIER)
    with pytest.raises(impl.NotPermittedError):
        order.transition_to(impl.OrderState.ACCEPTED, T0, impl.Actor.CUSTOMER)
    assert order.state is impl.OrderState.PLACED


def test_a_customer_cannot_mark_the_order_ready_or_delivered():
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    order = service.accept(place(service).id)
    with pytest.raises(impl.NotPermittedError):
        order.transition_to(impl.OrderState.READY, T0, impl.Actor.CUSTOMER)
    service.mark_ready(order.id)
    with pytest.raises(impl.NotPermittedError):
        order.transition_to(impl.OrderState.PICKED_UP, T0, impl.Actor.CUSTOMER)


def test_the_customer_may_cancel_before_acceptance_but_not_after():
    """餐厅一旦接单，菜就在做了，成本已经发生——顾客不能再单方面取消。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    first = place(service)
    service.cancel(first.id, impl.Actor.CUSTOMER, "改主意了")
    assert first.state is impl.OrderState.CANCELLED

    second = service.accept(place(service, customer="u2").id)
    with pytest.raises(impl.NotPermittedError):
        service.cancel(second.id, impl.Actor.CUSTOMER)
    service.cancel(second.id, impl.Actor.PLATFORM, "骑手全都忙不过来")
    assert second.state is impl.OrderState.CANCELLED


def test_a_rejected_order_is_terminal():
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    order = service.reject(place(service).id, "今天食材用完了")
    assert order.state is impl.OrderState.REJECTED
    assert order.history[-1].reason == "今天食材用完了"
    with pytest.raises(impl.IllegalTransitionError):
        service.accept(order.id)


# ---- 第 2 关：派单时机 -------------------------------------------------------


def test_no_courier_is_dispatched_before_the_restaurant_accepts():
    """派了骑手餐厅再拒单，骑手就白跑了——所以接单之前一个骑手都不派。"""
    clock, advance = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    order = place(service)
    advance(timedelta(minutes=60))
    assert service.dispatch_due() == ()
    assert order.batch_id is None


def test_dispatch_waits_so_the_courier_idles_at_most_the_configured_slack():
    """本策略优化的是食物温度：宁可骑手空等两分钟，也不让做好的菜等骑手。"""
    clock, advance = make_clock()
    service, pool = build(clock, couriers=(("c1", 2.0, 0.0),), max_courier_wait=2, speed=0.4)
    add_restaurant(service)                      # 骑手离店 2 公里 = 5 分钟
    order = service.accept(place(service).id)    # 17 分钟后出餐
    advance(timedelta(minutes=9))
    assert service.dispatch_due() == (), "太早派，骑手会在店里空等八分钟"
    advance(timedelta(minutes=1))                # T0+10：现在出发，T0+15 到店
    batches = service.dispatch_due()
    assert len(batches) == 1
    arrival = clock() + timedelta(minutes=5)
    assert timedelta() <= order.ready_at - arrival <= timedelta(minutes=2)


def test_a_courier_too_far_to_arrive_in_time_is_dispatched_immediately():
    """来不及的时候立刻发车——晚到的代价是菜凉，比骑手空等严重得多。"""
    clock, _ = make_clock()
    service, _ = build(clock, couriers=(("c1", 20.0, 0.0),), speed=0.4)   # 50 分钟路程
    add_restaurant(service)
    service.accept(place(service).id)
    assert len(service.dispatch_due()) == 1


def test_with_no_courier_online_the_order_simply_waits():
    clock, advance = make_clock()
    service, _ = build(clock, couriers=())
    add_restaurant(service)
    order = service.accept(place(service).id)
    advance(timedelta(minutes=30))
    assert service.dispatch_due() == ()
    assert order.batch_id is None and order.state is impl.OrderState.ACCEPTED


# ---- 第 3 关：批次合并 -------------------------------------------------------


def test_two_orders_ready_together_at_the_same_restaurant_share_one_courier():
    clock, advance = make_clock()
    service, pool = build(clock)
    add_restaurant(service)
    first = service.accept(place(service, customer="u1", drop=(0.0, 2.0)).id)
    second = service.accept(place(service, customer="u2", drop=(0.0, 2.4)).id)
    advance(timedelta(minutes=15))
    batches = service.dispatch_due()
    assert len(batches) == 1
    assert batches[0].order_ids == (first.id, second.id)
    assert batches[0].order_ids[0] == first.id, "锚单必须排在最前，它要先被送到"
    assert pool.idle_count == 0


def test_a_batch_is_refused_when_it_would_delay_the_first_order_too_much():
    """唯一的批次规则：拼进来给**第一单**增加的送达时延不超过上限。"""
    clock, advance = make_clock()
    service, _ = build(clock, max_added_delay=5)
    add_restaurant(service)
    first = service.accept(place(service, customer="u1").id)
    advance(timedelta(minutes=10))
    second = service.accept(place(service, customer="u2").id)    # 晚十分钟出餐
    advance(timedelta(minutes=5))
    batches = service.dispatch_due()
    assert len(batches) == 1
    assert batches[0].order_ids == (first.id,)
    assert second.batch_id is None


def test_a_batch_is_refused_when_the_second_restaurant_is_too_far():
    """同一条不等式也管住了"两家店要近"：绕路的时间直接进了公式。"""
    clock, advance = make_clock()
    service, _ = build(clock, max_added_delay=5)
    add_restaurant(service, "R1", at=(0.0, 0.0))
    add_restaurant(service, "R2", at=(6.0, 0.0))
    first = service.accept(place(service, customer="u1", restaurant_id="R1").id)
    second = service.accept(place(service, customer="u2", restaurant_id="R2",
                                  drop=(6.0, 2.0)).id)
    advance(timedelta(minutes=15))
    batches = service.dispatch_due()
    assert batches[0].order_ids == (first.id,)
    assert second.batch_id is None


def test_a_batch_never_exceeds_the_configured_size():
    clock, advance = make_clock()
    service, _ = build(clock, max_batch=2)
    add_restaurant(service)
    for customer in ("u1", "u2", "u3"):
        service.accept(place(service, customer=customer).id)
    advance(timedelta(minutes=15))
    batches = service.dispatch_due()
    assert len(batches) == 1 and len(batches[0].order_ids) == 2


def test_the_courier_is_freed_only_after_the_last_order_of_the_batch_is_delivered():
    clock, advance = make_clock()
    service, pool = build(clock)
    add_restaurant(service)
    first = service.accept(place(service, customer="u1").id)
    second = service.accept(place(service, customer="u2").id)
    advance(timedelta(minutes=15))
    service.dispatch_due()
    for order in (first, second):
        service.mark_ready(order.id)
        service.pick_up(order.id)
    service.deliver(first.id)
    assert pool.idle_count == 0, "批次还没送完，骑手不能被再次派单"
    assert service.open_batch_count == 1
    service.deliver(second.id)
    assert pool.idle_count == 1
    assert service.open_batch_count == 0, "批次表必须会缩小"


def test_concurrent_dispatch_never_gives_one_courier_two_batches():
    """四个线程同时派单：每位骑手至多一个批次，每张订单至多进一个批次。"""
    clock, advance = make_clock()
    fleet = tuple((f"c{i}", 0.0, 0.0) for i in range(4))
    service, pool = build(clock, couriers=fleet, max_batch=3)
    add_restaurant(service)
    orders = [service.accept(place(service, customer=f"u{i}", drop=(0.0, 2.0 + i * 0.1)).id)
              for i in range(9)]
    advance(timedelta(minutes=15))

    barrier = threading.Barrier(4)
    seen: list[tuple] = []
    lock = threading.Lock()

    def dispatch() -> None:
        barrier.wait()
        result = service.dispatch_due()
        with lock:
            seen.extend(result)

    threads = [threading.Thread(target=dispatch) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    couriers = [b.courier_id for b in seen]
    assigned = [order_id for b in seen for order_id in b.order_ids]
    assert len(couriers) == len(set(couriers)), "一位骑手不可能同时拿到两个批次"
    assert len(assigned) == len(set(assigned)), "一张订单不可能进两个批次"
    assert len(assigned) == 9 and {o.id for o in orders} == set(assigned)


# ---- 第 4 关：定时单与关店 ---------------------------------------------------


def test_a_scheduled_order_is_invisible_to_the_restaurant_until_it_is_due():
    clock, advance = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    order = place(service, deliver_by=T0 + timedelta(hours=3))
    assert order.state is impl.OrderState.SCHEDULED
    with pytest.raises(impl.IllegalTransitionError):
        service.accept(order.id)
    assert service.release_scheduled() == ()
    advance(timedelta(hours=3))
    released = service.release_scheduled()
    assert [o.id for o in released] == [order.id]
    assert order.state is impl.OrderState.PLACED
    assert order.history[-1].by is impl.Actor.PLATFORM
    service.accept(order.id)
    assert order.ready_at == clock() + timedelta(minutes=17)


def test_closing_a_restaurant_rejects_pending_orders_but_not_accepted_ones():
    """关店不是撤单：餐厅接单那一刻就已经承诺了，菜也已经在做。"""
    clock, _ = make_clock()
    service, _ = build(clock)
    add_restaurant(service)
    accepted = service.accept(place(service, customer="u1").id)
    pending = place(service, customer="u2")
    scheduled = place(service, customer="u3", deliver_by=T0 + timedelta(hours=2))
    rejected = service.close_restaurant("R1")
    assert set(rejected) == {pending.id, scheduled.id}
    assert pending.state is impl.OrderState.REJECTED
    assert pending.history[-1].by is impl.Actor.PLATFORM
    assert accepted.state is impl.OrderState.ACCEPTED
    with pytest.raises(impl.RestaurantClosedError):
        place(service, customer="u4")
    service.mark_ready(accepted.id)
    assert accepted.state is impl.OrderState.READY


def test_the_menu_snapshot_handed_out_is_immutable():
    clock, _ = make_clock()
    service, _ = build(clock)
    restaurant = add_restaurant(service)
    items = restaurant.available_items()
    assert isinstance(items, tuple)
    with pytest.raises(AttributeError):
        items[0].price = 1
    assert place(service).subtotal == 3800 + 600
