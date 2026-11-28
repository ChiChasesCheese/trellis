---
id: hi-pt-realtime-game-leaderboard-7-friends-cost
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 7
---
## Q
**在线游戏排行榜 · 好友榜的读成本**｜必会 · 出自：在线游戏排行榜 › 深入 3

好友榜读时计算：每次对 500 个好友批量查分约 0.1 ms，读 1.2 万次/秒。单线程 Redis 扛得住吗？怎么办？

## A
**算账。** 1.2 万 × 0.1 ms = 1.2 核秒/秒，超出单线程 Redis。

**办法。** 把读分摊到 3–4 个只读从库；对每个玩家的好友榜缓存 5 秒。

**产品约束。** 好友数设上限（如 5,000），否则读成本无界。
