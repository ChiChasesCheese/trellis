---
id: hi-sdx-gd-or-set
node: sd.problem-breakdowns.google-docs.more
type: qa
step: 5
---
## Q
**OR-Set：并发删除与重新加入**｜补充 · 协同文档（Google Docs） · 追问

面试官：「复制的集合里，副本 A 删除元素 x，副本 B 同时又把 x 加了一次。朴素集合和 2P-Set 为什么会出错？OR-Set 怎么解决？」

## A
**结论。** OR-Set（observed-remove）给每次添加附一个唯一标签，删除只删去删除者看见过的标签。B 并发重新加入的 x 带着 A 没见过的新标签，合并后存活，所以加入赢过并发的删除，删除后再加入也行得通。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="100" y="8" width="140" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">初始 {x#t1}</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个副本相同</text>
<polyline points="140,44 86.4,67.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,70 85.2,64.3 87.7,70.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="200,44 253.6,67.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,70 252.3,70.2 254.8,64.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="70" width="150" height="52" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A：删除 x</text>
<text x="85.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只删看见过的 t1</text>
<text x="85.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结果 {}</text>
<rect x="180" y="70" width="150" height="52" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B：重新加入 x</text>
<text x="255.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">带全新标签 t2</text>
<text x="255.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结果 {x#t1, x#t2}</text>
<polyline points="85,122 143.5,145.4" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150,148 142.3,148.4 144.7,142.4" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="255,122 196.5,145.4" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,148 195.3,142.4 197.7,148.4" style="fill:var(--accent,#3b6fd4)"/>
<rect x="80" y="148" width="180" height="52" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="163.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">合并：t2 没被 A 见过</text>
<text x="170.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没被删，结果 {x#t2}</text>
<text x="170.0" y="193.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x 保留：加入赢</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">朴素集合的增删不可交换，2P-Set 删了就再也加不回，</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">标签让并发的重新加入能存活。</text>
</svg>

**要点。**
- **朴素集合：** 添加和删除不可交换，副本按不同顺序看到就分叉，没有明确答案。
- **2P-Set：** 删除记进墓碑集合且永远生效，删了的元素再也加不回来。
- **OR-Set：** 标签区分了「同一个 x 的不同次添加」，删除只针对已观察到的那几次。
- **代价：** 标签和墓碑元数据随操作增长，需要定期压缩；用时间戳的 LWW 集合没有这份开销，但会因时钟偏差丢数据。

**面试里这样说。** 「购物车这类集合我用 OR-Set：每次添加带唯一标签，删除只删看见过的，所以一边删、一边并发重新加入，加入会保留，不会被悄悄吞掉。」

**易错。**
- **用 2P-Set 做购物车：** 删过的商品再也加不回。
- **以为删除总是赢：** OR-Set 里并发的加入赢。
