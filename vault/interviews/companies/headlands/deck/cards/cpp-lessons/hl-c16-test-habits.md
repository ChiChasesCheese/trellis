---
id: hl-c16-test-habits
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 7
---
## Q
面试问：怎么测试你的代码？应该覆盖哪些边界？
Interview question: How do you test your code in a live coding round?

## A
顺序：先写正常例子，再写**边界**。
- 空输入（`two_sum({}, 0)`）
- `k = 0`、`k > n`（`top_k(ts, 0)` 得 0 个，`top_k(ts, 99)` 得 4 个）
- 单元素、重复值、负数
- 最大值溢出
- 已空的订单簿（`best_bid()` 为空）

方法类别：正常 / 边界 / 大输入 / 对拍（暴力解对比）。
