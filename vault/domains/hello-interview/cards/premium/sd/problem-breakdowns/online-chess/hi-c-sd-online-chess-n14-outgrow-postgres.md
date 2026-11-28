---
id: hi-c-sd-online-chess-n14-outgrow-postgres
node: sd.problem-breakdowns.online-chess.notes
type: qa
step: 14
---
## Q
**在线象棋 · 追问：匹配池放不进 Postgres 怎么办**｜摘要 · 追问

在 Postgres 里做匹配撑得住吗？撑不住时怎样把等待池搬到 Redis，会引入什么新故障？

## A
- **先算：** 50 万局、平均 2 分钟，每秒约 4000 局结束（500000÷120≈4167）；双方立即再来一局，约 8000 次匹配请求/秒。这个量本身不说明 Postgres 不行：给等待请求按 rating 建索引、事务保持短、连同对局写入和状态轮询一起压测。
- **搬到 Redis：** 等待池做成有序集合，成员 requestId、分数 rating，按分数范围搜。竞争还在，所以"找对手并把两人移出池"必须原子，用 Lua 脚本：先 `ZREM` 自己（已不在池中说明被别人领走了，直接退出，也避免匹配到自己），再 `ZRANGEBYSCORE` 取窗口内一个，找到就 `ZREM` 并返回，找不到就把自己 `ZADD` 回去。
- **Redis 配出一对后：** 仍要跑 Postgres 事务锁住两条请求、确认都还 pending、建 Game、标 matched；任一已被匹配就拒绝这一对。客户端继续轮询 Postgres。
- **新故障：** 从 Redis 移出一对后服务崩溃、局还没建。后台任务找出在 Postgres 里仍是 pending 的请求，放回池中。
- **结论：** 本设计用 Postgres；匹配搜索成为实测瓶颈或面试官要求更大规模时再上 Redis。
