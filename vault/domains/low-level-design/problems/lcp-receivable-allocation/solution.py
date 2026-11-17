"""应收款汇总与分账：先按 (商户, 卡类型, 付款日) 汇总交易，再在合约与商户之间切分每一笔应收款。

设计（五行）：
1. 全程整数分（cent）：百分比用 `原始金额 * 基点 // 10000`，先乘后整除，不经过浮点数。
2. 分组键是 `ReceivableKey` 三元组，字典保持首次出现的顺序，所以输出是确定的。
3. 合约先按键归到各自的列表（保持输入顺序），每笔应收款只看自己那一组，总成本是 O(交易数 + 合约数)。
4. `Funds` 拥有一笔应收款的钱：百分比永远按 `original` 算，每份只能拿 `min(请求, remaining)`，剩下的归商户。
5. 函数不保存任何状态，也不修改参数；结果是新对象，记录是冻结的，所以重复调用互不影响。
   每笔应收款的各行之和必须等于它的金额（逐笔守恒）。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

BASIS_POINTS = 10_000  # 1 个基点 = 0.01%，10000 = 100%


# --- records:begin（工作区的 models.py 提供这四个冻结记录，字段顺序以它为准）
@dataclass(frozen=True, slots=True)
class Transaction:
    customer_id: str
    merchant_id: str
    payout_date: str
    card_type: str
    amount: int


@dataclass(frozen=True, slots=True)
class Receivable:
    merchant_id: str
    card_type: str
    payout_date: str
    amount: int


@dataclass(frozen=True, slots=True)
class Contract:
    contract_id: str
    merchant_id: str
    payout_date: str
    card_type: str
    kind: str
    value: int


@dataclass(frozen=True, slots=True)
class Allocation:
    id: str
    card_type: str
    payout_date: str
    amount: int


# --- records:end


class ConservationError(RuntimeError):
    """钱被凭空造出或丢掉：这是实现错误，不是输入错误，所以不用 assert（python -O 会把它去掉）。"""


class Kind(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class ReceivableKey(NamedTuple):
    """分组键。区分大小写、不做任何规范化；顺序固定为 商户、卡类型、付款日。"""

    merchant_id: str
    card_type: str
    payout_date: str


def key_of(row: Transaction | Receivable | Contract) -> ReceivableKey:
    """三种记录的字段顺序并不相同，所以一律按名字取，不按位置取。"""
    return ReceivableKey(row.merchant_id, row.card_type, row.payout_date)


@dataclass(slots=True)
class Funds:
    """一笔应收款里还没分出去的钱。

    不变量：0 <= remaining <= original；remaining 只减不增。
    """

    original: int
    remaining: int

    def __post_init__(self) -> None:
        if not 0 <= self.remaining <= self.original:
            raise ValueError(f"need 0 <= remaining <= original, got {self.remaining}/{self.original}")

    @classmethod
    def of(cls, amount: int) -> Funds:
        return cls(original=amount, remaining=amount)

    def take(self, requested: int) -> int:
        """给一份合约划钱：拿走 min(请求, 剩余)，返回实际拿到的金额。"""
        if requested < 0:
            raise ValueError(f"negative request: {requested}")
        granted = min(requested, self.remaining)
        self.remaining -= granted
        return granted


def requested_amount(contract: Contract, original: int) -> int:
    """合约想要多少分。百分比向下取整，并且永远基于原始金额，不基于剩余金额。"""
    kind = Kind(contract.kind)  # 未知种类直接 ValueError，不静默当成固定额
    if kind is Kind.FIXED:
        return contract.value
    return original * contract.value // BASIS_POINTS


def register_receivables(transactions: list[Transaction]) -> list[Receivable]:
    """按 (商户, 卡类型, 付款日) 汇总交易金额；客户编号不参与分组，重复行各算一次。"""
    totals: dict[ReceivableKey, int] = {}
    for transaction in transactions:
        key = key_of(transaction)
        totals[key] = totals.get(key, 0) + transaction.amount
    return [
        Receivable(merchant_id=key.merchant_id, card_type=key.card_type,
                   payout_date=key.payout_date, amount=amount)
        for key, amount in totals.items()
    ]


def allocate_one(receivable: Receivable, contracts: list[Contract]) -> list[Allocation]:
    """一笔应收款：合约按输入顺序各拿一份，正数才出行；最后一行是商户余额，零也要出。"""
    funds = Funds.of(receivable.amount)
    rows: list[Allocation] = []
    for contract in contracts:
        granted = funds.take(requested_amount(contract, funds.original))
        if granted > 0:
            rows.append(Allocation(contract.contract_id, receivable.card_type,
                                   receivable.payout_date, granted))
    rows.append(Allocation(receivable.merchant_id, receivable.card_type,
                           receivable.payout_date, funds.remaining))
    if sum(row.amount for row in rows) != receivable.amount:  # 逐笔守恒：钱不能在键与键之间流动
        raise ConservationError(f"rows of {key_of(receivable)} do not add up to {receivable.amount}")
    return rows


def allocate_receivables(receivables: list[Receivable], contracts: list[Contract]) -> list[Allocation]:
    """逐键独立分账。键不在应收款里的合约被忽略；每笔应收款恰好一行商户余额。"""
    by_key: dict[ReceivableKey, list[Contract]] = {}
    for contract in contracts:  # 一次遍历：按键归组，组内保持输入顺序
        by_key.setdefault(key_of(contract), []).append(contract)

    seen: set[ReceivableKey] = set()
    rows: list[Allocation] = []
    for receivable in receivables:
        key = key_of(receivable)
        if key in seen:  # 同一个键出现两次，合约会被分两遍：钱会被造出来
            raise ValueError(f"duplicate receivable key: {key}")
        seen.add(key)
        rows.extend(allocate_one(receivable, by_key.get(key, [])))
    return rows


def payout_totals(rows: list[Allocation]) -> dict[str, int]:
    """每一方（合约或商户）跨所有键一共分到多少：对账用，返回新字典。"""
    totals: dict[str, int] = {}
    for row in rows:
        totals[row.id] = totals.get(row.id, 0) + row.amount
    return totals


# --- CSV 两端：工作区自带同样的适配器；这里写一份，让单个文件就能从文本跑到文本
def parse_transactions(text: str) -> list[Transaction]:
    """第一行是表头；值里没有逗号、引号和空白，所以直接按逗号切。"""
    records = (line.split(",") for line in text.splitlines()[1:])
    return [Transaction(c, m, d, k, int(a)) for c, m, d, k, a in records]


def parse_contracts(text: str) -> list[Contract]:
    records = (line.split(",") for line in text.splitlines()[1:])
    return [Contract(i, m, d, k, kind, int(v)) for i, m, d, k, kind, v in records]


def render_allocations(rows: list[Allocation]) -> str:
    lines = ["id,card_type,payout_date,amount"]
    lines += [f"{r.id},{r.card_type},{r.payout_date},{r.amount}" for r in rows]
    return "\n".join(lines) + "\n"


def settle_csv(transactions_csv: str, contracts_csv: str) -> str:
    """文本进、文本出：汇总，再分账，再渲染。"""
    receivables = register_receivables(parse_transactions(transactions_csv))
    return render_allocations(allocate_receivables(receivables, parse_contracts(contracts_csv)))


if __name__ == "__main__":
    demo = allocate_receivables(
        [Receivable("Grocer", "Visa", "2026-12-05", 1203)],
        [Contract("Split2", "Grocer", "2026-12-05", "Visa", "fixed", 350),
         Contract("Split3", "Grocer", "2026-12-05", "Visa", "percentage", 1500)],
    )
    for row in demo:
        print(row)
    print(settle_csv("c,m,d,k,a\nP1,Bakery,2026-12-01,Visa,175\nP2,Bakery,2026-12-01,Visa,225\n",
                     "i,m,d,k,kind,v\nSplit1,Bakery,2026-12-01,Visa,percentage,1000\n"), end="")
