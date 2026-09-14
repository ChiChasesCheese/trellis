---
id: profile-exploding-join
node: query.reading-query-profile
type: qa
source: snowflake-docs
---
## Q
在查询画像（Query Profile）中，“爆炸式连接（exploding join）”有什么特征？常见成因是什么？

## A
特征：Join 算子输出的元组数远多于输入（经常多出几个数量级），并且该 Join 算子通常耗时很长。常见成因：连接时漏写了连接条件，产生笛卡尔积（Cartesian product）；或连接条件让一张表的每条记录匹配到另一张表的多条记录。另外，Join 节点的 Additional Join Condition 中若出现非等值连接谓词，处理可能明显变慢，应尽量避免。
