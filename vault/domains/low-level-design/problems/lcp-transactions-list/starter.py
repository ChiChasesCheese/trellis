"""交易列表视图模型（Transactions List）：起始文件，补全 `TransactionsList` 的四个方法。

合同（逐条都会被测试盯住）：

1. 构造：`TransactionsList(transactions)` 默认选中 `all`。`snapshot()` 返回的 `activeFilter` 是当前筛选，
   `filters` 恰好三项，顺序固定为 `all`、`credit`、`debit`，每项的 `active` 是布尔，且只有一项为真。
2. 筛选：`all` 显示全部；`credit`、`debit` 只显示 `txnType` 与之相等的交易。重复选同一个筛选没有副作用。
   没有任何交易匹配时，所选筛选仍然是生效的那一项，`items` 为空。
3. 展示项：每条可见交易恰好产生一项，顺序就是输入顺序（不按 id、日期或金额排序）。
   `id` 取交易自己的 `id`（不是 `location.id`），`address` 与 `city` 取自它的 `location`，
   `amount` 与 `date` 取自交易；`location.id` 和 `zipCode` 不出现在展示项里。
4. 换列表：`replaceTransactions` 用新列表整体替换旧列表，当前筛选保持不变并立刻作用在新列表上；
   不追加、不合并、不去重、不排序。初始列表和替换列表都可以为空。
5. 展示字符串原样保留：金额与日期只是文本，不解析、不计算、不去空白、不改格式；Unicode 与首尾空格都要原样出现。
6. 隔离：不修改传入的列表、交易或地点；构造或替换之后调用方再改这些对象，视图不受影响。
   快照可以随意改（增删项、改字段），不影响视图和其他快照；旧快照在之后的选择或替换后保持原样；不同实例互不影响。

范围：列表至多 1000 条、同一列表内交易 id 唯一、`txnType` 只会是 `credit` 或 `debit`、
筛选参数只会是三个合法值；调用是顺序的，不考虑并发与持久化；非法的原生参数不在要求之内。
"""
from __future__ import annotations

from dataclasses import dataclass


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


class TransactionsList:
    def __init__(self, transactions: list[Transaction]) -> None:
        raise NotImplementedError

    def selectFilter(self, filter: str) -> None:
        raise NotImplementedError

    def replaceTransactions(self, transactions: list[Transaction]) -> None:
        raise NotImplementedError

    def snapshot(self) -> ListSnapshot:
        raise NotImplementedError
