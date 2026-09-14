---
id: retention-expiry-moves-to-failsafe
node: continuity.retention-vs-failsafe
type: qa
source: snowflake-docs
---
## Q
一张表的历史数据超过了时间旅行（Time Travel）保留期、进入故障保护（Fail-safe）之后，用户还能对它做哪些操作？

## A
用户自己什么都做不了：历史数据不能再被查询，过去的对象不能再被克隆，已删除的对象也不能再用 UNDROP 恢复。时间旅行是用户可自助操作的恢复窗口，而故障保护是保留期结束后的后续阶段，不再对用户开放这些 SQL 操作。
