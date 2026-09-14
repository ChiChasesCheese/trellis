---
id: qh-grouped-parameterized-hash
node: cost.query-history-and-account-usage
type: qa
source: snowflake-docs
---
## Q
一个基于混合表的应用每分钟执行数万条只有用户 ID 不同的点查。为什么逐条查看查询历史没有意义？应该用什么视图？

## A
海量相似的短查询无法逐条分析，而且 Individual Queries 列表本身也不会反映 Unistore 负载的全部查询。应使用 Grouped Query History（基于 ACCOUNT_USAGE 的 `AGGREGATE_QUERY_HISTORY` 视图）：按参数化查询哈希（parameterized query hash，把字面量替换成参数后的语句指纹）分组，展示每组的总执行次数、失败次数、p50/p90/p99 延迟和每分钟执行次数，用来回答“哪类语句消耗最多时间、性能是否随时间退化、失败率多少”。分组列表的更新延迟最多约 3 小时，只保留最近 14 天。
