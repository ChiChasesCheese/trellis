"""股票交易系统（Stock Brokerage）——资金校验、限价订单簿与价格-时间优先撮合的参考实现。

五行设计：钱是**整数分**、股是整数股，任何一笔成交都只在两个账户之间搬运，绝不凭空产生或消失；
下单先**预留**（买单锁钱、卖单锁股），撮合与结算因此只是花掉已经锁住的额度，不会再失败一次；
订单簿一侧是「价位 → 该价位的挂单表」，价位表用 `bisect` 维持有序、`dict` 的插入序天然就是同
价位的 FIFO，于是撤单是 O(1) 的删键、取最优价是 O(1) 的取端点；`OrderBook` 只认股数不认钱，
钱由 `Brokerage` 在同一把锁里结算；行情快照在**锁外**推送给订阅者。单场所、进程内、不做撮合分片。
"""

from __future__ import annotations

import bisect
import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径：一个小异常家族。调用方可以只 catch 基类，也可以分别处理"钱不够"和"股不够"。


class TradingError(Exception):
    """本设计里所有失败路径的公共基类。

    被风控拒掉时它**带着那张 REJECTED 订单**：调用方既拿到异常，也拿到留痕的那条记录，
    不必去猜单号，也不必为了看一眼状态就去翻订单索引。
    """

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
    """可用资金不足以覆盖这张买单的预留额；订单已被记为 REJECTED。"""

class InsufficientSharesError(TradingError):
    """可用持仓不足以覆盖这张卖单；本设计不允许卖空，订单已被记为 REJECTED。"""

class OrderNotFoundError(TradingError):
    """订单号不存在（或已经被 `purge_terminal_orders_before` 清出索引）。"""

class OrderNotCancellableError(TradingError):
    """这张单已经处在终态（成交完、已撤、已拒），撤不了了。"""


# --------------------------------------------------------------------------
# 枚举：方向、订单类型、生命周期。


class Side(Enum):
    """买还是卖。撮合里到处要"对手方"，所以把它做成方向自己的属性。"""

    BUY = "buy"
    SELL = "sell"

    @property
    def opposite(self) -> "Side":
        """对手方向。"""
        return Side.SELL if self is Side.BUY else Side.BUY


class OrderType(Enum):
    """市价单立即用对手方的价成交、绝不挂单；限价单可以挂在簿子上等。"""

    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(Enum):
    """订单生命周期：NEW → PARTIALLY_FILLED → FILLED / CANCELLED / REJECTED。

    这里**没有** "PARTIALLY_FILLED_AND_CANCELLED"：撤掉一张成交了一半的单，状态就是
    CANCELLED，成交了多少由 `filled_quantity` 说话——同一件事不要两份表示。
    """

    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

    @property
    def is_terminal(self) -> bool:
        """终态不再变化，也就不可撤单。"""
        return self in (OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED)


@dataclass(slots=True)
class Order:
    """一张报单。它是**可变**的：`filled_quantity` 和 `status` 随成交推进。

    `reserved` 是这张单**还锁着**的额度——买单记分、卖单记股。它的不变式是：单一旦进入终态，
    `reserved` 必定为 0（要么被成交花掉，要么被释放回账户），这条不变式被测试直接断言。
    """

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
        return self.quantity - self.filled_quantity

    @property
    def is_open(self) -> bool:
        """还活着（可能继续成交、可以被撤）。"""
        return not self.status.is_terminal


@dataclass(frozen=True, slots=True)
class Fill:
    """一笔成交回报：不可变，是交易流水（tape）里的一行，任何人都不能事后改。"""

    symbol: str
    price: int
    quantity: int
    buy_order_id: str
    sell_order_id: str
    taker_order_id: str
    at: datetime
@dataclass(frozen=True, slots=True)
class TopOfBook:
    """盘口快照事件：**自带发生了什么**，订阅者只读它就够，不必回头去问 `Brokerage`
    要数据（那样就绕过了它的锁）。没有挂单的一侧价为 `None`、量为 0。
    """

    symbol: str
    bid: int | None
    bid_quantity: int
    ask: int | None
    ask_quantity: int
    last_price: int | None
    at: datetime

# --------------------------------------------------------------------------
# Account：一个账户的钱与股。它自己**不带锁**——每一次读写都发生在 `Brokerage` 的那把锁里，
# 账户再挂一把锁只会制造嵌套和锁顺序问题，却不会让"一笔成交两边一起动"变得更原子。


class Account:
    """现金与持仓。不变式：`reserved_cash <= cash`，且每只股票 `reserved <= position`。

    可用 = 总量 − 已预留。预留是这个设计的核心机制：下单那一刻就把钱/股冻住，于是撮合阶段
    不可能再出现"撮上了才发现买方没钱"——那种设计必须回滚，而回滚是一切错账的来源。
    """

    def __init__(self, account_id: str, cash: int = 0,
                 positions: Mapping[str, int] | None = None) -> None:
        self.id = account_id
        self.cash = cash
        self.reserved_cash = 0
        self._positions: dict[str, int] = {s: q for s, q in (positions or {}).items() if q}
        self._reserved_shares: dict[str, int] = {}

    @property
    def available_cash(self) -> int:
        """没有被挂单锁住、可以用来下新单的现金（分）。"""
        return self.cash - self.reserved_cash

    def position(self, symbol: str) -> int:
        """持有多少股。"""
        return self._positions.get(symbol, 0)

    def available_shares(self, symbol: str) -> int:
        """没有被挂着的卖单锁住的股数。"""
        return self.position(symbol) - self._reserved_shares.get(symbol, 0)

    def positions(self) -> Mapping[str, int]:
        """持仓的一份快照——内部那张表不外借。"""
        return dict(self._positions)

    def _bump(self, table: dict[str, int], symbol: str, delta: int) -> None:
        """加减一张"股票 → 数量"的表，**归零就删键**：没有这一步，一个账户清仓过的每只
        股票都会永远留下一条 0，表随着交易历史无限增长。
        """
        total = table.get(symbol, 0) + delta
        if total:
            table[symbol] = total
        else:
            table.pop(symbol, None)

    def reserve_cash(self, amount: int) -> None:
        """冻结现金；调用方须先确认 `available_cash` 够。"""
        self.reserved_cash += amount

    def release_cash(self, amount: int) -> None:
        """解冻现金（撤单或市价单剩余量作废）。"""
        self.reserved_cash -= amount

    def reserve_shares(self, symbol: str, quantity: int) -> None:
        """冻结持仓。"""
        self._bump(self._reserved_shares, symbol, quantity)

    def release_shares(self, symbol: str, quantity: int) -> None:
        """解冻持仓。"""
        self._bump(self._reserved_shares, symbol, -quantity)

    def apply_buy(self, symbol: str, quantity: int, price: int, reserve_price: int) -> None:
        """买方结算：按**预留价**解冻，按**成交价**扣钱，差额自动回到可用资金。

        限价买 100 分、对手挂 97 分成交，这 3 分的价格改善（price improvement）就是这样退
        回去的；先扣钱再解冻还是先解冻再扣钱都一样，因为两步在同一把锁里。
        """
        self.reserved_cash -= quantity * reserve_price
        self.cash -= quantity * price
        self._bump(self._positions, symbol, quantity)

    def apply_sell(self, symbol: str, quantity: int, price: int) -> None:
        """卖方结算：解冻并交出股票，收到现金。"""
        self._bump(self._reserved_shares, symbol, -quantity)
        self._bump(self._positions, symbol, -quantity)
        self.cash += quantity * price


# --------------------------------------------------------------------------
# 订单簿。BookSide 是一侧，OrderBook 是两侧加撮合。两个类都只认股数，不认钱。


class BookSide:
    """订单簿的一侧：`价位 → 该价位上的挂单表`，外加一张**升序**的活跃价位列表。

    同价位的时间优先由 `dict` 的插入序天然给出（Python 3.7 起是语言保证），所以不需要序号，
    也不需要 `deque`——`dict` 还额外白送 O(1) 的按单号删除，而 `deque` 删中间是 O(n)。
    不变式：`_levels` 和 `_prices` 的键集合永远相等，空价位立刻从两边一起删掉。
    """

    def __init__(self, side: Side) -> None:
        self.side = side
        self._levels: dict[int, dict[str, Order]] = {}
        self._prices: list[int] = []

    @property
    def level_count(self) -> int:
        """还有多少个活跃价位——价位空了必须立刻消失，这个数就是证据。"""
        return len(self._levels)

    @property
    def order_count(self) -> int:
        """这一侧挂着多少张单。"""
        return sum(len(level) for level in self._levels.values())

    def prices_in_priority(self) -> tuple[int, ...]:
        """按优先级排好的价位快照：买方价高者先，卖方价低者先。"""
        return tuple(reversed(self._prices)) if self.side is Side.BUY else tuple(self._prices)

    def best_price(self) -> int | None:
        """最优价；空簿返回 `None`。有序列表让它退化成取端点。"""
        if not self._prices:
            return None
        return self._prices[-1] if self.side is Side.BUY else self._prices[0]

    def quantity_at(self, price: int) -> int:
        """某价位上还挂着多少股。"""
        return sum(o.open_quantity for o in self._levels.get(price, {}).values())

    def front(self) -> Order | None:
        """最优价上排在最前面的那张单——价格-时间优先的"下一个该成交的人"。"""
        price = self.best_price()
        return None if price is None else next(iter(self._levels[price].values()))

    def add(self, order: Order) -> None:
        """把一张限价单挂到它的价位后面。"""
        price = order.limit_price
        assert price is not None
        level = self._levels.get(price)
        if level is None:
            level = self._levels[price] = {}
            bisect.insort(self._prices, price)
        level[order.id] = order

    def remove(self, order: Order) -> bool:
        """把一张单摘下来，返回它是不是真的在簿子上。价位空了就连价位一起删。"""
        price = order.limit_price
        level = self._levels.get(price) if price is not None else None
        if level is None or level.pop(order.id, None) is None:
            return False
        if not level:
            del self._levels[price]
            self._prices.pop(bisect.bisect_left(self._prices, price))
        return True

    def depth(self) -> tuple[tuple[int, int], ...]:
        """整侧的 `(价位, 股数)` 快照，按优先级排好。"""
        return tuple((p, self.quantity_at(p)) for p in self.prices_in_priority())


class OrderBook:
    """一只股票的订单簿：两侧 + 价格-时间优先的撮合。

    职责边界是这道题的关键一刀：**簿子只管谁排在谁前面、成交多少股、成交在什么价**，
    一分钱都不碰。于是撮合可以被单独测试，而资金规则换了（融资融券、手续费、分级费率）
    也不会动到这里的任何一行。
    """

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self._sides = {Side.BUY: BookSide(Side.BUY), Side.SELL: BookSide(Side.SELL)}
        self.last_price: int | None = None

    def side(self, side: Side) -> BookSide:
        """取某一侧。"""
        return self._sides[side]

    @property
    def resting_count(self) -> int:
        """簿子上还挂着多少张单——成交完和撤掉的都必须消失。"""
        return sum(s.order_count for s in self._sides.values())

    def _crosses(self, incoming: Order, resting_price: int) -> bool:
        """这张来单吃不吃得动挂在 `resting_price` 的对手单。市价单来者不拒。"""
        if incoming.type is OrderType.MARKET:
            return True
        assert incoming.limit_price is not None
        if incoming.side is Side.BUY:
            return incoming.limit_price >= resting_price
        return incoming.limit_price <= resting_price

    def walk_cost(self, quantity: int) -> tuple[int, int]:
        """市价买单专用的**试算**：照现在的卖方挂单能买到多少股、最差每股多少分。

        它和随后的撮合在同一把锁里跑，所以这份试算不会过期——这正是市价买单敢按"最差价"
        预留资金的前提。
        """
        asks = self._sides[Side.SELL]
        remaining, worst = quantity, 0
        for price in asks.prices_in_priority():
            if remaining <= 0:
                break
            take = min(remaining, asks.quantity_at(price))
            if take:
                remaining -= take
                worst = price
        return quantity - remaining, worst

    @staticmethod
    def _fill(order: Order, quantity: int) -> None:
        """推进一张单的成交量与状态。"""
        order.filled_quantity += quantity
        order.status = (OrderStatus.FILLED if order.open_quantity == 0
                        else OrderStatus.PARTIALLY_FILLED)

    def submit(self, incoming: Order) -> list[tuple[Order, int, int]]:
        """把一张新单撮进簿子，返回 `[(对手挂单, 成交价, 成交股数)]`。

        成交价永远取**挂单方**的限价：挂单方先到，它公布的价格就是市场承诺过的价；来单
        愿意出更好的价是它自己的事，多出来的部分退给它。剩余量：限价单挂上去，市价单作废。
        撮合是确定的——同一串报单序列，无论跑多少次都得到同一串成交。
        """
        matches: list[tuple[Order, int, int]] = []
        opposite = self._sides[incoming.side.opposite]
        while incoming.open_quantity > 0:
            resting = opposite.front()
            if resting is None or resting.limit_price is None or not self._crosses(incoming, resting.limit_price):
                break
            quantity = min(incoming.open_quantity, resting.open_quantity)
            price = resting.limit_price
            self._fill(incoming, quantity)
            self._fill(resting, quantity)
            if resting.open_quantity == 0:
                opposite.remove(resting)
            self.last_price = price
            matches.append((resting, price, quantity))
        if incoming.open_quantity > 0:
            if incoming.type is OrderType.LIMIT:
                self._sides[incoming.side].add(incoming)
            else:
                incoming.status = OrderStatus.CANCELLED
        return matches

    def cancel(self, order: Order) -> bool:
        """把一张挂单从簿子上摘掉。"""
        return self._sides[order.side].remove(order)

    def top_of_book(self, at: datetime) -> TopOfBook:
        """当前盘口快照。"""
        bid, ask = self._sides[Side.BUY].best_price(), self._sides[Side.SELL].best_price()
        return TopOfBook(
            symbol=self.symbol, bid=bid, ask=ask, last_price=self.last_price, at=at,
            bid_quantity=0 if bid is None else self._sides[Side.BUY].quantity_at(bid),
            ask_quantity=0 if ask is None else self._sides[Side.SELL].quantity_at(ask),
        )


# --------------------------------------------------------------------------
# Brokerage：门面。开户、报单、撤单、结算、行情。钱只在这里动。


Clock = Callable[[], datetime]
Subscriber = Callable[[TopOfBook], None]


class Brokerage:
    """单场所、进程内的经纪与撮合服务。

    锁纪律：一把 `RLock` 保护账户表、订单索引、所有订单簿。粒度粗，但"校验 → 预留 → 撮合
    → 结算"必须是一个原子动作，跨越两个账户和一个簿子，拆细只会换来锁顺序死锁。GIL 在这里
    一点忙都帮不上：它只保证单条字节码不被打断，而"查可用资金"和"冻结资金"是两条。
    外部回调（行情订阅者）一律在锁外调用。
    """

    def __init__(self, clock: Clock, symbols: Sequence[str]) -> None:
        self._clock = clock
        self._books: dict[str, OrderBook] = {s: OrderBook(s) for s in symbols}
        self._accounts: dict[str, Account] = {}
        self._orders: dict[str, Order] = {}
        self._fills: list[Fill] = []
        self._subscribers: list[Subscriber] = []
        self._lock = threading.RLock()
        self._ids = (f"O{n}" for n in itertools.count(1))

    # ---- 账户 ------------------------------------------------------------

    def open_account(self, account_id: str, cash: int = 0,
                     positions: Mapping[str, int] | None = None) -> None:
        """开户，可带初始现金（分）和初始持仓。"""
        with self._lock:
            self._accounts[account_id] = Account(account_id, cash, positions)

    def cash(self, account_id: str) -> tuple[int, int]:
        """`(总现金, 可用现金)`，单位分。读也要拿锁——否则会读到结算做到一半的账。"""
        with self._lock:
            account = self._account(account_id)
            return account.cash, account.available_cash

    def position(self, account_id: str, symbol: str) -> tuple[int, int]:
        """`(总持仓, 可用持仓)`。"""
        with self._lock:
            account = self._account(account_id)
            return account.position(symbol), account.available_shares(symbol)

    def portfolio(self, account_id: str) -> Mapping[str, int]:
        """整个持仓的快照。"""
        with self._lock:
            return self._account(account_id).positions()

    def total_cash(self) -> int:
        """全场现金总额。撮合是零和的搬运，这个数只会被入金改变——风控自检就看它。"""
        with self._lock:
            return sum(a.cash for a in self._accounts.values())

    def total_shares(self, symbol: str) -> int:
        """全场某只股票的总股数；同样只有建仓能改变它，成交不能。"""
        with self._lock:
            return sum(a.position(symbol) for a in self._accounts.values())

    def _account(self, account_id: str) -> Account:
        account = self._accounts.get(account_id)
        if account is None:
            raise UnknownAccountError(f"unknown account {account_id!r}")
        return account

    def _book(self, symbol: str) -> OrderBook:
        book = self._books.get(symbol)
        if book is None:
            raise UnknownSymbolError(f"{symbol!r} is not listed here")
        return book

    # ---- 报单 ------------------------------------------------------------

    def place_order(self, account_id: str, symbol: str, side: Side, quantity: int,
                    order_type: OrderType = OrderType.LIMIT,
                    limit_price: int | None = None) -> Order:
        """报一张单：校验 → 预留 → 撮合 → 逐笔结算 → 释放剩余预留，全程在一把锁里。

        资金/持仓不足时，订单仍然被建出来并记为 REJECTED 再抛异常——被拒的报单也是要留痕
        的事实，不能只在调用栈里闪一下。
        """
        now = self._clock()
        with self._lock:
            account, book = self._account(account_id), self._book(symbol)
            order = self._build(account_id, symbol, side, quantity, order_type, limit_price, now)
            self._orders[order.id] = order
            self._reserve(account, order, book)
            for resting, price, filled in book.submit(order):
                self._settle(order, resting, price, filled, now)
            if not order.is_open:
                self._release(order)
            event = book.top_of_book(now)
        self._publish(event)
        return order

    def _build(self, account_id: str, symbol: str, side: Side, quantity: int,
               order_type: OrderType, limit_price: int | None, now: datetime) -> Order:
        """建单前的纯校验：数量必须为正，限价单必须带正的价，市价单不许带价。"""
        if quantity <= 0:
            raise InvalidOrderError("quantity must be positive")
        if order_type is OrderType.LIMIT and (limit_price is None or limit_price <= 0):
            raise InvalidOrderError("a limit order needs a positive limit price")
        if order_type is OrderType.MARKET and limit_price is not None:
            raise InvalidOrderError("a market order must not carry a price")
        return Order(id=next(self._ids), account_id=account_id, symbol=symbol, side=side,
                     type=order_type, quantity=quantity, limit_price=limit_price, created_at=now)

    def _reserve(self, account: Account, order: Order, book: OrderBook) -> None:
        """冻结这张单需要的钱或股；不够就把单记成 REJECTED 并抛异常。

        限价买按限价冻结；市价买没有价，就先试算一次能吃到的最差价，按最差价冻结——宁可
        多冻一点，成交时按实际价扣、差额当场退。卖单冻股，因此本设计**不支持卖空**。
        """
        if order.side is Side.BUY:
            if order.type is OrderType.LIMIT:
                assert order.limit_price is not None
                order.reserve_price, fillable = order.limit_price, order.quantity
            else:
                fillable, order.reserve_price = book.walk_cost(order.quantity)
            needed = fillable * order.reserve_price
            if needed > account.available_cash:
                order.status = OrderStatus.REJECTED
                raise InsufficientFundsError(
                    f"order {order.id} needs {needed} but {account.id} has "
                    f"{account.available_cash}", order)
            account.reserve_cash(needed)
            order.reserved = needed
        else:
            if order.quantity > account.available_shares(order.symbol):
                order.status = OrderStatus.REJECTED
                raise InsufficientSharesError(
                    f"order {order.id} sells {order.quantity} {order.symbol} but "
                    f"{account.id} has {account.available_shares(order.symbol)} free", order)
            account.reserve_shares(order.symbol, order.quantity)
            order.reserved = order.quantity

    def _settle(self, taker: Order, resting: Order, price: int, quantity: int,
                at: datetime) -> None:
        """一笔成交的结算：买方的钱变成卖方的钱，卖方的股变成买方的股，一步不落。

        钱既不产生也不消失——买方 `cash` 减去的和卖方 `cash` 加上的都是 `price*quantity`。
        挂单方永远按自己的价成交，所以它的预留被精确花光，只有来单才会有差额要退。
        """
        buy, sell = (taker, resting) if taker.side is Side.BUY else (resting, taker)
        self._account(buy.account_id).apply_buy(buy.symbol, quantity, price, buy.reserve_price)
        buy.reserved -= quantity * buy.reserve_price
        self._account(sell.account_id).apply_sell(sell.symbol, quantity, price)
        sell.reserved -= quantity
        self._fills.append(Fill(symbol=taker.symbol, price=price, quantity=quantity,
                                buy_order_id=buy.id, sell_order_id=sell.id,
                                taker_order_id=taker.id, at=at))

    def _release(self, order: Order) -> None:
        """把一张终结的单**还没花掉**的预留退回账户，并把 `reserved` 清零。"""
        account = self._account(order.account_id)
        if order.side is Side.BUY:
            account.release_cash(order.reserved)
        else:
            account.release_shares(order.symbol, order.reserved)
        order.reserved = 0

    def cancel_order(self, order_id: str) -> Order:
        """撤单。撤单和成交的竞争由这把锁裁定：成交先到，这里看到的就是终态，直接拒绝；
        撤单先到，后来的对手单在簿子上已经找不到它。成交了一半的单撤掉剩下的一半，
        `filled_quantity` 保留，不会被退回去的预留抹掉。
        """
        now = self._clock()
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                raise OrderNotFoundError(f"unknown order {order_id!r}")
            if not order.is_open:
                raise OrderNotCancellableError(f"order {order_id} is already {order.status.value}")
            book = self._book(order.symbol)
            book.cancel(order)
            order.status = OrderStatus.CANCELLED
            self._release(order)
            event = book.top_of_book(now)
        self._publish(event)
        return order

    # ---- 查询与清理 ------------------------------------------------------

    def order(self, order_id: str) -> Order:
        """按单号取订单。"""
        with self._lock:
            order = self._orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"unknown order {order_id!r}")
        return order

    @property
    def order_count(self) -> int:
        """订单索引里还有多少条。"""
        with self._lock:
            return len(self._orders)

    def fills(self, symbol: str | None = None) -> tuple[Fill, ...]:
        """成交流水的快照。它是账，只增不删——真实系统把它流式落库，内存里只留当日。"""
        with self._lock:
            return tuple(f for f in self._fills if symbol is None or f.symbol == symbol)

    def depth(self, symbol: str, side: Side) -> tuple[tuple[int, int], ...]:
        """某一侧的档位快照 `((价, 量), …)`，按优先级排好。"""
        with self._lock:
            return self._book(symbol).side(side).depth()

    def top_of_book(self, symbol: str) -> TopOfBook:
        """当前盘口。"""
        with self._lock:
            return self._book(symbol).top_of_book(self._clock())

    def purge_terminal_orders_before(self, cutoff: datetime) -> int:
        """把终结于 `cutoff` 之前的订单清出索引，返回清掉的条数。

        没有它，`_orders` 会随着报单量无限增长，而其中绝大多数是当天就已经撤掉或成交完的。
        成交流水不跟着删——它记的是单号而不是 `Order` 引用，所以对象真的能被回收。
        """
        with self._lock:
            gone = [oid for oid, o in self._orders.items()
                    if not o.is_open and o.created_at < cutoff]
            for order_id in gone:
                del self._orders[order_id]
        return len(gone)

    # ---- 行情推送（第 4 关：加它没有动撮合的任何一行） --------------------

    def subscribe(self, subscriber: Subscriber) -> Callable[[], None]:
        """订阅盘口变化，返回一个退订函数——退订的手段和订阅一起交出去，订阅者表才会缩小。"""
        with self._lock:
            self._subscribers.append(subscriber)

        def unsubscribe() -> None:
            """退订；重复调用无害。"""
            with self._lock:
                if subscriber in self._subscribers:
                    self._subscribers.remove(subscriber)

        return unsubscribe

    @property
    def subscriber_count(self) -> int:
        """当前订阅者数量。"""
        with self._lock:
            return len(self._subscribers)

    def _publish(self, event: TopOfBook) -> None:
        """在**锁外**把盘口事件发出去：握着撮合锁调外部回调，一个慢订阅者就能让全场停摆。"""
        with self._lock:
            subscribers = tuple(self._subscribers)
        for subscriber in subscribers:
            subscriber(event)


if __name__ == "__main__":
    from datetime import UTC, timedelta

    now = datetime(2026, 3, 2, 9, 30, tzinfo=UTC)
    broker = Brokerage(clock=lambda: now, symbols=["BAC"])
    broker.open_account("alice", cash=30_000_00)
    broker.open_account("bob", positions={"BAC": 200})

    tape: list[TopOfBook] = []
    broker.subscribe(tape.append)

    broker.place_order("bob", "BAC", Side.SELL, 100, limit_price=240_12)
    broker.place_order("bob", "BAC", Side.SELL, 90, limit_price=237_45)
    taker = broker.place_order("alice", "BAC", Side.BUY, 110, limit_price=238_10)
    print(f"{taker.id}: {taker.status.value}, filled {taker.filled_quantity}")
    for fill in broker.fills("BAC"):
        print(f"  {fill.quantity} @ {fill.price / 100:.2f} ({fill.buy_order_id}/{fill.sell_order_id})")
    print("book:", broker.depth("BAC", Side.BUY), broker.depth("BAC", Side.SELL))
    print("alice cash:", broker.cash("alice"), "position:", broker.position("alice", "BAC"))
    print("conserved:", broker.total_cash(), broker.total_shares("BAC"))
    now = now + timedelta(days=1)
    print("purged:", broker.purge_terminal_orders_before(now), "top:", tape[-1])
