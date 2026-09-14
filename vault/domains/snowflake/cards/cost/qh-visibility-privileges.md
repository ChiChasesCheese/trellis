---
id: qh-visibility-privileges
node: cost.query-history-and-account-usage
type: qa
source: snowflake-docs
---
## Q
一名分析师在 Snowsight 的 Query History 里只能看到自己的查询。要让他看到别人在某个仓库上跑的查询，或者看到全账户的查询，分别需要什么权限？

## A
用户总能看到自己运行的查询。当前角色对某仓库有 MONITOR 或 OPERATE 权限时，可以看到其他用户在该仓库上的查询。要看全账户的查询，角色需要是 ACCOUNTADMIN，或在 SNOWFLAKE 数据库上被授予 IMPORTED PRIVILEGES。仅授予 GOVERNANCE_VIEWER 数据库角色可以直接用 SQL 查询 ACCOUNT_USAGE 视图并查看 Grouped Queries，但不足以在 Snowsight 中查看其他用户的单条查询。
