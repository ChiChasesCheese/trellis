"""在线拍卖（Online Auction）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/online-auction -q
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class AuctionError(Exception):
    """本设计里所有失败路径的公共基类。"""


class AuctionNotFoundError(AuctionError):
    """这场拍卖不存在。"""


class InvalidAuctionError(AuctionError):
    """拍卖本身的参数就不合法。"""


class AuctionNotStartedError(AuctionError):
    """还没到开拍时间。"""


class AuctionClosedError(AuctionError):
    """拍卖已经结束，不再接受任何出价。"""


class BidTooLowError(AuctionError):
    """出价上限没有达到当前所需的最低出价（或者没有超过自己已有的上限）。"""


class SellerCannotBidError(AuctionError):
    """卖家不能给自己的拍品出价。"""


class BuyNowUnavailableError(AuctionError):
    """没有一口价，或者当前价已经追上一口价。"""


class AuctionStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    SOLD = "sold"
    UNSOLD = "unsold"

    @property
    def is_closed(self) -> bool:
        """终态不再变化。"""
        raise NotImplementedError


class EventKind(Enum):
    OPENED = "opened"
    BID = "bid"
    EXTENDED = "extended"
    CLOSED = "closed"


@dataclass(frozen=True, slots=True)
class Bid:
    """一次出价；`maximum` 是出价者愿意付的上限，不是他当前要付的价。"""

    id: str
    auction_id: str
    bidder_id: str
    maximum: int
    at: datetime


@dataclass(frozen=True, slots=True)
class Standing:
    """拍卖的对外快照。"""

    auction_id: str
    status: AuctionStatus
    price: int
    leader_id: str | None
    ends_at: datetime
    bid_count: int


@dataclass(frozen=True, slots=True)
class AuctionEvent:
    """推给关注者的事件，自带订阅者需要的全部内容。"""

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
    """一场拍卖：一个卖家、一件拍品、一个底价、一段时间，和一台代理出价机。"""

    def __init__(self, auction_id: str, seller_id: str, item: str, starting_price: int,
                 ends_at: datetime, clock: Clock, *, reserve_price: int = 0,
                 starts_at: datetime | None = None, increment: int = 100,
                 soft_close: timedelta = timedelta(seconds=30), max_extensions: int = 10,
                 buy_now_price: int | None = None) -> None:
        raise NotImplementedError

    def standing(self) -> Standing:
        """当前状况的快照；读之前先推进一次时间。"""
        raise NotImplementedError

    @property
    def status(self) -> AuctionStatus:
        """当前状态。"""
        raise NotImplementedError

    @property
    def price(self) -> int:
        """当前价（分）。"""
        raise NotImplementedError

    @property
    def leader(self) -> str | None:
        """当前领先者。"""
        raise NotImplementedError

    @property
    def bid_count(self) -> int:
        """收到过多少次有效出价。"""
        raise NotImplementedError

    @property
    def watcher_count(self) -> int:
        """还有多少关注者。"""
        raise NotImplementedError

    @property
    def extension_count(self) -> int:
        """被反狙击规则延长过几次。"""
        raise NotImplementedError

    def bids(self) -> tuple[Bid, ...]:
        """出价历史的快照。"""
        raise NotImplementedError

    def minimum_bid(self) -> int:
        """下一位出价者至少要报的上限。"""
        raise NotImplementedError

    def winner(self) -> tuple[str, int] | None:
        """成交则返回 `(买家, 成交价)`；流拍返回 `None`。"""
        raise NotImplementedError

    def place_bid(self, bidder_id: str, maximum: int) -> Bid:
        """出一次代理价：交上限，系统替你出到刚好够用的那个数。"""
        raise NotImplementedError

    def buy_now(self, buyer_id: str) -> Standing:
        """一口价：立刻按 `buy_now_price` 成交并结束拍卖。"""
        raise NotImplementedError

    def watch(self, watcher: Watcher) -> Callable[[], None]:
        """关注这场拍卖，返回一个取消关注的函数。"""
        raise NotImplementedError

    def close_if_due(self) -> bool:
        """到点就结束，返回这一次调用是不是正好把它结束掉的那一次。"""
        raise NotImplementedError


class AuctionHouse:
    """拍卖行：拍品目录、批量到点扫描、清理已结束的拍卖。"""

    def __init__(self, clock: Clock) -> None:
        raise NotImplementedError

    def create(self, auction_id: str, seller_id: str, item: str, starting_price: int,
               ends_at: datetime, **options: object) -> Auction:
        """上架一场拍卖；`options` 透传给 `Auction`。"""
        raise NotImplementedError

    def auction(self, auction_id: str) -> Auction:
        """按 id 取拍卖。"""
        raise NotImplementedError

    @property
    def auction_count(self) -> int:
        """目录里还有多少场。"""
        raise NotImplementedError

    def live_auctions(self) -> tuple[Auction, ...]:
        """还没结束的拍卖的快照。"""
        raise NotImplementedError

    def close_due(self) -> tuple[str, ...]:
        """扫描一遍，把到点的拍卖结束掉，返回这一次真正被它结束掉的那些 id。"""
        raise NotImplementedError

    def purge_closed_before(self, cutoff: datetime) -> int:
        """把结束于 `cutoff` 之前的拍卖清出目录，返回清掉的场数。"""
        raise NotImplementedError
