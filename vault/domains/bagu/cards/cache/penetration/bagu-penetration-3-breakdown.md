---
id: bagu-penetration-3-breakdown
node: a.cache.penetration
type: qa
step: 2
---
## Q
**缓存击穿 · 热 key 过期的两种重建**｜必会

面试官：「一个爆款商品的缓存刚好过期，同一刻上万请求都未命中，数据库被打满。这叫什么？互斥重建和逻辑过期各在什么情况下会失效？」

## A
**基本回答。** 这是缓存击穿（Cache Breakdown）：数据存在，是热 key 暂时失效。方案一互斥重建：`SET lock:key NX PX 3000` 抢锁，抢到的读库回填，其余短暂休眠后重读缓存；方案二逻辑过期：不设 TTL，过期时间戳存在 value 里，读到过期值先返回旧值，抢到锁的线程异步重建；已知热点还可以永不过期加后台主动刷新。要强一致选互斥，要低延迟选逻辑过期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">热 key 刚过期，同一刻 N 个请求</text>
<rect x="8" y="26" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">N 个请求</text>
<line x1="104" y1="41" x2="124" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124.0,41.0 117.0,44.2 117.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="124" y="26" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="172.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存：已过期</text>
<line x1="220" y1="41" x2="240" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="240.0,41.0 233.0,44.2 233.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="240" y="26" width="92" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">方案一：互斥重建</text>
<rect x="8" y="94" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET lock NX PX 3000</text>
<text x="166" y="107" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抢到：读库回填</text>
<text x="166" y="122" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">其余：休眠几十毫秒重读</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要点：double check、锁要有 TTL</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">方案二：逻辑过期</text>
<rect x="8" y="198" width="150" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="217.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">value 里带过期时间</text>
<text x="166" y="207" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读到过期值：先返回旧值</text>
<text x="166" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抢到锁的线程异步重建</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：短暂读到旧数据、多占内存</text>
</svg>
顶部一行是击穿发生的瞬间；下方两块分别是两种保护办法，各带一句代价。
**容易错。**
- **把击穿当成穿透：** 击穿是数据存在、热 key 过期；穿透是数据根本不存在。办法也不同。
- **锁不设 TTL：** 重建线程崩溃，锁永远不释放，没人重建。
- **拿到锁就直接读库：** 要先再查一次缓存，否则别人刚回填完你又重复回源。
- **等待者无限等或无限重试：** 要有最大等待次数，否则等不到时全部去打库。
- **以为逻辑过期没代价：** 会读到旧数据，重建失败就一直旧。
- **singleflight 当全部方案：** singleflight（Go）或 Caffeine 的 `computeIfAbsent` 只合并单进程内同一 key 的并发加载。
**举个例子。** 爆款盲盒详情缓存整点过期，同一刻 10000 个请求：只有 1 个 `SET lock NX` 成功，读库回填；其余 9999 个休眠几十毫秒再读缓存，已命中。逻辑过期的对照：所有请求立刻拿到旧值，只有 1 个后台线程重建，代价是这几十毫秒内看到旧价格。
