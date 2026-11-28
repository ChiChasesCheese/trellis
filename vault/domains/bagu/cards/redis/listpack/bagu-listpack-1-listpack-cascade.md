---
id: bagu-listpack-1-listpack-cascade
node: b.redis.listpack
type: qa
step: 1
---
## Q
**listpack · 连锁更新**｜加分

面试官：「老版本的压缩列表（ziplist）为什么会连锁更新？listpack 怎么避免？」

## A
**基本回答。** ziplist 每个节点开头记前一个节点的长度（为了能从后往前遍历）：小于 254 字节占 1 字节，否则占 5 字节。前一个节点变长跨过 254，后一个的记录要从 1 字节扩成 5 字节、自己也变长 4 字节，若本来就在 250 到 253 之间也跨过 254，再逼着下一个扩，一路传下去；每步都重新分配并挪动后面的内存，最坏累计 O(N²)，只有长度卡在 254 边界附近才发生，是「偶尔很贵」。listpack 每个节点是「编码 + 数据 + 自身长度」，自身长度（1 到 5 字节）放末尾，不依赖相邻节点，没有连锁更新；长度每个字节用最高位标记前面还有没有字节，所以仍可从末尾往回解析、双向遍历。内存仍连续、中间插入删除要挪字节，只用于小数据：Hash 超 512 个字段（`hash-max-listpack-entries`）或某个值超 64 字节（`hash-max-listpack-value`）就转 hashtable，转了不回退；Hash、ZSet 自 7.0、Set 自 7.2 起用 listpack。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ziplist：每个节点开头记前一个节点的长度</text>
<rect x="8" y="22" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A：250 字节</text>
<text x="57" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 1 字节</text>
<rect x="116" y="22" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="165" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B：250 字节</text>
<text x="165" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 1 字节</text>
<rect x="224" y="22" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C：250 字节</text>
<text x="273" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 1 字节</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 变长到 260，超过 254</text>
<rect x="8" y="90" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A：260 字节</text>
<text x="57" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 1 字节</text>
<rect x="116" y="90" width="98" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="165" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B：254 字节</text>
<text x="165" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 5 字节</text>
<rect x="224" y="90" width="98" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C：254 字节</text>
<text x="273" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前长度 5 字节</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B、C……后面每个节点依次重写</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">listpack：每个节点末尾记自己的长度</text>
<rect x="8" y="184" width="98" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="57" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A：260 字节</text>
<text x="57" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只改自己</text>
<rect x="116" y="184" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="165" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B：250 字节</text>
<text x="165" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不用动</text>
<rect x="224" y="184" width="98" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="200.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C：250 字节</text>
<text x="273" y="215.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不用动</text>
</svg>
ziplist 三个节点各 250 字节，A 变成 260 后 B 的「前长度」从 1 变 5 字节、涨到 254，C 跟着涨，一路往后；listpack 里 A 变长只改 A 自己。
**业务场景。** 一个 Hash 的字段值长度在 253 字节上下波动，旧版本一次更新引发连锁重写、CPU 抖动；换成 listpack 后更新只动自己。
**容易错。**
- **以为每次更新都会连锁。**
- **以为 listpack 不能倒着遍历。**
- **以为 listpack 能装大数据。**
