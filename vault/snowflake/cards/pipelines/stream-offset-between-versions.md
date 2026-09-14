---
id: stream-offset-between-versions
node: pipelines.stream-offset-bookmark
type: qa
source: snowflake-docs
---
## Q
源表已提交了 v1 到 v10 共 10 个版本，流 `s1` 的偏移量位于 v3 与 v4 之间。查询 `s1` 会返回哪些变更？表版本又是何时产生的？

## A
每当包含一条或多条 DML 的事务提交到表上，就产生一个新的表版本。流的偏移量位于两个版本之间，查询时返回的是偏移量之后提交、截至当前时刻的所有事务的变更，也就是从 v4 到 v10（含）的变更。并且流返回的是从偏移量到当前版本的最小变更集（净变化），而不是逐条事务的流水。
