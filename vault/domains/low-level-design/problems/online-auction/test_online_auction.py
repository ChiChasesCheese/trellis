"""在线拍卖的测试：分关覆盖出价校验、代理出价、反狙击与"恰好结算一次"。"""

from __future__ import annotations

import importlib
import itertools
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 6, 1, 20, 0, tzinfo=UTC)


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
def house(clock: FakeClock):
    return impl.AuctionHouse(clock=clock)


def make(house, clock: FakeClock, **options):
    options.setdefault("increment", 1_00)
    return house.create("A1", seller_id="seller", item="Leica M6", starting_price=100_00,
                        ends_at=clock.now + timedelta(minutes=10), **options)


# --- 第 1 关：拍卖、时间窗、出价校验 ------------------------------------------


def test_an_auction_that_has_not_opened_refuses_bids(house, clock):
    lot = house.create("A2", seller_id="seller", item="lens", starting_price=100_00,
                       ends_at=clock.now + timedelta(hours=2),
                       starts_at=clock.now + timedelta(hours=1))
    assert lot.status is impl.AuctionStatus.SCHEDULED
    with pytest.raises(impl.AuctionNotStartedError):
        lot.place_bid("alice", 200_00)
    clock.advance(hours=1)
    assert lot.status is impl.AuctionStatus.ACTIVE
    lot.place_bid("alice", 200_00)
    assert lot.leader == "alice"


def test_the_first_bid_must_reach_the_starting_price_and_sets_it(house, clock):
    lot = make(house, clock)
    assert lot.minimum_bid() == 100_00
    with pytest.raises(impl.BidTooLowError):
        lot.place_bid("alice", 99_99)
    lot.place_bid("alice", 150_00)
    assert lot.price == 100_00
    assert lot.minimum_bid() == 101_00
    assert lot.bid_count == 1


def test_a_seller_may_not_bid_on_their_own_item(house, clock):
    lot = make(house, clock)
    with pytest.raises(impl.SellerCannotBidError):
        lot.place_bid("seller", 500_00)
    assert lot.bid_count == 0


@pytest.mark.parametrize("bad", [
    {"starting_price": 0},
    {"increment": 0},
    {"reserve_price": -1},
])
def test_an_auction_with_impossible_parameters_is_refused(house, clock, bad):
    kwargs = {"starting_price": 100_00, "increment": 1_00, "reserve_price": 0, **bad}
    with pytest.raises(impl.InvalidAuctionError):
        house.create("bad", seller_id="s", item="x", ends_at=clock.now + timedelta(minutes=5),
                     **kwargs)
    with pytest.raises(impl.InvalidAuctionError):
        house.create("bad2", seller_id="s", item="x", starting_price=100_00,
                     ends_at=clock.now - timedelta(minutes=5))
    with pytest.raises(impl.AuctionNotFoundError):
        house.auction("bad")


# --- 第 2 关：代理出价 --------------------------------------------------------


def test_a_losing_proxy_bid_pushes_the_leader_up_by_one_increment(house, clock):
    lot = make(house, clock)
    lot.place_bid("alice", 150_00)
    lot.place_bid("bob", 120_00)
    assert lot.leader == "alice"
    assert lot.price == 121_00
    lot.place_bid("carol", 200_00)
    assert (lot.leader, lot.price) == ("carol", 151_00)


def test_a_challenger_who_cannot_beat_the_maximum_never_leads_even_for_an_instant(house, clock):
    lot = make(house, clock)
    seen: list = []
    lot.watch(seen.append)
    lot.place_bid("alice", 150_00)
    lot.place_bid("bob", 149_00)
    assert all(e.leader_id in (None, "alice") for e in seen)
    assert seen[-1].outbid_id == "bob"
    assert lot.leader == "alice"


def test_a_tie_goes_to_the_earlier_maximum(house, clock):
    lot = make(house, clock)
    lot.place_bid("alice", 200_00)
    lot.place_bid("bob", 200_00)
    assert lot.leader == "alice"
    assert lot.price == 200_00
    with pytest.raises(impl.BidTooLowError):
        lot.place_bid("carol", 200_00)


def test_raising_your_own_maximum_does_not_bid_against_yourself(house, clock):
    lot = make(house, clock)
    lot.place_bid("alice", 150_00)
    lot.place_bid("bob", 120_00)
    price_before = lot.price
    lot.place_bid("alice", 400_00)
    assert lot.price == price_before
    assert lot.leader == "alice"
    with pytest.raises(impl.BidTooLowError):
        lot.place_bid("alice", 399_00)


def test_the_price_never_falls_when_a_small_bid_arrives_late(house, clock):
    lot = make(house, clock)
    lot.place_bid("alice", 500_00)
    lot.place_bid("bob", 300_00)
    assert lot.price == 301_00
    lot.place_bid("carol", 302_00)
    assert lot.price == 303_00
    with pytest.raises(impl.BidTooLowError):
        lot.place_bid("dave", 150_00)
    assert lot.price == 303_00


@pytest.mark.parametrize("order", list(itertools.permutations([1000_00, 1500_00, 2000_00, 2500_00])))
def test_the_outcome_does_not_depend_on_the_order_the_maxima_arrive(house, clock, order):
    """四个上限彼此相距 500 元、加价档只有 1 元，所以结果可以**推导**出来而不是跑出来看到：

    领先者永远是上限最高的那位（更高的上限一定顶得动在位者，更低的永远顶不动），
    最终价永远是 `min(最高上限, 次高上限 + 一档)` —— 因为价格只涨不跌，而能把价格抬到
    这个数的只有次高的那次出价。上限间距远大于两个加价档，保证这两位的出价都不会被
    "低于最低出价"挡掉。
    """
    lot = house.create("P", seller_id="seller", item="x", starting_price=500_00,
                       ends_at=clock.now + timedelta(minutes=10), increment=1_00)
    for n, maximum in enumerate(order):
        try:
            lot.place_bid(f"bidder{maximum}", maximum)
        except impl.BidTooLowError:
            pass
    assert lot.leader == "bidder250000"
    assert lot.price == min(2500_00, 2000_00 + 1_00)


def test_a_reserve_price_lifts_the_price_and_decides_whether_it_sells(house, clock):
    lot = make(house, clock, reserve_price=500_00)
    lot.place_bid("alice", 300_00)
    assert lot.price == 100_00
    clock.advance(minutes=11)
    assert lot.status is impl.AuctionStatus.UNSOLD
    assert lot.winner() is None

    clock.now = START
    other = house.create("A3", seller_id="seller", item="lens", starting_price=100_00,
                         ends_at=clock.now + timedelta(minutes=10), increment=1_00,
                         reserve_price=500_00)
    other.place_bid("alice", 300_00)
    other.place_bid("bob", 600_00)
    assert other.price == 500_00
    clock.advance(minutes=11)
    assert other.winner() == ("bob", 500_00)


# --- 第 3 关：反狙击、恰好结算一次、并发 --------------------------------------


def test_a_bid_in_the_last_seconds_pushes_the_deadline_back(house, clock):
    lot = make(house, clock, soft_close=timedelta(seconds=30), max_extensions=2)
    lot.place_bid("alice", 150_00)
    assert lot.extension_count == 0
    clock.advance(minutes=9, seconds=45)
    lot.place_bid("bob", 200_00)
    assert lot.extension_count == 1
    assert lot.standing().ends_at == clock.now + timedelta(seconds=30)
    lot.place_bid("carol", 300_00)
    lot.place_bid("dave", 400_00)
    assert lot.extension_count == 2
    assert lot.status is impl.AuctionStatus.ACTIVE
    clock.advance(seconds=31)
    assert lot.status is impl.AuctionStatus.SOLD


def test_the_deadline_settles_itself_even_though_nobody_ran_a_timer(house, clock):
    lot = make(house, clock)
    lot.place_bid("alice", 150_00)
    clock.advance(minutes=11)
    assert lot.status is impl.AuctionStatus.SOLD
    assert lot.winner() == ("alice", 100_00)
    with pytest.raises(impl.AuctionClosedError):
        lot.place_bid("bob", 900_00)


def test_closing_happens_exactly_once_however_many_threads_race_for_it(house, clock):
    lot = make(house, clock)
    closed: list = []
    lot.watch(lambda event: closed.append(event) if event.kind is impl.EventKind.CLOSED else None)
    lot.place_bid("alice", 150_00)
    clock.advance(minutes=11)

    racers, results, lock = 16, [], threading.Lock()
    barrier = threading.Barrier(racers)

    def race() -> None:
        barrier.wait()
        won = lot.close_if_due()
        with lock:
            results.append(won)

    threads = [threading.Thread(target=race) for _ in range(racers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(results) == 1
    assert len(closed) == 1
    assert lot.watcher_count == 0


def test_concurrent_bidders_reach_the_derived_leader_and_price(house, clock):
    """八位出价者同时出价，上限彼此相距 500 元。无论线程怎么交错，领先者必是上限最高的
    那位、成交价必是 `min(最高上限, 次高上限 + 一档)` —— 这两个数是从规则推导出来的。
    """
    maxima = [1000_00 + n * 500_00 for n in range(8)]
    lot = house.create("C", seller_id="seller", item="x", starting_price=500_00,
                       ends_at=clock.now + timedelta(minutes=10), increment=1_00)
    barrier = threading.Barrier(len(maxima))

    def bid(maximum: int) -> None:
        barrier.wait()
        try:
            lot.place_bid(f"bidder{maximum}", maximum)
        except impl.BidTooLowError:
            pass

    threads = [threading.Thread(target=bid, args=(m,)) for m in maxima]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    top, second = maxima[-1], maxima[-2]
    assert lot.leader == f"bidder{top}"
    assert lot.price == min(top, second + 1_00)
    assert lot.price <= top
    assert len(lot.bids()) == lot.bid_count


def test_watchers_can_leave_and_are_dropped_when_the_auction_ends(house, clock):
    lot = make(house, clock)
    first, second = [], []
    unwatch = lot.watch(first.append)
    lot.watch(second.append)
    assert lot.watcher_count == 2
    lot.place_bid("alice", 150_00)
    assert len(first) == len(second) >= 1
    unwatch()
    unwatch()
    assert lot.watcher_count == 1
    seen = len(first)
    lot.place_bid("bob", 200_00)
    assert len(first) == seen
    clock.advance(minutes=11)
    assert lot.status is impl.AuctionStatus.SOLD
    assert lot.watcher_count == 0


def test_the_catalogue_shrinks_when_finished_auctions_are_purged(house, clock):
    lot = make(house, clock)
    house.create("A9", seller_id="seller", item="tripod", starting_price=10_00,
                 ends_at=clock.now + timedelta(days=3))
    lot.place_bid("alice", 150_00)
    assert house.auction_count == 2
    clock.advance(minutes=11)
    assert house.close_due() == ("A1",)
    assert house.close_due() == ()
    assert len(house.live_auctions()) == 1
    clock.advance(days=1)
    assert house.purge_closed_before(clock.now) == 1
    assert house.auction_count == 1
    with pytest.raises(impl.AuctionNotFoundError):
        house.auction("A1")


# --- 第 4 关：一口价 ----------------------------------------------------------


def test_buy_it_now_ends_the_auction_immediately(house, clock):
    lot = make(house, clock, buy_now_price=300_00)
    lot.place_bid("alice", 150_00)
    standing = lot.buy_now("bob")
    assert standing.status is impl.AuctionStatus.SOLD
    assert lot.winner() == ("bob", 300_00)
    assert standing.ends_at == clock.now
    with pytest.raises(impl.AuctionClosedError):
        lot.place_bid("carol", 900_00)
    with pytest.raises(impl.AuctionClosedError):
        lot.buy_now("dave")


def test_buy_it_now_disappears_once_the_bidding_catches_up_with_it(house, clock):
    lot = make(house, clock, buy_now_price=300_00)
    lot.place_bid("alice", 350_00)
    lot.place_bid("bob", 340_00)
    assert lot.price >= 300_00
    with pytest.raises(impl.BuyNowUnavailableError):
        lot.buy_now("carol")
    plain = house.create("A8", seller_id="seller", item="strap", starting_price=10_00,
                         ends_at=clock.now + timedelta(minutes=10))
    with pytest.raises(impl.BuyNowUnavailableError):
        plain.buy_now("carol")


def test_the_whole_flow_runs_end_to_end():
    """不借助 fixture 的完整走一遍：出价 → 代理压价 → 反狙击延时 → 到点成交 → 关注者清空。"""
    clock = FakeClock()
    house = impl.AuctionHouse(clock=clock)
    lot = house.create("E1", seller_id="seller", item="camera", starting_price=100_00,
                       ends_at=clock.now + timedelta(minutes=10), increment=1_00,
                       soft_close=timedelta(seconds=30))
    seen: list = []
    lot.watch(seen.append)
    lot.place_bid("alice", 150_00)
    lot.place_bid("bob", 120_00)
    assert (lot.price, lot.leader) == (121_00, "alice")
    clock.advance(minutes=9, seconds=50)
    lot.place_bid("carol", 500_00)
    assert lot.extension_count == 1
    clock.advance(minutes=1)
    assert house.close_due() == ("E1",)
    assert lot.winner() == ("carol", 151_00)
    assert seen[-1].kind is impl.EventKind.CLOSED
    assert lot.watcher_count == 0
