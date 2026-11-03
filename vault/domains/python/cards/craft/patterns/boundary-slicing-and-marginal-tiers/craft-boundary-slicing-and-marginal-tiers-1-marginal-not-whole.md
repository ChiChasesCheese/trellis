---
id: craft-boundary-slicing-and-marginal-tiers-1-marginal-not-whole
node: craft.patterns.boundary-slicing-and-marginal-tiers
type: qa
step: 1
---
## Q
**边界切分与边际阶梯 · 阶梯费率：为什么每一档只对落在这一档里的那部分收费**｜模式

手续费规则：金额不超过 10000 的按 2.9%，超过部分按 2.5%。有人把它写成「看金额落在哪一档，整笔按那一档的费率」。金额从 10000 变成 10001 时，两种写法的结果各是什么？为什么有一种在生产里是不可接受的？

## A
**要点。** 阶梯有两种语义。整笔按档（whole-amount）：金额一跨过门槛，整笔适用新费率，费用在门槛处出现一个**断崖**，多花钱反而费用更低。边际累进（marginal）：金额按门槛切成几段，每段只按自己那一档的费率，总费用是金额的连续、单调函数。个人所得税的税率档就是边际的。

```python
from decimal import Decimal

TIERS = ((10_000, 290), (None, 250))              # 前 10000 收 2.9%，超出的部分收 2.5%（bps）

def whole_amount(amount):                         # 错：整笔金额只按"它落在的那一档"的费率
    for upper, bps in TIERS:
        if upper is None or amount <= upper:
            return Decimal(amount) * bps / 10_000

def marginal(amount):                             # 对：每一档只对落在本档内的那部分收本档的费率
    total, lower = Decimal(0), 0
    for upper, bps in TIERS:
        top = amount if upper is None else min(amount, upper)
        if top > lower:
            total += Decimal(top - lower) * bps / 10_000   # 只对落在本档内的 (lower, top] 收费
        if upper is None or amount <= upper:
            break
        lower = upper                             # 下一档从这一档的上限开始
    return total

for a in (9_999, 10_000, 10_001, 20_000):
    print(f"金额 {a:6}  整笔按档: {whole_amount(a):8}  边际累进: {marginal(a):8}")
```

实际输出：

```
金额   9999  整笔按档:  289.971  边际累进:  289.971
金额  10000  整笔按档:      290  边际累进:      290
金额  10001  整笔按档:  250.025  边际累进:  290.025
金额  20000  整笔按档:      500  边际累进:      540
```

**为什么。** 整笔按档的 10001 比 10000 少收约 40：商户会故意把一笔拆成两笔（或凑到门槛之上），费率表成了套利工具。边际累进下，每多一分钱最多按当前档的费率多收，不会出现多付钱却少收费的区间。

**怎么写。** 循环里维护 `lower`（上一档的上限）；`top = min(amount, upper)` 是本档能覆盖到的最高点，`top - lower` 就是落在本档里的那一段；金额没到本档上限就 `break`。最后一档的上限是 `None`，表示不封顶。

**易错。** 档上限必须严格递增且最后一档为 `None`，在构造时校验（`__post_init__`），不要留到计算时才炸；各档先累加成全精度，最后**取整一次**，不是每档各取整。
