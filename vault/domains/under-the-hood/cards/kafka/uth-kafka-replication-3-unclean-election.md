---
id: uth-kafka-replication-3-unclean-election
node: kafka.replication
type: qa
step: 3
---
## Q
**ISR 全挂了，落后的副本能当 leader 吗**｜Kafka · 4.0

一个分区的 ISR 副本全部宕机，只剩落后的副本还活着，Kafka 能不能让它当 leader？

## A
**背景。** 落后的副本缺最后几条消息。让它当 leader，分区马上能用，但缺的那几条再也找不回；不让它当，就只能等 ISR 成员回来，分区一直不可用。

**结构。** 由 `unclean.leader.election.enable` 决定，默认 `false`（0.11.0.0 起）：只有 ISR 成员有资格当 leader；设为 `true` 则允许落后副本“最后一搏”。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧 leader</text>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">落后副本</text>
<rect x="80" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="92.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="80" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="92.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="105" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="117.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="105" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="117.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="142.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="130" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="155" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="167.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="155" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="167.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="180" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="192.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="180" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="192.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="205" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="217.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="205" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="217.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="230" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="242.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="230" y="56" width="25" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="242.5" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="255" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="267.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="280" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="292.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="305" y="22" width="25" height="24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="317.5" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<line x1="255" y1="52" x2="330" y2="52" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="293" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7-9 会丢</text>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">它当 leader 后, 7-9 永远找不回</text>
</svg>
```

**细节。**

- 选 ISR 成员：保证拥有所有已提交（高水位以下）的消息，但 ISR 不恢复，分区就一直不可用。
- 选落后副本：分区马上可用，它的日志成为事实标准，却不保证含有每条已提交的消息，可能丢数据。

**为什么。** 这是可用性与一致性的二选一，基于投票的方案（如多数派）同样躲不开。

**对应 LeetCode：** 无直接对应的题
