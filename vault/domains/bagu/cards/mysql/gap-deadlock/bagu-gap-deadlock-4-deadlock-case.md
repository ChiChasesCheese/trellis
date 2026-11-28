---
id: bagu-gap-deadlock-4-deadlock-case
node: a.mysql.gap-deadlock
type: qa
step: 3
---
## Q
**死锁 · 是怎么发生的，举一个两个事务互相等待的例子**｜必会

面试官：「死锁是怎么发生的？给一个最常见的例子。」

## A
**基本回答。** 死锁是多个事务各自持有对方需要的锁，并互相等待，形成一个环。最典型的是加锁顺序相反：事务 A 先更新订单 1 再更新订单 10，事务 B 先更新订单 10 再更新订单 1；A 持有 1 想要 10，B 持有 10 想要 1，死锁。8.0.46 复现：InnoDB 立即检测到并回滚其中一个，被回滚的会话收到 `1213 Deadlock found when trying to get lock; try restarting transaction`，另一个继续提交。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<rect x="8" y="14" width="90" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="35.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务 A</text>
<rect x="242" y="14" width="90" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287.0" y="35.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务 B</text>
<rect x="8" y="104" width="90" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="125.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 1</text>
<rect x="242" y="104" width="90" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287.0" y="125.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 10</text>
<line x1="53" y1="48" x2="53.0" y2="97.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="53.0,104.0 49.8,97.0 56.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="62" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持有</text>
<line x1="287" y1="48" x2="287.0" y2="97.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="287.0,104.0 283.8,97.0 290.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="295" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持有</text>
<line x1="98" y1="34" x2="243.64183793655548" y2="101.0718990497295" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="250.0,104.0 242.3,104.0 245.0,98.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="242" y1="34" x2="96.35816206344451" y2="101.0718990497295" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="90.0,104.0 95.0,98.2 97.7,104.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实线：已持有    虚线：在等待</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A：先订单 1，再订单 10</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B：先订单 10，再订单 1 → 成环</text>
</svg>
实线表示已持有：A 持有订单 1，B 持有订单 10；虚线表示在等待：A 想要订单 10，B 想要订单 1。两条虚线交叉，形成环，谁也等不到。
**举个例子。** 退款和优惠券同时更新订单 A、B：
1. **请求 1 先锁订单 A：** 订单 A 退款，同时要更新订单 B 的优惠券。
2. **请求 2 先锁订单 B：** 订单 B 取消，同时要更新订单 A 的优惠券。
3. **交叉：** 请求 1 接着要锁订单 B，被请求 2 挡住；请求 2 接着要锁订单 A，被请求 1 挡住。
4. **成环：** 谁也等不到，InnoDB 检测到环，回滚其中一个，报 1213。
5. **修复：** 统一按订单号从小到大更新，两个请求都先锁订单号小的，一个等另一个，不再成环。
**容易错。**
- **以为死锁是 bug：** 并发下偶发死锁很正常，目标是降低概率并让系统能自动恢复。
- **不处理 1213：** 被回滚的事务要重试，而且操作要幂等。
- **以为只有更新同一行才会死锁：** 不同顺序更新多行、二级索引和主键的加锁路径不同，也会死锁。
- **只想靠超时解决：** 死锁会被 InnoDB 立刻检测并回滚，不是等超时。
