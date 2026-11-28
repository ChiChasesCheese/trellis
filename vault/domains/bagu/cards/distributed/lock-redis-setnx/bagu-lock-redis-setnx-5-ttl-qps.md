---
id: bagu-lock-redis-setnx-5-ttl-qps
node: a.distributed.lock-redis-setnx
type: qa
step: 4
---
## Q
**1 万 QPS 下 · 过期时间设多久、竞争激烈怎么办**｜必会

面试官：「1 万 QPS 的场景，这把锁的过期时间设多久？竞争太激烈怎么办？」

## A
**基本回答。** TTL（过期时间）要略大于业务正常的最长耗时，例如业务 P99（99% 的请求耗时都不超过它）是 50 ms，可设 1 到 3 秒，再靠看门狗或下游条件更新兜底；设太长，持有者崩溃后别人要等很久。竞争激烈时，先缩小锁粒度（按订单、用户，不要全局一把），其次快速失败而不是排队重试。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一把锁 = 排成一队，一次只过一个</text>
<rect x="6" y="24" width="84" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 万请求</text>
<text x="48" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每秒</text>
<line x1="90" y1="46" x2="111" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,46 111,49.2 111,42.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="104" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一把锁</text>
<text x="170" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持锁 10 ms</text>
<line x1="222" y1="46" x2="243" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,46 243,49.2 243,42.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="24" width="84" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 100 个</text>
<text x="292" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每秒通过</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">上限 = 1 ÷ 持锁时间 = 1 ÷ 0.01 秒 = 100 次/秒</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10000 个里只有约 1% 能通过</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拆成 4 段（分桶），4 把锁并行：</text>
<rect x="6" y="150" width="76" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="44" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁 1</text>
<text x="44" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100/s</text>
<rect x="89" y="150" width="76" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁 2</text>
<text x="127" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100/s</text>
<rect x="172" y="150" width="76" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁 3</text>
<text x="210" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100/s</text>
<rect x="255" y="150" width="76" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="293" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁 4</text>
<text x="293" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100/s</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合计约 400 次/秒，段越多吞吐越高</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">能用 Lua 原子扣减的，干脆别用锁</text>
</svg>
上半是一把全局锁的吞吐算式：持锁时间决定上限，1 万 QPS 只有约 1% 通过。下半是拆成 4 段锁，4 个窗口并行，吞吐乘 4。
**代码。** 用 Lua 原子扣库存，不需要锁：
```lua
-- KEYS[1]=库存 key；返回扣完后的库存，-1 表示没货
local n = tonumber(redis.call('get', KEYS[1]))
if n and n > 0 then
  return redis.call('decr', KEYS[1])
end
return -1
```
**容易错。**
- **把 TTL 随便设成 30 秒：** 太长，持有者崩溃后别人要等很久；要结合业务的 P99 来定。
- **全局一把锁扛高并发：** 吞吐上限是 `1 ÷ 持锁时间`，1 万 QPS 打一把锁，绝大多数请求拿不到。
- **竞争激烈就加重试：** 排队重试会让请求堆积，应该快速失败。
- **锁里放一堆不必串行的事：** 持锁越久，吞吐上限越低。
**业务场景。** 零点抢同一张券，1 万 QPS 全打一把全局锁，每秒只放行约 100 个，其余等到超时。改为把库存放进 Redis，用 Lua 原子扣减，不再需要锁。
