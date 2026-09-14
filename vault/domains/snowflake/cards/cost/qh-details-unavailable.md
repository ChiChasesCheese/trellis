---
id: qh-details-unavailable
node: cost.query-history-and-account-usage
type: qa
source: snowflake-docs
---
## Q
在 Snowsight 中打开一条查询，却看不到 Query Details 或 Query Profile；另一条 10 天前的查询没有显示执行用户。可能的原因有哪些？

## A
查询详情不可用的常见原因：查询仍在运行（结束后才有详情和 profile）；当前角色无权查看；查询发生在 14 天以前；查询执行失败因此没有 profile；详情和 profile 指标的保存本身是尽力而为（best-effort），不保证每条都有。超过 7 天的查询不显示 User 信息，这是由会话数据的保留策略决定的，但仍可用用户过滤器按用户检索。
