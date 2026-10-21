---
id: amz-discount-engine-stacking-and-clamp
node: amazon.amz-discount-engine
type: qa
step: 7
tags: [grown]
---
## Q
在购物车折扣引擎里，两个 10% 折扣叠在 100.00 元上各减多少？折扣算出负数或超过剩余价格怎么办？

## A
叠加是顺序执行，后一条看到的是剩余价格：第一条减 10.00，第二条在 90.00 上减 9.00，共 19.00 元，不是 20.00。

- 减免超过剩余价格：钳到剩余价格，总价最低为 0。
- 减免为负数：抛 `InvalidRuleError`，因为一条写坏的折扣不能让总价变高；这是安全不变量，所以用异常而不是 `assert`（`python -O` 会剥掉它）。

只取最大一条的需求用 `Stacking.BEST_ONLY` 枚举，不另写引擎类。
