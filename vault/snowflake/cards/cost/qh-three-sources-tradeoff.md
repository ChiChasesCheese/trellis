---
id: qh-three-sources-tradeoff
node: cost.query-history-and-account-usage
type: qa
source: snowflake-docs
---
## Q
查看 Snowflake 查询历史有三个入口：Snowsight 的 Query History 页面、`SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` 视图、`INFORMATION_SCHEMA.QUERY_HISTORY` 表函数。它们在数据延迟和保留期上怎么取舍？

## A
Snowsight Query History 页面：可交互浏览最近 14 天的查询，含查询详情和 Query Profile，适合排查单条查询。INFORMATION_SCHEMA 表函数：几乎无延迟，但只保留最近 7 天，且结果受当前角色权限限制，适合实时查看刚跑完的查询。ACCOUNT_USAGE 视图：有延迟（可达数小时），但保留约 365 天并覆盖整个账户，适合做长期趋势分析和成本报表。
