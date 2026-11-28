---
id: hi-c-sd-time-series-databases-n11-query
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 10
---
## Q
**时序数据库 · 查询执行**｜摘要 · 必会

执行 `SELECT mean(value) ... WHERE host='server-1' AND time > now()-1h GROUP BY time(5m)` 时，时序库按什么顺序工作？

## A
1. **按时间选分区：** 只考虑与查询时间范围重叠的分区。
2. **按标签找序列：** 在内存标签索引里查 `host='server-1'`，得到序列集合。
3. **读数据：** 缓冲里有最新数据，磁盘文件里有较旧数据，两边结果合并。
4. **边读边聚合：** 流式计算均值，不需要先把所有数据装进内存。

- **核心洞察：** 利用时间局部性（最近数据在内存或最近的文件）和序列局部性（同一序列的点存在一起），尽量少碰磁盘。
