---
id: hi-c-sd-db-indexing-x01-pick-index
node: sd.core-concepts.db-indexing.exam
type: qa
step: 1
---
## Q
**数据库索引 · 给场景选索引类型**｜考点 · 必会
选择索引类型并说理由：A) 用户表按邮箱登录查询；B) 每秒 20 万条传感器读数的写入与按设备、时间范围查询；C) "附近 2 公里的外卖商家"；D) 文章内容的关键词搜索。

## A
- **A B 树：** 唯一约束自带 B 树，等值查找够快，还支持前缀与排序。
- **B LSM 类存储（如 Cassandra），分区键为设备、排序键为时间：** 写入量极高，追加为主，读按分区加时间范围，LSM 的顺序写与有序存放正好匹配。
- **C 地理索引：** geohash 配 B 树（或 Redis GEO），或 PostGIS 的 R 树；两个单列 B 树无法做二维邻近。
- **D 倒排索引：** 如 Elasticsearch，`LIKE '%词%'` 用不上 B 树。
- **答题套路：** 先说访问方式（等值、范围、邻近、全文、写入量），再对应结构。
