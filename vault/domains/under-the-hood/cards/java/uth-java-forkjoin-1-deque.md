---
id: uth-java-forkjoin-1-deque
node: java.forkjoin
type: qa
step: 1
---
## Q
**工作窃取是怎么偷的**｜Java · OpenJDK 25

`ForkJoinPool` 的每个线程有自己的任务队列，空闲的线程怎么从别人那里「偷」任务？

## A
**背景。** 把大任务拆成许多小任务并行做（fork 拆分、join 等结果）。所有线程共用一个任务队列，就会抢同一把锁；每个线程各用一个队列，又会出现有的线程队列堆满、有的线程闲着。折中：各用各的队列，闲下来的线程去别人的队列里偷。

**结构。** 每个工作线程一个双端队列（deque）：环形数组，初始 64 个槽，数组长度是 2 的幂。主人在一端（`top`）放入、取出，后进先出（LIFO）；小偷从另一端（`base`）用 CAS 取走最老的任务，先进先出（FIFO）。例：线程 A 的队列有 4 个任务，线程 B 空了，B 从 A 的队尾偷走最老的那个，A 照常从队头取。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="170" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 A 的双端队列</text>
<rect x="30" y="40" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="64" y="40" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="40" width="34" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1</text>
<rect x="132" y="40" width="34" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="149" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t2</text>
<rect x="166" y="40" width="34" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="183" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t3</text>
<rect x="200" y="40" width="34" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="217" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t4</text>
<rect x="234" y="40" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="268" y="40" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="115" y1="108" x2="115" y2="72" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115.0,72.0 118.0,78.0 112.0,78.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="115" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">base</text>
<text x="115" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小偷取最老</text>
<line x1="217" y1="108" x2="217" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="217.0,72.0 220.0,78.0 214.0,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="217" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">top</text>
<text x="217" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主人放入 取出</text>
<rect x="14" y="172" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="49" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 B 空</text>
<line x1="84" y1="180" x2="94" y2="150" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="94.0,150.0 94.9,156.6 89.3,154.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="250" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主人 LIFO 小偷 FIFO</text>
</svg>
```

**细节。**

- 小偷随机扫描挑受害者。
- 异步模式（`asyncMode`）下，自己也改为 FIFO。

**为什么。** 主人和小偷分在两端，平时不抢同一端，几乎无锁；比起生产者给空闲线程派活，小偷自己去找更快。

**对应 LeetCode：** 无直接对应的题
