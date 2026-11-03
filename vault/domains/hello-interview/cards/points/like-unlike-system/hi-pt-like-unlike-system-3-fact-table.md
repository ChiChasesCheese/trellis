---
id: hi-pt-like-unlike-system-3-fact-table
node: qb.sd.like-unlike-system.points
type: qa
step: 3
---
## Q
**点赞与取消点赞系统 · 事实表与分片键**｜必会 · 出自：点赞与取消点赞系统 › 整体设计

点赞系统的事实表主键和分片键怎么选，才能让点查、列表都高效且热门内容不压垮分区？

## A
**要点。** 主键 (userId, itemId)，按 userId 哈希分片。
**效果。** 是否已点赞是一次主键点查，我的列表是分区内按 createdAt 的范围查。
**热点。** 一个内容的点赞者分散在各用户分区，热门内容不会让某分区过热。
