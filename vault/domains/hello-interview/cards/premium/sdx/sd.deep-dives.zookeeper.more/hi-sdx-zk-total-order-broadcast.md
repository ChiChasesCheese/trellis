---
id: hi-sdx-zk-total-order-broadcast
node: sd.deep-dives.zookeeper.more
type: qa
step: 5
---
## Q
**全序广播与共识：用日志决定先后**｜补充 · ZooKeeper · 加分

面试官：「全序广播（total order broadcast）保证什么？它和共识是什么关系？怎样靠它实现「用户名唯一」这种线性一致的比较并设置？」

## A
**结论。** 全序广播保证两点：消息可靠送达不丢，并且所有节点按同一顺序看到同样的消息。它与共识等价，日志的每个位置就是一次共识决定，所以 Raft、Paxos 能提供全序广播，反过来也成立。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">共享日志（位置就是全序）</text>
<rect x="10" y="28" width="100" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="60.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置 1</text>
<text x="60.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">认领 alice：A</text>
<rect x="120" y="28" width="100" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置 2</text>
<text x="170.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">认领 alice：B</text>
<rect x="230" y="28" width="100" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置 3</text>
<text x="280.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">认领 bob：C</text>
<polyline points="60,72 60.0,93.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,100 56.8,93.0 63.2,93.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,72 170.0,93.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,100 166.8,93.0 173.2,93.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每个节点按位置读日志，</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">alice 的第一条认领是位置 1：A 赢，B 输。</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">没有任何节点需要比较时钟，</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">日志位置就是唯一的先后。</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共识、全序广播、复制状态机是同一件事。</text>
</svg>

**要点。**
- **唯一性怎么做：** 把「我要认领 alice」这条消息追加到日志，再把日志按顺序读回来，只有当自己的消息是 alice 的第一条认领时才算赢。
- **为什么线性一致：** 日志位置就是串行顺序，不依赖任何时钟。
- **同一个想法：** 复制状态机、Raft 日志、Kafka 分区内的顺序，都是不同容错级别下的同一个「日志决定先后」。

**面试里这样说。** 「需要全局唯一的东西，我把认领追加到一个复制日志里，按日志顺序谁先谁赢；日志位置就是先后，所以不需要比较时钟。」

**易错。**
- **以为全序广播只是排序：** 它还要求可靠送达，和共识等价。
- **读了日志之前就认定赢了：** 必须读回日志，确认自己的认领是第一条。
