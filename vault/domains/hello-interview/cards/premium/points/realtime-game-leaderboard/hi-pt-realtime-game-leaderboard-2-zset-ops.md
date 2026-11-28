---
id: hi-pt-realtime-game-leaderboard-2-zset-ops
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 2
---
## Q
**在线游戏排行榜 · 有序集合的三个命令**｜必会 · 出自：在线游戏排行榜 › 整体设计

用 Redis 有序集合存全球榜，提交分数、查前 10、查我的名次和上下各 5 名分别用哪个命令？

## A
**提交。** `ZADD key GT score playerId`，`GT` 表示只在新分更高时更新，保留最高分。
**前 10。** `ZREVRANGE 0 9 WITHSCORES`。
**名次。** `ZREVRANK`（从 0 开始，显示时加 1），上下各 5 名用 `ZREVRANGE rank-5 rank+5`。

三者都是 O(log n + k)。前 10 对所有人相同，进程内缓存 1 秒。
