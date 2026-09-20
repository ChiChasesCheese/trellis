"""分账（Splitwise）——多种拆分算法、净额账本与债务化简的参考实现。

核心思路：拆分（Split）携带自己的数据和校验规则，几种拆分之间又确实共享一段“取整＋
按最大余数法分配余数”的算法，因此写成一个带模板方法的抽象基类，而不是像停车场那题
里无状态的单方法策略那样用普通函数。账本（Ledger）只维护每一对用户之间的净额这一份
真源，一归零就把这一行删掉，永远不会无限增长。债务化简（simplify_debts）是一个不
依赖账本内部结构的纯函数：给净额、还最少的转账笔数，贪心保证不超过 n-1 笔，但不保证
理论最优——那等价于一个 NP-hard 的子集和问题。并发由 `ExpenseManager` 里的一把
`RLock` 兜住：一笔开销要连改好几行账本，这几行必须整体原子，读也要持锁；给订阅者
发通知则在锁外，事件自带全部信息，订阅者不需要回头翻账本。
"""

from __future__ import annotations

import heapq
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from itertools import count
from threading import RLock
from types import MappingProxyType


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
    """一个用户。`id` 是身份，参与相等性判断和哈希；`name` 只是展示用的名字，不参与
    比较——同一个 `id` 的两个 `User` 对象永远相等，哪怕其中一个的 `name` 字段拼错了。
    """

    id: str
    name: str = field(compare=False)


class Group:
    """一个记账小组：有名字，成员会随时间增减。

    成员只在这里维护一份内部列表，`members` 永远只给外部一份不可变快照（元组）——
    调用方拿到的 tuple 改不了小组的真实成员表，也不会在遍历途中因为别处的增删而变化。
    """

    def __init__(self, id: str, name: str, members: Iterable[User] = ()) -> None:
        self.id = id
        self.name = name
        self._members: list[User] = list(dict.fromkeys(members))

    @property
    def members(self) -> tuple[User, ...]:
        return tuple(self._members)

    def add_member(self, user: User) -> None:
        if user not in self._members:
            self._members.append(user)


def _largest_remainder(exact: Mapping[User, Fraction], amount: int, order: Sequence[User]) -> dict[User, int]:
    """最大余数法：先把每个人的精确份额向下取整，取整损失掉的那几个最小货币单位，
    按“小数部分”从大到小依次补给参与人；小数部分相同时，按 `order` 里出现的先后
    顺序补——不是随机决定，是“你在参与人列表里排得靠前，这一分钱的取整优先补给你”，
    可复现、可对着账单解释，不会把余数悄悄丢给浮点误差。
    """
    floors = {u: exact[u].numerator // exact[u].denominator for u in order}
    remainder = amount - sum(floors.values())
    ranked = sorted(range(len(order)), key=lambda i: (-(exact[order[i]] - floors[order[i]]), i))
    shares = dict(floors)
    for i in ranked[:remainder]:
        shares[order[i]] += 1
    return shares


class Split(ABC):
    """一种拆分算法：把总额分给参与人，返回恰好加总等于 `amount` 的整数分账（单位与
    `Expense.amount` 相同，通常是“分”）。

    `compute` 是唯一公开入口，每个子类自己决定“怎么算比例、怎么校验自己的输入”；
    `_proportional` 是给“确实按比例分”的几种拆分（均分/百分比/份额）共享的一段算法——
    取整和分配余数的规则只写一次。`ExactSplit` 完全不调用它，因为它没有比例、没有
    需要“最大余数法”去抹平的余数：金额对不上总额是调用方的输入错了，不是可以悄悄
    修正的取整噪声。这段共享代码是这里选“类 + 模板方法”而不是像停车场分配策略那题
    选“普通函数”的原因：策略模式要求的是“算法可以整体替换”，不是“必须用类表达”，
    但当几种实现之间确实有值得共享而不是各自复制的代码时，类（而不是一组独立函数）
    就是那个能装下共享代码的地方。
    """

    @abstractmethod
    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        """算出每个参与人该付多少；参与人为空、金额为负或者子类自己的数据对不上时
        抛 `SplitError`。"""

    @staticmethod
    def _proportional(amount: int, participants: Sequence[User],
                       weights: Mapping[User, Fraction]) -> dict[User, int]:
        if amount < 0:
            raise SplitError(f"金额不能为负：{amount}")
        total_weight = sum(weights.values())
        if total_weight <= 0:
            raise SplitError("拆分权重之和必须大于 0")
        exact = {u: Fraction(amount) * weights[u] / total_weight for u in participants}
        return _largest_remainder(exact, amount, participants)


@dataclass(frozen=True, slots=True)
class EqualSplit(Split):
    """人均一份；不携带任何数据，是四种拆分里最简单的一种。"""

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        if not participants:
            raise SplitError("参与人不能为空")
        return self._proportional(amount, participants, {u: Fraction(1) for u in participants})


@dataclass(frozen=True, slots=True)
class ExactSplit(Split):
    """每个人该付多少钱是调用方直接给定的，不按比例推算。"""

    amounts: Mapping[User, int]

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        if not participants:
            raise SplitError("参与人不能为空")
        if set(self.amounts) != set(participants):
            raise SplitError("精确金额的参与人和费用的参与人不一致")
        if any(v < 0 for v in self.amounts.values()):
            raise SplitError("精确金额不能为负")
        total = sum(self.amounts.values())
        if total != amount:
            raise SplitError(f"精确金额之和 {total} 与费用总额 {amount} 不符")
        return dict(self.amounts)


@dataclass(frozen=True, slots=True)
class PercentageSplit(Split):
    """按百分比拆分；百分比之和必须恰好是 100，在构造时就检查，而不是等到 `compute`
    才发现——这条不变式和具体的费用总额、参与人无关，越早失败越好。
    """

    percentages: Mapping[User, Decimal]

    def __post_init__(self) -> None:
        total = sum(self.percentages.values(), Decimal(0))
        if total != Decimal(100):
            raise SplitError(f"百分比之和必须是 100，实际是 {total}")

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        if set(self.percentages) != set(participants):
            raise SplitError("百分比的参与人和费用的参与人不一致")
        weights = {u: Fraction(self.percentages[u]) for u in participants}
        return self._proportional(amount, participants, weights)


@dataclass(frozen=True, slots=True)
class ShareSplit(Split):
    """按份额（权重）拆分，例如两份给一个人、一份给另外两个人。份额必须是正整数——
    这一条同样和具体金额无关，在构造时就检查。
    """

    shares: Mapping[User, int]

    def __post_init__(self) -> None:
        if any(s <= 0 for s in self.shares.values()):
            raise SplitError("份额必须是正整数")

    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]:
        if set(self.shares) != set(participants):
            raise SplitError("份额的参与人和费用的参与人不一致")
        weights = {u: Fraction(self.shares[u]) for u in participants}
        return self._proportional(amount, participants, weights)


@dataclass(frozen=True, slots=True)
class Expense:
    """一笔已经记录的开销：谁付的、多少钱、哪些人分摊、用哪种拆分算法算出来的。

    `shares` 在构造时就用 `split.compute` 算好并冻结（`__post_init__` 只调用一次），
    不是每次访问时现算——哪怕调用方后来改了传进来的 `split` 对象引用的字典（比如
    `ExactSplit.amounts` 指向的那个 dict 被外部改了内容），这笔已经记好的账也不会
    跟着变：过去发生的事不应该被现在的操作动摇。`participants` 存成 tuple、`shares`
    存成 `MappingProxyType`，都是同一个理由的两处体现。
    """

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
        shares = self.split.compute(self.amount, self.participants)
        object.__setattr__(self, "shares", MappingProxyType(shares))


@dataclass(frozen=True, slots=True)
class Debt:
    """一对用户之间当前的净欠款：`debtor` 欠 `creditor` `amount`（恒为正数）。"""

    debtor: User
    creditor: User
    amount: int


def _canonical(a: User, b: User) -> tuple[User, User]:
    return (a, b) if a.id < b.id else (b, a)


class Ledger:
    """维护“谁欠谁多少”的唯一真源：每一对用户只有一行记录，存的是净额，而不是
    “A 欠 B 多少”和“B 欠 A 多少”各存一行——两行各自更新迟早会对不上（一次结算只
    改了其中一行）。键按用户 `id` 排成规范形式（canonical），(A, B) 和 (B, A) 永远
    落在同一行；值的正负号表示欠款方向（哪一边欠哪一边，见 `record_debt`）。净额
    归零的那一行会被立刻从字典里删掉——这是“容器必须会缩小”这条要求在这个设计里的
    落点：几百人用了几年之后互相结清的历史欠款，不会在这本账里留下永远占着内存的
    零余额条目。
    """

    def __init__(self) -> None:
        self._net: dict[tuple[User, User], int] = {}

    @property
    def row_count(self) -> int:
        """账本里还剩多少行。结清的一对用户必须让这个数变小——把"容器会缩小"这条
        不变量暴露成可以断言的东西，而不是让测试去读内部字典。
        """
        return len(self._net)

    def record_debt(self, debtor: User, creditor: User, delta: int) -> None:
        """`debtor` 对 `creditor` 的欠款增加 `delta`。`delta` 可以是负数，用来表示
        还款——欠款减少，减多了就变成反过来 `creditor` 欠 `debtor`，和现实中“多还了
        一点”是一回事，不需要特殊处理。
        """
        if debtor.id == creditor.id or delta == 0:
            return
        lo, hi = _canonical(debtor, creditor)
        key = (lo, hi)
        # 约定：这一行存的是“hi 欠 lo”的量，正值表示 hi 欠 lo，负值表示反过来 lo 欠 hi。
        signed = delta if debtor == hi else -delta
        new_value = self._net.get(key, 0) + signed
        if new_value == 0:
            self._net.pop(key, None)
        else:
            self._net[key] = new_value

    def balance_between(self, a: User, b: User) -> int:
        """`a` 净欠 `b` 多少；负数表示反过来 `b` 欠 `a`。"""
        if a.id == b.id:
            return 0
        lo, hi = _canonical(a, b)
        value = self._net.get((lo, hi), 0)
        return value if a == hi else -value

    def debts(self) -> tuple[Debt, ...]:
        """所有非零欠款的一份快照；不会把内部字典本身交出去。"""
        out: list[Debt] = []
        for (lo, hi), value in self._net.items():
            if value > 0:
                out.append(Debt(debtor=hi, creditor=lo, amount=value))
            elif value < 0:
                out.append(Debt(debtor=lo, creditor=hi, amount=-value))
        return tuple(out)

    def net_balance(self, user: User) -> int:
        """这个人当前净应收（正）或净应付（负）多少——把所有和他相关的行加总。

        符号约定必须和 `record_debt` 那一行的约定严格对偶：行里存的是“hi 欠 lo”的量，
        所以对 `lo` 来说这是应收（加），对 `hi` 来说这是应付（减）。这两处符号一旦
        写反，`debts()` 看起来仍然完全正确（它读的是同一行的正负号），只有
        `simplify()` 会把付款方和收款方整个对调——是一种不会抛异常、只会算反的错。
        测试因此不只断言金额，还断言每一笔建议转账的方向。
        """
        total = 0
        for (lo, hi), value in self._net.items():
            if lo == user:
                total += value
            elif hi == user:
                total -= value
        return total

    def net_balances(self, users: Iterable[User]) -> dict[User, int]:
        """一次遍历算出所有人的净额：O(行数 + 人数)，而不是每人各扫一遍账本的
        O(人数 × 行数)——`simplify()` 每次都要用到它，值得写成一趟。
        """
        totals = {u: 0 for u in users}
        for (lo, hi), value in self._net.items():
            if lo in totals:
                totals[lo] += value
            if hi in totals:
                totals[hi] -= value
        return totals


@dataclass(frozen=True, slots=True)
class Payment:
    """债务化简之后的一笔结算建议：`payer` 应该付给 `payee` `amount`。"""

    payer: User
    payee: User
    amount: int


def simplify_debts(net_balances: Mapping[User, int]) -> list[Payment]:
    """贪心债务化简：每一步都让当前净应收最多的人和净应付最多的人互相结清尽量多的
    金额，直到有一方归零；两个堆（应收方按余额取负数模拟大顶堆，应付方本身是负数、
    天然就是大顶堆）分别维护当前的最大值，每一步 O(log n) 弹出/压回。

    保证：每一步至少让一个人的净额归零，n 个人最多 n-1 步就能让所有人都结清——最后
    剩下的那个人的净额必然也是 0，因为全体净额之和恒为 0。

    不保证：这不是理论上转账笔数最少的方案。找真正的最优解等价于把净额划分成尽量
    多个“组内加总为零”的子集，这是一个子集和（subset sum）问题的变体，NP-hard。
    一个贪心确实比最优多付一笔的例子（题解“关键设计决策”有完整推导）：五个人的净额
    是 `[+3, +2, -3, +2, -4]`。贪心第一步永远选全场最大应付（-4）去配全场最大应收
    （+3），配对之后最大应收方结清、最大应付方还剩 -1；而真正的最优解是让净额恰好
    相等的 +3 和 -3 各自结清、剩下的 +2、+2、-4 三个人也恰好能两两配平——一共 3 笔，
    比贪心少一笔。贪心不是错的，只是不保证全局最优，这一点必须诚实地说给面试官听，
    而不是声称“贪心=最优”。
    """
    tie = count()
    creditors: list[tuple[int, int, User]] = []
    debtors: list[tuple[int, int, User]] = []
    for user, balance in net_balances.items():
        if balance > 0:
            heapq.heappush(creditors, (-balance, next(tie), user))
        elif balance < 0:
            heapq.heappush(debtors, (balance, next(tie), user))

    payments: list[Payment] = []
    while creditors and debtors:
        neg_credit, _, creditor = heapq.heappop(creditors)
        debt, _, debtor = heapq.heappop(debtors)
        amount = min(-neg_credit, -debt)
        payments.append(Payment(payer=debtor, payee=creditor, amount=amount))
        remaining_credit = -neg_credit - amount
        remaining_debt = debt + amount
        if remaining_credit > 0:
            heapq.heappush(creditors, (-remaining_credit, next(tie), creditor))
        if remaining_debt < 0:
            heapq.heappush(debtors, (remaining_debt, next(tie), debtor))
    return payments


class SplitwiseEventKind(Enum):
    EXPENSE_ADDED = "expense_added"
    SETTLED = "settled"


@dataclass(frozen=True, slots=True)
class SplitwiseEvent:
    """一次发生的事——加了一笔账，还是结清了一笔欠款。订阅者从这一条记录本身就能
    知道发生了什么，不需要回头去问 `ExpenseManager` “现在状态是什么”，更不需要拿到
    它内部的账本或用户表。
    """

    kind: SplitwiseEventKind
    at: datetime
    summary: str
    users: tuple[User, ...]
    amount: int


SplitwiseObserver = Callable[[SplitwiseEvent], None]


class ActivityLog:
    """订阅 `ExpenseManager` 的事件流，按时间顺序保留一份活动记录——这是第 4 关新加
    的一个类，`ExpenseManager` 从第一版起就有的 `subscribe` 挂钩原样复用，不改
    `ExpenseManager`、`Ledger` 或任何 `Split` 一行代码。`ActivityLog` 本身实现
    `__call__`，所以可以直接当成一个观察者传给 `subscribe`，不需要额外包一层适配。
    """

    def __init__(self) -> None:
        self._events: list[SplitwiseEvent] = []

    def __call__(self, event: SplitwiseEvent) -> None:
        self._events.append(event)

    def recent(self, n: int = 10) -> tuple[SplitwiseEvent, ...]:
        """最近 n 条，最新的排最前；只给调用方一份快照，改不了日志本身。"""
        return tuple(reversed(self._events[-n:]))


class ExpenseManager:
    """记一笔账、结一次款、问一句“谁欠谁多少”的入口。

    不做成 Singleton：测试要能同时开两个互不干扰的账本（两组朋友的账不该混在一起，
    并发测试也需要独立的实例互不污染），真的需要“整个进程只有一个账本”时，由调用方
    在应用启动的地方只构造一次、把这一个实例到处传，而不是让类在构造过程里自己保证
    唯一性——`ashishps1/awesome-low-level-design` 的题解把对应的 `SplitwiseService`
    写成了 Singleton（`__new__` 拦截），本文不同意这个选择，理由和停车场那题拒绝
    Singleton 完全一样：业务事实（现实里一群朋友只有一本账）和代码结构（这个类要不要
    拦截构造）是两回事，见题解“关键设计决策”。
    """

    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._users: dict[str, User] = {}
        self._groups: dict[str, Group] = {}
        self._expenses: list[Expense] = []
        self._ledger = Ledger()
        self._clock = clock
        self._observers: list[SplitwiseObserver] = []
        self._expense_ids = (f"E{n}" for n in count(1))
        # 一把锁守住“分配流水号 + 改账本 + 追加流水”这一段。锁在 Manager 而不在
        # Ledger：一笔开销要改好几行账本（每个参与人一行），这几行必须整体原子，
        # 锁在 Ledger 内部只能保证单行原子，不能保证一笔账不会被别的线程劈开。
        self._lock = RLock()

    @property
    def expense_count(self) -> int:
        """已记录的开销笔数；在锁内数好再交出去，不把内部列表暴露给调用方。"""
        with self._lock:
            return len(self._expenses)

    def add_user(self, user: User) -> None:
        with self._lock:
            self._users[user.id] = user

    def create_group(self, id: str, name: str, members: Iterable[User] = ()) -> Group:
        with self._lock:
            for member in members:
                self._require_known(member)
            group = Group(id, name, members)
            self._groups[id] = group
            return group

    def subscribe(self, observer: SplitwiseObserver) -> None:
        """挂一个“记了新账/结了一次款”的订阅者；`ActivityLog` 就是这么接进来的。"""
        self._observers.append(observer)

    def _notify(self, event: SplitwiseEvent) -> None:
        for observer in self._observers:
            observer(event)

    def _require_known(self, user: User) -> None:
        if user.id not in self._users:
            raise UnknownUserError(f"未知用户：{user.id}")

    def add_expense(self, payer: User, amount: int, description: str,
                     participants: Sequence[User], split: Split,
                     group: Group | None = None) -> Expense:
        """记一笔账：`payer` 垫付了 `amount`，按 `split` 分给 `participants`——`payer`
        不必是参与人之一（垫付一笔和自己完全无关的账是合法的）。分摊到的份额会计入
        账本，`payer` 自己那一份（如果他也是参与人）不会给自己记一笔债。
        """
        self._require_known(payer)
        for participant in participants:
            self._require_known(participant)
        created_at = self._clock()
        with self._lock:
            # 流水号来自一个生成器：`next()` 本身不是线程安全的（两个线程同时进入会
            # 抛 `ValueError: generator already executing`），必须和改账本一起在锁内。
            expense = Expense(id=next(self._expense_ids), payer=payer, amount=amount,
                               description=description, participants=tuple(participants),
                               split=split, created_at=created_at, group=group)
            for participant, share in expense.shares.items():
                if participant != payer and share:
                    self._ledger.record_debt(debtor=participant, creditor=payer, delta=share)
            self._expenses.append(expense)
        # 通知在锁外发出：订阅者是外部代码，可能很慢、可能反过来调用 `debts()`，
        # 在锁内回调等于把自己的临界区交给别人的代码决定长短。事件自带了全部信息，
        # 订阅者不需要回头访问账本，所以锁外通知不会读到半成品状态。
        self._notify(SplitwiseEvent(
            kind=SplitwiseEventKind.EXPENSE_ADDED, at=expense.created_at,
            summary=f"{payer.name} 支付了「{description}」共 {amount}，"
                    f"由 {len(expense.participants)} 人分摊",
            users=expense.participants, amount=amount))
        return expense

    def settle(self, payer: User, payee: User, amount: int) -> None:
        """`payer` 向 `payee` 还了 `amount`：减少 `payer` 欠 `payee` 的净额（还多了
        就变成 `payee` 反过来欠 `payer`，和现实里“多转了一点”一致，不当成错误）。
        """
        self._require_known(payer)
        self._require_known(payee)
        if amount <= 0:
            raise SettlementError("还款金额必须大于 0")
        with self._lock:
            self._ledger.record_debt(debtor=payer, creditor=payee, delta=-amount)
        self._notify(SplitwiseEvent(
            kind=SplitwiseEventKind.SETTLED, at=self._clock(),
            summary=f"{payer.name} 向 {payee.name} 支付了 {amount}",
            users=(payer, payee), amount=amount))

    def balance_between(self, a: User, b: User) -> int:
        with self._lock:
            return self._ledger.balance_between(a, b)

    def debts(self) -> tuple[Debt, ...]:
        """当前所有非零欠款的一份快照，回答“谁欠谁多少”。读也要持锁：一笔开销会
        连改好几行账本，锁外读到的可能是“改了一半”的账，金额加总对不上。"""
        with self._lock:
            return self._ledger.debts()

    def net_balance(self, user: User) -> int:
        with self._lock:
            return self._ledger.net_balance(user)

    def simplify(self) -> list[Payment]:
        """把当前所有欠款化简成尽量少的一批转账；不修改账本本身，调用方决定是否
        真的按这份建议去结算（结算请分别调用 `settle`）。只有“取一份净额快照”这一步
        需要持锁，贪心配对本身是对快照做的纯计算，放在锁外。
        """
        with self._lock:
            balances = self._ledger.net_balances(self._users.values())
        return simplify_debts(balances)


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)
    manager = ExpenseManager(clock=lambda: now)
    alice, bob, carol = User("u1", "Alice"), User("u2", "Bob"), User("u3", "Carol")
    for user in (alice, bob, carol):
        manager.add_user(user)
    log = ActivityLog()
    manager.subscribe(log)

    manager.add_expense(payer=alice, amount=9000, description="晚餐",
                         participants=[alice, bob, carol], split=EqualSplit())
    manager.add_expense(payer=bob, amount=6000, description="出租车",
                         participants=[alice, bob], split=ExactSplit({alice: 4000, bob: 2000}))

    print("谁欠谁：", manager.debts())
    print("化简后的转账：", manager.simplify())
    print("最近的活动：", log.recent(5))
