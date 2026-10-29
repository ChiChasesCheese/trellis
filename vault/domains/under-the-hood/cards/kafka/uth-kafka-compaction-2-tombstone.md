---
id: uth-kafka-compaction-2-tombstone
node: kafka.compaction
type: qa
step: 3
---
## Q
**墓碑：在只追加的日志里删数据**｜Kafka · 4.0

压实主题里想删掉一个 key，应该发什么消息？这条消息自己什么时候被清掉？

## A
**背景。** 日志只能追加，没法真的“擦掉”一条消息；而压实只保留每个 key 的最新值。

**结构。** 把“删除”也写成一条消息：同 key、value 为 `null`，叫墓碑（tombstone）。它是这个 key 的最新值，压实时盖掉前面所有旧值。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 178">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写入顺序</text>
<rect x="8" y="20" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K1 v1</text>
<rect x="92" y="20" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K2 v2</text>
<rect x="176" y="20" width="76" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="214" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K1 null</text>
<text x="262" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">墓碑</text>
<line x1="214" y1="48" x2="214" y2="72" stroke="currentColor" stroke-width="1.2"/>
<polygon points="214,78 211.0,72.0 217.0,72.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">压实后</text>
<rect x="8" y="82" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="46" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已盖掉</text>
<rect x="92" y="82" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K2 v2</text>
<rect x="176" y="82" width="76" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="214" y="99.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K1 null</text>
<line x1="214" y1="110" x2="214" y2="134" stroke="currentColor" stroke-width="1.2"/>
<polygon points="214,140 211.0,134.0 217.0,134.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="224" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">24 小时后</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后</text>
<rect x="8" y="144" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="46" y="161.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已盖掉</text>
<rect x="92" y="144" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="161.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">K2 v2</text>
<rect x="176" y="144" width="76" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="214" y="161.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已删除</text>
</svg>
```

**细节。**

- 墓碑自己最终也会被清掉，但先保留 `delete.retention.ms`（默认 24 小时），让读得慢的消费者也有机会看到“这个 key 被删了”。
- 压实不改偏移量：被删消息的位置变成空洞，从空洞位置读，得到的是下一个仍存在的偏移量。

**为什么。** 把“删除”写成普通消息，所有副本和消费者按同样的顺序重放，就得到同样的结果。

**对应 LeetCode：** 无直接对应的题
