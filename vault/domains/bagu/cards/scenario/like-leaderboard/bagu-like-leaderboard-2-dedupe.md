---
id: bagu-like-leaderboard-2-dedupe
node: a.scenario.like-leaderboard
type: qa
step: 2
---
## Q
**点赞计数 · 怎么防止重复点赞**｜必会

面试官：「点赞计数用什么存？用户连点两次，怎么保证只算一次？」

## A
**基本回答。** 用 Set 存点赞的用户：`SADD liked:{作品} <用户>` 返回 1 表示首次，0 表示已点过；只有返回 1 才 `INCR` 计数。判重和计数合成一个 Lua 脚本，保证原子（见下方代码）。
**一句话记住。** 点赞像电影院的签到本：每人进场先签名，签成功了才在门口计数器上加一；同一个人再签，本子会告诉你「已经有了」，计数器就不动。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<rect x="8" y="24" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">u1 点赞</text>
<line x1="84" y1="44" x2="91.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98,44 91.0,47.2 91.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="24" width="234" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="215" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SADD liked:作品 u1</text>
<text x="215" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">判重和计数在同一个 Lua 里</text>
<line x1="86" y1="64" x2="86.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,90 82.8,83.0 89.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="254" y1="64" x2="254.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254,90 250.8,83.0 257.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="90" width="156" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 1：首次</text>
<text x="86" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR 计数 +1</text>
<rect x="176" y="90" width="156" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 0：已点过</text>
<text x="254" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不计数，返回 -1</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大 V 作品的 Set 可能百万成员</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 大 key：换 Bitmap，或只在数据库判重</text>
</svg>
`SADD` 的返回值就是「这次是不是新增」：1 才计数，0 说明已点过；两步放在同一个脚本里，不会被别的请求打断。
**讲明白。**
- **用什么存：** 点赞关系放一个 Set（集合，不含重复元素），每个作品一个 Set，成员是点过赞的用户；点赞数放一个计数器（`INCR`）。
- **`SADD` 的返回值：** 加入集合时如果是新成员返回 1，已经在集合里返回 0。它本身就是「是否新增」，不需要另外先查一遍。
- **为什么要原子：** 判重和计数若分成两步，并发连点会各自通过判重，重复计数。合成一个 Lua 脚本，整段不会被其他命令打断。
- **大 V 作品是大 key：** 点赞 Set 可能有百万成员，一个 key 过大，操作和迁移都会变慢。
- **怎么应对大 key：** 用户 ID 稠密（连续、范围不大）时可以换成 Bitmap（位图，第几位对应哪个用户）；或者只在数据库用 `(用户ID, 作品ID)` 唯一索引判重，Redis 只存计数。
- **取消点赞同理：** `SREM` 返回 1 才 `DECR`，返回 0 说明本来就没点过，不能减。
**举个例子。** 作品 W，点赞数从 0 开始：
1. **u1 点赞：** `SADD` 返回 1，计数 `INCR` 变 1。
2. **u1 又点一次：** `SADD` 返回 0，脚本返回 -1，计数仍是 1。
3. **u2 点赞：** `SADD` 返回 1，计数变 2。
4. **最终：** u1 点了两次、u2 点了一次，计数是 2。
5. **如果没有判重：** 用户快速双击点赞，客户端因重试发出 3 个请求，计数会加 3；有原子判重只加 1。
**代码。** 判重和计数合成一个脚本：
```lua
-- KEYS[1]=点赞用户集合, KEYS[2]=计数; ARGV[1]=用户 ID
if redis.call("SADD", KEYS[1], ARGV[1]) == 1 then   -- 首次点赞才计数
  return redis.call("INCR", KEYS[2])
end
return -1                                            -- 重复点赞
```
**容易错。**
- **先 `INCR` 再 `SADD`：** 重复点赞已经加了计数，再也没法纠正。
- **判重和计数分两个请求：** 并发连点会各自通过判重，重复计数。
- **取消点赞直接 `DECR`：** 没点过赞的人取消也会把数减掉，要 `SREM` 返回 1 才减。
- **Set 当成永远放得下：** 大 V 的点赞 Set 是大 key，要换结构或把关系放数据库。
- **只靠 Redis 判重：** 数据库的 `(用户ID, 作品ID)` 唯一索引是最终防线。
**业务场景。** 用户在视频上快速双击点赞，客户端因重试发出 3 个请求。没有判重时计数加了 3；有原子判重后只加 1。
**系统设计。** [[links.food-item-reviews|带打赏的菜品评价系统（点评 + 投票 + 达标付款）]]：被问「同一用户给同一道菜只能投一票」，答 Set 判重加原子计数，数据库唯一索引作为最终防线。
**相关题。** LC 217 存在重复元素
**可能问法。**
- 点赞怎么防重复？ → 用 Set 存点赞用户：SADD 返回 1 表示首次，0 表示已点过；只有返回 1 才 INCR 计数。判重和计数合成一个 Lua 脚本保证原子，否则并发连点会各自通过判重而重复计数。数据库的 (用户ID, 作品ID) 唯一索引作最终防线。
- 点赞数和点赞关系分别怎么存？ → 计数存 Redis 的计数器，关系存 Set 判重；大 V 作品的 Set 可能有百万成员，是大 key，用户 ID 稠密时换 Bitmap，或只在数据库存关系、Redis 只存计数。取消点赞同理：SREM 返回 1 才 DECR。
