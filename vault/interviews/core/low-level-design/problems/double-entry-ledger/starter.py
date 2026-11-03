"""复式账本——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
from __future__ import annotations
import threading
from bisect import bisect_right
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, NamedTuple, TypeVar
F = TypeVar('F', bound=Callable[..., Any])

class Key(NamedTuple):
    """(账户, 币种)。仍然是 tuple，可以当字典键，但字段有名字，不用记 key[0] 是什么。"""
    account: str
    currency: str

class LedgerError(Exception):
    """账本所有失败路径的公共基类。"""

class InvalidEntry(LedgerError):
    """分录本身不合法：腿数不足、有零金额的腿、某个币种借贷不平，或冻结金额不是正数。"""

class ConflictError(LedgerError):
    """同一个 ID 带了不同的内容。"""

class UnknownEntry(LedgerError):
    """引用了不存在的分录或冻结。"""

class AlreadyReversed(LedgerError):
    """这条分录已经被另一条分录冲正过了。"""

class InsufficientFunds(LedgerError):
    """写入会让可用余额低于该账户的下限。"""

@dataclass(frozen=True, slots=True)
class Posting:
    account: str
    currency: str
    amount: int

@dataclass(frozen=True, slots=True)
class Entry:
    id: str
    postings: tuple[Posting, ...]
    reverses: str | None = None

@dataclass(frozen=True, slots=True)
class StatementLine:
    seq: int
    entry_id: str
    amount: int
    balance_after: int

class Ledger:

    def __init__(self) -> None:
        raise NotImplementedError

    def post(self, entry: Entry, release_hold: str | None=None) -> int:
        """写入一条分录，返回序号（从 1 开始）；同 ID 同内容重复提交返回原序号，什么也不改。

同 ID 不同内容抛 ConflictError；分录不合法抛 InvalidEntry；失败的调用不留任何痕迹。
`reverses` 指向不存在的分录抛 UnknownEntry，指向已被冲正的分录抛 AlreadyReversed。
账户设了下限（第 2 关）时，写入后"余额减冻结"低于下限抛 InsufficientFunds；
`release_hold` 非空表示在同一个原子步骤里先释放这笔冻结再写入（第 3 关）。"""
        raise NotImplementedError

    def balance(self, account: str, currency: str) -> int:
        """账户在某币种上的当前账面余额；从没出现过的账户是 0。"""
        raise NotImplementedError

    def total(self, currency: str) -> int:
        """某币种全部账户余额之和；账本正确时恒为 0。"""
        raise NotImplementedError

    def reverse(self, entry_id: str, new_id: str) -> int:
        """把一条分录的每条腿取反，作为新分录 `new_id` 写入，返回新序号；原分录原样保留。

原分录不存在抛 UnknownEntry；已被另一条分录冲正抛 AlreadyReversed；
用同一个 `new_id` 重试是幂等的，返回第一次的序号。"""
        raise NotImplementedError

    def journal(self) -> tuple[Entry, ...]:
        """日志的只读快照，按序号排列。"""
        raise NotImplementedError

    def balance_at(self, account: str, currency: str, seq: int) -> int:
        """第 `seq` 条分录写入之后的余额：seq 小于 1 得 0，大于当前序号得当前余额。"""
        raise NotImplementedError

    def statement(self, account: str, currency: str, after_seq: int=0, limit: int=100) -> list[StatementLine]:
        """序号大于 `after_seq` 的对账单行（每条分录一行，金额是净影响），最多 `limit` 行。

拿最后一行的 `seq` 当下一页的 `after_seq` 就能翻页。`limit` 小于 1 抛 ValueError。"""
        raise NotImplementedError

    def set_floor(self, account: str, currency: str, floor: int) -> None:
        """给账户设余额下限（比如 0 表示不许透支）。只约束之后的写入，不追溯检查已有余额。"""
        raise NotImplementedError

    def available(self, account: str, currency: str) -> int:
        """可用余额 = 账面余额 - 冻结合计。"""
        raise NotImplementedError

    def hold(self, hold_id: str, account: str, currency: str, amount: int) -> None:
        """冻结一笔金额。金额必须是正数（InvalidEntry）；账户有下限且冻结后可用余额低于下限抛 InsufficientFunds。

同一个 `hold_id` 同参数重复调用是幂等的（即使已经释放过）；同 ID 不同参数抛 ConflictError。"""
        raise NotImplementedError

    def release(self, hold_id: str) -> None:
        """释放冻结。冻结不存在抛 UnknownEntry；已经释放过再调用是无操作。"""
        raise NotImplementedError

    def exchange(self, entry_id: str, account: str, from_currency: str, from_amount: int, to_currency: str, to_amount: int, fx_account: str='fx') -> int:
        """账户用 `from_amount` 的 `from_currency` 换入 `to_amount` 的 `to_currency`，返回序号。

写成一条四条腿的分录，经由 `fx_account` 中转，各币种分别平衡；账本本身不需要任何改动。
币种相同或金额不是正数抛 InvalidEntry。"""
        raise NotImplementedError
