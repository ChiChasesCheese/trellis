"""银行账户系统（Bank Account System）——起始模板。

公开的类名、方法签名、`dataclass`、`Enum` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/bank-account -q
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BankError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownAccountError(BankError):
    """账户不存在，或者曾经存在但已经被合并掉、不再接受新操作。"""


class DuplicateAccountError(BankError):
    """这个账户 id 曾经被用过（哪怕现在已经合并掉了），不能再开一个同名账户。"""


class InvalidAmountError(BankError):
    """金额不是正数。"""


class SameAccountError(BankError):
    """转账或合并的两个账户 id 其实是同一个。"""


class InsufficientFundsError(BankError):
    """余额不足以覆盖这笔转出或定时支付。"""

    def __init__(self, account_id: str, available: int, requested: int) -> None:
        super().__init__(f"账户 {account_id} 余额 {available} 不足以支付 {requested}")
        self.account_id = account_id
        self.shortfall = requested - available


class UnknownPaymentError(BankError):
    """定时支付 id 不存在。"""


class InvalidPaymentStateError(BankError):
    """这笔定时支付已经结算或已经取消，不能再取消一次。"""


class NonMonotonicTimestampError(BankError):
    """这次调用的时间戳比上一次调用还早。"""


class EventKind(Enum):
    OPENED = "opened"
    DEPOSIT = "deposit"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    PAYMENT_OUT = "payment_out"
    PAYMENT_REFUND = "payment_refund"
    CASHBACK_IN = "cashback_in"
    MERGE_IN = "merge_in"


class PaymentStatus(Enum):
    IN_PROGRESS = "in_progress"
    CASHBACK_RECEIVED = "cashback_received"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Event:
    """一条不可变的账户历史记录：`account_id` 在时间戳 `at` 变化了 `delta`。"""

    seq: int
    kind: EventKind
    account_id: str
    at: int
    delta: int


@dataclass(slots=True)
class Payment:
    """一笔定时支付：立即扣款，`matures_at` 时刻返现。"""

    id: str
    account_id: str
    amount: int
    scheduled_at: int
    matures_at: int
    status: PaymentStatus = PaymentStatus.IN_PROGRESS


class EventLog:
    """账户历史的唯一真源：一张按账户 id 分组、只增不减的事件表。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def append(self, account_id: str, kind: EventKind, at: int, delta: int) -> Event:
        raise NotImplementedError

    def balance(self, account_id: str, at: int) -> int:
        raise NotImplementedError

    def outgoing_total(self, account_id: str, at: int) -> int:
        raise NotImplementedError

    def entries(self, account_id: str) -> tuple[Event, ...]:
        raise NotImplementedError


class Bank:
    """开户、存款、转账、按支出排行、定时支付带返现、合并账户的唯一入口。"""

    def __init__(self, cashback_rate: float = 0.02) -> None:
        raise NotImplementedError

    @property
    def payment_count(self) -> int:
        raise NotImplementedError

    @property
    def pending_payment_count(self) -> int:
        raise NotImplementedError

    def history(self, account_id: str) -> tuple[Event, ...]:
        raise NotImplementedError

    def create_account(self, timestamp: int, account_id: str) -> None:
        raise NotImplementedError

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int:
        raise NotImplementedError

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int:
        raise NotImplementedError

    def get_balance(self, timestamp: int, account_id: str) -> int:
        raise NotImplementedError

    def top_spenders(self, timestamp: int, n: int) -> list[tuple[str, int]]:
        raise NotImplementedError

    def schedule_payment(self, timestamp: int, account_id: str, amount: int,
                          cashback_delay: int) -> str:
        raise NotImplementedError

    def cancel_payment(self, timestamp: int, payment_id: str) -> None:
        raise NotImplementedError

    def payment_status(self, timestamp: int, payment_id: str) -> PaymentStatus:
        raise NotImplementedError

    def merge_accounts(self, timestamp: int, survivor_id: str, absorbed_id: str) -> None:
        raise NotImplementedError
