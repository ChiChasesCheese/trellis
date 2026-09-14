---
id: qh-query-tag-attribution
node: cost.query-history-and-account-usage
type: qa
source: snowflake-docs
---
## Q
多个团队和调度作业共用同一个仓库和同一个服务账号，事后想从查询历史里区分出“哪个作业跑了哪些查询”，最简单的办法是什么？

## A
在会话中设置 `QUERY_TAG` 会话参数（例如 `ALTER SESSION SET QUERY_TAG = 'team=finance;job=daily_revenue'`）。该会话中执行的每条查询都会带上这个标签，可以在 Snowsight 的 Query History 中按 Query Tag 过滤，也可以在 QUERY_HISTORY 视图中按标签列分组汇总耗时和扫描量。没有标签时，共用账号和仓库的查询在历史里无法区分来源。
