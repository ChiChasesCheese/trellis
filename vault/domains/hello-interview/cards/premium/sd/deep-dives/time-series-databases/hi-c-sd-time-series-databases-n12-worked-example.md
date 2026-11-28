---
id: hi-c-sd-time-series-databases-n12-worked-example
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 11
---
## Q
**时序数据库 · 多标签查询走一遍**｜摘要 · 必会

4 个序列（server-1 到 4，分属 us-west/us-east、prod/staging），查「us-west 的 prod 服务器平均 CPU」时数据库怎么执行，为什么比 Postgres 快？

## A
- **组织方式：** 指标加标签的每个唯一组合是一个序列；每个序列的点连续存成一个压缩块，文件末尾的索引把序列键映到块。示例里每块约 13 字节，原始 32 字节，约省 60%。
- **标签索引：** 内存里把「标签值」映到序列列表，本质是倒排索引（inverted index），和 Elasticsearch 同一种结构：`region=us-west` 得 [S1, S2]，`env=prod` 得 [S1, S2, S3]。
- **执行：** 取两个集合的交集得 [S1, S2]；查文件索引得块 0 和 1；只读这两块，跳过 us-east 的块；套时间过滤；算均值。
- **为什么快：** 不用扫数据就知道哪些序列匹配，且同序列数据物理相邻。Postgres 即使有索引，也要从分散位置逐行取回再提取列。
