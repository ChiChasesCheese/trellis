---
id: bagu-expire-eviction-3-evict-policy
node: a.redis.expire-eviction
type: qa
step: 3
---
## Q
**内存淘汰 · 内存满了会怎样，有哪些策略**｜必会

面试官：「Redis 内存用到上限会发生什么？有哪些淘汰策略，缓存场景怎么选？」

## A
**基本回答。** `maxmemory` 设上限，到上限后每次执行新命令前按 `maxmemory-policy` 淘汰 key 直到回到上限内；淘汰在主线程做，内存持续顶着上限时几乎每次写都伴随一次淘汰，耗时算在主线程。默认 `noeviction`：读照常，写报 `OOM command not allowed`。其余 7 种由「范围 × 依据」组成：`allkeys-*` 淘汰所有 key，`volatile-*` 只淘汰带过期时间的（没有 key 带 TTL 时退化成 `noeviction`）；依据 `lru`（最久没访问）、`lfu`（访问最少）、`random`，另有 `volatile-ttl`（剩余寿命最短）。缓存通常选 `allkeys-lru` 或 `allkeys-lfu`。锁、会话、计数器、幂等标记这类不能丢的数据要与缓存拆成不同实例：被不带 TTL 的 key 占满内存后，带 TTL 的缓存淘汰光了写入仍然失败。从库默认 `replica-ignore-maxmemory yes`，不自己淘汰，由主库淘汰后传 `DEL`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">策略名 = 范围 + 依据，再加一个 noeviction</text>
<rect x="96" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lru</text>
<rect x="154" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lfu</text>
<rect x="212" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">random</text>
<rect x="270" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ttl</text>
<text x="8" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">allkeys-*</text>
<rect x="96" y="58" width="56" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="154" y="58" width="56" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="182" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="212" y="58" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="270" y="58" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">—</text>
<text x="8" y="111" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">volatile-*</text>
<rect x="96" y="92" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="154" y="92" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="212" y="92" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="270" y="92" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="8" y="132" width="324" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">allkeys-*：所有 key 都可淘汰</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">volatile-*：只淘汰带过期时间的</text>
<rect x="8" y="190" width="324" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="209" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认 noeviction：读照常</text>
<text x="170" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写报 OOM command not allowed</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缓存通常选 allkeys-lru 或 allkeys-lfu</text>
</svg>
除 noeviction 外都是范围 × 依据的组合，高亮两格是缓存最常选的；allkeys 没有 ttl 一格，因为 ttl 只对带过期时间的 key 有意义。
**业务场景。** 大促商品和直播间缓存用 `allkeys-lfu`，满了先留热门直播间；同实例里的「打赏幂等标记」若被淘汰，同一回调会被当成新请求，应放进单独的 `noeviction` 实例并配容量告警。
**容易错。**
- **以为默认会自动淘汰。**
- **以为 volatile-* 总能腾出空间。**
- **以为从库会自己淘汰。**
