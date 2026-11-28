---
id: hi-pt-realtime-game-leaderboard-10-anti-cheat
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 10
---
## Q
**在线游戏排行榜 · 防作弊与幂等提交**｜追问 · 出自：在线游戏排行榜 › 深入 6

排行榜怎样防作弊？同一局分数被重复提交怎么办？

## A
**防作弊。** 分数只由游戏服务器提交且带签名，不信任客户端；超过物理上限的异常分数进复核队列，复核后可从榜上删除（`ZREM` 并改库）。

**幂等。** 提交带幂等键（`gameId + matchId`），同一局重复提交结果不变。
