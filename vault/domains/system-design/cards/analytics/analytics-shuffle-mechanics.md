---
id: analytics-shuffle-mechanics
node: analytics.batch
type: qa
---
## Q
Walk through what a shuffle actually does in Spark/MapReduce, and why it's the step that dominates job cost.

## A
1. Each map task **partitions its output by hash of the key** (one bucket per reducer) and spills sorted bucket files to local disk.
2. Every reduce task then **fetches its bucket from every map task** over the network and merges the sorted runs, so all records with the same key land on one machine.

It dominates because it's an **all-to-all barrier**: M×R network transfers, full materialization to disk, and downstream stages can't start until it completes. Wide operations (`groupByKey`, joins, `repartition`) trigger it; the core optimization in any batch job is shuffling **fewer bytes, fewer times** (pre-aggregate map-side, broadcast small tables).

## Q zh
走过 Spark/MapReduce 中 shuffle 实际做什么，为什么它是支配 job 代价的步骤。

## A zh
1. 每个 map task **按 key 的 hash 分区其输出**（每个 reducer 一个桶）并溅出排序桶文件到本地磁盘。
2. 每个 reduce task 然后**从每个 map task 通过网络获取其桶**并合并排序的 run，所以相同 key 的所有记录落地在一台机器。

它支配因为它是**全到全屏障**：M×R 网络转移、完整物化到磁盘、下游阶段无法启动直到它完成。宽操作（`groupByKey`、join、`repartition`）触发它；任何 batch job 的核心优化是 shuffle **更少字节、更少次**（pre-aggregate map-side、broadcast 小表）。
