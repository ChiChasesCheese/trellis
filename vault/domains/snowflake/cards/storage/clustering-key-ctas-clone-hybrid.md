---
id: clustering-key-ctas-clone-hybrid
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
以下三种情况下 Snowflake 表的聚簇键（clustering key）会怎样：① `CREATE TABLE ... CLONE` 复制表；② `CREATE TABLE ... AS SELECT` 建表；③ hybrid table（混合表）？

## A
① CLONE 会复制原有聚簇键，但克隆表上的自动聚簇（Automatic Clustering）处于暂停状态，需要手动恢复，否则不会维护。② CTAS 不支持带过来原有聚簇键，但建表后可以再定义。③ 混合表不能定义聚簇键，其数据始终按主键排序。另外，修改聚簇键不会立刻影响现有记录，要等 Snowflake 重新聚簇后才生效。
