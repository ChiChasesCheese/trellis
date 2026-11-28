---
id: hi-c-sd-leetcode-n09-leaderboard-options
node: sd.problem-breakdowns.leetcode.notes
type: qa
step: 9
---
## Q
**在线判题平台 · 深入二：实时排行榜的三种做法**｜摘要 · 必会

数据库轮询、缓存定期刷新、Redis 有序集合三种排行榜做法各有什么问题？为什么不用 WebSocket？

## A
- **差：轮询并查库。** 每个客户端每 5 秒触发一次聚合排序，库负载高、延迟随人数上升，比赛高峰时容易过载。
- **中：Redis 缓存定期刷新。** 每 30 秒从库里算一次放进缓存，客户端读缓存。库的压力降了，但数据最多晚 30 秒，且刷新频率过低还会有竞态，适合小比赛。
- **好：Redis 有序集合（sorted set）。** 处理一次提交时同时更新数据库和有序集合：键如 `competition:leaderboard:{id}`，分数是成绩，成员是 userId；用 `ZADD` 更新，`ZRANGE key 0 N-1 REV WITHSCORES` 取前 N 名（旧的 `ZREVRANGE` 已被取代）。读取不碰数据库，很快。首屏给前 1000 名，翻页再取。
- **刷新方式：** 客户端每 5 秒轮询。排行榜变化不算频繁，5 秒延迟用户可接受，比 WebSocket 简单得多；还可以渐进轮询，比赛最后几分钟 2 秒一次，其余时间 10 秒一次。
- **Staff 的表现：** 说得出 WebSocket 方案，并讲清它对这个规模是过度设计。
