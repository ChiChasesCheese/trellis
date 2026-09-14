---
id: profile-details-unavailable
node: query.reading-query-profile
type: qa
source: snowflake-docs
---
## Q
在 Snowsight 的 Query History 中点开一条查询，却看不到查询详情和查询画像（Query Profile），可能有哪些原因？

## A
可能原因：① 查询仍在运行，结束后才能查看详情与画像；② 当前角色没有查看该查询详情的权限；③ 查询运行于 14 天之前，详情和画像已不可用；④ 查询执行失败，因此没有画像；⑤ 画像指标的深度本身只是尽力而为（best-effort），并不保证对所有查询都完整保留。
