---
id: uth-java-forkjoin-2-common-pool
node: java.forkjoin
type: qa
step: 2
---
## Q
**parallelStream 的线程从哪来**｜Java · OpenJDK 25

`parallelStream()`、`CompletableFuture.supplyAsync` 不传线程池时，任务在哪个线程池里跑？有几个线程？

## A
**背景。** 如果每次并行调用都新建一个线程池，线程数会失控。所以 JDK 准备了一个全进程共享的默认池。

**结构。** 公共池 `ForkJoinPool.commonPool()`，`CompletableFuture` 的默认池也是它（`asyncCommonPool`）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="10" y="28" width="134" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">parallelStream</text>
<line x1="144" y1="42" x2="190" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,70.0 184.4,69.5 187.0,65.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="72" width="134" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CompletableFuture</text>
<line x1="144" y1="86" x2="190" y2="92" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,92.0 184.7,93.8 185.4,88.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="116" width="134" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ForkJoinTask</text>
<line x1="144" y1="130" x2="190" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,114.0 186.1,118.0 184.5,113.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="190" y="20" width="140" height="124" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">commonPool</text>
<rect x="202" y="56" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w1</text>
<rect x="242" y="56" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w2</text>
<rect x="282" y="56" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w3</text>
<rect x="202" y="86" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w4</text>
<rect x="242" y="86" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w5</text>
<rect x="282" y="86" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w6</text>
<text x="260" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并行度 = 核数 - 1</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全进程共享一个池</text>
</svg>
```

**细节。**

- 默认并行度是 `availableProcessors() - 1`；本机 12 核实测为 11，调用方线程也会参与干活。
- 线程名是 `ForkJoinPool.commonPool-worker-N`，用不到时会被慢慢回收。
- 可用系统属性 `java.util.concurrent.ForkJoinPool.common.parallelism` 调整。

**为什么。** 所有并行流共用一个池，线程数受控。

**坑。** 共享意味着一个人堵住大家都慢，所以 CPU 密集任务才适合放进去。

**对应 LeetCode：** 无直接对应的题
