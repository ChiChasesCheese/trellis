---
id: bagu-rdb-aof-2-bgsave-cow
node: a.redis.rdb-aof
type: qa
step: 2
---
## Q
**RDB · bgsave 为什么不阻塞主线程，写时复制有什么代价**｜必会

面试官：「`BGSAVE` 怎么做到一边快照一边处理请求？写时复制是怎么回事，对线上有什么风险？」

## A
**基本回答。** 主线程 `fork()` 出子进程，子进程持有 fork 那一刻内存的快照并写 RDB，主线程继续服务。fork 只复制页表（虚拟地址到物理页的映射），不复制物理内存，父子共享物理页并标为只读；主线程要改某页时触发缺页异常，内核先复制该页再写（写时复制 COW），子进程仍看到旧页，所以快照一致，也看不到之后的写入。用「只复制被修改的页」换「不用锁整个数据集」：读多写少几乎不涨内存。风险一：fork 复制页表在主线程里完成，实例越大越慢（物理机约十几毫秒每 GB，虚拟机更慢），`INFO` 的 `latest_fork_usec` 可查。风险二：快照期间写得越多复制的页越多，内存峰值最坏接近翻倍。对策：单实例控制在 10–20GB；关闭透明大页（THP，否则一次按 2MB 复制放大增长）；`vm.overcommit_memory=1` 防 fork 因内存不足失败；预留内存；备份放从库；纯缓存可关 RDB 和 AOF。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fork 只复制页表，不复制数据本身</text>
<rect x="10" y="24" width="120" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主进程页表</text>
<rect x="210" y="24" width="120" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程页表</text>
<rect x="40" y="100" width="90" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 A</text>
<rect x="210" y="100" width="90" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 B</text>
<line x1="50" y1="54" x2="62" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62,100 57.1,94.0 63.3,92.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="50" y1="54" x2="220" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220,100 212.4,101.3 214.1,95.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="290" y1="54" x2="110" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110,100 116.0,95.2 117.6,101.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="290" y1="54" x2="280" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280,100 278.4,92.5 284.6,93.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主线程要改页 B：缺页异常，内核先复制</text>
<rect x="10" y="176" width="150" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 B（旧）</text>
<text x="85" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程继续读它</text>
<line x1="160" y1="199" x2="180" y2="199" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,199 173.0,202.2 173.0,195.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="182" y="176" width="150" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 B′（副本）</text>
<text x="257" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主线程改这份</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读多写少几乎不涨内存；写密集可能翻倍</text>
</svg>
fork 后两个页表指向同样的物理页；主线程改页 B 时内核先复制出 B′，主线程改副本，子进程继续读旧的 B。
**业务场景。** 一台 30GB 实例在大促前夜 `BGSAVE`，恰逢打赏写入高峰：fork 复制页表阻塞数百毫秒，接口超时；快照持续几分钟，被改的页都要复制，内存峰值逼近 60GB，触发 OOM killer。预防是拆成更小的实例并在从库备份。
**容易错。**
- **以为 BGSAVE 完全不阻塞。**
- **以为 fork 会复制全部内存。**
- **以为子进程能看到最新写入。**
