---
id: uth-redis-streams-geo-2-delta
node: redis.streams-geo
type: qa
step: 2
---
## Q
**同样的消息为什么存得这么省**｜Redis · 8.10

一个 Stream 里每条消息都带相同的字段名，Redis 是不是重复存了很多遍？

## A
**背景。** 日志类的消息，字段名几乎一模一样，ID 又紧挨着。如果每条都把字段名和完整 ID 再写一遍，绝大部分字节都是重复的。办法：只记第一次的完整内容，后面的只记“和它的差别”。

**结构。** 每个 listpack 的开头有一条主条目（master entry），记下字段名；后面的消息只存相对它的差值。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">一个 listpack 里的消息</text>
<rect x="10" y="26" width="310" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="165" y="43" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">主条目: 字段名 (name, temp) + 基准 ID</text>
<text x="165" y="59" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">记一次, 后面的消息都不再重复</text>
<rect x="10" y="78" width="100" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="60" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">Δ毫秒 Δ序号</text>
<text x="60" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相同字段标志</text>
<text x="60" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值, 值</text>
<rect x="116" y="78" width="100" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="166" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">Δ毫秒 Δ序号</text>
<text x="166" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相同字段标志</text>
<text x="166" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值, 值</text>
<rect x="222" y="78" width="100" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="272" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">Δ毫秒 Δ序号</text>
<text x="272" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相同字段标志</text>
<text x="272" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值, 值</text>
<text x="8" y="158" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ID 只存与节点键的差值, 不存完整 128 位</text>
<text x="8" y="176" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">字段与主条目完全相同: 字段名和个数都省掉</text>
<text x="8" y="194" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">删除只打标记, 整个节点的消息删光才回收</text>
</svg>
```

**细节。**

- 消息 ID 存成与节点键的毫秒差、序号差，而非完整 128 位
- 字段与主条目完全相同的消息，带“相同字段”标志，字段名和个数都省掉
- 删除只是打标记，节点里的消息全被删光才回收整个节点

**为什么。** 日志类流的字段几乎一样，ID 又紧挨着，差值编码后每条只剩几个小整数和值本身。

**对应 LeetCode：** 无直接对应的题（差值编码）
