---
id: hi-pt-coding-contest-platform-6-leaderboard
node: qb.sd.coding-contest-platform.points
type: qa
step: 6
---
## Q
**在线判题与编程竞赛平台 · Redis 有序集合排行榜**｜必会 · 出自：在线判题与编程竞赛平台 › 深入 3

10 万人按「解题数降序、用时升序」排名，怎样用 Redis 有序集合实现？复杂度和分数怎么编码？

## A
**分数。** 编码成一个数：`score = 解题数 × 10^7 − 总用时秒数`（总用时小于 10^7 秒，不会进位）。
**操作。** 通过一题时 `ZADD`；前 N 名 `ZRANGE ... REV`；某用户名次 `ZREVRANK`，都是 O(log N)。
**对比。** 每次查提交表聚合会压垮数据库；定时缓存整榜则延迟取决于刷新周期。
