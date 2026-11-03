---
id: hi-pt-online-chess-platform-11-leaderboard
node: qb.sd.online-chess-platform.points
type: qa
step: 11
---
## Q
**在线国际象棋平台 · 排行榜与异步版本**｜追问 · 出自：在线国际象棋平台 › 取舍与追问

top-K 排行榜用什么存？1 亿用户量级要多大？如果是聊天软件里 10 亿用户的异步好友对弈，架构怎么变？

## A
**排行榜。** Redis 有序集合（`ZADD`、`ZREVRANGE 0 99`），1 亿用户约几 GB，按时间制分集合，由 Elo 更新事件异步写入，最终一致；我的名次用 `ZREVRANK`。再大则按评分段分片，top-K 做分片 top-K 归并。
**异步版本。** 连接不常驻，走子写入后只推送通知；状态落按 gameId 分片的键值存储（DynamoDB 或 Cassandra）而非内存所有者；悔棋是对手尚未查看或未走时的一次条件写入（compare-and-set）。
