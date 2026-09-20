---
id: problems-airline-sold-vs-seats-two-tables
node: problems.booking.airline
type: qa
step: 2
tags: [grown]
---
## Q
在航班管理设计里，`FlightInstance` 的库存为什么用 `_sold`（订单号→舱位）和 `_seats`（座位号→订单号）两张表，而不是一张“座位号→状态”的表？

## A
这两张表回答的是两个不同的问题：`_sold` 回答“这一舱卖给了谁”，决定能不能超售（卖出的票数可以超过物理座位数）；`_seats` 回答“哪把椅子归谁”，是值机之后才确定的具体分配。只用一张座位状态表意味着“卖出去”和“有物理座位”被绑成了同一件事，超售——卖出的票数超过座位数——这条业务事实就无法表达。
