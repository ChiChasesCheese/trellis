---
id: bagu-mvcc-1-what
node: a.mysql.mvcc
type: qa
step: 1
---
## Q
**MVCC · 它是什么，解决了什么问题**｜必会

面试官：「InnoDB 的读为什么不会被写阻塞？MVCC 是什么，解决了什么问题？」

## A
**基本回答。** MVCC（Multi-Version Concurrency Control，多版本并发控制）让每一行在内部保留多个版本，读操作按自己的时间点去读对应的历史版本，不需要加锁。效果是读不阻塞写、写不阻塞读：一个事务正在修改某行，别的事务的普通 `SELECT` 仍然读到修改前已经提交的旧版本。它主要作用于读已提交（RC）和可重复读（RR）两个隔离级别下的快照读。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<rect x="8" y="22" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写：事务100 改成 50</text>
<line x1="83" y1="50" x2="83" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,78.0 79.8,71.0 86.2,71.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="80" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最新版本：50</text>
<text x="83.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务100 还没提交</text>
<line x1="158" y1="102" x2="192" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="192.0,102.0 185.0,105.2 185.0,98.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="192" y="80" width="140" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧版本：100</text>
<text x="262.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务90 已提交</text>
<line x1="262" y1="152" x2="262" y2="126" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262.0,126.0 265.2,133.0 258.8,133.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="192" y="154" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262.0" y="172.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读：事务105 SELECT</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写照常进行，</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不会被读挡住</text>
<text x="262" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读到 100，不用等写</text>
</svg>
左边是写：事务 100 把余额改成 50，还没提交；右边是读：事务 105 顺着指针读到旧版本 100，不用等写完。
**举个例子。** 账户 A 余额 100，已提交。
1. **写：**事务 100 执行 `UPDATE account SET balance = 50 WHERE id = 1`，还没提交。行上现在是新版本 50，旧版本 100 保存在 undo log 里。
2. 用户刷新 App，事务 105 执行普通 `SELECT balance`，不等事务 100，直接读到旧版本 100。
3. 事务 100 提交：之后新开的读事务能读到 50。
4. 如果事务 100 回滚：50 被撤销，用户从来没有看到过 50。
5. **写写冲突：**如果此时另一个事务 101 也想 `UPDATE` 这一行：不行，要等事务 100 释放行锁，这是写写冲突，MVCC 不管。
**容易错。**
- **以为 MVCC 让所有并发问题消失：** 它只解决读写并发，写写冲突仍然靠行锁排队。
- **以为所有隔离级别都用 MVCC：** 读未提交读最新版本，串行化靠锁，只有 RC 和 RR 的快照读用它。
- **以为旧版本是整行复制：** 旧版本是通过 undo log 记录的，存的是改动前的内容，不是每次复制整张表。
- **以为多版本没有代价：** 旧版本占空间，长事务不结束，旧版本就没法清理，版本链越拖越长。
