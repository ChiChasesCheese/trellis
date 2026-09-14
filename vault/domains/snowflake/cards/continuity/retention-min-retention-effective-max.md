---
id: retention-min-retention-effective-max
node: continuity.retention-vs-failsafe
type: qa
source: snowflake-docs
---
## Q
账户级设置了 `MIN_DATA_RETENTION_TIME_IN_DAYS = 7`，某张表显式设置了 `DATA_RETENTION_TIME_IN_DAYS = 0`。这张表实际的保留期是多少？为什么要有这个参数？

## A
实际保留期是 7 天：有效保留期 = MAX(`DATA_RETENTION_TIME_IN_DAYS`, `MIN_DATA_RETENTION_TIME_IN_DAYS`)。这个账户级参数只能由 ACCOUNTADMIN 设置，它不修改各对象自己的参数值，而是强制一个下限，防止个别用户把重要表的保留期调成 0 后，一旦误删就无法恢复。
