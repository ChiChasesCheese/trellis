---
id: bagu-flash-sale-3-one-per-user
node: a.scenario.flash-sale
type: qa
step: 3
---
## Q
**一人一单 · Lua 里怎么写**｜必会

面试官：「怎么保证一个用户只能抢到一件？这个判断放在哪里？」

## A
**基本回答。** 把「是否抢过」和「扣库存」放进同一个 Lua 脚本：用 Set 记已抢用户，先 `SISMEMBER` 判重，再判库存，够就 `DECR` 并 `SADD`；分成两步时同一用户的并发请求会一起通过判重、各扣一次。返回值 1 抢到、-1 售罄、-2 已抢过。售罄时直接返回、不 `SADD`，没抢到的人以后仍可重试。数据库再建 `(用户ID, 活动ID)` 唯一索引兜底，Redis 判重失效时第二单插入会失败，两层缺一不可。Redis 集群下脚本的多个 key 必须在同一个槽，用哈希标签，如 `{act:1}:stock` 与 `{act:1}:users`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一段 Lua 脚本，一步做完</text>
<rect x="8" y="26" width="196" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 已经抢过？SISMEMBER</text>
<text x="214" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是 → 返回 -2</text>
<line x1="106" y1="58" x2="106.0" y2="67.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="106,74 102.8,67.0 109.2,67.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="74" width="196" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 库存 ≤ 0？</text>
<text x="214" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是 → 返回 -1</text>
<line x1="106" y1="106" x2="106.0" y2="115.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="106,122 102.8,115.0 109.2,115.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="122" width="196" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ DECR 库存 + SADD 记人</text>
<text x="214" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">返回 1 成功</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个 key 必须落在同一个槽</text>
</svg>
脚本按顺序做三件事：先判重，再判库存，最后一起扣库存并记下用户；整段不被别的命令打断。
**举个例子。** 库存 3，请求依次 u1、u2、u1、u3、u4、u5：u1 返回 1（库存 2），u2 返回 1（库存 1），u1 再点返回 -2（库存不动），u3 返回 1（库存 0），u4、u5 返回 -1；最终每人只抢到一件。用户狂点一秒发 5 个请求，只有第一个成功。
```lua
-- KEYS[1]=库存 key, KEYS[2]=已抢用户集合, ARGV[1]=用户 ID
if redis.call("SISMEMBER", KEYS[2], ARGV[1]) == 1 then return -2 end  -- 已抢过
local stock = tonumber(redis.call("GET", KEYS[1]) or "0")
if stock <= 0 then return -1 end                                       -- 售罄
redis.call("DECR", KEYS[1])
redis.call("SADD", KEYS[2], ARGV[1])
return 1
```
**容易错。**
- **没抢到也记人：** 售罄时 `SADD` 会让他以后再也不能试，要在判完库存之后再记人。
