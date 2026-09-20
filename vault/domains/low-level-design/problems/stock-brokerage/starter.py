"""股票交易系统（Stock Brokerage）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/stock-brokerage -q
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TradingError(Exception):
    """本设计里所有失败路径的公共基类；被风控拒掉时带着那张 REJECTED 订单。"""

    def __init__(self, message: str, order: "Order | None" = None) -> None:
        super().__init__(message)
        self.order = order


class UnknownSymbolError(TradingError):
    """这个交易所没有挂牌这只股票。"""


class UnknownAccountError(TradingError):
    """账户不存在。"""


class InvalidOrderError(TradingError):
    """报单本身就不合法：数量非正、限价单没给价、市价单却带了价。"""


class InsufficientFundsError(TradingError):
    """可用资金不足以覆盖这张买单的预留额。"""


class InsufficientSharesError(TradingError):
    """可用持仓不足以覆盖这张卖单（本设计不允许卖空）。"""


class OrderNotFoundError(TradingError):
    """订单号不存在。"""


class OrderNotCancellableError(TradingError):
    """这张单已经处在终态，撤不了了。"""


class Side(Enum):
    BUY = "buy"
    SELL = "sell"

    @property
    def opposite(self) -> "Side":
        """对手方向。"""
        raise NotImplementedError


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(Enum):
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

    @property
    def is_terminal(self) -> bool:
        """终态不再变化，也就不可撤单。"""
        raise NotImplementedError


@dataclass(slots=True)
class Order:
    """一张报单；`reserved` 是这张单还锁着的额度（买单记分、卖单记股）。"""

    id: str
    account_id: str
    symbol: str
    side: Side
    type: OrderType
    quantity: int
    limit_price: int | None
    created_at: datetime
    status: OrderStatus = OrderStatus.NEW
    filled_quantity: int = 0
    reserved: int = 0
    reserve_price: int = 0

    @property
    def open_quantity(self) -> int:
        """还没成交的股数。"""
        raise NotImplementedError

    @property
    def is_open(self) -> bool:
        """还活着（可能继续成交、可以被撤）。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Fill:
    """一笔成交回报，不可变。"""

    symbol: str
    price: int
    quantity: int
    buy_order_id: str
    sell_order_id: str
    taker_order_id: str
    at: datetime


@dataclass(frozen=True, slots=True)
class TopOfBook:
    """盘口快照事件；没有挂单的一侧价为 `None`、量为 0。"""

    symbol: str
    bid: int | None
    bid_quantity: int
    ask: int | None
    ask_quantity: int
    last_price: int | None
    at: datetime


class Account:
    """现金与持仓。可用 = 总量 − 已预留；自己不带锁。"""

    def __init__(self, account_id: str, cash: int = 0,
                 positions: Mapping[str, int] | None = None) -> None:
        raise NotImplementedError

    @property
    def available_cash(self) -> int:
        """没有被挂单锁住的现金（分）。"""
        raise NotImplementedError

    def position(self, symbol: str) -> int:
        """持有多少股。"""
        raise NotImplementedError

    def available_shares(self, symbol: str) -> int:
        """没有被挂着的卖单锁住的股数。"""
        raise NotImplementedError

    def positions(self) -> Mapping[str, int]:
        """持仓的一份快照。"""
        raise NotImplementedError

    def reserve_cash(self, amount: int) -> None:
        """冻结现金。"""
        raise NotImplementedError

    def release_cash(self, amount: int) -> None:
        """解冻现金。"""
        raise NotImplementedError

    def reserve_shares(self, symbol: str, quantity: int) -> None:
        """冻结持仓。"""
        raise NotImplementedError

    def release_shares(self, symbol: str, quantity: int) -> None:
        """解冻持仓。"""
        raise NotImplementedError

    def apply_buy(self, symbol: str, quantity: int, price: int, reserve_price: int) -> None:
        """买方结算：按预留价解冻，按成交价扣钱，差额回到可用资金。"""
        raise NotImplementedError

    def apply_sell(self, symbol: str, quantity: int, price: int) -> None:
        """卖方结算：解冻并交出股票，收到现金。"""
        raise NotImplementedError


class BookSide:
    """订单簿的一侧：价位 → 该价位上的挂单表，外加一张有序的活跃价位列表。"""

    def __init__(self, side: Side) -> None:
        raise NotImplementedError

    @property
    def level_count(self) -> int:
        """还有多少个活跃价位。"""
        raise NotImplementedError

    @property
    def order_count(self) -> int:
        """这一侧挂着多少张单。"""
        raise NotImplementedError

    def prices_in_priority(self) -> tuple[int, ...]:
        """按优先级排好的价位快照。"""
        raise NotImplementedError

    def best_price(self) -> int | None:
        """最优价；空簿返回 `None`。"""
        raise NotImplementedError

    def quantity_at(self, price: int) -> int:
        """某价位上还挂着多少股。"""
        raise NotImplementedError

    def front(self) -> Order | None:
        """最优价上排在最前面的那张单。"""
        raise NotImplementedError

    def add(self, order: Order) -> None:
        """把一张限价单挂到它的价位后面。"""
        raise NotImplementedError

    def remove(self, order: Order) -> bool:
        """把一张单摘下来，返回它是不是真的在簿子上。"""
        raise NotImplementedError

    def depth(self) -> tuple[tuple[int, int], ...]:
        """整侧的 `(价位, 股数)` 快照。"""
        raise NotImplementedError


class OrderBook:
    """一只股票的订单簿：两侧 + 价格-时间优先撮合。只认股数，不认钱。"""

    def __init__(self, symbol: str) -> None:
        raise NotImplementedError

    def side(self, side: Side) -> BookSide:
        """取某一侧。"""
        raise NotImplementedError

    @property
    def resting_count(self) -> int:
        """簿子上还挂着多少张单。"""
        raise NotImplementedError

    def walk_cost(self, quantity: int) -> tuple[int, int]:
        """市价买单的试算：能买到多少股、最差每股多少分。"""
        raise NotImplementedError

    def submit(self, incoming: Order) -> list[tuple[Order, int, int]]:
        """撮合一张新单，返回 `[(对手挂单, 成交价, 成交股数)]`。"""
        raise NotImplementedError

    def cancel(self, order: Order) -> bool:
        """把一张挂单从簿子上摘掉。"""
        raise NotImplementedError

    def top_of_book(self, at: datetime) -> TopOfBook:
        """当前盘口快照。"""
        raise NotImplementedError


Clock = Callable[[], datetime]
Subscriber = Callable[[TopOfBook], None]


class Brokerage:
    """单场所、进程内的经纪与撮合服务。一把锁保护账户、订单索引与所有订单簿。"""

    def __init__(self, clock: Clock, symbols: Sequence[str]) -> None:
        raise NotImplementedError

    def open_account(self, account_id: str, cash: int = 0,
                     positions: Mapping[str, int] | None = None) -> None:
        """开户，可带初始现金（分）和初始持仓。"""
        raise NotImplementedError

    def cash(self, account_id: str) -> tuple[int, int]:
        """`(总现金, 可用现金)`。"""
        raise NotImplementedError

    def position(self, account_id: str, symbol: str) -> tuple[int, int]:
        """`(总持仓, 可用持仓)`。"""
        raise NotImplementedError

    def portfolio(self, account_id: str) -> Mapping[str, int]:
        """整个持仓的快照。"""
        raise NotImplementedError

    def total_cash(self) -> int:
        """全场现金总额。"""
        raise NotImplementedError

    def total_shares(self, symbol: str) -> int:
        """全场某只股票的总股数。"""
        raise NotImplementedError

    def place_order(self, account_id: str, symbol: str, side: Side, quantity: int,
                    order_type: OrderType = OrderType.LIMIT,
                    limit_price: int | None = None) -> Order:
        """报一张单：校验 → 预留 → 撮合 → 逐笔结算 → 释放剩余预留。"""
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> Order:
        """撤单；已经终结的单抛 `OrderNotCancellableError`。"""
        raise NotImplementedError

    def order(self, order_id: str) -> Order:
        """按单号取订单。"""
        raise NotImplementedError

    @property
    def order_count(self) -> int:
        """订单索引里还有多少条。"""
        raise NotImplementedError

    def fills(self, symbol: str | None = None) -> tuple[Fill, ...]:
        """成交流水的快照。"""
        raise NotImplementedError

    def depth(self, symbol: str, side: Side) -> tuple[tuple[int, int], ...]:
        """某一侧的档位快照。"""
        raise NotImplementedError

    def top_of_book(self, symbol: str) -> TopOfBook:
        """当前盘口。"""
        raise NotImplementedError

    def purge_terminal_orders_before(self, cutoff: datetime) -> int:
        """把终结于 `cutoff` 之前的订单清出索引，返回清掉的条数。"""
        raise NotImplementedError

    def subscribe(self, subscriber: Subscriber) -> Callable[[], None]:
        """订阅盘口变化，返回一个退订函数。"""
        raise NotImplementedError

    @property
    def subscriber_count(self) -> int:
        """当前订阅者数量。"""
        raise NotImplementedError
