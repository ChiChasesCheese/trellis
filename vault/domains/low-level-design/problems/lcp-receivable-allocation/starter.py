"""应收款汇总与分账（补全 `register_receivables` 和 `allocate_receivables` 两个函数）。

规则（每条都可以写成一个测试）：
1. 汇总：按 (merchant_id, card_type, payout_date) 精确分组（区分大小写），金额相加；customer_id 不参与分组，
   重复的行各算一次；空输入返回空列表。
2. 分账：每个键各自独立。合约按输入顺序处理。`fixed` 请求 value 分；`percentage` 请求
   `原始金额 * value // 10000` 分（value 是基点，2500 = 25%），永远基于该键的原始金额，哪怕前面已经分走了固定额。
3. 每份合约实际拿到 `min(请求, 该键剩余)`。键不在应收款里的合约被忽略。拿到的金额为正才输出一行：
   id 是 contract_id，卡类型和付款日不变。
4. 每笔输入的应收款输出一行商户余额，哪怕余额是 0：id 是 merchant_id。不同合约不合并。
5. 返回顺序不限；不得修改传入的列表或记录；结果与输入互不相连；重复调用互不影响；合约为空时只返回商户行。
6. 金额全程是整数分，不用浮点数。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

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


class Kind(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


def register_receivables(transactions: list[Transaction]) -> list[Receivable]:
    raise NotImplementedError


def allocate_receivables(receivables: list[Receivable], contracts: list[Contract]) -> list[Allocation]:
    raise NotImplementedError
