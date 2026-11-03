---
id: craft-rule-chain-pipeline-2-engine-owns-the-clamp
node: craft.patterns.rule-chain-pipeline
type: qa
step: 2
---
## Q
**规则链 · 「折扣不能把价格减到负数」应该写在引擎里还是各个折扣里**｜架构

购物车的折扣有「全场 5 折」「立减 30 元」「买一送一」等几十种，可以叠加。每种折扣都在自己的 `apply` 里小心地 `min(减免, 剩余价格)`，和只在引擎里钳位一次，各自的风险是什么？

## A
**要点。** 约束放在引擎。折扣只回答「在你看到的剩余价格上，我想减多少」，引擎负责：拒绝负数（会让价格变高）、钳在剩余价格以内、记账、决定叠加或只取最大。折扣类本身越简单，越没有写错的余地。

```python
from enum import Enum

class Stacking(Enum):
    STACK = "stack"; BEST_ONLY = "best_only"

class InvalidRule(ValueError): ...

def bounded(amount, remaining, label):
    if amount < 0:
        raise InvalidRule(f"{label}: 折扣算出了负数 {amount}，会让总价变高")
    return min(amount, remaining)       # 折扣永远不会把价格减到负数

def price(original, discounts, stacking=Stacking.STACK):
    elig = list(discounts.items())      # 折扣 = 看到剩余价格、返回想减多少分的函数
    if stacking is Stacking.BEST_ONLY and elig:        # 叠加策略是引擎的参数，不是第二个引擎
        elig = [max(elig, key=lambda kv: bounded(kv[1](original), original, kv[0]))]
    remaining, taken = original, []
    for label, fn in elig:              # 后一条看到的是前一条减完后的剩余价格
        cents = bounded(fn(remaining), remaining, label)
        if cents:
            taken.append((label, cents)); remaining -= cents
    return remaining, taken

ds = {"全场5折": lambda r: r // 2, "立减30元": lambda r: 3000, "买一送一": lambda r: r}
print("叠加      :", price(4000, ds))
print("只取最大  :", price(4000, ds, Stacking.BEST_ONLY))
try: price(4000, {"坏规则": lambda r: -500})
except InvalidRule as e: print("坏规则:", e)
```

原价 4000 分，三条折扣都适用：

```
叠加      : (0, [('全场5折', 2000), ('立减30元', 2000)])
只取最大  : (0, [('买一送一', 4000)])
坏规则: 坏规则: 折扣算出了负数 -500，会让总价变高
```

**为什么。** 立减 30 元（3000）在 5 折后的剩余 2000 上只能减到 2000；若各折扣自己钳位，第 40 个新折扣的作者忘了这一行，就会出现 -1000 的价格，而且只在恰好叠加到那一种组合时才出现。引擎里这一行写一次，测试一次。

**代价。** 引擎需要知道「剩余价格」「叠加策略」这些概念，是一个更厚的核心；规则不能自己决定「我要独占」，这类需求要通过引擎的参数（见下一张卡）表达。

**什么时候不用。** 规则之间没有共同的不变量（各自产出互不相干的东西）时，没有什么可放进引擎，这时一个函数列表就够了。
