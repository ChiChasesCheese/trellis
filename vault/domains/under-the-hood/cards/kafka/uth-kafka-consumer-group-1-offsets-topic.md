---
id: uth-kafka-consumer-group-1-offsets-topic
node: kafka.consumer-group
type: qa
step: 2
---
## Q
**位点存在哪：__consumer_offsets**｜Kafka · 4.0

消费者提交的位点（读到哪了）存在哪里？一个消费者组的位点由哪台 broker 负责？

## A
**背景。** 位点就是一张“（组，主题，分区）→ 读到哪了”的表，重启或换人之后它必须还在。可以另找一个数据库来存，但那等于给 Kafka 再装一套存储系统。

**结构。** Kafka 用自己存：写进内部主题 `__consumer_offsets`，key 是（组、主题、分区），value 是位点。这个主题开了压实（只留每个 key 的最新值），所以表不会无限变长。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="8" y="18" width="76" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">groupId</text>
<line x1="84" y1="32" x2="94" y2="32" stroke="currentColor" stroke-width="1.2"/>
<polygon points="100,32 94.0,35.0 94.0,29.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="18" width="118" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="159" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">abs(hash) % 50</text>
<line x1="218" y1="32" x2="228" y2="32" stroke="currentColor" stroke-width="1.2"/>
<polygon points="234,32 228.0,35.0 228.0,29.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="234" y="18" width="98" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="283" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区 17</text>
<line x1="283" y1="48" x2="283" y2="72" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="283,78 280.0,72.0 286.0,72.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="293" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">leader</text>
<rect x="222" y="80" width="110" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="277" y="98.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">broker 协调者</text>
<rect x="8" y="80" width="180" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="98" y="98.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(组,主题,分区) -&gt; 位点</text>
<line x1="222" y1="94" x2="196" y2="94" stroke="currentColor" stroke-width="1.2"/>
<polygon points="190,94 196.0,91.0 196.0,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__consumer_offsets: 50 个分区, 开压实</text>
</svg>
```

**细节。**

- 默认 50 个分区（`offsets.topic.num.partitions`），副本因子 3。
- 组到分区：`abs(groupId.hashCode()) % 50`；该分区 leader 所在的 broker 就是这个组的协调者。
- 位点默认保留 7 天（`offsets.retention.minutes`），从组变空开始计时。

**为什么。** 按组名哈希分到 50 个分区，各组的协调工作就均匀分给不同的 broker。

**对应 LeetCode：** 无直接对应的题
