---
id: hl-sd02-db-polling
node: system-design.sd02-job-scheduler
type: qa
step: 9
---
## Q
最朴素的「轮询数据库」方案怎么写？它的优点、五个缺点是什么？什么时候它是对的答案？

## A
做法：`INSERT INTO jobs(id, fire_at, state='SCHEDULED', ...)`；worker 每 p 秒 `SELECT id FROM jobs WHERE state='SCHEDULED' AND fire_at <= now() ORDER BY fire_at LIMIT k FOR UPDATE SKIP LOCKED`，对每个 job 交付再 `UPDATE state='FIRED'`。

优点：简单，持久化与事务白给；`SKIP LOCKED` 让多个 worker 并发取而不重复领取（Quartz 的 JDBC JobStore 就这样）。

缺点：
1. **延迟下界 = 轮询周期 p**，Δ = 1 s 要 p 至多几百 ms；
2. **热点索引范围**：所有 worker 读 `(state, fire_at)` 索引的同一个当前时刻区域，同时有随机时间插入，大量已触发行需删除，索引膨胀；
3. **突发**：整点 2×10⁵ 个同时到期，`LIMIT k` 要几十个来回，每次领取一个事务；
4. **没有精度**：毫秒级就得更高频率轮询；
5. **故障切换**依赖数据库自身 HA，延迟不可控。

适用：Δ 分钟级、规模 < 10⁷、已有成熟数据库。面试要先说这个方案和适用范围，再说为什么这里要更进一步。
