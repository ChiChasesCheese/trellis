---
id: bagu-java-threadpool-3-pool-size
node: a.runtime.java-threadpool
type: qa
step: 3
---
## Q
**线程池 · 线程池大小怎么设，CPU 密集和 IO 密集有何不同**｜必会

面试官：「线程池核心线程数设多少？CPU 密集型和 IO 密集型有什么区别？公式能直接用吗？」

## A
**基本回答。** CPU 密集型约 `N_cpu + 1`（多出的一个在某线程缺页阻塞时顶上），线程多于核数只增加切换和内存。IO 密集型约 `N_cpu × (1 + W/C)`，W 是等待时间，C 是计算时间；线程等待时不占 CPU，所以可以多排。公式只是起点：要压测找到吞吐不再上升、延迟开始变差的拐点，还受下游限制，数据库连接池只有 20 个，开 80 个线程只是排队等连接。另一个估算：执行中的任务数 ≈ 每秒提交数 × 平均耗时（400 个/秒、80ms，约 32 个并发）；队列长度 ≈ 吞吐 × 可容忍的等待时间。
**2026 亮点。** Java 21 虚拟线程让 IO 密集任务不必精调池大小，限并发改用信号量。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个 IO 密集任务的 100ms</text>
<rect x="8" y="28" width="30" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="38" y="28" width="270" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="23" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">算 C</text>
<text x="23" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10ms</text>
<text x="173" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等数据库、网络 W = 90ms</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">IO 密集：N × (1 + W/C)</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8 核：8 × (1 + 90/10) = 80 个线程</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">CPU 密集：N + 1</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再受下游限制：连接池只有 20，</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">80 个线程也只是排队等连接</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">公式是起点，压测找拐点才是答案</text>
</svg>
一个任务 100ms 里只有 10ms 在计算，其余 90ms 在等；线程等待时不占 CPU，所以 8 个核可以同时安排约 80 个线程轮流算。
**举个例子。** 8 核：CPU 密集（压缩、加密）设 9；IO 密集等 90ms、算 10ms，W/C = 9，线程数 8 × 10 = 80，同一时刻约 1/10 在计算，刚好吃满 8 核；但这些任务都要数据库连接、连接池只有 20，就该按 20 左右设。爬虫等网络 190ms、解析 10ms，W/C = 19，公式给 160 个线程，但对同一站点限制 5 并发，真正的上限由礼貌策略和带宽决定。
**容易错。**
- **把公式当答案：** 只是起点，最终靠压测。
- **只算线程池不看下游：** 连接池、站点限速会封顶。
