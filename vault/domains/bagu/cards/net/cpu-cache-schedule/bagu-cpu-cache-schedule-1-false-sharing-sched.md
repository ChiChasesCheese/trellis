---
id: bagu-cpu-cache-schedule-1-false-sharing-sched
node: b.net.cpu-cache-schedule
type: qa
step: 1
---
## Q
**CPU 缓存与调度 · 伪共享、缓存一致性与调度算法**｜追问

面试官：「多个线程各自更新相邻的计数器，为什么比预期慢很多？什么是伪共享，怎么避免？常见的进程调度算法有哪些？」

## A
**基本回答。** CPU 缓存以缓存行（cache line，常见 64 字节）为单位加载。不同线程写的变量落在同一缓存行，一个核写入就让其他核的这一行副本失效（MESI 协议里变 Invalid），对方下次读要重新加载，来回抢占，代码里没有锁却像在抢锁，这是伪共享（false sharing）。避免：填充或对齐让热点变量各占一行（Java 用 `@Contended`，Go 加 `[56]byte`，8 字节计数器加 56 字节正好 64），或每个线程先累加局部变量再汇总。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">伪共享：A、B 挤在同一条缓存行里</text>
<rect x="10" y="22" width="320" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="18" y="28" width="144" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数器 A</text>
<rect x="178" y="28" width="144" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数器 B</text>
<rect x="10" y="98" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">核 0：只写 A</text>
<rect x="180" y="98" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">核 1：只写 B</text>
<line x1="85" y1="98" x2="85.0" y2="69.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,62 88.2,69.0 81.8,69.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="255" y1="98" x2="255.0" y2="69.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,62 258.2,69.0 251.8,69.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每次写都让对方那一行失效（Invalid）</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对方下次读要重新加载，来回抢</text>
<text x="10" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">各占一行：A、B 各加 56 字节填充</text>
<rect x="10" y="202" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="221" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存行 1：A + 填充</text>
<rect x="180" y="202" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="221" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存行 2：B + 填充</text>
<text x="10" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实测 849 ms → 71 ms，快约 12 倍</text>
</svg>
上半两个核各写自己的变量却共用一行，互相使对方失效；下半隔开后实测（Go，两个 goroutine 各 5000 万次原子加，Apple 芯片）从约 849 ms 降到约 71 ms，快约 12 倍。
**调度算法。** 先来先服务（长任务堵住短任务）；短作业优先（平均等待最短，但要预知时长，长任务可能饿死）；时间片轮转（太短则切换开销大，太长则退化成先来先服务，不区分优先级）；优先级；多级反馈队列（兼顾短任务响应和长任务吞吐）。Linux 通用调度器是 CFS（按最小 vruntime 选进程，红黑树组织），Linux 6.6 起由 EEVDF 取代。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="10" y="10" width="190" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 1：优先级最高</text>
<text x="105" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间片最短</text>
<line x1="105" y1="50" x2="105.0" y2="69.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105,76 101.8,69.0 108.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用完时间片没跑完，降一级</text>
<rect x="10" y="76" width="190" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 2</text>
<text x="105" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间片较长</text>
<line x1="105" y1="116" x2="105.0" y2="135.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105,142 101.8,135.0 108.2,135.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还没跑完，再降一级</text>
<rect x="10" y="142" width="190" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 3：优先级最低</text>
<text x="105" y="173.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间片最长</text>
<text x="212" y="26" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">短任务在这</text>
<text x="212" y="42" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">跑完，响应快</text>
<text x="212" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">长任务沉到这</text>
<text x="212" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次跑得久</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新任务总是先进队列 1</text>
</svg>
多级反馈队列：新任务进最高优先级队列（时间片最短），短任务一个时间片内跑完；用完时间片没跑完就降一级，长任务沉到低优先级队列，每次跑得久，吞吐高。
**业务场景。** 4 个 8 字节计数器放在数组里共 32 字节，全在同一条 64 字节缓存行，4 个线程各写自己那一格，吞吐却远低于线程数应有的水平；每个计数器填充到独占一行后明显提升。
**容易错。**
- **把伪共享当成变量真的共享：** 伪共享是改不同变量却在同一行；改同一变量是真共享，要用锁或原子操作。
- **以为原子操作能解决：** 实测里本来就是原子加，仍慢 12 倍，慢在缓存行来回失效。
- **以为填充越多越好：** 只填充被不同线程频繁写的变量，否则浪费缓存和内存。
