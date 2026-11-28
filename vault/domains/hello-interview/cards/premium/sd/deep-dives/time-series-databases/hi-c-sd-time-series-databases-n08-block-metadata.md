---
id: hi-c-sd-time-series-databases-n08-block-metadata
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 14
---
## Q
**时序数据库 · 块级元数据**｜摘要 · 追问

时序库如何用块级元数据（block-level metadata）在扫描文件时跳过整块数据？

## A
- **做法：** 每个数据块额外记录最小/最大时间戳，有时还记录最小/最大值。
- **用法：** 查询「CPU 高于 10%」时，若某块元数据显示只含 0–5% 的值，整块不用读，直接跳过（块裁剪，block pruning）。
- **位置：** 它和时间分区叠加：分区先排除整段时间，块元数据再在分区内排除块，数据量再大也能保持查询快。
- **同类想法：** 搜索引擎的查询规划也是先用统计信息排除不可能的段。
