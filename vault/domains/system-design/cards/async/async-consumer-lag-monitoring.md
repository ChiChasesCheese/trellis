---
id: async-consumer-lag-monitoring
node: async.log
type: qa
---
## Q
"Consumer lag" is the first metric on any Kafka dashboard. Define it precisely, explain what a steadily growing lag tells you, and give the response options in order.

## A
**Lag = log-end offset (latest produced) − committed consumer offset, summed or maxed per partition.** It measures how far behind reality the consumer's view is — in messages; divide by produce rate for lag-in-time, which is what SLOs care about.

A *steadily growing* lag means **consumption throughput < production throughput** — not a one-off hiccup. The consumer will never catch up on its own, and when lag exceeds the retention window you start **losing unread data**.

Responses, cheapest first:
- **Speed up the handler**: batch downstream writes, remove a slow synchronous call, process a partition's batch concurrently where ordering allows.
- **Add consumers** — but only up to the partition count; beyond that they idle.
- **Raise the partition count** — a re-shard: disturbs key→partition mapping for future messages, so it's a planned change, not an incident response.
- **Check for a skewed/hot partition first**: if one partition holds most of the lag, more consumers fix nothing — the key distribution is the problem.

Also alert on **no committed offset advancing** (stuck consumer, poison pill) — zero throughput can look like "no lag growth" if production also stopped.

## Q zh
"consumer lag（消费滞后）"是任何 Kafka 仪表盘上的第一个指标。给出它的精确定义，说明持续增长的 lag 说明了什么，并按顺序给出应对选项。

## A zh
**Lag = log-end offset（最新生产的位点）− 消费者已提交的 offset，按分区求和或取最大。** 它衡量消费者的视图落后现实多远——单位是消息条数；除以生产速率可换算成时间维度的 lag，这才是 SLO 关心的量。

*持续增长*的 lag 意味着**消费吞吐 < 生产吞吐**——不是偶发抖动。消费者靠自己永远追不上，而当 lag 超过保留窗口时，你会开始**丢失还没读到的数据**。

应对，从最便宜的开始：
- **提速处理逻辑**：批量化下游写入、去掉慢的同步调用、在顺序允许的范围内并发处理一个分区的批。
- **加消费者**——但上限是分区数；超过就只能闲着。
- **提高分区数**——这是一次 re-shard：会打乱未来消息的 key→分区映射，属于计划内变更，不是应急手段。
- **先检查是否有倾斜/热分区**：如果大部分 lag 集中在一个分区，加消费者毫无用处——问题出在 key 的分布上。

另外要对**已提交 offset 完全不前进**告警（消费者卡死、poison pill）——如果生产也停了，零吞吐看起来会像"lag 没有增长"。
