---
id: hi-c-sd-data-modeling-n11-wide-column
node: sd.core-concepts.data-modeling.notes
type: qa
step: 11
---
## Q
**数据建模 · 宽列数据库**｜摘要 · 追问
宽列数据库为什么写入特别快？适合哪类数据，建模上要怎么改变思路？

## A
- **结构：** 数据按列族（column family）组织，不同行可以有不同的列集合。
- **为什么写快：** 新帖按 (user_id, timestamp) 作键写入，同一分区键（user_id）的数据物理上存在一起，写入只是追加到该分区，读取用户的帖子则是扫描一段连续范围。
- **适用：** 写入量巨大、时间序列、以追加和聚合为主的分析，如遥测、事件日志、IoT 传感器数据。
- **建模影响：** 比 SQL 更加"围绕查询设计"，常为不同访问方式在不同列族里复制数据；时间是一等公民。例：Cassandra、HBase。
