---
id: stream-select-does-not-advance
node: pipelines.stream-consumption-and-offset-advance
type: qa
source: snowflake-docs
---
## Q
开发者在显式事务中执行 `SELECT * FROM my_stream` 检查变更，然后 COMMIT。流的偏移量前移了吗？什么操作才会让它前移？

## A
没有前移。单纯查询流不会推进偏移量，即使在显式事务中也是如此。只有当流在 DML 事务中被使用时（例如 `INSERT INTO target SELECT … FROM my_stream`、MERGE、CTAS 或 `COPY INTO <location>`），并且事务成功提交，偏移量才会前移；这对显式事务和自动提交（autocommit）事务同样适用。
