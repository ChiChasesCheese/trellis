---
id: uth-os-net-scheduler-2-weight
node: os-net.scheduler
type: qa
step: 2
---
## Q
**nice 值怎么变成 CPU 份额**｜Linux · 内核 7.3

nice 值只差 1，两个任务分到的 CPU 差多少？一棵树怎么同时容纳不同优先级？

## A
**背景。** 任务有优先级：`nice` 值（-20 到 19，越小越优先）。想让高优先级任务多拿 CPU，又不想给每个优先级各建一个队列。办法：让它的 `vruntime` 涨得慢。涨得慢，长期靠左，就更常被选中。

**结构。** 每个任务有一个权重，`vruntime += 实际运行时间 × 1024 / 权重`，权重越大涨得越慢。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<line x1="40" y1="20" x2="40" y2="172" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="172" x2="262" y2="172" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">vruntime</text>
<text x="262" y="190" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">实际运行时间</text>
<line x1="40" y1="172" x2="250" y2="62" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="172" x2="250" y2="34" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="66" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">nice 0</text>
<text x="258" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">nice 1</text>
<text x="130" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">权重 1024 涨得慢</text>
<text x="60" y="60" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">权重 820 涨得快</text>
<text x="170" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">涨得慢 排得靠左 被选得更多</text>
</svg>
```

**细节。**

- 权重表 `sched_prio_to_weight[40]`：nice 0 是 1024，nice 1 是 820，nice -1 是 1277，每级约 1.25 倍
- 两端：nice -20 是 88761，nice 19 是 15，相差近 6000 倍
- 两个任务 nice 差 1，份额约 55% 对 45%

**为什么。** 不给每个优先级各建一个队列，而是把优先级折进“时钟走速”，一个排序键就够了。

**对应 LeetCode：** 无直接对应的题
