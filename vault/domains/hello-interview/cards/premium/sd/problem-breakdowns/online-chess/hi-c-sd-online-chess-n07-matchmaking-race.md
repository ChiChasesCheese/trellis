---
id: hi-c-sd-online-chess-n07-matchmaking-race
node: sd.problem-breakdowns.online-chess.notes
type: qa
step: 7
---
## Q
**在线象棋 · 深入一：防止同一人匹配进两局**｜摘要 · 必会

Alice 在等人，Bob 和 Charlie 同时请求且 rating 都合适，怎么保证 Alice 只进一局？崩溃时会怎样？

## A
- **问题：** 两个请求各自查到 Alice 仍是 pending，在谁都没改状态前各建一局。单实例也会发生，因为服务能并发处理请求。这是**争用（contention）**：找到可用者不等于建局时它仍可用。
- **做法：** 一个 Postgres 事务：①`SELECT … FOR UPDATE` 锁 Bob 自己的请求，已不是 pending 就返回其 gameId；②`FOR UPDATE SKIP LOCKED` 挑一个 pending 对手，已被别人锁住的行直接跳过；③插入 Game，把两条请求标为 matched 并写 gameId；④提交，锁释放。
- **结果：** Charlie 撞上 Alice 被 Bob 锁住时会跳过去找别人；若在 Bob 提交后才查，Alice 已是 matched，查不到。无论哪种她只进一局。
- **崩溃：** 提交前崩溃则回滚，两人仍 pending，下次可重新配对；提交后崩溃则局已存好，客户端轮询就能拿到。
- **找不到人：** 结束事务让请求保持 pending，后台任务每隔几秒用同样步骤重试，并随等待时间放宽范围。
