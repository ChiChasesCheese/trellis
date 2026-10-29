---
id: uth-java-forkjoin-3-blocking
node: java.forkjoin
type: qa
step: 3
---
## Q
**并行流里放阻塞调用会怎样**｜Java · OpenJDK 25

在 `parallel()` 流里每个元素 `Thread.sleep(500)`，8 个元素要多久？把公共池并行度设为 3 又会怎样？

## A
**背景。** 工作窃取假设任务短小、一直在算：线程忙着算，别的线程才轮得到偷。如果任务里在等（`sleep`、读网络、等锁），线程占着位置却不干活。

**结构。** 公共池线程数固定（约等于核数）；线程在 `sleep` 时就占着位置，其余任务只能排队。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="20" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">默认 11 个线程 8 个任务 一轮</text>
<rect x="30" y="28" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="37" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="46" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="55" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="64" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="73" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="82" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="30" y="91" width="100" height="7" rx="3" stroke="currentColor" stroke-width="0.8" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="140" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约 0.5 s</text>
<text x="20" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并行度 3 同样 8 个任务 两轮</text>
<rect x="30" y="132" width="100" height="13" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="132" width="100" height="13" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="30" y="149" width="100" height="13" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="149" width="100" height="13" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="30" y="166" width="100" height="13" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="166" width="100" height="13" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="30" y="183" width="100" height="13" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="183" width="100" height="13" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约 1.2 s</text>
<line x1="30" y1="208" x2="230" y2="208" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,208.0 224.0,211.0 224.0,205.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="30" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="130" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0.5 s</text>
<text x="230" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 s</text>
</svg>
```

**细节。**

- 实测默认（11 个工作线程）：8 个任务约 502 毫秒。
- 并行度设为 3：同样 8 个任务约 1180 毫秒，要排两轮。
- 池的补偿机制默认只在可能整池停摆时才补线程，不会帮 `sleep` 补位。

**为什么。** 工作窃取适合短小、纯计算的任务。

**坑。** I/O 或锁等待不要放进公共池，自己建线程池，或用虚拟线程。

**对应 LeetCode：** 无直接对应的题
