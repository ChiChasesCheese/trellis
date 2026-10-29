---
id: uth-go-rust-go-scheduler-2-steal
node: go-rust.go-scheduler
type: qa
step: 2
---
## Q
**空闲的 P 怎么找活干**｜Go · 1.27 运行时

某个 P 的本地队列空了，它怎么拿到别人的 goroutine？

## A
**背景。** 每个 P 只管自己的本地队列，有的队列会先空掉，有的还排得很长。要让闲的 P 去拿忙的 P 手里的活，又不能频繁加锁。

**结构。** 工作窃取（work stealing）：空闲 P 随机挑别的 P，从它的本地队列里偷走一半。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">P2 的队列空了, 随机挑 P1 去偷</text>
<text x="8" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">P1 本地队列</text>
<rect x="90" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="107" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g1</text>
<rect x="128" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="145" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g2</text>
<rect x="166" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="183" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g3</text>
<rect x="204" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="221" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g4</text>
<rect x="242" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="259" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g5</text>
<rect x="280" y="26" width="34" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="297" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g6</text>
<text x="8" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">P2 本地队列</text>
<rect x="90" y="86" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="128" y="86" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="166" y="86" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="205" y1="52" x2="130" y2="84" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="130,84 134.5,79.2 136.6,84.1" style="fill:var(--accent,#3b6fd4)"/>
<text x="205" y="70" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">偷走后一半 n - n/2 个</text>
<text x="8" y="140" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">找活最多重试 4 轮, 最后一轮才偷对方的 runnext</text>
<text x="8" y="158" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每调度 61 次, 先看一眼全局队列, 免得它饿死</text>
</svg>
```

**细节。**

- 每次偷 `n - n/2` 个，也就是队列长度的一半向上取整
- 找活最多重试 4 轮，最后一轮才会去偷对方的 `runnext`
- 每调度 61 次（`schedtick % 61`）先看一眼全局队列

**为什么。** 偷一半让负载一次就平摊开；每 61 次查全局队列，避免两个互相唤醒的 goroutine 一直占着本地队列，全局队列里的 goroutine 饿死。

**对应 LeetCode：** 无直接对应的题（调度策略）
