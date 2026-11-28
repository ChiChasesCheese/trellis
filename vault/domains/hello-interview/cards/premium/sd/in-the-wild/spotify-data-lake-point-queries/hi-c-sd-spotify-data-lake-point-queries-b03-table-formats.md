---
id: hi-c-sd-spotify-data-lake-point-queries-b03-table-formats
node: sd.in-the-wild.spotify-data-lake-point-queries.beyond
type: qa
step: 3
---
## Q
**Spotify 数据湖点查 · 湖表格式（Iceberg、Delta、Hudi）做了什么**｜拓展 · 加分

行业里把"元数据层"放进数据湖已成惯例。这类表格式与本案例的索引思路有何异同？

## A
- **做了什么：** Apache Iceberg、Delta Lake、Apache Hudi 在对象存储的文件之上维护元数据层：快照、清单文件、每个数据文件的列统计，让引擎不必列出目录就能知道该读哪些文件，并支持事务性的提交、时间旅行。
- **和案例相同的思想：** 用独立于数据文件的元数据做剪枝（文件级最小最大值、分区剪枝），写入时可按某列排序或聚簇（clustering）使统计更有效。
- **不同：** 这些元数据多数只能排除文件，告诉你"哪些文件可能含有该键"，但不会精确到行号；RAP 这类索引精确到文件内的行。因此点查场景下表格式能减少文件，但文件内部的依赖读仍存在。
- **取舍：** 小文件太多会让元数据膨胀，需要定期合并（compaction）；元数据层本身要维护和并发提交，是新的运维对象。
