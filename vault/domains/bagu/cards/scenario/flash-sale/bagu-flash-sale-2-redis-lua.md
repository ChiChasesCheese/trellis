---
id: bagu-flash-sale-2-redis-lua
node: a.scenario.flash-sale
type: qa
step: 2
---
## Q
**Redis + Lua 预扣 · 为什么不直接扣数据库**｜必会

面试官：「为什么要用 Redis 加 Lua 预扣库存，而不是直接扣数据库？」

## A
**基本回答。** 同一商品是数据库同一行，`UPDATE` 要拿行锁，同一行只能串行，吞吐只有几百；几千个请求都在等同一把锁，每个占一个连接，连接池耗尽，商品详情页、下单页等无关功能一起超时，拖垮主站。Redis 命令串行执行、不落盘，单实例十万级 QPS；Lua 脚本执行期间不被其他命令打断，「判断加扣减」天然原子。单条 `DECR` 也原子，但没法同一步里再判断「是否已抢过」，Lua 把多步合成一步。脚本必须短小，因为它执行时阻塞整个 Redis。库存活动前预热进 Redis，配持久化和副本，异常时以数据库为准，它不是唯一数据源。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接扣数据库</text>
<text x="184" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis + Lua 预扣</text>
<rect x="8" y="26" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="60" y1="39" x2="84" y2="64" stroke-width="1.2" stroke="currentColor"/>
<rect x="184" y="26" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="236" y1="39" x2="256" y2="64" stroke-width="1.2" stroke="currentColor"/>
<rect x="8" y="60" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="60" y1="73" x2="77.4" y2="66.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84,64 78.6,69.5 76.3,63.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="184" y="60" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="236" y1="73" x2="249.6" y2="66.9" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,64 250.9,69.8 248.3,64.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="94" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="60" y1="107" x2="84" y2="64" stroke-width="1.2" stroke="currentColor"/>
<rect x="184" y="94" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<line x1="236" y1="107" x2="256" y2="64" stroke-width="1.2" stroke="currentColor"/>
<rect x="84" y="38" width="78" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="123" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一行</text>
<text x="123" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">行锁串行</text>
<rect x="256" y="38" width="76" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="294" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="294" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Lua 一步</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">吞吐只有几百</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">连接池被打满</text>
<text x="184" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">单实例十万级</text>
<text x="184" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">QPS</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">瓶颈是串行点：行锁加磁盘，还是内存</text>
</svg>
左边所有请求挤过同一把行锁，右边所有请求交给 Redis 在内存里一个一个跑完一段 Lua。
**举个例子。** 库存预热为 2，三个请求依次执行脚本：r1 读 2 扣成 1 返回 1；r2 读 1 扣成 0 返回 1；r3 读 0，返回 -1 不扣减。每个请求的「读加扣」是一整段，不会有两个请求都读到 1。
```lua
local stock = tonumber(redis.call("GET", KEYS[1]) or "0")
if stock <= 0 then return -1 end   -- 售罄
redis.call("DECR", KEYS[1])
return 1                           -- 扣减成功
```
**容易错。**
- **先 GET 再 DECR 分成两条命令：** 中间别的请求能插进来，又会超卖。
- **在 Lua 里做耗时操作：** 阻塞整个 Redis，同分片上所有业务都变慢。
- **把 Redis 当库存唯一真相：** 它可能丢数据，要以数据库为准。
