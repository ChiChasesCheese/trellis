---
id: hi-sd-fb-live-comments-3-pagination
node: sd.problem-breakdowns.fb-live-comments
type: qa
step: 3
---
## Q
**历史评论分页：偏移还是游标**｜系统设计 · 题目拆解

直播评论要支持用户向上滚动、不断加载更早的评论（无限滚动）。请比较偏移分页（offset）和游标分页（cursor），并说明在 DynamoDB 里怎样实现游标。

## A
**偏移分页（差）。** 请求带 `offset=N`。数据库要数过前面 N 行才能返回，评论越多越慢；更要命的是不稳定：滚动过程中有评论新增或删除，偏移就错位，用户会看到重复或漏掉的评论。

**游标分页（好）。** 请求带“上一页最后一条评论的 ID”。只要游标字段有索引，数据库直接定位，不用数前面的行，性能不随评论量增长；新增评论不会改变游标指向的位置，所以稳定。

**DynamoDB 实现。** 条件为“分区键等于 liveVideoId 且排序键 commentId 小于 cursor”，`ScanIndexForward=false`（倒序），`Limit=pageSize`。

**残余成本。** 每翻一页仍要查一次库，高流量下依然可观。
