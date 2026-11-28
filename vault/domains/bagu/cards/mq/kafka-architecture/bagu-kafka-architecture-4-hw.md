---
id: bagu-kafka-architecture-4-hw
node: a.mq.kafka-architecture
type: qa
step: 4
---
## Q
**Kafka 结构 · 高水位与 leader epoch**｜追问

面试官：「为什么消费者只能看到高水位之前的消息？换 leader 时日志怎么不分叉？」

## A
**基本回答。** 高水位（HW，High Watermark）是 ISR 里所有副本都已复制的位置。消费者只能读到 HW 之前的消息，所以还没充分复制的数据不会被读到后又丢失。
LEO（Log End Offset）是每个副本日志的末端位置，HW 取各副本 LEO 的最小值，不会超过它。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="166" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">HW = 4</text>
<text x="8" y="51" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">leader</text>
<rect x="70" y="34" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="34" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="118" y="34" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="142" y="34" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="166" y="34" width="24" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="178.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="190" y="34" width="24" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="202.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="222" y="51" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO=6</text>
<text x="8" y="91" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F1</text>
<rect x="70" y="74" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="74" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="118" y="74" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="142" y="74" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="166" y="74" width="24" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="178.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="222" y="91" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO=5</text>
<text x="8" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">F2</text>
<rect x="70" y="114" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="114" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="118" y="114" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="142" y="114" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="222" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO=4</text>
<line x1="166" y1="22" x2="166" y2="144" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">消费者只能读 offset 0~3（HW 之前）</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4、5 还没被所有同步副本复制，不让读</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">leader epoch：每次换 leader 加一，follower 据此截断</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">截断多余日志，换主后日志不分叉</text>
</svg>
三个副本的日志长度不同；虚线是高水位 4，高亮的格子（offset 0~3）所有副本都有，消费者只能读这一段。
**举个例子。** 一个分区三个副本，leader 已写到 offset 5，F1 到 4，F2 到 3。
1. **各自的 LEO：**leader 6，F1 5，F2 4（LEO 是下一个要写的位置）。
2. **HW：**取最小值，HW = 4。
3. **消费者能读：**offset 0~3，共 4 条。
4. **offset 4、5：**还没被所有同步副本复制，消费者读不到。
5. **leader 宕机：**F1 当选新 leader，它有 offset 0~4；之前消费者读到的 0~3 都还在，不会出现「读到了又消失」。
6. **epoch 加一：**新 leader 的 epoch 增加，之后重启回来的旧 leader 先按新 epoch 截断自己多余的日志，再追赶。
**容易错。**
- **以为消费者能读到 leader 上最新的消息：** 只能读到 HW 之前。
- **以为 HW 等于 leader 的 LEO：** HW 是各副本里最小的位置，不会超过任何一个副本的 LEO。
- **以为换 leader 后日志靠 HW 就一致：** 早期只靠 HW 会分叉或丢数据，要靠 leader epoch 截断。
- **以为 ISR 和 Raft 多数派一样：** ISR 容忍 f 个故障要 f+1 个副本，多数派要 2f+1；代价是成员判断依赖时间。
