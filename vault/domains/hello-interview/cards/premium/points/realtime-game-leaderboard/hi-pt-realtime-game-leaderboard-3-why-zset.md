---
id: hi-pt-realtime-game-leaderboard-3-why-zset
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 3
---
## Q
**在线游戏排行榜 · 为什么不用数据库排序**｜必会 · 出自：在线游戏排行榜 › 深入 1

用关系数据库存分数，名次用 `COUNT(*) WHERE score > x` 查，前 10 用 `ORDER BY score DESC LIMIT 10`。1 亿行、1.2 万次/秒下为什么不行，有序集合凭什么行？

## A
**为什么不行。** 名次查询要数索引区间，是 O(名次)，1 亿行下每次都很重。

**有序集合。** 内部是跳表加哈希表，更新、查名次、取区间都是对数时间。

**结论。** 数据库做真相（存最高分），有序集合做榜。
