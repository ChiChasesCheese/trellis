---
id: vectorized-vs-mapreduce-materialization
node: query.vectorized-columnar-execution
type: qa
tags: [grown]
---
## Q
与 MapReduce 风格的执行相比，Snowflake 的向量化流水线执行在中间结果处理上有什么不同？这为什么重要？

## A
MapReduce 通常在阶段之间把中间结果完整物化（写到磁盘）后再交给下一阶段。Snowflake 避免物化中间结果：数据以列式批次在算子之间流水线式流动，上一个算子产出一批，下一个算子立刻处理。这省去了大量中间结果的 I/O，也更好地利用了 CPU 缓存，对多算子串联的分析查询尤其明显。
