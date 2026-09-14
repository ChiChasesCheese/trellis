---
id: profile-metadata-only-operators
node: query.reading-query-profile
type: qa
source: snowflake-docs
---
## Q
为什么 `SELECT COUNT(*) FROM t` 或 `CREATE SCHEMA` 在查询画像（Query Profile）中只有一个单步节点，而且不消耗虚拟仓库（virtual warehouse）？

## A
它们属于元数据算子（metadata operator），是纯元数据/目录操作而非数据处理。`SELECT COUNT(*)`、`SELECT CURRENT_DATABASE()` 这类 Metadata-based Result 查询的结果完全由元数据计算得出，不访问任何数据；CREATE、ALTER、DROP、COMMIT 等 DDL 与事务命令通常也不由虚拟仓库处理。因此它们的画像只有与该 SQL 对应的单个步骤。
