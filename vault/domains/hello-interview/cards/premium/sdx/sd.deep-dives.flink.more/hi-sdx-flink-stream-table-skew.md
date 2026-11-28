---
id: hi-sdx-flink-stream-table-skew
node: sd.deep-dives.flink.more
type: qa
step: 1
---
## Q
**流与表连接的时间偏差**｜补充 · Flink · 追问

面试官：「订单流要和用户地址表连接，地址表是用变更日志物化在本地的。订单事件晚到了几分钟，连出来的地址对吗？流与流的连接又会在哪里出问题？」

## A
**结论。** 不一定对。事件处理时去查的是表的当前状态，如果这期间地址改过，订单就连上了比它发生时更新的版本。解法是版本化的表（时态连接）：按事件时间查事件发生时有效的那一行，代价是要多存历史版本。

**要点。**
- **流与表：** 表一侧是变更日志物化出的本地存储（压缩主题加 RocksDB），每个事件查当前值；失败模式是时间偏差。
- **时态连接：** 保留每个键的多个版本，按事件时间选版本；状态更大，还要定义历史保留多久。
- **流与流：** 两侧都缓存在带窗口的状态里，每来一条就去探测对侧缓存；窗口之外才到的匹配，悄悄成了不连接，窗口大小是完整性和状态大小的交换。
- **共同前提：** 两边必须同键同分区数，否则先插入一次重分区。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">流与表连接：事件看到了较新的表</text>
<text x="8" y="42" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表：用户地址的版本</text>
<rect x="8" y="50" width="100" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v1 北京</text>
<rect x="140" y="50" width="100" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="190.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v2 上海</text>
<text x="250" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">← 之后才改</text>
<rect x="60" y="140" width="220" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单事件（改地址之前下的单）</text>
<polyline points="110,140 62.9,91.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="58,86 65.2,88.8 60.6,93.3" fill="currentColor"/>
<polyline points="230,140 194.2,91.6" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,86 196.7,89.7 191.6,93.5" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">应该关联</text>
<text x="240" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">实际关联</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">事件晚到被处理时，表里已是上海。</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">解法：版本化的表，按事件时间查当时的行</text>
</svg>

**面试里这样说。** 「流和表连接，我会先问这个业务要的是事件发生时的值，还是处理时的最新值。要前者就用版本化的表按事件时间连接；流和流的连接要为晚到的匹配留够窗口，并监控没匹配上的比例。」

**易错。**
- **默认处理时的值就是对的：** 重放或迟到时，同一条事件会连到不同的表版本，结果不可复现。
- **流流连接窗口设得太小：** 晚到的匹配静默丢失，没有任何错误。
