---
id: bagu-isolation-levels-5-acid
node: a.mysql.isolation-levels
type: qa
step: 5
---
## Q
**ACID 四个特性分别靠什么机制实现**｜追问

面试官：「事务的 ACID 在 InnoDB 里分别靠什么实现？」

## A
**基本回答。** 原子性靠 undo log：改数据前先记下旧值，回滚时按旧值反向恢复。隔离性靠锁加 MVCC：写写冲突用行锁，读写之间靠多版本快照读。持久性靠 redo log：提交时先把 redo 刷到磁盘（`innodb_flush_log_at_trx_commit=1`），崩溃后可以重做。一致性是目的，不是单独的机制：靠前三者，再加应用层约束（主键、唯一键、外键、`CHECK`、业务代码）共同达成。
持久性另有双写缓冲（doublewrite buffer），防止 16KB 页写到磁盘时只写了一半。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<rect x="8" y="10" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 原子性</text>
<line x1="120" y1="28" x2="107.0" y2="28.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,28.0 107.0,24.8 107.0,31.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="10" width="212" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo log：记修改前旧值</text>
<text x="226.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回滚时反向恢复</text>
<rect x="8" y="56" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">I 隔离性</text>
<line x1="120" y1="74" x2="107.0" y2="74.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,74.0 107.0,70.8 107.0,77.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="56" width="212" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.0" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">行锁 + MVCC</text>
<text x="226.0" y="85.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写写冲突用锁；读用多版本快照</text>
<rect x="8" y="102" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D 持久性</text>
<line x1="120" y1="120" x2="107.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,120.0 107.0,116.8 107.0,123.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="102" width="212" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.0" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">redo log + 双写缓冲</text>
<text x="226.0" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交先刷 redo；双写防半页写</text>
<rect x="8" y="148" width="92" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54.0" y="170.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C 一致性</text>
<line x1="120" y1="166" x2="107.0" y2="166.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,166.0 107.0,162.8 107.0,169.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="148" width="212" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前三者 + 应用层约束</text>
<text x="226.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主键 唯一键 外键 CHECK 业务规则</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">C 是目标，不是单独的机制</text>
</svg>
左边是四个特性，右边是各自靠什么实现。前三个是具体机制；一致性（C）高亮在最下面，它是前三个再加应用层约束共同达到的目标。
**举个例子。** 转账：A 账户扣 100、B 账户加 100，放在同一个事务里：
1. **扣款：** 先在 undo log 记下 A 的旧余额，再改数据页，同时产生 redo。
2. **宕机且未提交：** 重启后发现这个事务没提交，用 undo 把 A 的扣款撤销，钱不会凭空消失（原子性）。
3. **已提交但脏页没落盘：** 重启后用 redo 把 A 和 B 的两处修改重做，已提交的转账不会丢（持久性）。
4. **并发时：** 别的事务读余额，靠 MVCC 读旧版本，写同一行的事务靠行锁排队（隔离性）。
5. **最终账平：** 转账前后 A + B 的总额不变，这是一致性，靠前三者加业务约束。
**容易错。**
- **把一致性说成一个机制：** 它是目标，靠前三者加应用层约束共同达成。
- **混淆 undo 和 redo：** undo 是改前的旧值，用来回滚；redo 是改后的新值，用来崩溃后重做。
- **以为隔离性只靠锁：** 读写之间主要靠 MVCC，只有写写冲突靠行锁。
- **忘了双写缓冲：** redo 解决不了「一页只写了一半」，要靠双写缓冲兜底。
