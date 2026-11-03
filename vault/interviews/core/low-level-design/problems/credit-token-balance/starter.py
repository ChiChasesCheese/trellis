"""额度账本（Credit Token Balance）——起始模板。公开的类名、签名和异常与 `solution.py` 一致。"""

from __future__ import annotations

from datetime import datetime
from typing import NamedTuple


class LedgerError(Exception):
    """所有失败路径的公共基类。"""


class InsufficientCreditsError(LedgerError):
    """额度不够：这笔扣费，或者因它而扣不下的某笔已有扣费。"""


class ConflictError(LedgerError):
    """同一个 id 已经用不同的参数提交过。"""


class UnknownGrantError(LedgerError):
    pass


class UnknownChargeError(LedgerError):
    pass


class Allocation(NamedTuple):
    grant_id: str
    amount: int


class CreditLedger:
    """所有时间都由调用方通过 `at` 传入（带时区的 datetime）；账本不读系统时钟。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def grant(self, grant_id: str, amount: int, at: datetime, expires_at: datetime | None = None) -> None:
        """发放一个额度包：从 at 起（含）可用，到 expires_at 失效（不含）；None 永不过期。

        amount <= 0，或 expires_at <= at，抛 ValueError。
        第 2 关：同一个 grant_id 用完全相同的参数再次调用是幂等的（什么都不做）；参数不同抛 ConflictError。
        """
        raise NotImplementedError

    def charge(self, charge_id: str, amount: int, at: datetime) -> tuple[Allocation, ...]:
        """在时刻 at 扣 amount，从 at 时刻可用的额度包里扣：先到期的先扣，永不过期的最后；
        同一时刻到期的，先发放的先扣，再按 grant_id。一笔可以跨多个包，返回按扣减顺序排列的 (包, 数量)。

        - amount <= 0 抛 ValueError；额度不够抛 InsufficientCreditsError，账本原封不动，这个 charge_id 也不被记住。
        - 第 2 关：同一个 charge_id 用相同参数重试，返回和第一次相同的分配，不再扣第二次；参数不同抛 ConflictError。
        - 第 3 关：at 可以早于已经处理过的事件。账本的行为等同于所有事件按 (at, 额度包先于扣费, id) 排好序处理。
          接受迟到事件的条件是：重放后每一笔已接受的扣费仍然能全额扣下，否则抛 InsufficientCreditsError 并保持原样。
        """
        raise NotImplementedError

    def balance(self, at: datetime) -> int:
        """at 这一刻可用的额度：只算 at 及之前发生的事件，已经过期（expires_at <= at）的包不算。"""
        raise NotImplementedError

    def allocations(self, charge_id: str) -> tuple[Allocation, ...]:
        """第 3 关：这笔扣费按"所有事件按时间排好"的结果用了哪些包。迟到的事件可能改变分配，总额不变。
        不认识的 charge_id 抛 UnknownChargeError。"""
        raise NotImplementedError

    def revoke(self, grant_id: str, at: datetime) -> None:
        """第 4 关：从 at 起作废这个包剩余的额度（等价于把到期时间提前到 at；已经更早失效则什么都不做）。

        不认识抛 UnknownGrantError；at <= 发放时间抛 ValueError；会让某笔已有扣费凑不够则抛
        InsufficientCreditsError 并保持原样。已经扣掉的不追回。
        """
        raise NotImplementedError
