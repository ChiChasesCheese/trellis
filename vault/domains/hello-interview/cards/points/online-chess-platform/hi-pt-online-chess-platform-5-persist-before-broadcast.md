---
id: hi-pt-online-chess-platform-5-persist-before-broadcast
node: qb.sd.online-chess-platform.points
type: qa
step: 5
---
## Q
**在线国际象棋平台 · 先持久后广播**｜必会 · 出自：在线国际象棋平台 › 整体设计

所有者校验走子通过后，持久化和广播谁先谁后？这样做防止什么？

## A
**要点。** 先把 `(moveNo, move, 本步用时, 双方剩余时间)` 追加写入 Redis 的该局日志（也可同步写一条 Kafka 记录），再向双方和观战频道广播 `move_applied`。
**为什么。** 所有者宕机时才不会出现观众看见了而存储里没有的步。
