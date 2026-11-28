---
id: hi-c-sd-online-chess-n04-matchmaking-flow
node: sd.problem-breakdowns.online-chess.notes
type: qa
step: 4
---
## Q
**在线象棋 · 高层设计一：匹配**｜摘要 · 必会

玩家点"找对局"之后，最朴素的匹配流程是怎样的？卡在多久之后怎么办？

## A
- **组件：** 客户端、API 网关（认证、限流、转发）、匹配服务、Postgres（`MatchRequests` 记录等待者及 rating，`Games` 记录对局、黑白方和状态）。
- **流程：** `POST /matchmaking` → 服务端查出玩家 rating，写一条 pending 请求 → 查 rating 在 ±200 内的另一条 pending → 找到就建 Game、把两条请求标为 matched 并写入同一个 gameId → 双方轮询 `GET /matchmaking/:id` 拿到 gameId 后连游戏服务器。
- **等不到人：** 约 30 秒后放宽 rating 范围再试，最终超时并提示稍后再来，不让玩家无限等。范围越宽对局越快，但实力越悬殊，这是匹配质量与等待时间的取舍。
- **遗留问题：** 并发请求可能把同一个等待者匹配进两局，留给深入一。
