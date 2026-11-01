---
id: hi-sd-leetcode-7-leaderboard-scale
node: sd.problem-breakdowns.leetcode
type: qa
step: 7
---
## Q
**高效的实时排行榜**｜系统设计 · 问题拆解

比赛排行榜用数据库轮询、缓存定期刷新、Redis 有序集合加轮询三种做法，各有什么特点？为什么不必上 WebSocket？

## A
**差：轮询并查库。** 客户端每 5 秒轮询，服务器每次都对数据库聚合排序，库压力大、延迟随人数上升。

**中：Redis 缓存定期刷新。** 每 30 秒从数据库算一次放进缓存，客户端读缓存。数据库压力小了，但最多晚 30 秒，并有刷新竞态，适合小规模比赛。

**好：Redis 有序集合（sorted set）。** 处理一次提交时同时更新数据库和有序集合：键如 `competition:leaderboard:{competitionId}`，分数是成绩，成员是 userId，`ZADD` 更新，`ZRANGE ... REV WITHSCORES` 取前 N 名。读取不碰数据库，速度极快。先给客户端前 1000 名，翻页再取。

**取舍。** 客户端每 5 秒轮询就够：排行榜变化不频繁，5 秒延迟用户可接受，比 WebSocket 简单得多。还可以渐进轮询：比赛最后几分钟 2 秒一次，平时 10 秒一次。Staff 级的表现就是知道更复杂的方案是什么，并说明为什么对这个系统是过度设计。
