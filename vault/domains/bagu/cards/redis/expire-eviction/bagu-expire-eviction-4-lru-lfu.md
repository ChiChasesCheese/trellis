---
id: bagu-expire-eviction-4-lru-lfu
node: a.redis.expire-eviction
type: qa
step: 4
---
## Q
**LRU 与 LFU · Redis 的近似 LRU 怎么实现**｜追问

面试官：「Redis 的 LRU 和教科书里链表加哈希表的 LRU 一样吗？LRU 和 LFU 有什么区别？」

## A
**基本回答。** 不一样。教科书 LRU 要全局双向链表加哈希表，每次读挪节点，还要每 key 多存两个指针。Redis 用近似 LRU：每个对象只存 24 位访问时钟（秒级），淘汰时随机抽 `maxmemory-samples`（默认 5）个 key 放进大小 16 的候选池，淘汰空闲最久的；省指针内存、读不用挪节点，样本越大越接近真 LRU、CPU 越高。LRU 只看最近一次访问，一次性大扫描会把冷数据变成「最近使用」，挤出真正的热数据。LFU 看频率、抗扫描：同样 24 位，高 16 位记最近一次衰减时间（分钟），低 8 位是对数计数器；计数概率性增长，`lfu-log-factor`（默认 10）越大越难涨，约 100 万次访问才饱和到 255；`lfu-decay-time`（默认 1 分钟）控制衰减，曾经很热的慢慢降温；新 key 起点是 5 而不是 0，避免刚写入就被淘汰。`OBJECT IDLETIME` 用于 LRU，`OBJECT FREQ` 只在 LFU 策略下可用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">近似 LRU：不维护链表，只抽样</text>
<rect x="8" y="24" width="92" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全部 key</text>
<text x="54" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（百万个）</text>
<line x1="100" y1="52" x2="118" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,52 111.0,55.2 111.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="96" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">随机抽 5 个</text>
<text x="166" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（samples）</text>
<line x1="214" y1="52" x2="232" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232,52 225.0,55.2 225.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="24" width="100" height="56" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">候选池</text>
<text x="282" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大小 16</text>
<line x1="282" y1="80" x2="282" y2="104" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="282,104 278.8,97.0 285.2,97.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="332" y="122" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">淘汰空闲最久的</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LRU 对象头：24 位</text>
<rect x="8" y="156" width="324" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="172.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">访问时钟（秒级）</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LFU 同样 24 位：</text>
<rect x="8" y="210" width="216" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="116" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高 16 位：最近访问（分钟）</text>
<rect x="224" y="210" width="108" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">低 8 位：计数</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">计数概率性增长，新 key 起点是 5</text>
</svg>
上半是近似 LRU 的抽样；下半是 LRU 和 LFU 各占的同样 24 位。
**业务场景。** 缓存里 3000 个正在直播的热门房间，每个每分钟被访问几百次；运营导出任务扫了 100 万个历史直播间各访问 1 次。LRU 下这 100 万个冷房间空闲时间只有几秒，抽样里「空闲最久」的反而是恰好这几秒没人看的热门房间，被淘汰；LFU 下冷房间计数只有 5 或 6，先被淘汰，热门房间保住。
**容易错。**
- **以为 Redis 用链表实现 LRU。**
- **以为 LFU 计数是精确次数。**
- **在 LRU 策略下用 OBJECT FREQ。**
