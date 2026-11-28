---
id: bagu-isolation-levels-3-rc-rr
node: a.mysql.isolation-levels
type: qa
step: 3
---
## Q
**RC 和 RR 的实际区别，为什么不少公司用 RC**｜必会

面试官：「RC 和 RR 在 InnoDB 里实际差别是什么？为什么很多互联网公司改用 RC？」

## A
**基本回答。** 实际差别在三处。快照读：RC 每条普通 `SELECT` 都新建一个读视图（ReadView），能读到别人刚提交的数据；RR 在第一次快照读时建一次，之后复用同一个。加锁：RR 的当前读（`FOR UPDATE`、`UPDATE`、`DELETE`）会加间隙锁和 next-key 锁；RC 只锁记录（外键与唯一键检查除外）。RC 下 `UPDATE`/`DELETE` 扫描时，不满足条件的行的锁会提前释放（半一致读），RR 要一直持有到事务结束。很多公司改用 RC，是因为锁范围小、死锁和锁等待少；代价是事务内多次读可能不一致。
用 RC 要求 `binlog_format=ROW`，STATEMENT 格式下写 InnoDB 表会报错 1665；8.0 默认已是 ROW。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RC：每条 SELECT 都建新视图</text>
<rect x="8" y="22" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 1</text>
<text x="58.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新建视图</text>
<line x1="108" y1="40" x2="113.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,40.0 113.0,43.2 113.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="22" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 2</text>
<text x="170.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新建视图</text>
<line x1="220" y1="40" x2="225.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,40.0 225.0,43.2 225.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="22" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 3</text>
<text x="282.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新建视图</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次都读到最新已提交的数据</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RR：第一次读建一次，之后复用</text>
<rect x="8" y="112" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 1</text>
<text x="58.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">建视图（一次）</text>
<rect x="120" y="112" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 2</text>
<text x="170.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">复用同一视图</text>
<rect x="232" y="112" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT 3</text>
<text x="282.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">复用同一视图</text>
<line x1="108" y1="130" x2="113.0" y2="130.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,130.0 113.0,133.2 113.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="130" x2="225.0" y2="130.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,130.0 225.0,133.2 225.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一直读到第一次读时的那份快照</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">加锁：RR 当前读有间隙锁 + next-key 锁</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RC 只锁记录，不满足条件的行锁提前放</text>
</svg>
第一行是 RC：每条 SELECT 都建一个新视图，所以每次都读到最新已提交的数据；第二行是 RR：第一次读建视图，之后两次都复用，一直读到第一次读时的快照。最后两行是加锁的差别。
**举个例子。** 秒杀订单库有一条范围更新 `UPDATE ... WHERE status=0 AND created_at < ...`：
1. **RR：** 扫描时给扫过的记录加 next-key 锁，连记录之间的空隙也锁上，这些锁一直持有到事务结束。
2. **别的事务：** 想往这些空隙里插入新订单，就被挡住，开始排队。
3. **互相等待：** 高并发下两个事务各拿一部分锁、又互相等，出现死锁和 1205 锁等待超时。
4. **改 RC：** 只锁满足条件的记录，不满足条件的行锁提前放掉，也没有间隙锁，死锁大幅下降。
5. **补偿：** 对账读事务自己带时间截止条件，保证前后一致。
**容易错。**
- **以为 RC 比 RR 弱就不能用于资金业务：** 能用，前提是业务不依赖事务内多次读一致，需要的地方自己加锁或带截止条件。
- **以为 RR 和 RC 的区别只是读视图：** 还有加锁范围和锁释放时机，这才是改 RC 的主要理由。
- **忘了 RC 要 ROW 格式 binlog：** STATEMENT 下写 InnoDB 表报错 1665。
- **以为 RC 完全没有间隙锁：** 外键与唯一键检查除外，仍可能用到。
