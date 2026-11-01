---
id: hi-sd-time-series-databases-7-data-model-query
node: qb.sd.top-k-counts.pre-sd-deep-dives-time-series-databases
type: qa
step: 7
---
## Q
**时序库的数据模型与查询过程**｜系统设计 · 深入专题

时序库里的指标、标签（tag）、字段（field）分别是什么？一个多标签查询是怎么执行的，为什么比 Postgres 快？

## A
**数据模型。** 一个数据点：`cpu_usage,host=server-1,region=us-west value=45.2 <时间戳>`。度量名（measurement）像表名；标签是被索引的元数据，用来过滤（host、region、service）；字段是实际测量值，不建索引；再加上时间戳。度量名加标签的每个唯一组合是一个序列（series）。标签字段用错，会导致查询慢或基数爆炸。

**存储引擎。** 先写预写日志（WAL）保证持久；同时写内存缓冲；达到阈值后刷成不可变的压缩文件（时间戳列与值列分别压缩）；后台压缩合并。文件末尾有索引：序列 → 数据块偏移，查一个序列只需先查索引、再读数据，两次磁盘操作。

**查询过程**（地区为 us-west 且环境为 prod 的平均 CPU）：
1. 按时间过滤选出相关分区
2. 查内存里的标签索引（本质是倒排索引，和 Elasticsearch 一样，只是映射标签值到序列），得到各条件的序列集合，求交集
3. 用文件索引找到块位置，只读这些块，跳过其他
4. 流式聚合，不必把数据全加载到内存

**为什么快。** 同一序列的数据在磁盘上物理相邻；Postgres 即使有索引，也要从分散的位置逐行取数。
