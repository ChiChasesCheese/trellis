---
id: hi-c-sd-online-chess-n03-entities-api
node: sd.problem-breakdowns.online-chess.notes
type: qa
step: 3
---
## Q
**在线象棋 · 实体与接口**｜摘要 · 必会

在线象棋有哪些核心实体？为什么匹配和榜单用 REST，对局用 WebSocket？

## A
- **实体：** Player（身份加 rating，rating 同时驱动匹配和榜单位置）；Game（黑白方、当前局面、轮到谁、棋钟、结果）；Move（起止格、步序号、时间，只追加，故障后重放即可重建棋盘）；MatchRequest（rating 与等待或已匹配状态）。
- **REST：** `POST /matchmaking` 返回 requestId，`GET /matchmaking/:id` 每隔几秒轮询，匹配成功时带 gameId；榜单是 `GET /leaderboard?cursor&limit` 和 `GET /players/:id/rank`。它们是一问一答。
- **WebSocket `/games/:gameId`：** 对局是持续的双向消息流。客户端发 `sendMove{move, moveNumber}`；服务端发 `gameState`、`moveAck`、`opponentMove`、`gameEnd`，都带双方剩余毫秒数。`moveNumber` 是期望的下一步序号，重试不会重复落子；连接或恢复时 `gameState` 把客户端补齐。
- **身份规则：** playerId 和 rating 取自会话或 JWT 与服务端 Player 记录，不放进请求体。客户端能撒谎来换取更容易对手的字段，都必须由服务端提供。
