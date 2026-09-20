---
id: problems-stock-exchange-sequencer-down-halt-not-degrade
node: problems.commerce.stock-exchange
type: qa
step: 7
tags: [grown]
---
## Q
When the sequencer/journal layer for a symbol's matching engine becomes unavailable, why should the exchange stop accepting new orders for that symbol rather than let orders bypass sequencing and go straight to the matching engine to keep availability up?

## A
The sequencer's job is to assign each incoming event a single, globally agreed, unalterable order number, which is the sole basis for the deterministic replay that durability and failover depend on. If orders bypassed sequencing during an outage, the matching engine would be free to process them in whatever order it happened to receive them, and there would be no durable, ordered record to replay if that matching engine then also failed — silently breaking the 'one authoritative order' guarantee that is the exchange's core correctness property. Rejecting new orders for that symbol until the sequencer recovers sacrifices availability but preserves correctness, which for a matching engine is the higher-priority requirement.

## Q zh
当某支股票撮合引擎的序列化/日志层（sequencer/journal）不可用时，为什么交易所应该停止接受这支股票的新订单，而不是让订单绕过序列化、直接进撮合引擎以维持可用性？

## A zh
序列化层的职责是给每一条到达的事件分配一个全局唯一、公认、不可篡改的顺序号，这是持久化和故障转移所依赖的确定性重放的唯一依据。如果在故障期间让订单绕过序列化，撮合引擎就会按它恰好收到的顺序处理，而且如果撮合引擎随后也发生故障，将不存在可重放的、有序的持久记录——这会在无声无息中打破“单一权威顺序”这条交易所最核心的正确性保证。在序列化层恢复之前拒绝该股票的新订单，牺牲的是可用性，保住的是正确性，而对撮合引擎来说，正确性是优先级更高的要求。
