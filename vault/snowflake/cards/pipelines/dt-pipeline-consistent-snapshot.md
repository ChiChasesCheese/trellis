---
id: dt-pipeline-consistent-snapshot
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
多个互相依赖的动态表组成管道时，下游表会不会读到上游「刷了一半」的数据，或者两张上游表处于不同时间点？

## A
不会。Snowflake 从各表的查询中自动推断依赖图（无需手动声明依赖或编排顺序），为管道选取一致的快照时间戳，并按依赖顺序刷新，使下游表总是看到其上游输入的一致视图。每次刷新的新结果也是原子地写入动态表，读者永远看不到部分完成的刷新。
