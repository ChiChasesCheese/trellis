---
id: table-types-min-retention-override
node: storage.table-types
type: qa
source: snowflake-docs
---
## Q
账户管理员设置了 `MIN_DATA_RETENTION_TIME_IN_DAYS = 7`，某开发者把自己的表 `DATA_RETENTION_TIME_IN_DAYS` 设为 0 想省存储费，实际保留期是多少？

## A
7 天。设置账户级 MIN_DATA_RETENTION_TIME_IN_DAYS 后，对象的有效保留期为 MAX(DATA_RETENTION_TIME_IN_DAYS, MIN_DATA_RETENTION_TIME_IN_DAYS)，较大者优先。这个参数不会改写表上设置的值，但会改变有效保留期，从而让管理员为全账户兜底，防止个别对象关闭 Time Travel（时间旅行）后被误删而无法恢复。
