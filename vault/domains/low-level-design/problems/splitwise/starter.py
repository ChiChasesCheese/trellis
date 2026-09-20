"""分账（Splitwise）——练习骨架：公开 API 与参考解完全一致，方法体留给你补全。

第 1 关：`User`/`Group`/`Expense`/`ExpenseManager.add_expense`，均分，`debts()` 回答谁欠谁。
第 2 关：四种 `Split`，各自校验自己的输入，份额之和必须精确等于总额。
第 3 关：`simplify_debts` 用两个堆做贪心化简。
第 4 关：`settle`、`ActivityLog` 通过 `subscribe` 接入，不改前面任何一个类。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction


class SplitwiseError(Exception):
    """本设计里所有失败路径的公共基类，方便调用方一次性捕获。"""


class SplitError(SplitwiseError):
    """拆分参数本身不合法：参与人对不上、金额或比例之和不对。"""


class UnknownUserError(SplitwiseError):
    """引用了一个系统里不存在的用户。"""


class SettlementError(SplitwiseError):
    """还款请求本身不合法。"""


@dataclass(frozen=True, slots=True)
class User:
    """一个用户；`id` 是身份，`name` 只用于展示，不参与相等性判断。"""

    id: str
    name: str = field(compare=False)


class Group:
    """一个记账小组：有名字，成员会随时间增减；对外只给不可变快照。"""

    def __init__(self, id: str, name: str, members: Iterable[User] = ()) -> None:
        raise NotImplementedError

    @property
    def members(self) -> tuple[User, ...]:
        raise NotImplementedError

    def add_member(self, user: User) -> None:
        raise NotImplementedError


def _largest_remainder(exact: Mapping[User, Fraction], amount: int, order: Sequence[User]) -> dict[User, int]:
    """最大余数法：向下取整，余下的几个最小货币单位按小数部分从大到小分配，
    小数部分相同时按 `order` 的先后顺序——要可复现、可解释。"""
    raise NotImplementedError


class Split(ABC):
    """一种拆分算法：把总额分给参与人，返回恰好加总等于 `amount` 的整数分账。"""

    @abstractmethod
    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        """算出每个参与人该付多少；输入不合法时抛 `SplitError`。"""

    @staticmethod
    def _proportional(amount: int, participants: Sequence[User],
                      weights: Mapping[User, Fraction]) -> dict[User, int]:
        """按权重分摊并抹平取整余数；均分/百分比/份额三种拆分共享这一段。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class EqualSplit(Split):
    """人均一份。"""

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ExactSplit(Split):
    """每个人该付多少由调用方直接给定；之和必须等于总额。"""

    amounts: Mapping[User, int]

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class PercentageSplit(Split):
    """按百分比拆分；百分比之和必须恰好是 100，构造时就检查。"""

    percentages: Mapping[User, Decimal]

    def __post_init__(self) -> None:
        raise NotImplementedError

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ShareSplit(Split):
    """按份额（正整数权重）拆分；份额必须为正，构造时就检查。"""

    shares: Mapping[User, int]

    def __post_init__(self) -> None:
        raise NotImplementedError

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Expense:
    """一笔已经记录的开销；`shares` 在构造时算好并冻结，之后不会再变。"""

    id: str
    payer: User
    amount: int
    description: str
    participants: tuple[User, ...]
    split: Split
    created_at: datetime
    group: Group | None = None
    shares: Mapping[User, int] = field(init=False)

    def __post_init__(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Debt:
    """一对用户之间当前的净欠款：`debtor` 欠 `creditor` `amount`（恒为正）。"""

    debtor: User
    creditor: User
    amount: int


def _canonical(a: User, b: User) -> tuple[User, User]:
    """把一对用户排成规范顺序，使 (A, B) 和 (B, A) 落在账本的同一行。"""
    raise NotImplementedError


class Ledger:
    """“谁欠谁多少”的唯一真源：每一对用户一行净额，归零的行立刻删掉。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def row_count(self) -> int:
        """账本里还剩多少行。结清的一对用户必须让这个数变小——把"容器会缩小"这条
        不变量暴露成可以断言的东西，而不是让测试去读内部字典。
        """
        return len(self._net)

    def record_debt(self, debtor: User, creditor: User, delta: int) -> None:
        """`debtor` 对 `creditor` 的欠款增加 `delta`（可为负，表示还款）。"""
        raise NotImplementedError

    def balance_between(self, a: User, b: User) -> int:
        """`a` 净欠 `b` 多少；负数表示反过来 `b` 欠 `a`。"""
        raise NotImplementedError

    def debts(self) -> tuple[Debt, ...]:
        """所有非零欠款的一份快照。"""
        raise NotImplementedError

    def net_balance(self, user: User) -> int:
        """这个人当前净应收（正）或净应付（负）多少。"""
        raise NotImplementedError

    def net_balances(self, users: Iterable[User]) -> dict[User, int]:
        """一次遍历算出所有人的净额。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Payment:
    """债务化简之后的一笔结算建议：`payer` 应该付给 `payee` `amount`。"""

    payer: User
    payee: User
    amount: int


def simplify_debts(net_balances: Mapping[User, int]) -> list[Payment]:
    """贪心债务化简：最大应收方与最大应付方反复配对，两个堆各维护一端的最大值。
    保证不超过 n-1 笔；不保证是理论最优（那等价于 NP-hard 的子集和问题）。"""
    raise NotImplementedError


class SplitwiseEventKind(Enum):
    EXPENSE_ADDED = "expense_added"
    SETTLED = "settled"


@dataclass(frozen=True, slots=True)
class SplitwiseEvent:
    """一次发生的事；订阅者从事件本身就能知道发生了什么。"""

    kind: SplitwiseEventKind
    at: datetime
    summary: str
    users: tuple[User, ...]
    amount: int


SplitwiseObserver = Callable[[SplitwiseEvent], None]


class ActivityLog:
    """订阅事件流、按时间顺序保留一份活动记录；本身可调用，可直接当观察者传入。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def __call__(self, event: SplitwiseEvent) -> None:
        raise NotImplementedError

    def recent(self, n: int = 10) -> tuple[SplitwiseEvent, ...]:
        """最近 n 条，最新的排最前；只给一份快照。"""
        raise NotImplementedError


class ExpenseManager:
    """记一笔账、结一次款、问一句“谁欠谁多少”的入口；不是 Singleton。"""

    def __init__(self, clock: Callable[[], datetime]) -> None:
        raise NotImplementedError

    @property
    def expense_count(self) -> int:
        """已记录的开销笔数；在锁内数好再交出去，不把内部列表暴露给调用方。"""
        raise NotImplementedError

    def add_user(self, user: User) -> None:
        raise NotImplementedError

    def create_group(self, id: str, name: str, members: Iterable[User] = ()) -> Group:
        raise NotImplementedError

    def subscribe(self, observer: SplitwiseObserver) -> None:
        """挂一个“记了新账/结了一次款”的订阅者。"""
        raise NotImplementedError

    def add_expense(self, payer: User, amount: int, description: str,
                    participants: Sequence[User], split: Split,
                    group: Group | None = None) -> Expense:
        """记一笔账：`payer` 垫付 `amount`，按 `split` 分给 `participants`。"""
        raise NotImplementedError

    def settle(self, payer: User, payee: User, amount: int) -> None:
        """`payer` 向 `payee` 还了 `amount`。"""
        raise NotImplementedError

    def balance_between(self, a: User, b: User) -> int:
        raise NotImplementedError

    def debts(self) -> tuple[Debt, ...]:
        """当前所有非零欠款的一份快照。"""
        raise NotImplementedError

    def net_balance(self, user: User) -> int:
        raise NotImplementedError

    def simplify(self) -> list[Payment]:
        """把当前所有欠款化简成尽量少的一批转账；不修改账本本身。"""
        raise NotImplementedError
