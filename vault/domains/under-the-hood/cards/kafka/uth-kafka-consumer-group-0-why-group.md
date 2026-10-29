---
id: uth-kafka-consumer-group-0-why-group
node: kafka.consumer-group
type: qa
step: 1
---
## Q
**消费者组：几个消费者怎么分着读一个主题**｜Kafka · 4.0

一个主题被切成多个分区（各自独立的一条日志）。想让几个消费者一起把它读完、不重不漏，该怎么分工？成员进进出出怎么办？

## A
**背景。** 一个主题每秒可能有几十万条消息，一个消费者读不过来。但同一个分区里的消息有先后顺序，两个人同时读同一个分区就会乱。最直接的办法是人工给每个消费者指定分区，可机器一挂，就得有人去改配置。

**结构。** 配了相同 `group.id` 的消费者自动组成消费者组（consumer group），Kafka 保证每个分区在同一时刻只分给组内一个消费者。成员加入或离开时，由协调者（coordinator，某一台 broker）发现，重新分配分区，叫再平衡（rebalance）。每个消费者会记下自己读到哪了（位点，offset），换人之后新负责人从那里接着读。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 个分区, 2 个消费者</text>
<rect x="8" y="22" width="120" height="34" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C0</text>
<rect x="46" y="28" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="64" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="86" y="28" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="104" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="140" y="22" width="90" height="34" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<rect x="178" y="28" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="196" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<line x1="170" y1="60" x2="170" y2="88" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,94 167.0,88.0 173.0,88.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">C2 加入: 再平衡</text>
<rect x="8" y="98" width="98" height="34" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C0</text>
<rect x="54" y="104" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="114" y="98" width="98" height="34" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<rect x="160" y="104" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="178" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="220" y="98" width="98" height="34" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="226" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C2</text>
<rect x="266" y="104" width="36" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<text x="170" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每个分区同一时刻只有一个读者</text>
</svg>
```

**为什么。** 分区数就是组内并行读的上限；“一个分区一个读者”换来分区内有序。

**对应 LeetCode：** 无直接对应的题
