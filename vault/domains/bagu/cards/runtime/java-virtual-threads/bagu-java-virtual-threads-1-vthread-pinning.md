---
id: bagu-java-virtual-threads-1-vthread-pinning
node: b.runtime.java-virtual-threads
type: qa
step: 1
---
## Q
**虚拟线程 · 调度、Pinning 与适用场景**｜追问

面试官：「JDK 21 的虚拟线程是什么？和平台线程、协程有什么区别？什么是 Pinning？」

## A
**基本回答。** 虚拟线程由 JVM 调度，成千上万个复用少量载体线程（carrier，ForkJoinPool，默认并行度等于核数）；阻塞 IO 时从载体卸载（unmount）让出载体，IO 就绪再挂载（mount）回去，所以同步风格的代码就能撑高并发。平台线程是 1:1 的 OS 线程，栈重、数量有限，「一请求一线程」到几万就扛不住。Pinning：虚拟线程阻塞时卸载不下来，把载体一起钉住，别的虚拟线程用不上它，钉多了耗尽载体。适合 IO 密集；CPU 密集没有收益（瓶颈在核数）。不要池化，用时新建；线程不稀缺后，下游连接池要用 `Semaphore` 单独限流，否则几万个虚拟线程打垮下游。思路和 Go 协程相似，但沿用 `Thread` API。
**2026 亮点。** JDK 21 定稿（JEP 444）；JDK 21–23 在 `synchronized` 内阻塞会钉住，JDK 24 的 JEP 491 修复，本地方法栈帧里阻塞仍会钉住。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚拟线程（堆上的对象，可以有几万个）</text>
<rect x="10" y="24" width="72" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="46.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">V1 在跑</text>
<rect x="90" y="24" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="126.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">V2 等 IO</text>
<rect x="170" y="24" width="72" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="206.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">V3 在跑</text>
<rect x="250" y="24" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="286.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">V4 等 IO</text>
<line x1="46" y1="50" x2="100" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100.0,98.0 93.3,95.9 97.1,91.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="206" y1="50" x2="230" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230.0,98.0 224.6,93.6 229.7,91.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="40" y="98" width="120" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="100.0" y="116.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">载体线程 C1</text>
<rect x="180" y="98" width="120" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="240.0" y="116.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">载体线程 C2</text>
<text x="10" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">V2、V4 在等 IO：已卸载，不占载体</text>
<line x1="10" y1="158" x2="330" y2="158" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Pinning（JDK 21–23 的 synchronized 内）</text>
<rect x="10" y="186" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">V5 在 synchronized</text>
<text x="80.0" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">里阻塞，卸不掉</text>
<line x1="150" y1="206" x2="190" y2="206" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,206.0 183.6,208.9 183.6,203.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="190" y="186" width="140" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">载体 C2 被钉住</text>
<text x="260.0" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只能空等</text>
<text x="10" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">钉住的载体多了，别的虚拟线程没载体可用</text>
</svg>
上半部分：4 个虚拟线程只有 2 个在载体上跑，另外 2 个等 IO 已卸下；下半部分：在 synchronized 里阻塞的虚拟线程卸不下来，把载体一起钉住。
**举个例子。** 实测（JDK 25）：1 万个虚拟线程各阻塞 1 秒，总耗时约 1.2 秒。12 核机器 48 个任务在 `synchronized` 内睡 500ms，耗时约 548ms；若被钉住，12 个载体一次只能处理 12 个，要分 4 批约 2 秒，所以 JDK 25 没有钉住。
**业务场景。** 大量阻塞 IO 的网关改用虚拟线程后吞吐上升，但下游连接池被瞬间打满，要在调用下游处加 `Semaphore` 限流。
**容易错。**
- **以为虚拟线程让单个任务更快：** 只是等 IO 时不占线程。
