---
id: bagu-lock-redis-setnx-1-basic
node: a.distributed.lock-redis-setnx
type: qa
step: 1
---
## Q
**Redis 分布式锁 · 为什么需要、最简实现**｜必会

面试官：「用户连点两次打赏按钮，两个实例同时处理，扣了两次币。为什么本地锁解决不了？怎么用 Redis 做一把最简单的分布式锁？」

## A
**基本回答。** 本地锁（`synchronized`、`ReentrantLock`）只在一个 JVM 内有效，服务多实例部署时各锁各的，挡不住两个实例同时处理。分布式锁把「谁持有」放进大家共享的 Redis：加锁用 `SET lock:order:123 <uuid> NX PX 30000`，成功才执行业务；释放时用 Lua 脚本先比对 value 再删除。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一用户连点两次，请求落在不同实例</text>
<rect x="6" y="28" width="86" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="49" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 A</text>
<text x="49" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 1</text>
<rect x="6" y="112" width="86" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="49" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 B</text>
<text x="49" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求 2</text>
<rect x="200" y="28" width="134" height="122" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="267" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="267" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lock:gift:42</text>
<text x="267" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= uuid-A</text>
<text x="98" y="42" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET NX → OK</text>
<line x1="92" y1="48" x2="193" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="200,48 193,51.2 193,44.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="98" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SET NX → nil</text>
<line x1="92" y1="132" x2="193" y2="132" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200,132 193,135.2 193,128.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 拿不到锁，直接提示「处理中」</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本地锁只在各自的 JVM 里有效，A、B 互相看不见</text>
</svg>
两个请求落在不同实例，各自带着本地锁也互不相识；都去 Redis 抢同一个 key，只有先到的 `SET NX` 成功，后到的拿到 nil，只能放弃。
**容易错。**
- **以为在多实例上加 `synchronized` 就行：** 它只管一个 JVM 之内，两个实例照样同时进入。
- **用一把全局大锁：** 所有请求串行，吞吐被锁死；要按订单、用户拆开。
- **加锁时不带过期时间：** 持有者一崩，锁永远在，其他请求全部卡死。
- **以为拿到锁就绝对安全：** 锁会过期，主从切换也会丢，所以它减少重复，但不是最后一道防线。
- **释放直接 DEL：** 锁可能已过期并被别人拿走，原持有者直接 `DEL` 会删掉新持有者的锁，要用 Lua 先比对 value。`SET ... NX PX` 从 Redis 2.6.12 起取代了老的 `SETNX` 加 `EXPIRE`。
**业务场景。** 打赏扣币接口被连点：两个请求落在不同实例。以 `lock:gift:{用户ID}` 加锁，后到的请求拿不到锁，直接提示「处理中」，同一用户的扣币就变成串行。
