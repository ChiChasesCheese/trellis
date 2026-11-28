---
id: bagu-java-deadlock-threads-1-deadlock-order
node: b.runtime.java-deadlock-threads
type: qa
step: 1
---
## Q
**线程状态与死锁 · 四个条件、检测与预防**｜追问

面试官：「两个线程同时给 A→B 和 B→A 转账会怎样？线程有哪些状态？死锁怎么排查和避免？」

## A
**基本回答。** 两个线程各持一把锁又等对方的锁，就是死锁。四个必要条件：互斥、持有并等待、不可抢占、循环等待，同时成立才死锁，破坏一个即可。最实用的是破坏循环等待：所有线程按固定顺序加锁（如账户 ID 小的先锁），等待关系只能从小指向大，不会成环。其他办法：带超时的 `tryLock`，拿不到就放弃重试（要有重试策略）；一次拿全所有锁。线程六态：NEW、RUNNABLE、BLOCKED（等 monitor 锁）、WAITING（`wait`/`join`/`park`）、TIMED_WAITING（带超时、`sleep`）、TERMINATED。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">死锁：互相等对方手里的锁</text>
<rect x="10" y="26" width="120" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<text x="70.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有锁 A</text>
<rect x="210" y="26" width="120" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<text x="270.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有锁 B</text>
<text x="170" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">等锁 B</text>
<line x1="130" y1="46" x2="210" y2="46" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,46.0 203.6,48.9 203.6,43.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="210" y1="62" x2="130" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,62.0 136.4,59.1 136.4,64.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">等锁 A</text>
<line x1="10" y1="98" x2="330" y2="98" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">修复：都按 ID 小的先锁</text>
<rect x="10" y="126" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="143.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<line x1="80" y1="139" x2="98" y2="139" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,139.0 91.6,141.9 91.6,136.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="126" width="100" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="148.0" y="143.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先锁 A</text>
<line x1="198" y1="139" x2="216" y2="139" stroke-width="1.2" stroke="currentColor"/>
<polygon points="216.0,139.0 209.6,141.9 209.6,136.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="216" y="126" width="100" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="266.0" y="143.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再锁 B</text>
<rect x="10" y="164" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<line x1="80" y1="177" x2="98" y2="177" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,177.0 91.6,179.9 91.6,174.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="164" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="148.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在 A 外等</text>
<line x1="198" y1="177" x2="216" y2="177" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="216.0,177.0 209.6,179.9 209.6,174.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="216" y="164" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="266.0" y="181.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 1 放锁</text>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没人拿着一把等另一把，不会成环</text>
</svg>
上半部分：线程 1 拿着锁 A 等锁 B，线程 2 拿着锁 B 等锁 A，两条等待线首尾相连成环；下半部分：统一先锁 A 再锁 B 后，线程 2 在 A 外面等线程 1 放锁，不成环。
**业务场景。** 账户 A=1、B=2：线程 1 转 1→2 先锁 1，线程 2 转 2→1 先锁 2，各想锁对方，两个线程都是 BLOCKED，`jstack` 打印 `Found one Java-level deadlock`，代码里 `ThreadMXBean.findDeadlockedThreads()` 能找到并给出各自等的锁和持有者。统一先锁 ID 小的，线程 2 在账户 1 外面等，不再死锁。数据库同理：事务按固定顺序更新行，InnoDB 检测到死锁会回滚其中一个。
**容易错。**
- **以为 BLOCKED 就是死锁：** 只是在等锁，要看等待关系是否成环。
