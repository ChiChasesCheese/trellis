"""交易列表视图模型（Transactions List）：参考解。

1. 视图只记两样东西：当前筛选（`all`/`credit`/`debit` 之一）和一份“冻结的行”元组。
2. 来源列表在进入视图的那一刻就被读成冻结的行（`_Row`），之后调用方怎么改自己的对象都碰不到视图。
3. 每次 `snapshot()` 都从冻结的行现造一批新的展示项和筛选项，所以快照之间、快照与视图之间不共享任何可变对象。
4. 换列表时先把新元组完整建好再赋值，旧列表整体丢弃；筛选另存一处，换列表不碰它。
5. 展示用的字符串（金额、日期、地址）一律原样搬运，不解析、不去空白、不重排。
"""
from __future__ import annotations

from dataclasses import dataclass

FILTERS = ("all", "credit", "debit")  # 对外固定的筛选顺序


@dataclass
class Location:
    id: int
    address: str
    city: str
    zipCode: int


@dataclass
class Transaction:
    id: int
    date: str
    txnType: str
    amount: str
    location: Location


@dataclass
class FilterState:
    filter: str
    active: bool


@dataclass
class TransactionItem:
    id: int
    address: str
    city: str
    amount: str
    date: str


@dataclass
class ListSnapshot:
    activeFilter: str
    filters: list[FilterState]
    items: list[TransactionItem]


@dataclass(frozen=True, slots=True)
class _Row:
    """一条交易里视图真正需要的全部内容：冻结，所以放进元组后没有任何代码能再改它。"""

    kind: str
    id: int
    address: str
    city: str
    amount: str
    date: str

    @classmethod
    def read(cls, txn: Transaction) -> _Row:
        # 只在这里碰调用方的对象；字符串和整数本身不可变，读出来就是独立的值
        return cls(txn.txnType, txn.id, txn.location.address, txn.location.city, txn.amount, txn.date)

    def visible_under(self, active: str) -> bool:
        return active == "all" or self.kind == active

    def to_item(self) -> TransactionItem:
        return TransactionItem(self.id, self.address, self.city, self.amount, self.date)


def _freeze(transactions: list[Transaction]) -> tuple[_Row, ...]:
    return tuple(_Row.read(t) for t in transactions)


class TransactionsList:
    def __init__(self, transactions: list[Transaction]) -> None:
        self._rows = _freeze(transactions)
        self._active = "all"

    def selectFilter(self, filter: str) -> None:
        self._active = filter

    def replaceTransactions(self, transactions: list[Transaction]) -> None:
        self._rows = _freeze(transactions)  # 建完再赋值：中途出错时旧列表还在

    def snapshot(self) -> ListSnapshot:
        active = self._active
        return ListSnapshot(
            active,
            [FilterState(name, name == active) for name in FILTERS],
            [row.to_item() for row in self._rows if row.visible_under(active)],
        )
