"""股票交易系统的测试：分关覆盖账户校验、价格-时间优先撮合、生命周期与并发守恒。"""

from __future__ import annotations

import importlib
import os
import random
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 3, 2, 9, 30, tzinfo=UTC)


class FakeClock:
    """注入的时钟：测试里绝不 `sleep`，时间只在我们说它走的时候走。"""

    def __init__(self, now: datetime = START) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs: float) -> None:
        self.now = self.now + timedelta(**kwargs)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def broker(clock: FakeClock):
    b = impl.Brokerage(clock=clock, symbols=["BAC", "XOM"])
    b.open_account("alice", cash=10_000_00)
    b.open_account("bob", cash=10_000_00, positions={"BAC": 500})
    b.open_account("carol", cash=10_000_00, positions={"BAC": 500})
    return b


def buy(broker, who: str, quantity: int, price: int | None = None, symbol: str = "BAC"):
    if price is None:
        return broker.place_order(who, symbol, impl.Side.BUY, quantity, impl.OrderType.MARKET)
    return broker.place_order(who, symbol, impl.Side.BUY, quantity, limit_price=price)


def sell(broker, who: str, quantity: int, price: int | None = None, symbol: str = "BAC"):
    if price is None:
        return broker.place_order(who, symbol, impl.Side.SELL, quantity, impl.OrderType.MARKET)
    return broker.place_order(who, symbol, impl.Side.SELL, quantity, limit_price=price)


# --- 第 1 关：账户、校验、挂单 ------------------------------------------------


def test_a_limit_order_that_does_not_cross_rests_and_reserves(broker):
    order = buy(broker, "alice", 10, 100_00)
    assert order.status is impl.OrderStatus.NEW
    assert order.filled_quantity == 0
    assert broker.depth("BAC", impl.Side.BUY) == ((100_00, 10),)
    total, available = broker.cash("alice")
    assert total == 10_000_00
    assert available == 10_000_00 - 10 * 100_00


def test_a_buy_without_buying_power_is_rejected_and_left_on_the_record(broker):
    with pytest.raises(impl.InsufficientFundsError) as excinfo:
        buy(broker, "alice", 200, 100_00)
    rejected = excinfo.value.order
    assert rejected.status is impl.OrderStatus.REJECTED
    assert rejected.reserved == 0
    assert broker.cash("alice") == (10_000_00, 10_000_00)
    assert broker.depth("BAC", impl.Side.BUY) == ()


def test_selling_more_than_you_own_is_rejected_because_shorting_is_not_allowed(broker):
    with pytest.raises(impl.InsufficientSharesError) as excinfo:
        sell(broker, "bob", 501, 100_00)
    assert excinfo.value.order.status is impl.OrderStatus.REJECTED
    assert broker.position("bob", "BAC") == (500, 500)


def test_the_same_cash_cannot_back_two_orders(broker):
    buy(broker, "alice", 90, 100_00)
    with pytest.raises(impl.InsufficientFundsError):
        buy(broker, "alice", 20, 100_00)
    assert broker.cash("alice")[1] == 10_000_00 - 90 * 100_00


@pytest.mark.parametrize(
    "kwargs",
    [
        {"quantity": 0, "limit_price": 100_00},
        {"quantity": -5, "limit_price": 100_00},
        {"quantity": 5, "limit_price": None},
        {"quantity": 5, "limit_price": 0},
    ],
)
def test_malformed_orders_are_refused_before_anything_is_reserved(broker, kwargs):
    with pytest.raises(impl.InvalidOrderError):
        broker.place_order("alice", "BAC", impl.Side.BUY, **kwargs)
    assert broker.cash("alice") == (10_000_00, 10_000_00)


def test_a_market_order_must_not_carry_a_price_and_the_venue_must_list_the_symbol(broker):
    with pytest.raises(impl.InvalidOrderError):
        broker.place_order("alice", "BAC", impl.Side.BUY, 5, impl.OrderType.MARKET, 100_00)
    with pytest.raises(impl.UnknownSymbolError):
        buy(broker, "alice", 5, 100_00, symbol="TSLA")
    with pytest.raises(impl.UnknownAccountError):
        buy(broker, "nobody", 5, 100_00)


# --- 第 2 关：价格-时间优先、部分成交、成交价 --------------------------------


def test_time_priority_fills_the_older_order_first_at_the_same_price(broker):
    first = sell(broker, "bob", 10, 100_00)
    second = sell(broker, "carol", 10, 100_00)
    buy(broker, "alice", 10, 100_00)
    assert first.status is impl.OrderStatus.FILLED
    assert second.status is impl.OrderStatus.NEW
    assert broker.depth("BAC", impl.Side.SELL) == ((100_00, 10),)


def test_price_priority_beats_time_priority(broker):
    expensive = sell(broker, "bob", 10, 101_00)
    cheap = sell(broker, "carol", 10, 100_00)
    buy(broker, "alice", 10, 101_00)
    assert cheap.status is impl.OrderStatus.FILLED
    assert expensive.status is impl.OrderStatus.NEW


def test_the_trade_prints_at_the_resting_price_and_refunds_the_difference(broker):
    sell(broker, "bob", 10, 97_00)
    taker = buy(broker, "alice", 10, 100_00)
    (fill,) = broker.fills("BAC")
    assert (fill.price, fill.quantity) == (97_00, 10)
    assert fill.taker_order_id == taker.id
    assert broker.cash("alice") == (10_000_00 - 10 * 97_00,) * 2
    assert taker.reserved == 0


def test_a_big_order_partially_fills_and_the_remainder_rests(broker):
    sell(broker, "bob", 4, 100_00)
    taker = buy(broker, "alice", 10, 100_00)
    assert taker.status is impl.OrderStatus.PARTIALLY_FILLED
    assert taker.filled_quantity == 4
    assert broker.depth("BAC", impl.Side.BUY) == ((100_00, 6),)
    assert taker.reserved == 6 * 100_00


def test_a_market_buy_walks_several_price_levels(broker):
    sell(broker, "bob", 5, 100_00)
    sell(broker, "carol", 5, 101_00)
    taker = buy(broker, "alice", 8)
    assert taker.status is impl.OrderStatus.FILLED
    assert [(f.price, f.quantity) for f in broker.fills("BAC")] == [(100_00, 5), (101_00, 3)]
    assert broker.cash("alice")[0] == 10_000_00 - 5 * 100_00 - 3 * 101_00
    assert taker.reserved == 0


def test_a_market_order_never_rests_and_dies_when_liquidity_runs_out(broker):
    sell(broker, "bob", 3, 100_00)
    taker = buy(broker, "alice", 10)
    assert taker.status is impl.OrderStatus.CANCELLED
    assert taker.filled_quantity == 3
    assert taker.reserved == 0
    assert broker.depth("BAC", impl.Side.BUY) == ()
    assert broker.cash("alice")[1] == 10_000_00 - 3 * 100_00


def test_a_market_order_against_an_empty_book_is_cancelled_not_rejected(broker):
    taker = buy(broker, "alice", 10)
    assert taker.status is impl.OrderStatus.CANCELLED
    assert taker.filled_quantity == 0
    assert broker.cash("alice") == (10_000_00, 10_000_00)


def test_the_same_sequence_of_orders_produces_the_same_trades(clock):
    def run() -> list[tuple[int, int, str, str]]:
        b = impl.Brokerage(clock=clock, symbols=["BAC"])
        b.open_account("alice", cash=100_000_00)
        b.open_account("bob", cash=100_000_00, positions={"BAC": 1000})
        b.open_account("carol", cash=100_000_00, positions={"BAC": 1000})
        sell(b, "bob", 100, 240_12)
        sell(b, "bob", 90, 237_45)
        buy(b, "alice", 110, 238_10)
        buy(b, "carol", 10, 237_80)
        buy(b, "carol", 40, 237_80)
        sell(b, "bob", 50, 236_00)
        return [(f.price, f.quantity, f.buy_order_id, f.sell_order_id) for f in b.fills("BAC")]

    first = run()
    assert first == run()
    assert first[0][:2] == (237_45, 90)
    assert [(price, quantity) for price, quantity, _, _ in first[1:]] == [
        (238_10, 20), (237_80, 10), (237_80, 20)]


# --- 第 3 关：生命周期、撤单与成交的竞争、结算守恒 ---------------------------


def test_cancelling_a_resting_order_releases_its_reservation_and_shrinks_the_book(broker):
    order = buy(broker, "alice", 10, 100_00)
    assert broker.depth("BAC", impl.Side.BUY) == ((100_00, 10),)
    cancelled = broker.cancel_order(order.id)
    assert cancelled.status is impl.OrderStatus.CANCELLED
    assert cancelled.reserved == 0
    assert broker.depth("BAC", impl.Side.BUY) == ()
    assert broker.top_of_book("BAC").bid is None
    assert broker.cash("alice") == (10_000_00, 10_000_00)


def test_cancelling_a_half_filled_order_keeps_what_was_filled(broker):
    sell(broker, "bob", 4, 100_00)
    taker = buy(broker, "alice", 10, 100_00)
    broker.cancel_order(taker.id)
    assert taker.status is impl.OrderStatus.CANCELLED
    assert taker.filled_quantity == 4
    assert taker.reserved == 0
    assert broker.position("alice", "BAC") == (4, 4)
    assert broker.cash("alice") == (10_000_00 - 4 * 100_00,) * 2


def test_cancelling_an_already_filled_order_loses_the_race(broker):
    sell(broker, "bob", 10, 100_00)
    taker = buy(broker, "alice", 10, 100_00)
    assert taker.status is impl.OrderStatus.FILLED
    with pytest.raises(impl.OrderNotCancellableError):
        broker.cancel_order(taker.id)
    with pytest.raises(impl.OrderNotFoundError):
        broker.cancel_order("no-such-order")


def test_a_fill_moves_money_and_shares_without_creating_either(broker):
    cash_before, shares_before = broker.total_cash(), broker.total_shares("BAC")
    sell(broker, "bob", 10, 100_00)
    buy(broker, "alice", 10, 100_00)
    assert broker.total_cash() == cash_before
    assert broker.total_shares("BAC") == shares_before
    assert broker.cash("bob")[0] == 10_000_00 + 10 * 100_00
    assert broker.position("alice", "BAC") == (10, 10)
    assert broker.position("bob", "BAC") == (490, 490)


@pytest.mark.parametrize("seed", range(12))
def test_a_random_session_never_creates_or_destroys_money_or_shares(seed):
    rng = random.Random(seed)
    clock = FakeClock()
    b = impl.Brokerage(clock=clock, symbols=["BAC"])
    traders = ["t0", "t1", "t2", "t3"]
    for who in traders:
        b.open_account(who, cash=50_000_00, positions={"BAC": 100})
    cash_before, shares_before = b.total_cash(), b.total_shares("BAC")
    placed: list = []
    for _ in range(300):
        who = rng.choice(traders)
        side = rng.choice([impl.Side.BUY, impl.Side.SELL])
        quantity = rng.randint(1, 20)
        try:
            if rng.random() < 0.25:
                order = b.place_order(who, "BAC", side, quantity, impl.OrderType.MARKET)
            else:
                order = b.place_order(who, "BAC", side, quantity,
                                      limit_price=rng.randrange(95_00, 105_00, 25))
            placed.append(order)
        except impl.TradingError:
            pass
        if placed and rng.random() < 0.3:
            victim = rng.choice(placed)
            try:
                b.cancel_order(victim.id)
            except impl.TradingError:
                pass
        clock.advance(seconds=1)
        # 每一步之后都必须守恒，而不是只在最后守恒。
        assert b.total_cash() == cash_before
        assert b.total_shares("BAC") == shares_before
        for trader in traders:
            total, available = b.cash(trader)
            held, free = b.position(trader, "BAC")
            assert 0 <= available <= total
            assert 0 <= free <= held
    # 终态订单不许还锁着任何额度；挂单锁着的量必须正好等于账户冻结的量。
    for order in placed:
        if not order.is_open:
            assert order.reserved == 0
    for trader in traders:
        open_buys = sum(o.reserved for o in placed
                        if o.account_id == trader and o.is_open and o.side is impl.Side.BUY)
        total, available = b.cash(trader)
        assert total - available == open_buys


def test_concurrent_buyers_cannot_take_more_shares_than_are_offered(broker):
    """20 个买家同时抢 100 股：成交总量必须恰好是 min(需求, 供给) = 100，一股不多不少。

    这个界是**推导**出来的，不是跑出来观察到的——卖方只挂了 100 股，每个买家最多买 10 股，
    需求 200 股，所以无论线程怎么交错，成交总量都只能是 100。
    """
    supply, per_buyer, buyers = 100, 10, 20
    seller_before = broker.position("bob", "BAC")[0]
    sell(broker, "bob", supply, 100_00)
    for n in range(buyers):
        broker.open_account(f"b{n}", cash=per_buyer * 100_00)
    orders: list = []
    barrier = threading.Barrier(buyers)
    lock = threading.Lock()

    def trade(n: int) -> None:
        barrier.wait()
        order = buy(broker, f"b{n}", per_buyer, 100_00)
        with lock:
            orders.append(order)

    threads = [threading.Thread(target=trade, args=(n,)) for n in range(buyers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(orders) == buyers
    assert sum(o.filled_quantity for o in orders) == min(buyers * per_buyer, supply)
    assert all(o.filled_quantity in (0, per_buyer) for o in orders)
    assert broker.position("bob", "BAC")[0] == seller_before - supply
    assert broker.depth("BAC", impl.Side.SELL) == ()
    assert sum(f.quantity for f in broker.fills("BAC")) == supply


# --- 第 4 关：行情推送与索引清理 ---------------------------------------------


def test_the_top_of_book_feed_carries_the_state_subscribers_need(broker):
    seen: list = []
    unsubscribe = broker.subscribe(seen.append)
    assert broker.subscriber_count == 1
    buy(broker, "alice", 10, 99_00)
    sell(broker, "bob", 5, 101_00)
    last = seen[-1]
    assert (last.symbol, last.bid, last.bid_quantity) == ("BAC", 99_00, 10)
    assert (last.ask, last.ask_quantity, last.last_price) == (101_00, 5, None)
    sell(broker, "carol", 4, 99_00)
    assert seen[-1].last_price == 99_00
    assert seen[-1].bid_quantity == 6
    unsubscribe()
    unsubscribe()
    assert broker.subscriber_count == 0
    count = len(seen)
    buy(broker, "alice", 1, 98_00)
    assert len(seen) == count


def test_the_order_index_shrinks_when_finished_orders_are_purged(broker, clock):
    resting = buy(broker, "alice", 5, 90_00)
    sell(broker, "bob", 5, 100_00)
    buy(broker, "carol", 5, 100_00)
    assert broker.order_count == 3
    clock.advance(days=1)
    assert broker.purge_terminal_orders_before(clock.now) == 2
    assert broker.order_count == 1
    assert broker.order(resting.id).id == resting.id
    assert len(broker.fills("BAC")) == 1
