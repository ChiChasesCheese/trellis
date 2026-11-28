---
id: bagu-mem-oom-4-jvm-offheap
node: a.linux.mem-oom
type: qa
step: 4
---
## Q
**JVM 堆外内存与 Metaspace · OOM 怎么排查**｜追问

面试官：「容器限制 2 GB，堆也设 2 GB，没出堆溢出，进程却被杀了，为什么？」

## A
**基本回答。** 因为进程总内存不只是堆：还有元空间（Metaspace）、线程栈、直接内存（Direct Buffer）、代码缓存和 JNI 原生内存。堆已经占满 2 GB，再加上这些，整个进程必然超过容器的 2 GB 限制，被内核杀掉。排查用 `-XX:NativeMemoryTracking=summary` 启动，再用 `jcmd <pid> VM.native_memory` 看各部分。
看报错分类：`Java heap space` 是堆，`Metaspace` 多半是动态生成类或类加载器泄漏，`Direct buffer memory` 是直接内存，`unable to create native thread` 是线程太多。NMT 先 `jcmd <pid> VM.native_memory baseline`，过一阵再 `summary.diff` 看哪块在涨。典型堆外泄漏：Netty 的 `ByteBuf` 用完没 `release`，直接内存只增不减。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个 JVM 进程占的内存</text>
<rect x="20" y="28" width="180" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">JNI 原生内存</text>
<rect x="20" y="50" width="180" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代码缓存（Code Cache）</text>
<rect x="20" y="72" width="180" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接内存（Direct Buffer）</text>
<rect x="20" y="94" width="180" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程栈（每线程一份）</text>
<rect x="20" y="116" width="180" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">元空间（Metaspace）</text>
<rect x="20" y="138" width="180" height="86" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆（Heap）</text>
<text x="110" y="192.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-Xmx 2 GB</text>
<line x1="8" y1="138" x2="332" y2="138" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="208" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">容器上限 2 GB</text>
<text x="208" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">全是堆之外的</text>
<text x="208" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">合计超出上限</text>
<text x="208" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 被 OOM Killer 杀</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">堆已经占满上限，其余再没地方放</text>
</svg>
最底部的堆刚好等于容器上限，堆之上的几块都是堆之外的内存，它们全都落在虚线之外。进程总量超过上限，就被杀，而 JVM 自己并不会报堆溢出。
**举个例子。** 容器限制 2 GB，堆也设成 2 GB（演示用的假设值）：
1. **算总账：** 堆满时 2048 MB；再加元空间约 100 MB，200 个线程每个栈约 1 MB 共约 200 MB，还有直接内存和代码缓存，进程总量超过 2.3 GB。
2. **结果：** 堆没报溢出，进程却超过容器上限，被 OOM Killer 杀掉，退出码 137。
3. **修正：** 用 `-XX:MaxRAMPercentage=70`，堆约 1.4 GB，给非堆留出约 600 MB。
4. **再用 NMT 实测：** 看各部分实际占用，按需要继续调整。
**容易错。**
- **以为堆设多大进程就占多大：** 堆之外还有好几块，总量比堆大。
- **堆没满就以为不会被杀：** 容器限制管的是整个进程，不是堆。
- **堆外泄漏去翻堆转储：** 堆转储里看不到直接内存，要靠 NMT 和泄漏检测。
- **把 137 当成 `OutOfMemoryError`：** 137 是系统杀的，JVM 自己抛的 OOM 进程还活着。
**业务场景。** 推送网关堆曲线平稳，RSS 却每天涨几百兆直到被杀；NMT 对比发现直接内存在涨，原因是某条异常路径没释放缓冲区。
