---
id: uth-compose-thread-pool-2-structures
node: compose.thread-pool
type: qa
step: 2
---
## Q
**组合：一个原子整数、一个队列、一个线程集合**｜Java ThreadPoolExecutor · JDK 21

一次 `execute` 会碰哪几个结构？按什么顺序决定任务的去向？

## A
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="10" y="8" width="120" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="70.0" y="26.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">execute(task)</text>
<rect x="190" y="8" width="140" height="44" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ctl</text>
<text x="260.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态 + 线程数</text>
<line x1="130" y1="22" x2="184.0" y2="22.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="190,22 184.0,25.0 184.0,19.0" fill="currentColor"/>
<text x="160" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CAS</text>
<rect x="10" y="116" width="130" height="42" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="75.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">workQueue</text>
<text x="75.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">BlockingQueue</text>
<rect x="200" y="116" width="130" height="42" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="265.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">workers</text>
<text x="265.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Worker 线程集合</text>
<line x1="60" y1="36" x2="60.0" y2="110.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,116 57.0,110.0 63.0,110.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 入队</text>
<line x1="120" y1="36" x2="244.9" y2="112.9" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,116 243.3,115.4 246.5,110.3" fill="currentColor"/>
<text x="206" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 或 3 新建线程</text>
<line x1="140" y1="137" x2="194.0" y2="137.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200,137 194.0,140.0 194.0,134.0" fill="currentColor"/>
<text x="170" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">取任务</text>
<text x="265" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">改集合先拿 mainLock</text>
<rect x="10" y="190" width="130" height="30" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="75.0" y="209.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝策略</text>
<line x1="60" y1="158" x2="60.0" y2="184.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="60,190 57.0,184.0 63.0,184.0" fill="currentColor"/>
<text x="68" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 满了</text>
</svg>
```

**结构。** 三个结构各管一件事（core 是常驻线程数，max 是线程数上限）：`ctl`（一个原子整数）同时存运行状态和线程数；`workQueue` 存还没人取的任务；`workers`（`HashSet`）存所有工人线程，改它要先拿 `mainLock`。

**细节。**

- `ctl` 的高 3 位是运行状态（RUNNING、SHUTDOWN、STOP、TIDYING、TERMINATED），低 29 位是线程数，一次 CAS（比较并交换）就能同时检查、修改。
- 工人先跑手里的第一个任务，之后不停从 `workQueue` 取。

| 步骤 | 条件 | 碰哪几个结构 |
|---|---|---|
| 1 | 线程数 < core | `ctl` 加一，新建工人放进 `workers`，任务当它的第一个任务 |
| 2 | 否则 | `workQueue.offer`，成功就结束 |
| 3 | 入队失败（队满） | 线程数 < max 则新建工人，同步骤 1 |
| 4 | 仍失败 | 交给拒绝策略 |

**对应 LeetCode：** 无直接对应的题
