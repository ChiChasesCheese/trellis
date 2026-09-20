"""数字钱包（Digital Wallet）——起始模板。

公开的类名、方法签名、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/digital-wallet -q
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime


class WalletError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownAccountError(WalletError):
    """引用了一个不存在的账户，或者试图直接操作保留的系统账户。"""


class InvalidAmountError(WalletError):
    """金额不是正数。"""


class InsufficientFundsError(WalletError):
    """账户余额不足以覆盖这笔转出，操作被整体拒绝，两边余额都不变。"""

    def __init__(self, account_id: str, available: int, requested: int) -> None:
        super().__init__(f"账户 {account_id} 余额 {available} 不足以转出 {requested}")
        self.account_id = account_id
        self.shortfall = requested - available


class SameAccountTransferError(WalletError):
    """转账的转入转出是同一个账户。"""


class IdempotencyConflictError(WalletError):
    """同一个 `client_key` 被用在了两笔参数不同的移动上。"""


class LedgerIntegrityError(WalletError):
    """一次记账的两条分录没有相加为零。"""


EXTERNAL_ACCOUNT_ID = "EXTERNAL"


@dataclass(slots=True)
class Account:
    """一个账户：缓存余额，加一把保护它的独立锁。"""

    id: str
    balance: int = 0
    reserved: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    """一条记账分录：某个账户在某次移动里变化了多少。"""

    id: str
    transfer_id: str
    account_id: str
    delta: int
    memo: str
    at: datetime


class Ledger:
    """“钱从哪笔移动来”的唯一真源：一张只增不减的分录表。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def entry_count(self) -> int:
        raise NotImplementedError

    def record_pair(self, transfer_id: str, debit: tuple[str, int], credit: tuple[str, int],
                     memo: str, at: datetime) -> tuple[LedgerEntry, LedgerEntry]:
        raise NotImplementedError

    def derived_balance(self, account_id: str) -> int:
        raise NotImplementedError

    def total_delta(self) -> int:
        raise NotImplementedError

    def count_for(self, account_id: str) -> int:
        raise NotImplementedError

    def page(self, account_id: str, offset: int, limit: int) -> tuple[LedgerEntry, ...]:
        raise NotImplementedError

    def entries_for_transfer(self, transfer_id: str) -> tuple[LedgerEntry, LedgerEntry]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TransferReceipt:
    """一次移动（充值/提现/转账）的回执；幂等重试返回的就是这同一个对象。"""

    transfer_id: str
    from_account: str
    to_account: str
    amount: int
    at: datetime
    client_key: str | None


class Wallet:
    """充值、提现、转账、查余额、查流水的唯一入口。"""

    def __init__(self, clock: Callable[[], datetime]) -> None:
        raise NotImplementedError

    def open_account(self, account_id: str, opening_balance: int = 0) -> None:
        raise NotImplementedError

    def top_up(self, account_id: str, amount: int, client_key: str | None = None) -> TransferReceipt:
        raise NotImplementedError

    def withdraw(self, account_id: str, amount: int, client_key: str | None = None) -> TransferReceipt:
        raise NotImplementedError

    def transfer(self, from_id: str, to_id: str, amount: int,
                 client_key: str | None = None) -> TransferReceipt:
        raise NotImplementedError

    def balance(self, account_id: str) -> int:
        raise NotImplementedError

    def history(self, account_id: str, offset: int = 0, limit: int = 20) -> tuple[LedgerEntry, ...]:
        raise NotImplementedError

    def history_count(self, account_id: str) -> int:
        raise NotImplementedError

    def transfer_entries(self, transfer_id: str) -> tuple[LedgerEntry, LedgerEntry]:
        raise NotImplementedError

    def derived_balance(self, account_id: str) -> int:
        raise NotImplementedError

    @property
    def ledger_size(self) -> int:
        raise NotImplementedError

    def ledger_total(self) -> int:
        raise NotImplementedError

    def reconcile(self, account_id: str) -> bool:
        raise NotImplementedError

    def purge_idempotency_before(self, cutoff: datetime) -> int:
        raise NotImplementedError
