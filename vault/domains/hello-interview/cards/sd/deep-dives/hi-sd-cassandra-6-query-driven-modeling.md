---
id: hi-sd-cassandra-6-query-driven-modeling
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 6
---
## Q
**查询驱动建模：与关系库相反**｜系统设计 · 深入专题

从关系库转到 Cassandra，数据建模的思路要怎么变？建表时要考虑哪四件事？

## A
**要点。** 关系库按实体关系建模、规范化、靠外键和 JOIN。Cassandra 没有 JOIN、没有外键，只能高效回答单表查询，所以反过来：先列出访问模式（access patterns），再为每个查询设计一张表，必要时重复存数据（反规范化，denormalization）。

要考虑的四件事：

1. 分区键：查询能否落在一个分区，避免跨节点的散播与汇聚（scatter-gather）。
2. 分区大小：最坏情况下有多大，会不会无限增长。
3. 聚簇键：分区内怎么排序。
4. 反规范化：哪些数据要冗余到别的表。

**为什么。** 查询效率取决于数据怎么存放。

**取舍。** 少见的查询不值得单独建一张冗余表，可以用存储附加索引（SAI，全局二级索引）；物化视图（materialized view）能自动维护反规范化副本，省去应用层多表双写；也可经插件接 Elasticsearch、Solr。
