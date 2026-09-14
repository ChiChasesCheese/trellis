---
id: retention-period-edition-limits
node: continuity.retention-vs-failsafe
type: qa
source: snowflake-docs
---
## Q
Snowflake 时间旅行（Time Travel）的数据保留期（data retention period）默认是多长？在不同版本和表类型下可以设成多少？

## A
默认 1 天（24 小时），所有账户自动启用。标准版（Standard Edition）只能设为 0 或 1 天。企业版（Enterprise Edition）及以上：永久（permanent）数据库、模式、表可设为 0 到 90 天；临时性（transient）对象和临时表（temporary table）仍只能是 0 或 1 天。保留期设为 0 等于关闭该对象的时间旅行。
