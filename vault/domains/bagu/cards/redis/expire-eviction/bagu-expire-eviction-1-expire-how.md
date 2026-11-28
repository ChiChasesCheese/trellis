---
id: bagu-expire-eviction-1-expire-how
node: a.redis.expire-eviction
type: qa
step: 1
---
## Q
**过期键 · Redis 怎么删除过期的 key**｜必会

面试官：「给 key 设了 10 秒过期，到点 Redis 怎么删？是立刻删吗？」

## A
**基本回答。** 不是到点立刻删（每个 key 一个定时器，百万个占内存和 CPU，还要在单线程里准时触发，抢命令执行的时间），而是惰性加定期。惰性：访问时先查过期时间，过期当场删并按不存在返回，所以过期的 key 一定读不到。定期：后台周期性抽样带过期时间的 key 删掉过期的（不全量扫描，O(N) 会长时间阻塞主线程），补上没人访问的残留。过期时间存在每个库的 `expires` 字典里（key 到毫秒时间戳）；传给从库和持久化文件的是绝对时间戳，主从系统时钟要同步。`TTL` 返回 -2 表示 key 不存在，-1 表示存在但没设过期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="8" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">expires 字典（每个库一份）</text>
<text x="170" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key → 到期的毫秒时间戳</text>
<line x1="86" y1="52" x2="86" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,82 82.8,75.0 89.2,75.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="254" y1="52" x2="254" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254,82 250.8,75.0 257.2,75.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="82" width="156" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">惰性：访问时检查</text>
<text x="86" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期就当场删</text>
<text x="86" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按不存在返回</text>
<rect x="176" y="82" width="156" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">定期：后台抽样</text>
<text x="254" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带过期时间的 key</text>
<text x="254" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期的删掉</text>
<rect x="8" y="164" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">效果：过期的 key 一定读不到</text>
<text x="170" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">但内存不一定马上释放</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不用定时器：百万个定时器占内存又抢 CPU</text>
</svg>
惰性发生在访问的那一刻，定期由后台抽样触发，两条路径合起来才保证「读不到」；但内存不一定马上释放，就算删了 jemalloc 也不一定把空闲内存还给操作系统。
**业务场景。** 活动页给每个用户的「今日已领奖励」标记设 24 小时过期：到点用户再访问立刻发现不存在；没人再访问的几百万个标记还会在内存里留一会，容量规划要留余量，不能按 TTL 精确算。
**容易错。**
- **以为到点立刻删。**
- **以为 key 过期后内存就降了。**
- **以为 -1 和 -2 一回事。**
