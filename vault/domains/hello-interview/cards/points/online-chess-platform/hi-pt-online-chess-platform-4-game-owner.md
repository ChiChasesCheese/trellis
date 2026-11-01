---
id: hi-pt-online-chess-platform-4-game-owner
node: qb.sd.online-chess-platform.points
type: qa
step: 4
---
## Q
**在线国际象棋平台 · 对局所有者与 actor 模型**｜出自：在线国际象棋平台 › 整体设计

一局棋的事件怎样路由才能不用分布式锁就有全序？所有者节点校验哪些内容？

## A
**路由。** 每局按哈希（gameId）固定到一台对局所有者节点，内存持有棋盘和时钟，每局用单线程队列（actor 模型）串行处理事件，走子、悔棋、超时天然全序。
**校验。** 是否轮到该方、`moveNo` 是否等于期望值、走法是否合法（用成熟的规则库）、时钟是否已耗尽。
