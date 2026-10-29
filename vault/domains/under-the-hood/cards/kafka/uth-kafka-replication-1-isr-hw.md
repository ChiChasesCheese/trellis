---
id: uth-kafka-replication-1-isr-hw
node: kafka.replication
type: qa
step: 1
---
## Q
**多副本：高水位与 ISR**｜Kafka · 4.0

一个分区的数据存了好几份，消息写进 leader 后，消费者什么时候才读得到？一个副本落后到什么程度，会被当作“不同步”？

## A
**背景。** 机器会坏，所以每个分区存多份（副本）。两个极端都不好：只等一台写好就算成功，那台一坏刚写的消息就丢了；要求所有副本都写好才算成功，一个慢副本就拖住整个分区。

**结构。** 每个分区一个 leader（负责读写）加若干 follower（向 leader 拉取数据来复制）。ISR（in-sync replicas）是跟得上 leader 的副本集合；高水位（high watermark）是 ISR 内所有副本都已经有的最远位置，也就是各副本日志末端（LEO，下一条要写的位置）的最小值，消费者只能读到它之前的消息。图中三份日志的末端是 8、7、6，高水位就是 6。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="228" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">高水位 HW = 6</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">leader</text>
<rect x="60" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="88" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="102" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="144" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="172" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="186" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="200" y="24" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="214" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="228" y="24" width="28" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="256" y="24" width="28" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="290" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO 8</text>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f1</text>
<rect x="60" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="88" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="102" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="144" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="172" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="186" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="200" y="52" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="214" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="228" y="52" width="28" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="262" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO 7</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">f2</text>
<rect x="60" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="88" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="102" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="144" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="158" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="172" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="186" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="200" y="80" width="28" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="214" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="234" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LEO 6</text>
<line x1="228" y1="20" x2="228" y2="106" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者只能读到 HW 之前</text>
</svg>
```

**细节。**

- `replica.lag.time.max.ms` 默认 30000：follower 超过 30 秒没追上 leader 的末端，就被移出 ISR。
- 每当 follower 拉取进度更新，leader 就重算高水位（`maybeIncrementLeaderHW`）。

**为什么。** 对比多数派（如 Raft，多数副本确认才算提交）：容忍 f 个故障，ISR 只要 f+1 个副本，多数派要 2f+1 个；代价是慢副本会拖住提交，所以要把它踢出 ISR。

**对应 LeetCode：** 无直接对应的题
