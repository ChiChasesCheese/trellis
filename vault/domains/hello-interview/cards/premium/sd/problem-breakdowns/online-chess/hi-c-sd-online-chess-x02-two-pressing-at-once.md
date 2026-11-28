---
id: hi-c-sd-online-chess-x02-two-pressing-at-once
node: sd.problem-breakdowns.online-chess.exam
type: qa
step: 2
---
## Q
**在线象棋 · 预测：两个人同一瞬间点"找对局"**｜考点 · 必会

匹配事务先 `FOR UPDATE` 锁自己的请求，再 `FOR UPDATE SKIP LOCKED` 找对手。Alice 和 Bob 是仅有的两个等待者，同一毫秒各开一个事务。会发生什么？如果去掉 `SKIP LOCKED` 又会怎样？

## A
- **有 `SKIP LOCKED`：** 两个事务各锁住自己的请求；各自搜对手时，对方那行已被对方事务锁住，被跳过，于是都得到"没有对手"，两人保持 pending，不会建出两局，也不会死锁。几秒后后台重试任务单独处理其中一人，才把他们配上。代价是多等一个重试周期。
- **去掉 SKIP LOCKED 会死锁：** 去掉 `SKIP LOCKED`（只有 `FOR UPDATE`）：Alice 的事务要等 Bob 持有的锁，Bob 的事务要等 Alice 持有的锁，形成死锁。Postgres 在 `deadlock_timeout`（默认 1 秒）后检测到并终止其中一个，被终止的请求要重试；用户感到卡顿，而且高并发下死锁反复出现。
- **为什么先锁自己：** 请求处理和后台重试可能同时处理同一条请求，先锁自己能保证一条请求只被一个事务推进；锁住后若已 matched，直接返回它的 gameId。
- **要点：** 这个选择说明"调度上宁可漏配一次，由重试补上，也不要重复匹配或死锁"。
