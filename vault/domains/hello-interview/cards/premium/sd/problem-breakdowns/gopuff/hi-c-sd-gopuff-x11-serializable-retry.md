---
id: hi-c-sd-gopuff-x11-serializable-retry
node: sd.problem-breakdowns.gopuff.exam
type: qa
step: 21
---
## Q
**即时配送库存 · 并发下单：SERIALIZABLE 失败后怎么办**｜考点 · 必会

两个用户同时下单，都要买仅剩的 3 包薯片（库存表一行一件实物）。事务隔离级别 SERIALIZABLE 下，两个事务都读到「有货」后都想更新。会发生什么？应用要做什么？有没有更轻的写法？

## A
- **结果：** Postgres 会让其中一个提交失败，报序列化失败（错误码 40001），另一个成功；失败不等于缺货，只是并发冲突。
- **应用要做：** 捕获 40001 并重试整个事务，重试时重新读库存：若已无货就向用户返回明确的缺货信息，若还有就继续。必须限制重试次数，并保证事务里没有外部副作用（比如发邮件）。
- **更轻的写法：** 条件更新：`UPDATE inventory SET status='ordered' WHERE id = ANY(:ids) AND status='available'`，检查影响行数是否等于要买的件数，不等就回滚。这在 READ COMMITTED 下就是原子的，冲突的更新会等待行锁，不需要 SERIALIZABLE。
- **多件商品：** 若显式加行锁（`FOR UPDATE`），所有事务按同一顺序（如按 id 排序）加锁，避免 A、B 交叉等待形成死锁。
- **取舍：** SERIALIZABLE 最省心也最保守，会有误报的冲突；条件更新是更精确的乐观写法。
