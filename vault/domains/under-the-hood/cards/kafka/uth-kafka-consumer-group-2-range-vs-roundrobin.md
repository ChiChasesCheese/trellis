---
id: uth-kafka-consumer-group-2-range-vs-roundrobin
node: kafka.consumer-group
type: qa
step: 3
---
## Q
**Range 与 RoundRobin：把分区分给消费者**｜Kafka · 4.0

2 个主题各 3 个分区，2 个消费者都订阅全部主题。Range 和 RoundRobin 两种分配策略，各分出什么结果？

## A
**背景。** 再平衡时要决定“哪个分区给哪个消费者”，这套规则叫分配策略（assignor）。

**结构。** Range 按主题逐个分：每个主题里，分区数除以消费者数取整，前面的消费者多拿一个。RoundRobin 把所有主题的分区排成一队，像发牌一样轮流发。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 142">
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Range</text>
<text x="8" y="86" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RoundRobin</text>
<rect x="100" y="24" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="118" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p0</text>
<rect x="100" y="70" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="118" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p0</text>
<rect x="139" y="24" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="157" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p1</text>
<rect x="139" y="70" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="157" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p1</text>
<rect x="178" y="24" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="196" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p2</text>
<rect x="178" y="70" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="196" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t0p2</text>
<rect x="217" y="24" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p0</text>
<rect x="217" y="70" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p0</text>
<rect x="256" y="24" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="274" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p1</text>
<rect x="256" y="70" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="274" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p1</text>
<rect x="295" y="24" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="313" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p2</text>
<rect x="295" y="70" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="313" y="87.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1p2</text>
<rect x="100" y="108" width="36" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="118" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C0</text>
<rect x="144" y="108" width="36" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="162" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<text x="192" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个消费者, 两个主题</text>
</svg>
```

**细节。**

- 图中 Range 让 C0 拿 4 个、C1 拿 2 个；RoundRobin 各拿 3 个。
- 客户端默认策略是 `[RangeAssignor, CooperativeStickyAssignor]`（3.0 起，之前只有 Range）。

**坑。** Range 对每个主题都让排在前面的消费者多拿：主题越多、分区数越除不尽，前面的消费者越吃重。

**对应 LeetCode：** 无直接对应的题
