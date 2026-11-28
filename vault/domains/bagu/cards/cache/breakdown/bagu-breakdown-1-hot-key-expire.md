---
id: bagu-breakdown-1-hot-key-expire
node: b.cache.breakdown
type: qa
step: 1
---
## Q
**缓存击穿 · 热 key 过期的三种解法**｜必会

面试官：「秒杀商品详情的缓存在零点过期，十万请求同时回源。这叫什么，和穿透、雪崩有什么区别，怎么解决？」

## A
**基本回答。** 这是击穿：一个访问量极大的热 key 恰好过期，同一时刻大量请求都未命中，一起回源并重建，数据库被瞬间打满。穿透是查不存在的数据，雪崩是大批 key 同时失效。方案：互斥重建，`SET lock:key NX PX 3000` 抢锁，抢到的回源回填，其余短暂休眠后重读缓存；逻辑过期，缓存不设 TTL、过期时间戳放在 value 里，读到过期值先返回旧值，抢到锁的线程异步重建，读请求不用等，代价是短暂读旧数据、多占内存、重建一直失败就一直读旧值；爆款（首页、秒杀商品）后台定时刷新，永不靠过期触发。要强一致选互斥，要低延迟选逻辑过期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没保护：十万个请求一起回源</text>
<rect x="10" y="22" width="72" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 万请求</text>
<rect x="112" y="22" width="98" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存：已过期</text>
<rect x="260" y="22" width="70" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="295" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<line x1="82" y1="39" x2="112" y2="39" stroke="currentColor" stroke-width="1.2"/>
<polygon points="112,39 105.7,42.0 105.7,36.0" fill="currentColor"/>
<text x="235" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×10 万</text>
<line x1="210" y1="39" x2="260" y2="39" stroke="currentColor" stroke-width="1.2"/>
<polygon points="260,39 253.7,42.0 253.7,36.0" fill="currentColor"/>
<text x="10" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">互斥重建：只有一个去查库</text>
<rect x="10" y="94" width="72" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="115" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 万请求</text>
<rect x="112" y="94" width="98" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="115" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存：已过期</text>
<rect x="260" y="94" width="70" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="295" y="115" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<line x1="82" y1="111" x2="112" y2="111" stroke="currentColor" stroke-width="1.2"/>
<polygon points="112,111 105.7,114.0 105.7,108.0" fill="currentColor"/>
<text x="235" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×1</text>
<line x1="210" y1="111" x2="260" y2="111" stroke="currentColor" stroke-width="1.2"/>
<polygon points="260,111 253.7,114.0 253.7,108.0" fill="currentColor"/>
<text x="10" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抢到 SET lock:key NX PX 3000 的回源并回填</text>
<text x="10" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">其余的休眠片刻，再重读缓存</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">逻辑过期：不设 TTL，value 里存过期时间戳，</text>
<text x="10" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读到过期值先返回旧值，抢到锁的线程后台重建</text>
</svg>
第一排是没保护的情形：十万个请求都撞上过期的 key，一起打数据库；第二排是互斥重建，只放一个请求回源。
**容易错。**
- **锁没有 TTL：** 持有者崩溃后锁永不释放，所有人都卡住。
- **抢到锁不再查缓存：** 别人刚重建完，你又回源一次。
- **等待者无限重试：** 把数据库的压力转成了 Redis 的请求。
- **重建耗时超过锁 TTL：** 锁被别人抢走；所以释放时要比对 value，确认是自己的锁再删。
- **只用 singleflight：** singleflight（Go）或 Caffeine 的 `computeIfAbsent` 只合并单进程内同一 key 的并发加载，N 个实例仍有 N 次回源，要和 Redis 互斥锁一起用。

**业务场景。** 秒杀商品详情缓存在零点过期，十万请求同时回源；只让一个请求重建，其余等待或返回旧值。
