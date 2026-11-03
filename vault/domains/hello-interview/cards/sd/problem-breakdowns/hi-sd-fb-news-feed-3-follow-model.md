---
id: hi-sd-fb-news-feed-3-follow-model
node: sd.problem-breakdowns.fb-news-feed.exam
type: qa
step: 3
---
## Q
**用键值库建模关注关系**｜系统设计 · 问题拆解

关注关系是多对多的图。为什么不用图数据库？在键值库（DynamoDB）里怎样存才能支持常见查询？

## A
**要点。** 图数据库适合遍历和推荐，比如朋友的朋友。这里只有简单查询，用图库会引来「Neo4j 怎么扩展」之类的额外问题，所以用键值库自己建模。

Follow 表：分区键 userFollowing，排序键 userFollowed；再建一个全局二级索引（GSI），键反过来（分区键 userFollowed，排序键 userFollowing）。三种查询：
- 是否已关注：用分区键加排序键精确查找。
- 我关注了谁：按分区键范围查询。
- 谁关注了我：查 GSI 的范围。

**取舍。** AWS 推荐 DynamoDB 单表设计，但面试里分开建表讨论更清晰，也完全可以。

**使用时机。** 只在需要多跳遍历时才引入图数据库。
