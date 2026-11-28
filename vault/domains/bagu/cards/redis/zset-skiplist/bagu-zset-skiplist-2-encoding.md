---
id: bagu-zset-skiplist-2-encoding
node: a.redis.zset-skiplist
type: qa
step: 2
---
## Q
**ZSet · 底层数据结构，小数据和大数据有什么不同**｜必会

面试官：「ZSet 底层是什么结构？成员少和多的时候一样吗？为什么要同时用两个结构？」

## A
**基本回答。** 成员少用紧凑的 listpack（7.0 前叫 ziplist），多了换成 skiplist 加 dict。成员数不超过 128（`zset-max-listpack-entries`）且每个成员不超过 64 字节（`zset-max-listpack-value`）用 listpack，两个条件是「或」的关系，任一项超过就转；`OBJECT ENCODING key` 可查。listpack 是连续内存、无指针，省内存，按成员查要扫一遍 O(N) 但 N 最多 128，且对 CPU 缓存友好。大了之后：跳表按分数排序，管范围和名次，但只知道成员名时没法定位；dict 记成员到分数，让 `ZSCORE` 是 O(1)，`ZADD` 更新已有成员时也靠它一步找到旧分数。两者指向同一份成员字符串，没存两遍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小：listpack（一整块连续内存）</text>
<rect x="8" y="26" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="72.8" y1="26" x2="72.8" y2="56" stroke-width="1.2" stroke="currentColor"/>
<line x1="137.6" y1="26" x2="137.6" y2="56" stroke-width="1.2" stroke="currentColor"/>
<line x1="202.39999999999998" y1="26" x2="202.39999999999998" y2="56" stroke-width="1.2" stroke="currentColor"/>
<line x1="267.2" y1="26" x2="267.2" y2="56" stroke-width="1.2" stroke="currentColor"/>
<line x1="332.0" y1="26" x2="332.0" y2="56" stroke-width="1.2" stroke="currentColor"/>
<text x="40.4" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成员1 分数</text>
<text x="105.19999999999999" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成员2 分数</text>
<text x="170.0" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成员3 分数</text>
<text x="234.79999999999998" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成员4 分数</text>
<text x="299.59999999999997" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…最多128</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">成员 ≤128 且每个 ≤64 字节</text>
<line x1="170" y1="82" x2="170" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,106.0 166.8,99.0 173.2,99.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="178" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">任一项超过就转换</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大：skiplist + dict，共用同一份成员</text>
<rect x="8" y="138" width="150" height="56" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">skiplist</text>
<text x="83.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">管名次和范围</text>
<rect x="182" y="138" width="150" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dict</text>
<text x="257.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成员→分数 ZSCORE</text>
<line x1="158" y1="166" x2="182" y2="166" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查名次走跳表，查分数走 dict</text>
</svg>
上半是小榜单：一整块连续内存，成员挨着放；任一阈值被突破就转成下半：跳表管排序，哈希表管按成员查分数，两者指向同一份成员数据。
**业务场景。** 每个直播间的「本场前 10 名观众」榜很小，用 listpack 几乎不占内存；全站日榜有百万主播，是 skiplist 加 dict，量级上 10 万个 `anchor:12345` 形的成员约 8.5MB（每元素约 85 字节），按此做容量规划；100 个同样的成员 listpack 只要约 1.6–2KB。再加一个 65 字节的成员，哪怕才 3 个成员也会转成 skiplist。
**容易错。**
- **把阈值记成 128 个字节：** 128 是成员个数，64 才是单个成员的字节数。
- **以为跳表节点只存成员和分数：** 还有后退指针（`ZREVRANGE` 用）和层数组，每层有 forward 指针与跨度 span（累加得名次）。
