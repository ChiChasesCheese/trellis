---
id: hi-ov-online-chess-2-options
node: sd.problem-breakdowns.online-chess
type: qa
step: 2
tags: [通览]
---
## Q
**在线象棋 · 高层设计**｜通览

在线象棋的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** API 网关、匹配服务、游戏服务器、Postgres。

**每条路径。**
- **匹配开局：** `POST /matchmaking` 经网关到匹配服务，写 pending 请求，找 rating 相近的另一条，建 Game 并标为 matched；双方轮询拿到 gameId。数据落 Postgres。
- **实时对局：** 双方凭 gameId 连 WebSocket；游戏服务器校验走法并算棋钟，走法与 Game 更新同事务落库，再推给双方。
- **看榜与名次：** 局终同一事务存结果与双方新 rating；榜单读 Players 表，前 50 名走 rating 索引。

**存储。** Postgres 存请求、对局、走法和 rating；棋盘与棋钟在游戏服务器内存，先落库再广播。
