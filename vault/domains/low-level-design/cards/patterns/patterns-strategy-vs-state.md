---
id: patterns-strategy-vs-state
node: patterns.strategy
type: qa
step: 3
---
## Q
Strategy 和 State 都是"把行为封装到对象里"，区分它们的关键是什么？

## A
**Strategy**：由**调用方**选定一个算法再使用，各个策略互不通信、互不感知，生命周期是"创建时选好，之后基本不变"——例如排序比较器、支付方式。

**State**：对象**自己**在运行过程中改变当前状态并因此改变行为，状态之间还会互相触发转移——例如订单从待处理转到已发货。

一句话：Strategy 是"调用方挑一种算法"，State 是"对象自己的性质随时间改变"。
