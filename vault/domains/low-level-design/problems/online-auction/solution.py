"""在线拍卖（Online Auction）——代理出价、反狙击延时与"恰好结算一次"的参考实现。

五行设计：出价者交给系统的是一个**上限**（maximum），不是一个价格——系统替他出"刚好压过对手
所需的最小金额"，于是当前价由 `min(最高上限, 次高上限 + 一档)` 决定，金额一律整数分；并列时
**先到的上限赢**，而且当前价永不回落，这两条让结果与到达顺序无关。时间只从注入的时钟来，
状态推进是**惰性**的：任何一次读写都先 `_tick` 一下，结束由锁内的一次状态翻转裁定，所以"恰好
一次"不依赖任何定时器。最后几秒落下的出价把结束时间推后（反狙击），推后次数有上限。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径。


class AuctionError(Exception):
    """本设计里所有失败路径的公共基类。"""

class AuctionNotFoundError(AuctionError):
    """这场拍卖不存在（或已经被 `purge_closed_before` 清掉）。"""

class InvalidAuctionError(AuctionError):
    """拍卖本身的参数就不合法：结束早于开始、价格非正、加价档非正。"""

class AuctionNotStartedError(AuctionError):
    """还没到开拍时间。"""

class AuctionClosedError(AuctionError):
    """拍卖已经结束，不再接受任何出价。"""

class BidTooLowError(AuctionError):
    """出价上限没有达到当前所需的最低出价（或者没有超过自己已有的上限）。"""

class SellerCannotBidError(AuctionError):
    """卖家不能给自己的拍品出价——这是托价（shill bidding）。"""

class BuyNowUnavailableError(AuctionError):
    """这场拍卖没有一口价，或者当前价已经追上一口价，一口价随之失效。"""


class AuctionStatus(Enum):
    """拍卖的四个状态。两个终态：成交与流拍。

    流拍有两种原因——没人出价，或者最终价没到底价（reserve）——但对系统行为而言它们完全
    一样（没有赢家、不收款），所以**不给它们两个状态**，原因由"有没有领先者"自己说明。
    """

    SCHEDULED = "scheduled"
    ACTIVE = "active"
    SOLD = "sold"
    UNSOLD = "unsold"

    @property
    def is_closed(self) -> bool:
        """终态不再变化。"""
        return self in (AuctionStatus.SOLD, AuctionStatus.UNSOLD)


class EventKind(Enum):
    """关注者会收到的四类事件。"""

    OPENED = "opened"
    BID = "bid"
    EXTENDED = "extended"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class Bid:
    """一次出价。`maximum` 是出价者愿意付的**上限**，不是他当前要付的价。

    上限是私密的：它进入事件与快照的从来只有"当前价"和"谁领先"。把上限广播出去，
    代理出价就失去全部意义——别人只要出到你的上限加一档就能精准地把你顶掉。
    """

    id: str
    auction_id: str
    bidder_id: str
    maximum: int
    at: datetime


@dataclass(frozen=True, slots=True)
class Standing:
    """拍卖的对外快照：任何时候问"现在什么情况"，拿到的都是这个不可变对象。"""

    auction_id: str
    status: AuctionStatus
    price: int
    leader_id: str | None
    ends_at: datetime
    bid_count: int


@dataclass(frozen=True, slots=True)
class AuctionEvent:
    """推给关注者的事件：**自带发生了什么**（现价、谁领先、谁被顶掉、结束时间、状态），
    订阅者读事件就够，不必回头去问 `Auction` 要数据——那等于绕过它的锁读一份正在变的状态。
    """

    kind: EventKind
    auction_id: str
    status: AuctionStatus
    price: int
    leader_id: str | None
    ends_at: datetime
    at: datetime
    outbid_id: str | None = None


Clock = Callable[[], datetime]
Watcher = Callable[[AuctionEvent], None]


class Auction:
    """一场拍卖：一个卖家、一件拍品、一个底价、一段时间，和一台代理出价机。

    不变量：当前价**只涨不跌**；领先者恒有一个 ≥ 当前价的上限；状态只沿
    SCHEDULED → ACTIVE → SOLD/UNSOLD 单向推进，而且从 ACTIVE 翻出去这件事
    **全局只会发生一次**——它在锁内完成，谁翻的谁负责发"已结束"事件。

    锁的粒度是**一场拍卖一把**：两场拍卖之间没有任何共享状态（不像撮合要跨账户搬钱），
    所以全局一把锁只会让热门拍品拖死所有冷门拍品。
    """

    def __init__(self, auction_id: str, seller_id: str, item: str, starting_price: int,
                 ends_at: datetime, clock: Clock, *, reserve_price: int = 0,
                 starts_at: datetime | None = None, increment: int = 100,
                 soft_close: timedelta = timedelta(seconds=30), max_extensions: int = 10,
                 buy_now_price: int | None = None) -> None:
        self.id = auction_id
        self.seller_id = seller_id
        self.item = item
        self.starting_price = starting_price
        self.reserve_price = reserve_price
        self.increment = increment
        self.soft_close = soft_close
        self.max_extensions = max_extensions
        self.buy_now_price = buy_now_price
        self.starts_at = starts_at if starts_at is not None else clock()
        if ends_at <= self.starts_at:
            raise InvalidAuctionError("an auction must end after it starts")
        if starting_price <= 0 or increment <= 0 or reserve_price < 0:
            raise InvalidAuctionError("prices and the increment must be positive")
        self._clock = clock
        self._ends_at = ends_at
        self._status = AuctionStatus.SCHEDULED
        self._price = starting_price
        self._leader: str | None = None
        self._leader_max = 0
        self._extensions = 0
        self._bids: list[Bid] = []
        self._watchers: list[Watcher] = []
        self._lock = threading.Lock()
        self._ids = (f"{auction_id}-B{n}" for n in itertools.count(1))

    # ---- 读：一律先推进时间，再给不可变快照 ------------------------------

    def standing(self) -> Standing:
        """当前状况的快照。读之前先推进一次时间，所以"过了点还显示进行中"不可能发生。"""
        events: list[AuctionEvent] = []
        with self._lock:
            events += self._tick(self._clock())
            snapshot = Standing(auction_id=self.id, status=self._status, price=self._price,
                                leader_id=self._leader, ends_at=self._ends_at,
                                bid_count=len(self._bids))
        self._notify(events)
        return snapshot

    @property
    def status(self) -> AuctionStatus:
        """当前状态。"""
        return self.standing().status

    @property
    def price(self) -> int:
        """当前价（分）：领先者此刻若成交要付的金额。"""
        return self.standing().price

    @property
    def leader(self) -> str | None:
        """当前领先者。"""
        return self.standing().leader_id

    @property
    def bid_count(self) -> int:
        """收到过多少次有效出价。"""
        with self._lock:
            return len(self._bids)

    @property
    def watcher_count(self) -> int:
        """还有多少关注者——结束之后必须归零。"""
        with self._lock:
            return len(self._watchers)

    @property
    def extension_count(self) -> int:
        """被反狙击规则延长过几次。"""
        with self._lock:
            return self._extensions

    def bids(self) -> tuple[Bid, ...]:
        """出价历史的快照。内部那张表不外借。"""
        with self._lock:
            return tuple(self._bids)

    def minimum_bid(self) -> int:
        """下一位出价者至少要报的上限：首次出价是起拍价，之后是现价加一档。"""
        with self._lock:
            self._tick(self._clock())
            return self._minimum_locked()

    def winner(self) -> tuple[str, int] | None:
        """成交则返回 `(买家, 成交价)`；流拍返回 `None`。"""
        snapshot = self.standing()
        if snapshot.status is not AuctionStatus.SOLD or snapshot.leader_id is None:
            return None
        return snapshot.leader_id, snapshot.price

    # ---- 写：出价、一口价、关注、到点结束 --------------------------------

    def place_bid(self, bidder_id: str, maximum: int) -> Bid:
        """出一次代理价：交上限，系统替你出到刚好够用的那个数。"""
        now = self._clock()
        events: list[AuctionEvent] = []
        try:
            with self._lock:
                events += self._tick(now)
                bid = self._accept_locked(bidder_id, maximum, now, events)
        finally:
            self._notify(events)
        return bid

    def buy_now(self, buyer_id: str) -> Standing:
        """一口价：立刻按 `buy_now_price` 成交并结束拍卖。

        第 4 关的新需求，它**没有改动出价那段代码的任何一行**：只是把价与领先者直接写成
        一口价，再让状态走同一条结束路径。规则是"现价追上一口价，一口价就失效"——市场已经
        把它估到这个数以上，再给人捡便宜就不对了。
        """
        now = self._clock()
        events: list[AuctionEvent] = []
        try:
            with self._lock:
                events += self._tick(now)
                if self._status is AuctionStatus.SCHEDULED:
                    raise AuctionNotStartedError(f"auction {self.id} has not started")
                if self._status.is_closed:
                    raise AuctionClosedError(f"auction {self.id} is {self._status.value}")
                if buyer_id == self.seller_id:
                    raise SellerCannotBidError("the seller cannot buy their own item")
                if self.buy_now_price is None or self._price >= self.buy_now_price:
                    raise BuyNowUnavailableError(f"buy-it-now is gone on auction {self.id}")
                self._price, self._leader = self.buy_now_price, buyer_id
                self._leader_max = self.buy_now_price
                self._bids.append(Bid(id=next(self._ids), auction_id=self.id, bidder_id=buyer_id,
                                      maximum=self.buy_now_price, at=now))
                self._ends_at, self._status = now, AuctionStatus.SOLD
                events.append(self._event(EventKind.CLOSED, now))
                snapshot = Standing(self.id, self._status, self._price, self._leader,
                                    self._ends_at, len(self._bids))
        finally:
            self._notify(events)
        return snapshot

    def watch(self, watcher: Watcher) -> Callable[[], None]:
        """关注这场拍卖，返回一个取消关注的函数——退订的手段和订阅一起交出去，
        关注者表才会缩小；拍卖一结束，整张表当场清空，因为之后不会再有任何事件。
        """
        with self._lock:
            self._watchers.append(watcher)

        def unwatch() -> None:
            """取消关注；重复调用无害。"""
            with self._lock:
                if watcher in self._watchers:
                    self._watchers.remove(watcher)

        return unwatch

    def close_if_due(self) -> bool:
        """到点就结束，返回"这一次调用是不是正好把它结束掉的那一次"。

        扫描线程和任何一次读写都会走到同一段代码，而翻状态发生在锁内，所以无论多少个线程
        同时到达，**只有一个**会拿到 `True`，也只有它会发出"已结束"事件。
        """
        events: list[AuctionEvent] = []
        with self._lock:
            events += self._tick(self._clock())
        self._notify(events)
        return any(e.kind is EventKind.CLOSED for e in events)

    # ---- 内部：时间推进、代理出价、反狙击、事件 --------------------------

    def _tick(self, now: datetime) -> list[AuctionEvent]:
        """把状态推进到 `now` 应有的样子，返回这一步产生的事件。调用方须已持有锁。

        这是"恰好一次"的全部机密：结束不是被定时器触发的，而是被**第一个看它的人**
        触发的，而看的动作在锁里，所以翻转只能发生一次。
        """
        events: list[AuctionEvent] = []
        if self._status is AuctionStatus.SCHEDULED and now >= self.starts_at:
            self._status = AuctionStatus.ACTIVE
            events.append(self._event(EventKind.OPENED, now))
        if self._status is AuctionStatus.ACTIVE and now >= self._ends_at:
            sold = self._leader is not None and self._price >= self.reserve_price
            self._status = AuctionStatus.SOLD if sold else AuctionStatus.UNSOLD
            events.append(self._event(EventKind.CLOSED, now))
        return events

    def _minimum_locked(self) -> int:
        """当前所需的最低出价上限。调用方须已持有锁。"""
        return self.starting_price if self._leader is None else self._price + self.increment

    def _accept_locked(self, bidder_id: str, maximum: int, now: datetime,
                       events: list[AuctionEvent]) -> Bid:
        """校验并接受一次出价。调用方须已持有锁。"""
        if self._status is AuctionStatus.SCHEDULED:
            raise AuctionNotStartedError(f"auction {self.id} opens at {self.starts_at}")
        if self._status.is_closed:
            raise AuctionClosedError(f"auction {self.id} is {self._status.value}")
        if bidder_id == self.seller_id:
            raise SellerCannotBidError("the seller cannot bid on their own item")
        before = (self._price, self._leader)
        if bidder_id == self._leader:
            # 自己已经领先：只抬自己的上限，**价格一动不动**——没人会和自己竞价。
            if maximum <= self._leader_max:
                raise BidTooLowError(f"raise your own maximum above {self._leader_max}")
            self._leader_max = maximum
            outbid = None
        else:
            minimum = self._minimum_locked()
            if maximum < minimum:
                raise BidTooLowError(f"auction {self.id} needs at least {minimum}, got {maximum}")
            outbid = self._proxy_locked(bidder_id, maximum)
        bid = Bid(id=next(self._ids), auction_id=self.id, bidder_id=bidder_id,
                  maximum=maximum, at=now)
        self._bids.append(bid)
        if (self._price, self._leader) != before:
            events.append(self._event(EventKind.BID, now, outbid_id=outbid))
        self._extend_locked(now, events)
        return bid

    def _proxy_locked(self, bidder_id: str, maximum: int) -> str | None:
        """代理出价的核心三行：谁领先、价格涨到多少、谁被顶掉。调用方须已持有锁。

        规则：新上限**严格高于**在位者才换人，换人后的价格是"刚好压过在位者一档"与
        "自己的上限"之中的较小值；新上限没超过在位者，则在位者被顶到"挑战者上限加一档"
        与"自己上限"之中的较小值。并列（两人上限相同）走后一条，于是**先到的上限赢**。
        `max(...)` 那一层保证价格只涨不跌，这也是结果与到达顺序无关的前提。
        """
        if self._leader is None:
            self._leader, self._leader_max = bidder_id, maximum
            outbid = None
        elif maximum > self._leader_max:
            outbid = self._leader
            self._price = max(self._price, min(maximum, self._leader_max + self.increment))
            self._leader, self._leader_max = bidder_id, maximum
        else:
            outbid = bidder_id
            self._price = max(self._price, min(self._leader_max, maximum + self.increment))
        if self._leader_max >= self.reserve_price:
            # 领先者的上限已经够到底价：价格直接抬到底价，卖家反正会接受。
            self._price = max(self._price, self.reserve_price)
        return outbid

    def _extend_locked(self, now: datetime, events: list[AuctionEvent]) -> None:
        """反狙击（anti-sniping）：落在最后 `soft_close` 内的出价把结束时间推后。

        延长次数有上限，否则两个人可以把一场拍卖无限地拖下去——"能延长"必须配一个"延到头"。
        """
        if self._ends_at - now > self.soft_close or self._extensions >= self.max_extensions:
            return
        self._ends_at = now + self.soft_close
        self._extensions += 1
        events.append(self._event(EventKind.EXTENDED, now))

    def _event(self, kind: EventKind, at: datetime, outbid_id: str | None = None) -> AuctionEvent:
        """按当前状态造一个事件。调用方须已持有锁。"""
        return AuctionEvent(kind=kind, auction_id=self.id, status=self._status, price=self._price,
                            leader_id=self._leader, ends_at=self._ends_at, at=at,
                            outbid_id=outbid_id)

    def _notify(self, events: Sequence[AuctionEvent]) -> None:
        """在**锁外**把事件发给关注者：关注者是外部代码，握着拍卖的锁调它，
        一个慢关注者就能卡住这场拍卖的所有出价。
        """
        if not events:
            return
        with self._lock:
            watchers = tuple(self._watchers)
            if any(e.kind is EventKind.CLOSED for e in events):
                self._watchers.clear()
        for event in events:
            for watcher in watchers:
                watcher(event)


class AuctionHouse:
    """拍卖行：拍品目录、批量到点扫描、清理已结束的拍卖。

    它**不转发** `place_bid`——那样只会多一层什么也不做的壳。它的责任是目录本身：
    按 id 找到那场拍卖、把该结束的一批结束掉、把过期的从目录里摘掉。
    """

    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._auctions: dict[str, Auction] = {}
        self._lock = threading.Lock()

    def create(self, auction_id: str, seller_id: str, item: str, starting_price: int,
               ends_at: datetime, **options: object) -> Auction:
        """上架一场拍卖；`options` 直接透传给 `Auction`（底价、加价档、软关闭窗口、一口价）。"""
        auction = Auction(auction_id, seller_id, item, starting_price, ends_at,
                          self._clock, **options)  # type: ignore[arg-type]
        with self._lock:
            if auction_id in self._auctions:
                raise InvalidAuctionError(f"auction {auction_id!r} already exists")
            self._auctions[auction_id] = auction
        return auction

    def auction(self, auction_id: str) -> Auction:
        """按 id 取拍卖。"""
        with self._lock:
            auction = self._auctions.get(auction_id)
        if auction is None:
            raise AuctionNotFoundError(f"unknown auction {auction_id!r}")
        return auction

    @property
    def auction_count(self) -> int:
        """目录里还有多少场。"""
        with self._lock:
            return len(self._auctions)

    def live_auctions(self) -> tuple[Auction, ...]:
        """还没结束的拍卖的快照（读的过程中顺带推进每一场的时间）。"""
        with self._lock:
            auctions = tuple(self._auctions.values())
        return tuple(a for a in auctions if not a.status.is_closed)

    def close_due(self) -> tuple[str, ...]:
        """扫描一遍，把到点的拍卖结束掉，返回**这一次**真正被它结束掉的那些 id。

        先在自己的锁内拿一份目录快照，出锁后再去碰每一场各自的锁，不形成嵌套，也就没有
        锁顺序死锁。这个扫描只是让通知**及时**；正确性不靠它——没人扫描时，任何一次读写
        也会把状态推进到位。
        """
        with self._lock:
            auctions = tuple(self._auctions.values())
        return tuple(a.id for a in auctions if a.close_if_due())

    def purge_closed_before(self, cutoff: datetime) -> int:
        """把结束于 `cutoff` 之前的拍卖清出目录，返回清掉的场数。

        没有它，目录会随着上架量无限增长，而其中绝大多数早就尘埃落定。关注者表在结束那一刻
        已经清空，所以这些 `Auction` 对象真的能被回收。
        """
        with self._lock:
            auctions = tuple(self._auctions.items())
        gone = [aid for aid, a in auctions
                if (s := a.standing()).status.is_closed and s.ends_at < cutoff]
        with self._lock:
            for auction_id in gone:
                self._auctions.pop(auction_id, None)
        return len(gone)


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 6, 1, 20, 0, tzinfo=UTC)
    house = AuctionHouse(clock=lambda: now)
    lot = house.create("A1", seller_id="seller", item="Leica M6", starting_price=100_00,
                       ends_at=now + timedelta(minutes=10), reserve_price=90_00,
                       increment=1_00, soft_close=timedelta(seconds=30))
    lot.watch(lambda e: print(f"  [{e.kind.value}] price={e.price / 100:.2f} leader={e.leader_id}"))

    for bidder, maximum in [("alice", 150_00), ("bob", 120_00), ("carol", 200_00),
                            ("alice", 210_00), ("dave", 210_00)]:
        try:
            lot.place_bid(bidder, maximum)
            print(f"{bidder} max {maximum / 100:.2f} -> price {lot.price / 100:.2f}, "
                  f"leader {lot.leader}")
        except AuctionError as exc:
            print(f"{bidder} rejected: {exc}")

    now = now + timedelta(minutes=9, seconds=50)  # 进入软关闭窗口
    lot.place_bid("bob", 220_00)
    print(f"extended {lot.extension_count} time(s), now ends at {lot.standing().ends_at:%H:%M:%S}")
    now = now + timedelta(minutes=1)
    print("closed by this call:", house.close_due(), "winner:", lot.winner())
    print("watchers left:", lot.watcher_count, "purged:", house.purge_closed_before(now))
