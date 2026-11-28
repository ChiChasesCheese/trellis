---
id: hi-c-sd-online-chess-x03-plain-for-update
node: sd.problem-breakdowns.online-chess.exam
type: qa
step: 3
---
## Q
**在线象棋 · 比较：不加 SKIP LOCKED，匹配事务会怎样**｜考点 · 必会

对手查询写成 `WHERE status='pending' AND rating BETWEEN … ORDER BY createdAt LIMIT 1 FOR UPDATE`（没有 `SKIP LOCKED`）。1000 个请求同时匹配，等待队列里最老的是 Alice。吞吐会怎样？结果还对吗？

## A
- **行为：** 所有事务按 `createdAt` 排序后都选中最老的 Alice，第一个拿到行锁，其余 999 个阻塞，直到它提交。提交后 Alice 已是 matched，下一个事务重新检查条件、转而锁下一个最老的 pending，其余继续排队。
- **正确性：** 没有出错。在 Postgres 16 上实测，拿到锁后条件不再满足的事务会顺延到下一行，不会重复匹配。
- **吞吐：** 全部事务挤在同一行上排队，一次只有一个能推进，把并发匹配变成串行，延迟随并发线性变长。这是"结果正确但排队过长"的失败。
- **`SKIP LOCKED`：** 被别人锁住的行直接跳过，各事务当场锁住不同的 pending 行，并行推进。代价：看到的是"当前没被锁的行"，不保证严格按等待先后配对。
- **规则：** 要"任意挑一个可用行"（等待池、库存池）用 `SKIP LOCKED`；要"必须是这一行"才用普通行锁。
