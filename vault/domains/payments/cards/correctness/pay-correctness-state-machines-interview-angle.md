---
id: pay-correctness-state-machines-interview-angle
node: correctness.state-machines
type: qa
step: 8
---
## Q
面试官让你"画出支付单的状态机并说明如何防止乱序和并发"，怎么回答？

## A
**先画主线**：created → requires_action → authorized → captured，旁支 failed、voided、expired；之后 partially_refunded、refunded。退款单和打款单各有独立状态机。

**四个要点**
1. **原则**：状态只前进，终态不可变；合法转移集中在转移表里。
2. **并发**：条件更新 `WHERE state = 旧状态`，影响行数为 1 才成功；失败时区分"已在目标状态（幂等）"与"冲突（告警）"。
3. **乱序**：状态阶位，过期事件忽略；允许跳过中间状态并补记历史；关键状态以主动查询渠道为准。
4. **一致性**：状态变更、状态历史、分录、outbox 事件同一事务；下游动作（发货、发币）由转移事件触发，而不是扫描状态。

**加分点**
- UNKNOWN 作为一等状态，驱动查询和对账。
- 部分请款和多次退款用金额字段加约束，而不是状态爆炸。
- 渠道状态映射层，不直接暴露渠道状态。

**追问预判**
- 为什么不直接用事件溯源？审计强但复杂；折中是状态加追加型历史表。
- 一单多尝试怎么建模？attempt 表独立状态，同一支付最多一个活跃尝试。
