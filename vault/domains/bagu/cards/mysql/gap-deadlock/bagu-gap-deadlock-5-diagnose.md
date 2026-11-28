---
id: bagu-gap-deadlock-5-diagnose
node: a.mysql.gap-deadlock
type: qa
step: 4
---
## Q
**死锁排查 · 线上怎么定位是哪两条 SQL**｜必会

面试官：「线上报了死锁，怎么定位是哪两个事务、哪两条语句？」

## A
**基本回答。** 执行 `SHOW ENGINE INNODB STATUS`，看其中的 `LATEST DETECTED DEADLOCK` 一段：里面有两个事务正在执行的语句、各自持有的锁（`HOLDS THE LOCK(S)`）、正在等待的锁（`WAITING FOR THIS LOCK TO BE GRANTED`）、以及回滚了哪一个（`WE ROLL BACK TRANSACTION (2)`），据此就能还原出这个环。它只保留最近一次死锁，要保留全部就开启 `innodb_print_all_deadlocks`，把死锁写进错误日志。再对照应用日志，找到这两条语句所在的接口。
锁等待（没有死锁）查 `performance_schema.data_locks`、`data_lock_waits` 或 `sys.innodb_lock_waits`。1213 是死锁，立即发生，应用重试；1205 是锁等待超时（`innodb_lock_wait_timeout` 默认 50 秒），要找长事务。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="8" y="8" width="324" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRANSACTION (1)</text>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务 1 正在执行的语句</text>
<rect x="8" y="48" width="324" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HOLDS THE LOCK(S) / WAITING FOR THIS</text>
<text x="170.0" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LOCK TO BE GRANTED：持有的锁、等的锁</text>
<rect x="8" y="88" width="324" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRANSACTION (2)</text>
<text x="170.0" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务 2：同样三段</text>
<rect x="8" y="128" width="324" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HOLDS THE LOCK(S) / WAITING FOR THIS</text>
<text x="170.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LOCK TO BE GRANTED：持有的锁、等的锁</text>
<rect x="8" y="168" width="324" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">WE ROLL BACK TRANSACTION (2)</text>
<text x="170.0" y="196.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">InnoDB 回滚了谁</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只保留最近一次；全留要开</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">innodb_print_all_deadlocks（写进错误日志）</text>
<text x="8" y="260" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1213 死锁；1205 锁等待超时（默认 50 秒）</text>
</svg>
`LATEST DETECTED DEADLOCK` 的结构：事务 1 的语句、它持有的锁和等待的锁；事务 2 的同样三段；最后一行告诉你 InnoDB 回滚了谁。下面三行是只保留最近一次的限制，以及 1213 和 1205 的区别。
**举个例子。** 凌晨对账批处理和白天退款在同一批订单上偶发 1213：
1. **事务 1 是批处理：** 在 `LATEST DETECTED DEADLOCK` 里，它的语句是按 `batch_id` 更新。
2. **事务 1 的锁：** 持有 batch 索引上的锁，在等主键上的锁。
3. **事务 2 的锁：** 是退款，按主键更新，持有主键锁，在等 batch 索引上的锁。
4. **还原：** 一个先锁 batch 索引再锁主键，一个先锁主键再锁 batch 索引，顺序相反。
5. **回滚了谁：** 最后一行若是 `WE ROLL BACK TRANSACTION (2)`，就是退款被回滚、收到 1213。
6. **修复：** 批处理改为按主键分批更新，两边都先锁主键，不再成环。
**容易错。**
- **只看错误码不看现场：** 1213 只告诉你死锁了，要靠 `LATEST DETECTED DEADLOCK` 才能知道哪两条语句。
- **以为能一直查到历史死锁：** 只保留最近一次，要留全部要开 `innodb_print_all_deadlocks`。
- **把 1205 当成死锁：** 1205 是锁等待超时，不是死锁，根因多是长事务持锁不放。
- **关掉死锁检测来省 CPU：** 只靠超时风险很大，应从热点行竞争本身入手。
