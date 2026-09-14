---
id: table-types-choose-transient-for-staging
node: storage.table-types
type: qa
source: snowflake-docs
---
## Q
ETL 流水线每天会整表重建一张中间结果表，出错了随时可以从上游重跑。这张表该用永久表（permanent）还是瞬态表（transient）？为什么？

## A
用瞬态表。它的 Time Travel（时间旅行）保留期最多 1 天，且被修改或删除的历史数据不会进入 Fail-safe（故障保护），直接删除。频繁整表重建会产生大量被替换的历史数据，永久表会把这些数据长时间保留在 Time Travel 和 Fail-safe 中并计入存储费用；而对可随时重跑的数据来说，这种保护没有价值。
