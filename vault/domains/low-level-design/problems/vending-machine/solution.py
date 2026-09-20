"""自动售货机（Vending Machine）——购买流程的状态机、库存与币箱、找零与失败路径。

核心思路：状态用 `Enum`，"哪个动作在哪个状态下合法"整个写进一张转移表 `TRANSITIONS`，
于是非法转移（没投币就选货、出货中再投币）由数据统一拒绝，而且可以被一个穷举测试盖满；
"数据够不够"（余额、库存、找不找得开）是另一回事，由守卫在转移之前检查，失败时状态原地
不动、钱一分不少。钱一律用整数分，绝不出现浮点。最关键的一条业务不变式是"要么完整成交、
要么原样退款"：找零方案在**货还没出来之前**就必须算出来，算不出来就拒绝这笔交易。支付方式
做成 `Tender` 协议（硬币托管／刷卡授权），因此加一个读卡器不需要动状态机的任何一行。
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Protocol


class Coin(IntEnum):
    """支持的硬币面额，单位是分。枚举值就是面值，可以直接参与算术。"""

    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100


class State(Enum):
    """一次购买流程所处的阶段。"""

    IDLE = "idle"
    COIN_INSERTED = "coin_inserted"
    DISPENSING = "dispensing"
    RETURNING_CHANGE = "returning_change"

    @property
    def prompt(self) -> str:
        """屏幕上该显示什么——状态要携带的"数据"用一张表就够，不必为此一状态一个类。"""
        return _PROMPTS[self]


class Event(Enum):
    """买家或机器可以发起的动作。名字不带"硬币"，因为刷卡走的是同一个 `PAY`。"""

    PAY = "pay"
    SELECT = "select"
    DISPENSE = "dispense"
    COLLECT = "collect"
    REFUND = "refund"


_PROMPTS: dict[State, str] = {
    State.IDLE: "请投币或刷卡",
    State.COIN_INSERTED: "请选择商品，或按退币",
    State.DISPENSING: "正在出货",
    State.RETURNING_CHANGE: "请取走找零",
}

# 状态机的全部合法转移。表里没有的组合一律非法——"没投币就按选择""出货中再投币"都在
# 这里被一次性拒绝，不需要在每个方法里重写一遍 if。
TRANSITIONS: dict[tuple[State, Event], State] = {
    (State.IDLE, Event.PAY): State.COIN_INSERTED,
    (State.COIN_INSERTED, Event.PAY): State.COIN_INSERTED,
    (State.COIN_INSERTED, Event.SELECT): State.DISPENSING,
    (State.COIN_INSERTED, Event.REFUND): State.IDLE,
    (State.DISPENSING, Event.DISPENSE): State.RETURNING_CHANGE,
    (State.RETURNING_CHANGE, Event.COLLECT): State.IDLE,
}


class VendingMachineError(Exception):
    """本设计全部失败路径的公共基类。"""


class IllegalTransitionError(VendingMachineError):
    """这个动作在当前状态下不合法（转移表里没有这一项）。"""


class InvalidSelectionError(VendingMachineError):
    """没有这个货道编号。"""


class OutOfStockError(VendingMachineError):
    """这个货道空了。"""


class InsufficientFundsError(VendingMachineError):
    """已投金额不够买这件商品。"""


class CannotMakeChangeError(VendingMachineError):
    """币箱凑不出该找的零钱——货还没出，这笔交易整笔拒绝。"""


@dataclass(frozen=True, slots=True)
class Item:
    """一件商品：名字和价格（单位是分）。不可变，货道换货就是换一个 `Item`。"""

    name: str
    price: int


@dataclass(slots=True)
class Slot:
    """一个货道：装着哪种商品、还剩几件。库存只在这里有一份，不另开一本账。"""

    item: Item
    quantity: int


class CoinBank:
    """币箱：每种面额各存了多少枚。

    不变式：计数降到 0 的面额会被从字典里删掉。这不是洁癖——找零算法遍历的就是这个字典，
    留着一条 `NICKEL: 0` 会让它反复尝试一种其实没有的硬币，而"明明没有却以为有"正是
    找零算法最难查的一类 bug。
    """

    def __init__(self, counts: Mapping[Coin, int] | None = None) -> None:
        self._counts: dict[Coin, int] = {c: n for c, n in (counts or {}).items() if n > 0}

    def counts(self) -> Mapping[Coin, int]:
        """一份只读快照；币箱从不把自己的字典交出去。"""
        return MappingProxyType(dict(self._counts))

    @property
    def total(self) -> int:
        return sum(int(coin) * n for coin, n in self._counts.items())

    def add(self, coins: Iterable[Coin]) -> None:
        for coin in coins:
            self._counts[coin] = self._counts.get(coin, 0) + 1

    def take(self, coins: Iterable[Coin]) -> None:
        """取走一组硬币；数量不足直接报错，取空的面额立刻从字典里消失。"""
        wanted: dict[Coin, int] = {}
        for coin in coins:
            wanted[coin] = wanted.get(coin, 0) + 1
        for coin, n in wanted.items():
            if self._counts.get(coin, 0) < n:
                raise CannotMakeChangeError(f"bank holds fewer than {n} × {coin.name}")
        for coin, n in wanted.items():
            self._counts[coin] -= n
            if self._counts[coin] == 0:
                del self._counts[coin]


# --------------------------------------------------------------------------
# 找零算法：给应找金额和一份"可用硬币"的计数，给出一种凑法或者 `None`。
# 两种实现都是纯函数，机器不知道它们的内容，构造时传进来即可。

ChangeMaker = Callable[[int, Mapping[Coin, int]], "tuple[Coin, ...] | None"]


def greedy_change(amount: int, available: Mapping[Coin, int]) -> tuple[Coin, ...] | None:
    """贪心：从大面额往小拿，能拿几枚拿几枚。

    在 5/10/25/100 这种规范币制（canonical system）下，只要硬币管够，贪心给出的就是
    最少枚数的解。它的失效不在"币制奇怪"这种教科书情形，而在**币箱缺货**：比如要找 30 分，
    币箱里只有 25 分和 10 分，贪心先拿走 25 分，剩下 5 分再也凑不出，于是报告"找不开"——
    可实际上三枚 10 分就是一个完美的解。
    """
    plan: list[Coin] = []
    remaining = amount
    for coin in sorted(available, reverse=True):
        take = min(remaining // int(coin), available[coin])
        plan.extend([coin] * take)
        remaining -= int(coin) * take
    return tuple(plan) if remaining == 0 else None


def exact_change(amount: int, available: Mapping[Coin, int]) -> tuple[Coin, ...] | None:
    """有界背包 DP：只要存在一种凑法就一定找得到，代价是 O(金额 × 硬币总枚数)。

    机器里的金额是几百分、硬币是几十枚这个量级，这点代价完全付得起；而"明明能找却说
    找不开"会直接变成一次拒单，所以默认值得用它。
    """
    if amount <= 0:
        return ()
    best: list[tuple[Coin, ...] | None] = [None] * (amount + 1)
    best[0] = ()
    for coin in sorted(available, reverse=True):
        for _ in range(available[coin]):  # 每轮最多再用掉一枚这种面额
            for total in range(amount, int(coin) - 1, -1):
                head = best[total - int(coin)]
                if best[total] is None and head is not None:
                    best[total] = head + (coin,)
    return best[amount]


# --------------------------------------------------------------------------
# 支付方式：现金和刷卡在状态机眼里是同一件事（都触发 `PAY`），差别全部封在这里。


class Tender(Protocol):
    """一笔尚未结清的付款。真有两种行为不同的实现，所以这里的协议是挣来的，不是摆设。"""

    @property
    def amount(self) -> int:
        """当前可用于购买的金额，单位分。"""

    @property
    def wants_coin_change(self) -> bool:
        """找零是否必须以硬币形式给出（刷卡不用，多授权的部分不扣即可）。"""

    def coins_held(self) -> tuple[Coin, ...]:
        """正被托管、成交后会进入币箱的硬币。"""

    def settle(self, bank: CoinBank, price: int) -> None:
        """成交：现金存进币箱，刷卡只扣实际货价。"""

    def release(self) -> tuple[Coin, ...]:
        """退款：现金原样退回，刷卡撤销授权后没有硬币可退。"""


@dataclass(slots=True)
class CoinTender:
    """现金付款：投进来的硬币原样托管，退币时退回的就是这几枚。"""

    coins: list[Coin] = field(default_factory=list)

    @property
    def amount(self) -> int:
        return sum(int(c) for c in self.coins)

    @property
    def wants_coin_change(self) -> bool:
        return True

    def coins_held(self) -> tuple[Coin, ...]:
        return tuple(self.coins)

    def settle(self, bank: CoinBank, price: int) -> None:
        bank.add(self.coins)  # 先入箱，找零才可能用上买家刚投进来的硬币
        self.coins.clear()

    def release(self) -> tuple[Coin, ...]:
        refund = tuple(self.coins)
        self.coins.clear()
        return refund


@dataclass(slots=True)
class CardTender:
    """刷卡付款：预授权一个额度，成交时只扣实际货价，其余自动释放。"""

    card_id: str
    authorized: int
    captured: int = 0
    voided: bool = False

    @property
    def amount(self) -> int:
        return self.authorized

    @property
    def wants_coin_change(self) -> bool:
        return False  # 多授权的部分原路释放，所以刷卡这条路径永远不会"找不开"

    def coins_held(self) -> tuple[Coin, ...]:
        return ()

    def settle(self, bank: CoinBank, price: int) -> None:
        self.captured = price

    def release(self) -> tuple[Coin, ...]:
        self.voided = True
        return ()


@dataclass(frozen=True, slots=True)
class PendingSale:
    """`select` 成功之后、货还没出来之前，这笔交易已经确定下来的全部信息。"""

    code: str
    item: Item
    change: tuple[Coin, ...]


@dataclass(frozen=True, slots=True)
class Transitioned:
    """一次成功的状态转移：自带前后状态、触发动作和当前余额。

    显示屏订阅这个事件就能刷新自己，不需要反过来去读机器的库存字典或托管硬币。
    """

    event: Event
    before: State
    after: State
    balance: int
    code: str | None = None


Observer = Callable[[Transitioned], None]


class VendingMachine:
    """一台自动售货机：货道、币箱、一次购买流程的状态机。

    不变式：
    1. 任意时刻最多有一笔交易在流程里（状态机本身就是这条约束的实现）。
    2. 任何失败路径都不改变库存和币箱——找零方案在货出来之前就算好，算不出来整笔拒绝，
       绝不出现"货出了、零钱没了"的半成品。
    3. `_pending` 在出货或退币之后立刻清空，`_tender` 同理；币箱里计数归零的面额会被删掉。
    4. 一把粗锁保护"查状态→改状态"这段读-改-写。粒度粗是对的：一台机器只有一个出货口，
       这里本来就没有并行度可言，细化锁只会换来死锁风险。
    """

    def __init__(self, slots: Mapping[str, Slot], bank: CoinBank,
                 change_maker: ChangeMaker = exact_change) -> None:
        self._slots = dict(slots)
        self._bank = bank
        self._change_maker = change_maker
        self._state = State.IDLE
        self._tender: Tender | None = None
        self._pending: PendingSale | None = None
        self._change_ready: tuple[Coin, ...] = ()
        self._lock = threading.Lock()
        self._observers: list[Observer] = []

    @property
    def state(self) -> State:
        return self._state

    @property
    def prompt(self) -> str:
        return self._state.prompt

    @property
    def balance(self) -> int:
        """当前这笔交易可用的金额（分）。没有交易在进行时是 0。"""
        return self._tender.amount if self._tender is not None else 0

    def stock(self) -> Mapping[str, int]:
        """各货道剩余件数的只读快照；货道字典本身不交出去。"""
        with self._lock:
            return MappingProxyType({code: slot.quantity for code, slot in self._slots.items()})

    def catalog(self) -> Mapping[str, Item]:
        with self._lock:
            return MappingProxyType({code: slot.item for code, slot in self._slots.items()})

    def bank_counts(self) -> Mapping[Coin, int]:
        return self._bank.counts()

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def insert_coin(self, coin: Coin) -> int:
        """投币。返回投币后的可用余额。"""
        with self._lock:
            nxt = self._next(Event.PAY)
            if self._tender is None:
                self._tender = CoinTender()
            if not isinstance(self._tender, CoinTender):
                raise IllegalTransitionError("card payment in progress; cannot mix coins")
            self._tender.coins.append(coin)
            event = self._enter(nxt, Event.PAY)
        self._notify(event)
        return event.balance

    def swipe_card(self, card_id: str, authorized: int) -> int:
        """刷卡：预授权一个额度。走的是和投币完全相同的 `PAY` 转移。"""
        with self._lock:
            nxt = self._next(Event.PAY)
            if self._tender is not None:
                raise IllegalTransitionError("a payment is already in progress")
            self._tender = CardTender(card_id=card_id, authorized=authorized)
            event = self._enter(nxt, Event.PAY)
        self._notify(event)
        return event.balance

    def select(self, code: str) -> Item:
        """选货。四道守卫全部通过才进入出货状态；任何一道没过，状态和钱都原地不动。"""
        with self._lock:
            nxt = self._next(Event.SELECT)
            assert self._tender is not None  # COIN_INSERTED 状态下必然有一笔付款
            slot = self._slots.get(code)
            if slot is None:
                raise InvalidSelectionError(f"no such slot {code!r}")
            if slot.quantity <= 0:
                raise OutOfStockError(f"slot {code!r} ({slot.item.name}) is sold out")
            if self._tender.amount < slot.item.price:
                raise InsufficientFundsError(
                    f"{slot.item.name} costs {slot.item.price}, balance is {self._tender.amount}")
            change = self._plan_change(slot.item.price)
            self._pending = PendingSale(code=code, item=slot.item, change=change)
            event = self._enter(nxt, Event.SELECT, code=code)
        self._notify(event)
        return slot.item

    def dispense(self) -> Item:
        """出货：扣库存、把托管的钱收进币箱、把找零从币箱里取出来放到出币口。"""
        with self._lock:
            nxt = self._next(Event.DISPENSE)
            assert self._pending is not None and self._tender is not None
            sale, tender = self._pending, self._tender
            self._slots[sale.code].quantity -= 1
            tender.settle(self._bank, sale.item.price)
            self._bank.take(sale.change)
            self._change_ready = sale.change
            self._pending = None
            self._tender = None
            event = self._enter(nxt, Event.DISPENSE, code=sale.code)
        self._notify(event)
        return sale.item

    def collect_change(self) -> tuple[Coin, ...]:
        """取走出币口的找零，机器回到待机。没有找零时返回空元组，流程一样走完。"""
        with self._lock:
            nxt = self._next(Event.COLLECT)
            change, self._change_ready = self._change_ready, ()
            event = self._enter(nxt, Event.COLLECT)
        self._notify(event)
        return change

    def refund(self) -> tuple[Coin, ...]:
        """退币：把托管的硬币原样退回（刷卡则撤销授权）。出货开始之后就不再允许。"""
        with self._lock:
            nxt = self._next(Event.REFUND)
            assert self._tender is not None
            refund = self._tender.release()
            self._tender = None
            self._pending = None
            event = self._enter(nxt, Event.REFUND)
        self._notify(event)
        return refund

    def restock(self, code: str, quantity: int) -> None:
        """补货。只在待机且没有钱被托管时允许——这是一道守卫，不是一个新状态。"""
        with self._lock:
            self._require_idle("restock")
            slot = self._slots.get(code)
            if slot is None:
                raise InvalidSelectionError(f"no such slot {code!r}")
            slot.quantity += quantity

    def load_coins(self, counts: Mapping[Coin, int]) -> None:
        """给币箱补硬币，通常是为了让机器重新找得开零钱。"""
        with self._lock:
            self._require_idle("load coins")
            for coin, n in counts.items():
                self._bank.add([coin] * n)

    def _require_idle(self, action: str) -> None:
        if self._state is not State.IDLE or self._tender is not None:
            raise IllegalTransitionError(f"cannot {action} mid-transaction: {self._state.prompt}")

    def _next(self, event: Event) -> State:
        """查转移表。表里没有就是非法动作，报错里顺带告诉买家机器正在等什么。"""
        nxt = TRANSITIONS.get((self._state, event))
        if nxt is None:
            raise IllegalTransitionError(
                f"cannot {event.value} while {self._state.value}: {self._state.prompt}")
        return nxt

    def _plan_change(self, price: int) -> tuple[Coin, ...]:
        """在货出来之前算好找零；算不出来就整笔拒绝，绝不半成交。

        可用硬币是"币箱现有的 + 买家刚投进来的"——真实的机器就是用你刚投的硬币找零的。
        """
        assert self._tender is not None
        due = self._tender.amount - price
        if due <= 0 or not self._tender.wants_coin_change:
            return ()
        available = dict(self._bank.counts())
        for coin in self._tender.coins_held():
            available[coin] = available.get(coin, 0) + 1
        plan = self._change_maker(due, available)
        if plan is None:
            raise CannotMakeChangeError(f"cannot make {due} in change; insert exact money or refund")
        return plan

    def _enter(self, state: State, event: Event, code: str | None = None) -> Transitioned:
        before, self._state = self._state, state
        return Transitioned(event=event, before=before, after=state, balance=self.balance, code=code)

    def _notify(self, event: Transitioned) -> None:
        """在锁外通知：一个慢订阅者不该把下一个买家挡在机器前面。"""
        for observer in self._observers:
            observer(event)


if __name__ == "__main__":
    machine = VendingMachine(
        slots={"A1": Slot(Item("可乐", 75), 2), "A2": Slot(Item("薯片", 120), 1)},
        bank=CoinBank({Coin.QUARTER: 1, Coin.DIME: 3}))
    machine.subscribe(lambda e: print(f"  {e.before.value} --{e.event.value}--> {e.after.value}"))
    machine.insert_coin(Coin.DOLLAR)
    print("选货:", machine.select("A1").name)
    print("出货:", machine.dispense().name)
    print("找零:", [c.name for c in machine.collect_change()])
    print("币箱:", {c.name: n for c, n in machine.bank_counts().items()})
