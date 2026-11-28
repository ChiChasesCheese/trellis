---
id: bagu-isolation-levels-1-levels
node: a.mysql.isolation-levels
type: qa
step: 1
---
## Q
**隔离级别 · 四个级别分别解决什么，InnoDB 默认是哪个**｜必会

面试官：「MySQL 事务的四个隔离级别是什么？各自避免哪些并发问题？InnoDB 默认哪个？」

## A
**基本回答。** 从弱到强四个级别：读未提交、读已提交（RC）、可重复读（RR）、串行化。读未提交会出现脏读、不可重复读、幻读；RC 避免了脏读；RR 再避免不可重复读，按 SQL 标准仍允许幻读，但 InnoDB 下快照读不会幻读、当前读靠 next-key 锁基本防住；串行化把三种都避免，代价是读也要加锁。InnoDB 默认是 RR（`SELECT @@transaction_isolation` 得到 `REPEATABLE-READ`）。
设置：`SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED`，或配置里写 `transaction-isolation`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="104" y="8" width="72" height="24" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="140.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">脏读</text>
<rect x="180" y="8" width="72" height="24" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="216.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不可重复读</text>
<rect x="256" y="8" width="72" height="24" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="292.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">幻读</text>
<rect x="8" y="38" width="92" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="55.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读未提交</text>
<rect x="104" y="38" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="55.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会</text>
<rect x="180" y="38" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="216.0" y="55.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会</text>
<rect x="256" y="38" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292.0" y="55.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会</text>
<rect x="8" y="68" width="92" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RC 读已提交</text>
<rect x="104" y="68" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<rect x="180" y="68" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="216.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会</text>
<rect x="256" y="68" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会</text>
<rect x="8" y="98" width="92" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RR 可重复读</text>
<rect x="104" y="98" width="72" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<rect x="180" y="98" width="72" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="216.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<rect x="256" y="98" width="72" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">基本防住</text>
<rect x="8" y="128" width="92" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">串行化</text>
<rect x="104" y="128" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<rect x="180" y="128" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="216.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<rect x="256" y="128" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不会</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">高亮行：InnoDB 默认级别 RR</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RR 的幻读：快照读看不到，当前读靠锁</text>
</svg>
横向三种并发问题，纵向四个级别，「会」表示这个级别下仍会出现；越往下越强，也越慢。高亮的 RR 是 InnoDB 默认级别，它的幻读格里写的是「基本防住」。
**举个例子。** 账户余额 100，事务 B 要扣 50（还没提交），事务 A 在读：
1. **读未提交：** A 读到 50，这是 B 还没提交的值；B 如果回滚，A 读到的就是一个从没真正存在过的数（脏读）。
2. **RC：** A 此时读到 100（B 未提交）；等 B 提交后 A 再读，读到 50。同一事务里两次读不一样（不可重复读）。
3. **RR：** A 第一次读之后，不管 B 提交没有，A 再读仍是 100，符合「可重复读」。
4. **串行化：** A 的普通 `SELECT` 要先拿行上的共享锁；B 还没提交，手里的排他锁不放，A 只能等到 B 结束再读（读到 50 或回滚后的 100）。谁也看不到中间状态，代价是互相等待，并发最低。
**容易错。**
- **以为 RR 一定能完全防住幻读：** 快照读不会，但同一事务里混用当前读仍可能出现幻读，下一类题会展开。
- **以为隔离级别越低越快：** 低级别的代价是读到不一致的数据，业务金额对不上；级别要按场景选。
- **以为默认就是 RC：** MySQL InnoDB 默认是 RR，很多公司自己改成 RC。
- **以为串行化只是在加锁读时才串行：** 关闭自动提交后，连普通 `SELECT` 都会被当成加共享锁的读。
