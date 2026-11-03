"""复式账本：一份只追加的分录日志（唯一事实来源）加几份随写入同步更新的派生索引。

三条不变量撑起整个设计：
1. 每条分录按币种各自借贷平衡（腿的金额之和为 0），所以任何时刻全账户余额之和也是 0；
2. 余额等于它之前所有腿之和——余额只是日志的缓存，不是独立的事实；
3. 纠错只靠追加新分录（冲正），已写入的分录永远不改。

金额约定：整数最小货币单位，正数增加该账户余额，负数减少。这是"借方为正、贷方为负"的同一件事换了说法：
对钱包这类对用户而言的资产账户，余额为正；平台内部的对手账户（比如充值来源）余额为负，代表欠出去的钱。

写入路径一律是"先校验、后修改"，且日志、去重表、余额、历史、冻结在同一个临界区内更新，
所以失败的调用不留任何痕迹，并发读到的也不会是写了一半的状态。
"""

from __future__ import annotations

import threading
from bisect import bisect_right
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, NamedTuple, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])


class Key(NamedTuple):
    """(账户, 币种)。仍然是 tuple，可以当字典键，但字段有名字，不用记 key[0] 是什么。"""

    account: str
    currency: str


def _synchronized(method: _F) -> _F:
    """整个方法是一个临界区：锁的作用域写在方法头上，而不是散落在每个方法体里。"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return wrapper  # type: ignore[return-value]


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
    amount: int          # 带符号的最小货币单位：正数增加该账户余额，负数减少


@dataclass(frozen=True, slots=True)
class Entry:
    id: str
    postings: tuple[Posting, ...]     # 必须是 tuple，分录是不可变值
    reverses: str | None = None       # 冲正分录指向被冲正的那一条


@dataclass(frozen=True, slots=True)
class StatementLine:
    seq: int
    entry_id: str
    amount: int          # 这条分录对该账户该币种的净影响
    balance_after: int


@dataclass(slots=True)
class _Hold:
    key: Key
    amount: int
    active: bool = True


class Ledger:
    def __init__(self) -> None:
        self._journal: list[Entry] = []                           # 唯一事实来源，只追加
        self._by_id: dict[str, int] = {}                          # 分录 ID -> 序号，去重用
        self._bal: dict[Key, int] = defaultdict(int)              # 派生索引：当前余额
        self._hist: dict[Key, list[StatementLine]] = defaultdict(list)   # 派生索引：每次变动后的余额
        self._reversed_by: dict[str, str] = {}                    # 被冲正的分录 -> 冲正它的分录
        self._floors: dict[Key, int] = {}
        self._holds: dict[str, _Hold] = {}
        self._held: dict[Key, int] = defaultdict(int)             # 每个账户当前冻结的合计
        self._lock = threading.RLock()                            # 代替数据库事务；reverse 会重入 post

    # ---- 第 1 关：分录、借贷平衡、幂等提交、余额、冲正 ------------------------

    @_synchronized
    def post(self, entry: Entry, release_hold: str | None = None) -> int:
        """写入一条分录，返回序号（从 1 开始）；同 ID 同内容重复提交返回原序号，什么也不改。

        同 ID 不同内容抛 ConflictError；分录不合法抛 InvalidEntry；失败的调用不留任何痕迹。
        `reverses` 指向不存在的分录抛 UnknownEntry，指向已被冲正的分录抛 AlreadyReversed。
        账户设了下限（第 2 关）时，写入后"余额减冻结"低于下限抛 InsufficientFunds；
        `release_hold` 非空表示在同一个原子步骤里先释放这笔冻结再写入（第 3 关）。
        """
        if (seq := self._by_id.get(entry.id)) is not None:
            if self._journal[seq - 1] != entry:
                raise ConflictError(f"分录 {entry.id} 被复用但内容不同")
            return seq
        self._validate(entry)                                 # 先校验后修改：失败不留痕迹
        self._check_reverses(entry)
        delta: dict[Key, int] = defaultdict(int)
        for p in entry.postings:
            delta[Key(p.account, p.currency)] += p.amount
        freed = self._hold_to_release(release_hold)
        self._check_floors(delta, freed)
        self._journal.append(entry)                           # 以下是提交：不会再失败
        seq = self._by_id[entry.id] = len(self._journal)
        for key, d in delta.items():                          # 日志和余额在同一个临界区里更新
            self._bal[key] += d
            self._hist[key].append(StatementLine(seq, entry.id, d, self._bal[key]))
        if freed is not None:
            freed.active = False
            self._held[freed.key] -= freed.amount
        if entry.reverses is not None:
            self._reversed_by[entry.reverses] = entry.id
        return seq

    @_synchronized
    def balance(self, account: str, currency: str) -> int:
        """账户在某币种上的当前账面余额；从没出现过的账户是 0。"""
        return self._bal.get(Key(account, currency), 0)

    @_synchronized
    def total(self, currency: str) -> int:
        """某币种全部账户余额之和；账本正确时恒为 0。"""
        return sum(v for (_, c), v in self._bal.items() if c == currency)

    def _validate(self, entry: Entry) -> None:
        if not entry.id or len(entry.postings) < 2:
            raise InvalidEntry("分录需要 ID 和至少两条腿")
        net: dict[str, int] = defaultdict(int)
        for p in entry.postings:
            if p.amount == 0:
                raise InvalidEntry("腿的金额不能为 0")
            net[p.currency] += p.amount
        if any(net.values()):                                     # 每个币种各自借贷平衡
            raise InvalidEntry(f"分录 {entry.id} 不平衡: {dict(net)}")

    @_synchronized
    def reverse(self, entry_id: str, new_id: str) -> int:
        """把一条分录的每条腿取反，作为新分录 `new_id` 写入，返回新序号；原分录原样保留。

        原分录不存在抛 UnknownEntry；已被另一条分录冲正抛 AlreadyReversed；
        用同一个 `new_id` 重试是幂等的，返回第一次的序号。
        """
        if entry_id not in self._by_id:
            raise UnknownEntry(entry_id)
        orig = self._journal[self._by_id[entry_id] - 1]
        legs = tuple(Posting(p.account, p.currency, -p.amount) for p in orig.postings)
        return self.post(Entry(new_id, legs, reverses=entry_id))

    @_synchronized
    def journal(self) -> tuple[Entry, ...]:
        """日志的只读快照，按序号排列。"""
        return tuple(self._journal)

    def _check_reverses(self, entry: Entry) -> None:
        if entry.reverses is None:
            return
        if entry.reverses not in self._by_id:
            raise UnknownEntry(entry.reverses)
        if self._reversed_by.get(entry.reverses, entry.id) != entry.id:
            raise AlreadyReversed(entry.reverses)

    # ---- 第 2 关：历史余额、账户下限、对账单 ----------------------------------

    @_synchronized
    def balance_at(self, account: str, currency: str, seq: int) -> int:
        """第 `seq` 条分录写入之后的余额：seq 小于 1 得 0，大于当前序号得当前余额。"""
        hist = self._hist.get(Key(account, currency), [])
        i = bisect_right(hist, seq, key=lambda line: line.seq)   # 序号严格递增，列表天然有序
        return hist[i - 1].balance_after if i else 0

    @_synchronized
    def statement(self, account: str, currency: str, after_seq: int = 0, limit: int = 100) -> list[StatementLine]:
        """序号大于 `after_seq` 的对账单行（每条分录一行，金额是净影响），最多 `limit` 行。

        拿最后一行的 `seq` 当下一页的 `after_seq` 就能翻页。`limit` 小于 1 抛 ValueError。
        """
        if limit < 1:
            raise ValueError("limit 必须大于 0")
        hist = self._hist.get(Key(account, currency), [])
        i = bisect_right(hist, after_seq, key=lambda line: line.seq)
        return hist[i:i + limit]

    @_synchronized
    def set_floor(self, account: str, currency: str, floor: int) -> None:
        """给账户设余额下限（比如 0 表示不许透支）。只约束之后的写入，不追溯检查已有余额。"""
        self._floors[Key(account, currency)] = floor

    def _check_floors(self, delta: dict[Key, int], freed: _Hold | None) -> None:
        for key, d in delta.items():
            floor = self._floors.get(key)
            if floor is None:
                continue
            held = self._held.get(key, 0) - (freed.amount if freed and freed.key == key else 0)
            if self._bal.get(key, 0) + d - held < floor:          # 检查和写入在同一把锁里：并发下不会一起透支
                raise InsufficientFunds(f"{key.account} 写入后可用余额低于下限 {floor}")

    # ---- 第 3 关：冻结、原子释放、并发 ----------------------------------------

    @_synchronized
    def available(self, account: str, currency: str) -> int:
        """可用余额 = 账面余额 - 冻结合计。"""
        return self._bal.get(Key(account, currency), 0) - self._held.get(Key(account, currency), 0)

    @_synchronized
    def hold(self, hold_id: str, account: str, currency: str, amount: int) -> None:
        """冻结一笔金额。金额必须是正数（InvalidEntry）；账户有下限且冻结后可用余额低于下限抛 InsufficientFunds。

        同一个 `hold_id` 同参数重复调用是幂等的（即使已经释放过）；同 ID 不同参数抛 ConflictError。
        """
        key = Key(account, currency)
        if (old := self._holds.get(hold_id)) is not None:
            if (old.key, old.amount) != (key, amount):
                raise ConflictError(f"冻结 {hold_id} 被复用但内容不同")
            return
        if not hold_id or amount <= 0:
            raise InvalidEntry("冻结需要 ID 和正数金额")
        floor = self._floors.get(key)
        if floor is not None and self.available(account, currency) - amount < floor:
            raise InsufficientFunds(f"{account} 可用余额不足以冻结 {amount}")
        self._holds[hold_id] = _Hold(key, amount)
        self._held[key] += amount

    @_synchronized
    def release(self, hold_id: str) -> None:
        """释放冻结。冻结不存在抛 UnknownEntry；已经释放过再调用是无操作。"""
        hold = self._holds.get(hold_id)
        if hold is None:
            raise UnknownEntry(hold_id)
        if hold.active:
            hold.active = False
            self._held[hold.key] -= hold.amount

    def _hold_to_release(self, hold_id: str | None) -> _Hold | None:
        if hold_id is None:
            return None
        hold = self._holds.get(hold_id)
        if hold is None:
            raise UnknownEntry(hold_id)
        if not hold.active:
            raise ConflictError(f"冻结 {hold_id} 已经释放过")
        return hold

    # ---- 第 4 关（选做）：换汇 -------------------------------------------------

    def exchange(self, entry_id: str, account: str, from_currency: str, from_amount: int,
                 to_currency: str, to_amount: int, fx_account: str = "fx") -> int:
        """账户用 `from_amount` 的 `from_currency` 换入 `to_amount` 的 `to_currency`，返回序号。

        写成一条四条腿的分录，经由 `fx_account` 中转，各币种分别平衡；账本本身不需要任何改动。
        币种相同或金额不是正数抛 InvalidEntry。
        """
        if from_currency == to_currency or from_amount <= 0 or to_amount <= 0:
            raise InvalidEntry("换汇需要两个不同的币种和正数金额")
        return self.post(Entry(entry_id, (
            Posting(account, from_currency, -from_amount), Posting(fx_account, from_currency, from_amount),
            Posting(fx_account, to_currency, -to_amount), Posting(account, to_currency, to_amount))))
