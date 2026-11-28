---
id: bagu-lock-redis-setnx-6-db-instead
node: a.distributed.lock-redis-setnx
type: qa
step: 5
---
## Q
**锁不是最后防线 · 数据库唯一约束能否替代**｜必会

面试官：「你加这把锁是为了保证什么？什么情况下可以不要锁，直接靠数据库？」

## A
**基本回答。** 先问「重复执行的代价是什么」。代价是多发一条通知，用 Redis 锁就够；代价是重复扣款、重复入账，正确性必须由数据库保证：唯一键（支付请求号建唯一索引）、条件更新（`WHERE balance >= ?`、`WHERE status = 'INIT'`）、乐观锁版本号。锁只负责大多数时候避免重复干活，是优化，不是最后防线。示例 SQL 放在后面的代码一节。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="14" y="8" width="180" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个重复的请求</text>
<line x1="104" y1="38" x2="104" y2="47" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104,54 100.8,47 107.2,47" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="14" y="54" width="180" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="104" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 分布式锁</text>
<text x="104" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大多数时候挡住重复</text>
<line x1="104" y1="100" x2="104" y2="109" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104,116 100.8,109 107.2,109" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="14" y="116" width="180" height="62" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="104" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库约束</text>
<text x="104" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一键 · 条件更新</text>
<text x="104" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乐观锁版本号</text>
<line x1="104" y1="178" x2="104" y2="187" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104,194 100.8,187 107.2,187" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="14" y="194" width="180" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="213" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只生效一次</text>
<line x1="194" y1="23" x2="270" y2="23" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<line x1="270" y1="23" x2="270" y2="147" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<line x1="270" y1="147" x2="201" y2="147" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="194,147 201,143.8 201,150.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="206" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">锁失效时</text>
<text x="206" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">（超时、长 GC、</text>
<text x="206" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主从切换）</text>
<text x="206" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">走这条路</text>
</svg>
请求先过 Redis 锁这一关（虚线，因为它可能失效），再过数据库约束这一关（实线，不依赖时间）。锁失效时，重复请求顺着右边的虚线直接到数据库，被唯一键或条件更新挡住。
**代码。** 唯一键和条件更新：
```sql
-- 幂等：同一个回调只能插入一次，冲突就是重复
INSERT INTO pay_record(out_trade_no, amount) VALUES (?, ?);
-- 条件更新：余额够才扣，影响行数为 0 表示失败
UPDATE account SET balance = balance - 100 WHERE id = 7 AND balance >= 100;
```
**容易错。**
- **以为拿到了锁就不会重复：** 锁会超时、会因 GC 停顿丢失、会在主从切换时丢，不保证绝对互斥。
- **用锁代替唯一键：** 钱的事要靠数据库约束，锁只减少无谓的并发。
- **乐观锁冲突多还硬用：** 冲突少用乐观锁（带版本号更新，影响行数 0 说明被抢先），吞吐高；冲突多一直重试反而更慢，改用悲观锁 `SELECT ... FOR UPDATE`。
- **悲观锁事务拖得很长：** 持锁久会拖垮连接池，事务要尽量短。

**业务场景。** 支付回调重复到达，同一笔 `out_trade_no` 落在两个实例。靠唯一键，第二次插入冲突就直接返回成功，不依赖 Redis 锁，即使锁失效也不会重复入账。
