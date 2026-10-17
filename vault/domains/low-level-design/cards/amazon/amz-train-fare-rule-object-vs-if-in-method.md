---
id: amz-train-fare-rule-object-vs-if-in-method
node: amazon.amz-train-fare
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，周末封顶是写成 `calculate_fare` 里的一个 `if`，还是做成 `FareRule` 对象？各自的代价和选择？

## A
写 `if`：第 3 关当场可用，但第 4 关的高峰加价、节假日各再加一个 `if`，核心方法越改越长，每次都要动它。做成协议 `FareRule.apply(fare, trip)`：`WeekendCap`、`PeakSurcharge` 各是一个小类，计算器只循环应用，加规则只新增类并改装配列表。因为已经有至少两个真实现，选对象；规则顺序有语义（先加价后封顶与反过来结果不同），由调用方列表顺序决定。
