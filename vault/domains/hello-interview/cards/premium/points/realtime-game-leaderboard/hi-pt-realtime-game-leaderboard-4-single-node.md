---
id: hi-pt-realtime-game-leaderboard-4-single-node
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 4
---
## Q
**在线游戏排行榜 · 第一版不要分片**｜必会 · 出自：在线游戏排行榜 › 深入 1

1 亿玩家的榜，面试时是否一开始就要分片？可用性和数据丢失怎么处理？

## A
**要点。** 不要。10 GB 单机放得下，写 1.2 万次/秒远低于单机约 10 万次/秒；第一版是一个有序集合加一个从库加 AOF 持久化。

**可用性。** 主从复制加自动故障转移。

**恢复。** Redis 的榜是派生数据，从最高分表重建：1 亿条 ÷ 10 万条/秒 ≈ 1,000 秒。
