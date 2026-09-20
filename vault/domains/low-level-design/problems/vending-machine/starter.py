"""自动售货机（Vending Machine）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的地方一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/vending-machine -q
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Protocol


class Coin(IntEnum):
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100


class State(Enum):
    IDLE = "idle"
    COIN_INSERTED = "coin_inserted"
    DISPENSING = "dispensing"
    RETURNING_CHANGE = "returning_change"

    @property
    def prompt(self) -> str:
        raise NotImplementedError


class Event(Enum):
    PAY = "pay"
    SELECT = "select"
    DISPENSE = "dispense"
    COLLECT = "collect"
    REFUND = "refund"


# 状态机的全部合法转移，表里没有的组合一律非法。补全这张表。
TRANSITIONS: dict[tuple[State, Event], State] = {}


class VendingMachineError(Exception):
    """本设计全部失败路径的公共基类。"""


class IllegalTransitionError(VendingMachineError):
    """这个动作在当前状态下不合法。"""


class InvalidSelectionError(VendingMachineError):
    """没有这个货道编号。"""


class OutOfStockError(VendingMachineError):
    """这个货道空了。"""


class InsufficientFundsError(VendingMachineError):
    """已投金额不够买这件商品。"""


class CannotMakeChangeError(VendingMachineError):
    """币箱凑不出该找的零钱。"""


@dataclass(frozen=True, slots=True)
class Item:
    name: str
    price: int


@dataclass(slots=True)
class Slot:
    item: Item
    quantity: int


class CoinBank:
    """币箱：每种面额各存了多少枚；计数降到 0 的面额必须从字典里删掉。"""

    def __init__(self, counts: Mapping[Coin, int] | None = None) -> None:
        self._counts: dict[Coin, int] = {c: n for c, n in (counts or {}).items() if n > 0}

    def counts(self) -> Mapping[Coin, int]:
        raise NotImplementedError

    @property
    def total(self) -> int:
        raise NotImplementedError

    def add(self, coins: Iterable[Coin]) -> None:
        raise NotImplementedError

    def take(self, coins: Iterable[Coin]) -> None:
        raise NotImplementedError


ChangeMaker = Callable[[int, Mapping[Coin, int]], "tuple[Coin, ...] | None"]


def greedy_change(amount: int, available: Mapping[Coin, int]) -> tuple[Coin, ...] | None:
    """贪心：从大面额往小拿，能拿几枚拿几枚。"""
    raise NotImplementedError


def exact_change(amount: int, available: Mapping[Coin, int]) -> tuple[Coin, ...] | None:
    """有界背包 DP：只要存在一种凑法就一定找得到。"""
    raise NotImplementedError


class Tender(Protocol):
    """一笔尚未结清的付款。"""

    @property
    def amount(self) -> int: ...

    @property
    def wants_coin_change(self) -> bool: ...

    def coins_held(self) -> tuple[Coin, ...]: ...

    def settle(self, bank: CoinBank, price: int) -> None: ...

    def release(self) -> tuple[Coin, ...]: ...


@dataclass(slots=True)
class CoinTender:
    """现金付款：投进来的硬币原样托管。"""

    coins: list[Coin] = field(default_factory=list)

    @property
    def amount(self) -> int:
        raise NotImplementedError

    @property
    def wants_coin_change(self) -> bool:
        raise NotImplementedError

    def coins_held(self) -> tuple[Coin, ...]:
        raise NotImplementedError

    def settle(self, bank: CoinBank, price: int) -> None:
        raise NotImplementedError

    def release(self) -> tuple[Coin, ...]:
        raise NotImplementedError


@dataclass(slots=True)
class CardTender:
    """刷卡付款：预授权一个额度，成交时只扣实际货价。"""

    card_id: str
    authorized: int
    captured: int = 0
    voided: bool = False

    @property
    def amount(self) -> int:
        raise NotImplementedError

    @property
    def wants_coin_change(self) -> bool:
        raise NotImplementedError

    def coins_held(self) -> tuple[Coin, ...]:
        raise NotImplementedError

    def settle(self, bank: CoinBank, price: int) -> None:
        raise NotImplementedError

    def release(self) -> tuple[Coin, ...]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class PendingSale:
    code: str
    item: Item
    change: tuple[Coin, ...]


@dataclass(frozen=True, slots=True)
class Transitioned:
    event: Event
    before: State
    after: State
    balance: int
    code: str | None = None


Observer = Callable[[Transitioned], None]


class VendingMachine:
    """一台自动售货机：货道、币箱、一次购买流程的状态机。"""

    def __init__(self, slots: Mapping[str, Slot], bank: CoinBank,
                 change_maker: ChangeMaker = exact_change) -> None:
        self._slots = dict(slots)
        self._bank = bank
        self._change_maker = change_maker

    @property
    def state(self) -> State:
        raise NotImplementedError

    @property
    def prompt(self) -> str:
        raise NotImplementedError

    @property
    def balance(self) -> int:
        raise NotImplementedError

    def stock(self) -> Mapping[str, int]:
        raise NotImplementedError

    def catalog(self) -> Mapping[str, Item]:
        raise NotImplementedError

    def bank_counts(self) -> Mapping[Coin, int]:
        raise NotImplementedError

    def subscribe(self, observer: Observer) -> None:
        raise NotImplementedError

    def insert_coin(self, coin: Coin) -> int:
        """投币。返回投币后的可用余额。"""
        raise NotImplementedError

    def swipe_card(self, card_id: str, authorized: int) -> int:
        """刷卡：预授权一个额度，走和投币相同的 `PAY` 转移。"""
        raise NotImplementedError

    def select(self, code: str) -> Item:
        """选货。守卫全部通过才进入出货状态；任何一道没过，状态和钱都原地不动。"""
        raise NotImplementedError

    def dispense(self) -> Item:
        """出货：扣库存、收钱、把找零放到出币口。"""
        raise NotImplementedError

    def collect_change(self) -> tuple[Coin, ...]:
        """取走出币口的找零，机器回到待机。"""
        raise NotImplementedError

    def refund(self) -> tuple[Coin, ...]:
        """退币：把托管的硬币原样退回。"""
        raise NotImplementedError

    def restock(self, code: str, quantity: int) -> None:
        """补货。只在待机且没有钱被托管时允许。"""
        raise NotImplementedError

    def load_coins(self, counts: Mapping[Coin, int]) -> None:
        """给币箱补硬币。"""
        raise NotImplementedError
