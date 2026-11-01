---
id: hi-sd-elasticsearch-7-inverted-index
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 7
---
## Q
**倒排索引、doc values 与查询规划**｜系统设计 · 深入技术

为什么 Elasticsearch 的关键词搜索很快？排序和聚合又靠什么？协调节点的查询规划（query planner）在优化什么？

## A
**倒排索引。** 加速查找有两种办法：按查询方式组织数据，或者复制一份按查询方式组织。倒排索引就是后者：词到文档列表的映射，找含「lazy」的书不必扫 10 亿本，直接查表。

**doc values。** 对匹配结果按价格排序时只要价格一列，行存要读整行。doc values 是某字段在整个段内的列式连续存储，与倒排索引配合：前者找文档，后者取排序所需的值。

**查询规划。** 搜「bill nye」，bill 有上百万条记录，nye 只有几百条，先从哪边求交集，性能差几个数量级。引擎靠词频、字段类型、文档长度等统计信息选择最省时的执行顺序。
