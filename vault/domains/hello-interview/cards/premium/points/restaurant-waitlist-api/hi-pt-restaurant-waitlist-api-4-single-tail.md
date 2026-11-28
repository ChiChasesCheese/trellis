---
id: hi-pt-restaurant-waitlist-api-4-single-tail
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 4
---
## Q
**餐厅候位 API · 统一收尾步骤**｜必会 · 出自：餐厅候位 API › 整体设计

`join`、`leave`、`finish` 三个会改变状态的入口，收尾应该怎么写？为什么不让每个入口各自决定要不要入座？

## A
**做法。** 每个入口先校验、改自己那一小部分，最后都调 `_seat_everyone_possible()`，它调用 `_drain` 并把结果写进 `_seated`，`finish` 的返回值就是它的结果。

**为什么。** 各写各的会漏：例如防饿死时，挡路的人 `leave` 之后后面的人要能坐下。统一收尾，后加的规则只改一处。
