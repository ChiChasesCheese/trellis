---
id: hi-sd-fb-live-comments-2-post-store
node: sd.problem-breakdowns.fb-live-comments.exam
type: qa
step: 2
---
## Q
**发评论的基础链路与存储选型**｜系统设计 · 题目拆解

直播评论系统里，用户发一条评论，请求要经过哪些组件、最终存在哪里？为什么评论库可以选 DynamoDB，换成 Postgres 或 MySQL 行不行？

## A
**链路。** 评论客户端（Commenter Client）带令牌调用 `POST /comments/:liveVideoId`，评论管理服务（Comment Management Service）校验请求，把评论写入评论库。同一个服务之后也负责查询历史评论。

**选型。** 评论是简单记录，没有复杂关联，也不需要跨行事务；需要的是高写入、高可用、可水平扩展，DynamoDB 正合适：以直播视频 ID 作分区键、评论 ID 作排序键，同一场直播的评论物理上连续，后面的游标分页也能直接用键范围查询。

**取舍。** Postgres 或 MySQL 同样能用，只是水平扩展要自己分片；面试里说清“为什么够用”比押注某个产品更重要。
