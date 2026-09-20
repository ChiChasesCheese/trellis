---
id: problems-stock-exchange-10x-symbol-count-not-throughput
node: problems.commerce.stock-exchange
type: qa
step: 8
tags: [grown]
---
## Q
At 10x scale, a stock exchange design grows from 8,000 symbols to 80,000 symbols, with market-wide peak order rate growing proportionally to 3,000,000 orders/sec. Given that even the busiest single symbol has thousands of times more per-thread matching headroom than it needs, why is the 10x bottleneck about symbol-to-partition assignment rather than about matching engine throughput?

## A
A single symbol's matching load stays far below what one thread can process even after 10x growth, so no individual matching engine needs to get faster or more parallel. The actual risk is at the sequencer/partition layer: if symbols are assigned to sequencing partitions in a way that happens to cluster several of the hottest symbols onto the same partition, that partition's aggregate load can exceed its capacity even though every symbol on it is individually cheap — so the design problem becomes distributing symbols across more partitions in a way that spreads hot symbols apart, not adding more compute per symbol.

## Q zh
在 10 倍演进场景下，一个股票交易所设计从 8,000 支股票增长到 80,000 支，全市场峰值订单速率同比例增长到 3,000,000 单/秒。既然连负载最重的单支股票，其单线程撮合冗余都是所需算力的数千倍，为什么 10 倍演进的瓶颈在于“股票如何分配到分区”而不是“撮合引擎吞吐”？

## A zh
即使经过 10 倍增长，单支股票的撮合负载仍然远低于单线程能处理的量，所以不需要任何一个撮合引擎变得更快或更并行。真正的风险在序列化/分区层：如果股票被分配到序列化分区的方式恰好把好几支最热门的股票聚集到了同一个分区，即使这个分区上每支股票单独看都很轻量，这个分区的总负载也可能超出它的容量——所以真正要解决的设计问题是如何把股票分布到更多分区上、让热门股票彼此分开，而不是给单支股票增加更多算力。
