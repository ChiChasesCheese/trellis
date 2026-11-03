---
id: craft-boundary-slicing-and-marginal-tiers-4-floor-and-cap
node: craft.patterns.boundary-slicing-and-marginal-tiers
type: qa
step: 4
---
## Q
**边界切分与边际阶梯 · 保底和封顶写在哪一层，对「不适用」的规则怎么办**｜架构

手续费需要「最低 30 分、最高 500 分」。可以把保底封顶写进每个费率规则里，也可以写成一个包在任何规则外面的装饰器。另外，金额为 0 的交易本来不产生手续费行，套上保底后该不该变成 30？停车费的「每日封顶」是对每天分别封顶，还是对总额封顶？

## A
**要点。** 保底封顶写成**装饰器**（`Bounded(inner, minimum, maximum)`），包任何规则，不改规则本身：规则只回答「按我的逻辑该收多少」，装饰器再钳到区间。内层返回 `None`（不适用）时保持 `None`，不被保底硬凑出一行；否则零金额交易会凭空多出一笔 30 分的手续费。封顶的**粒度**是业务规则的一部分：每日封顶 = 每个日历日分别 `min(raw, cap)`，再求和。

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Percent:
    bps: int
    def apply(self, amount):
        return None if amount <= 0 else Decimal(amount) * self.bps / 10_000   # 金额不是正数：不适用

@dataclass(frozen=True)
class Bounded:                      # 装饰器：给任意规则加保底和封顶
    inner: Percent
    minimum: int = 0
    maximum: int | None = None
    def apply(self, amount):
        raw = self.inner.apply(amount)
        if raw is None: return None          # 不适用保持不适用：不被保底硬凑出一行
        raw = max(raw, Decimal(self.minimum))
        return raw if self.maximum is None else min(raw, Decimal(self.maximum))

fee = Bounded(Percent(290), minimum=30, maximum=500)
for amt in (0, 100, 5_000, 100_000):
    print(f"金额 {amt:7}: {fee.apply(amt)}")

days = [1500, 800]; cap = 1200                   # 两天的原始费用，每日封顶 1200
print("每日各自封顶:", sum(min(d, cap) for d in days), " 对总额封顶:", min(sum(days), cap))
```

保底 30、封顶 500、费率 2.9%；以及两天的原始费用 1500 和 800、每日封顶 1200：

```
金额       0: None
金额     100: 30
金额    5000: 145
金额  100000: 500
每日各自封顶: 2000  对总额封顶: 1200
```

**为什么。** 装饰器让保底封顶对阶梯、固定费、比例费都通用，规则类不用各写一份；`None` 的传递保证「不适用」这个语义不被偷换。每日封顶和总额封顶差 800，不是实现细节，是定价产品的一部分：停车场的「每日最高」鼓励长时间停放，所以必须按天封顶。

**顺序也是规则。** 保底封顶发生在取整之前还是之后、折扣之前还是之后，结果都不同（丢票罚款放在折扣之后，所以不会被打折）。把顺序写成代码里一条显式的流水线，而不是散在各处的 `if`。
