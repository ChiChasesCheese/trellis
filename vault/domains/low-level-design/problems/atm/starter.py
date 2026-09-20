"""ATM 取款机——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的地方一个个填上，就是一份完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/atm -q
"""

from __future__ import annotations

import math
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Protocol

YUAN = 100


class Note(IntEnum):
    TEN = 10 * YUAN
    TWENTY = 20 * YUAN
    FIFTY = 50 * YUAN
    HUNDRED = 100 * YUAN


NOTE_STEP = math.gcd(*(int(n) for n in Note))
MAX_NOTES_PER_DISPENSE = 40


class SessionState(Enum):
    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    AUTHENTICATED = "authenticated"
    DISPENSING = "dispensing"


class Action(Enum):
    INSERT_CARD = "insert_card"
    ENTER_PIN = "enter_pin"
    PIN_REJECTED = "_pin_rejected"
    RETAIN_CARD = "_retain_card"
    BALANCE = "balance"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    COLLECT_CASH = "collect_cash"
    EJECT = "eject_card"


# 授权表：会话状态机的全部合法转移，表里没有的组合一律非法。补全这张表。
TRANSITIONS: dict[tuple[SessionState, Action], SessionState] = {}


class ATMError(Exception):
    """本设计全部失败路径的公共基类。"""


class IllegalActionError(ATMError):
    """这个动作在当前会话状态下不合法。"""


class WrongPinError(ATMError):
    """密码错误。卡不存在时报的也是它。"""

    def __init__(self, remaining: int) -> None:
        super().__init__(f"wrong PIN, {remaining} attempt(s) left")
        self.remaining = remaining


class CardRetainedError(ATMError):
    """卡被机器吞掉了。"""


class InvalidAmountError(ATMError):
    """金额不是正数，或者钞票张数为负。"""


class InsufficientFundsError(ATMError):
    """账户余额不足。"""


class DispenseFailure(Enum):
    NOT_REPRESENTABLE = "amount is not a multiple of the smallest note"
    NOT_IN_STOCK = "the cassettes cannot make this amount"
    TOO_MANY_NOTES = "the amount needs more notes than the feeder can move"


class AmountNotDispensableError(ATMError):
    """这笔金额吐不出来；`reason` 说明是哪一种。"""

    def __init__(self, amount: int, reason: DispenseFailure) -> None:
        super().__init__(f"cannot dispense {amount}: {reason.value}")
        self.amount = amount
        self.reason = reason


class TxKind(Enum):
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    BALANCE = "balance"
    REVERSAL = "reversal"
    PIN_FAILURE = "pin_failure"
    CARD_RETAINED = "card_retained"


class TxStatus(Enum):
    OK = "ok"
    DECLINED = "declined"
    REVERSED = "reversed"


@dataclass(frozen=True, slots=True)
class JournalEntry:
    """一条流水，不可变、只增不改；同时就是发给订阅者的事件。"""

    ref: str
    at: datetime
    kind: TxKind
    status: TxStatus
    amount: int
    card_tail: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class Reconciliation:
    """一次对账的结果。"""

    loaded: int
    in_cassette: int
    on_tray: int
    in_reject_bin: int
    collected: int
    deposited: int

    @property
    def balanced(self) -> bool:
        """钞票守恒：装钞总额 = 钞箱 + 出钞口 + 回收箱 + 已取走。"""
        raise NotImplementedError


class Cassette:
    """一组钞箱。不变式：张数降到 0 的面额要从字典里删掉。"""

    def __init__(self, counts: Mapping[Note, int] | None = None) -> None:
        raise NotImplementedError

    def counts(self) -> Mapping[Note, int]:
        """一份只读快照。"""
        raise NotImplementedError

    @property
    def total(self) -> int:
        """箱内金额合计（分）。"""
        raise NotImplementedError

    @property
    def note_count(self) -> int:
        """箱内张数。测试断言的是它，而不是内部字典。"""
        raise NotImplementedError

    def load(self, counts: Mapping[Note, int]) -> None:
        """装钞，也用于把留好的钞票原样放回。"""
        raise NotImplementedError

    def take(self, plan: Mapping[Note, int]) -> None:
        """按方案取走钞票：先整体校验再整体扣减。"""
        raise NotImplementedError


NoteSelector = Callable[[int, Mapping[Note, int]], "dict[Note, int] | None"]


def fewest_notes(amount: int, available: Mapping[Note, int]) -> dict[Note, int] | None:
    """有界背包 DP：在库存允许的凑法里选张数最少的一种，凑不出返回 `None`。"""
    raise NotImplementedError


@dataclass(slots=True)
class Account:
    """一个账户。不变式：余额不为负，当日累计取现不超过限额。"""

    account_id: str
    balance: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    def debit(self, amount: int) -> int:
        """扣款；不变式过了才动余额。"""
        raise NotImplementedError

    def credit(self, amount: int) -> int:
        """贷记：存款走它，冲正也走它。"""
        raise NotImplementedError


class BankNetwork(Protocol):
    """ATM 能向网络另一端提出的全部问题。"""

    def authenticate(self, card_number: str, pin: str) -> str: ...

    def balance(self, account_id: str) -> int: ...

    def withdraw(self, account_id: str, amount: int, ref: str) -> int: ...

    def deposit(self, account_id: str, amount: int, ref: str) -> int: ...

    def reverse(self, account_id: str, amount: int, ref: str) -> int: ...


class LocalBank:
    """发卡行：管账户、管卡、管密码错误次数。"""

    def __init__(self, bank_id: str = "BANK", max_pin_attempts: int = 3) -> None:
        raise NotImplementedError

    def open_account(self, account_id: str, balance: int = 0) -> Account:
        raise NotImplementedError

    def issue_card(self, card_number: str, account_id: str, pin: str) -> None:
        raise NotImplementedError

    def account(self, account_id: str) -> Account:
        raise NotImplementedError

    def authenticate(self, card_number: str, pin: str) -> str:
        """验密码。卡不存在、密码错、卡已作废，必须抛同一个异常。"""
        raise NotImplementedError

    def balance(self, account_id: str) -> int:
        raise NotImplementedError

    def withdraw(self, account_id: str, amount: int, ref: str) -> int:
        raise NotImplementedError

    def deposit(self, account_id: str, amount: int, ref: str) -> int:
        raise NotImplementedError

    def reverse(self, account_id: str, amount: int, ref: str) -> int:
        raise NotImplementedError


class ATM:
    """一台取款机：会话状态机、钞箱、流水，以及一条通往银行的网络。"""

    def __init__(self, network: BankNetwork, cassette: Cassette, *,
                 selector: NoteSelector = fewest_notes,
                 clock: Callable[[], datetime] = datetime.now,
                 machine_id: str = "ATM-01") -> None:
        raise NotImplementedError

    @property
    def state(self) -> SessionState:
        raise NotImplementedError

    def cassette_counts(self) -> Mapping[Note, int]:
        raise NotImplementedError

    def tray_counts(self) -> Mapping[Note, int]:
        """出钞口上正等着客户拿走的钞票。"""
        raise NotImplementedError

    def journal(self) -> tuple[JournalEntry, ...]:
        raise NotImplementedError

    def cash_up(self) -> Reconciliation:
        """对账：把机器里现在的钱和装钞总额摆在一起。"""
        raise NotImplementedError

    def insert_card(self, card_number: str) -> SessionState:
        """插卡；这里什么都不验证。"""
        raise NotImplementedError

    def enter_pin(self, pin: str) -> SessionState:
        """输密码；最后一次错由银行作废、由机器吞卡。"""
        raise NotImplementedError

    def eject_card(self) -> SessionState:
        """退卡，会话结束。"""
        raise NotImplementedError

    def withdraw(self, amount: int) -> Mapping[Note, int]:
        """取款：先留钞、再扣账、最后把钞票放到出钞口。"""
        raise NotImplementedError

    def collect_cash(self) -> Mapping[Note, int]:
        """客户取走现金。"""
        raise NotImplementedError

    def retract_uncollected(self) -> Mapping[Note, int]:
        """超时无人取走：钞票进回收箱，并向银行发一笔冲正。"""
        raise NotImplementedError

    def balance(self) -> int:
        """查余额，永远从网络问来。"""
        raise NotImplementedError

    def deposit(self, notes: Mapping[Note, int]) -> int:
        """存款：钞票进存钞箱，账户入账。"""
        raise NotImplementedError
