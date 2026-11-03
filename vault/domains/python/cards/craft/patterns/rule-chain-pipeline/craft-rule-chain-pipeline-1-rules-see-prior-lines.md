---
id: craft-rule-chain-pipeline-1-rules-see-prior-lines
node: craft.patterns.rule-chain-pipeline
type: qa
step: 1
---
## Q
**规则链 · 规则为什么要看见前面各行的结果**｜写法

支付平台对每笔交易收手续费（fee），再对手续费收一道税（tax）。把每条规则写成「只看交易金额，自己算出一个数」最简单。税规则也这样写（自己重算一遍手续费，再乘税率）会出什么问题？规则链（rule chain）怎样避免它？

## A
**要点。** 每条规则实现同一个小接口 `apply(txn, prior)`：看交易和前面已经算好、已经取整的各行，返回金额，或返回 `None` 表示不适用。引擎只负责按序调用、`None` 跳过、统一取整、累加。税规则从 `prior` 里按 `kind == "fee"` 找出费用行，所以税是建在账面上那个整数的手续费之上，而不是建在被重算出来的另一个数上。

```python
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN

@dataclass(frozen=True)
class Line:
    rule_id: str; kind: str; amount: int           # 整数分

def to_minor(x: Decimal) -> int:                   # 全系统唯一的取整点
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))

@dataclass(frozen=True)
class Fee:
    rule_id: str; bps: int; kind: str = "fee"
    def apply(self, amount, prior):
        return Decimal(amount) * self.bps / 10_000

@dataclass(frozen=True)
class TaxOnFees:
    rule_id: str; bps: int; kind: str = "tax"
    def apply(self, amount, prior):
        fees = [l.amount for l in prior if l.kind == "fee"]   # 已取整的费用行，按 kind 找，不靠名字猜
        return Decimal(sum(fees)) * self.bps / 10_000 if fees else None   # 没有费用就不凑一行 0

def run(rules, amount):
    lines = ()
    for r in rules:                    # 引擎：按序、None 跳过、统一取整、累加
        raw = r.apply(amount, lines)
        if raw is not None:
            lines += (Line(r.rule_id, r.kind, to_minor(raw)),)
    return lines

amount = 100                           # 100 分，手续费 1.5%，税 = 费用的 33.33%
lines = run([Fee("fee", 150), TaxOnFees("tax", 3333)], amount)
print(lines)
print("若税按未取整的费用算：", to_minor(Decimal(amount) * 150 / 10_000 * 3333 / 10_000), "（账上费用却是", lines[0].amount, "）")
```

100 分的交易，手续费 1.5%，税是手续费的 33.33%：

```
(Line(rule_id='fee', kind='fee', amount=2), Line(rule_id='tax', kind='tax', amount=1))
若税按未取整的费用算： 0 （账上费用却是 2 ）
```

**为什么。** 手续费 1.5 取整后账上是 2，税按账上的 2 算是 0.67，取整为 1；若税自己重算，用的是 1.5，得到 0。商户拿对账单自己核算税，只能用账上的 2，对不上。规则看见前面的行，账面上每行相加就是总数，每一行都可以由它前面的行复算。

**代价。** 规则之间有了顺序依赖（税必须在费用之后），顺序要显式声明（`needs`），并用拓扑排序校验，见依赖图那张卡。接口里 `prior` 是一个值（元组），规则不能修改它。
