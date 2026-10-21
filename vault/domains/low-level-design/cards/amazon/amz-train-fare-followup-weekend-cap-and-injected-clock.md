---
id: amz-train-fare-followup-weekend-cap-and-injected-clock
node: amazon.amz-train-fare
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，面试官追加「周末总票价要封顶」。时间从哪来？该改哪里、不改哪里？

## A
新增 `WeekendCap(cap)` 一个类：周末（`weekday() >= 5`）取 `min(fare, cap)`。时间不在规则里取：`FareCalculator` 构造时注入时钟，`calculate_fare(start, stop)` 签名不变，另有 `quote(start, stop, when)`。`Route` 与已有规则不动。例：注入周六 9 点，G 到 I 原价 4.00、封顶 3.00，得 3.00。
