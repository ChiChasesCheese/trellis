---
id: bagu-redlock-2-algorithm
node: a.distributed.redlock
type: qa
step: 2
---
## Q
**RedLock 加锁流程 · 有效时间怎么算**｜必会

面试官：「RedLock 的加锁流程是什么？拿到锁之后，锁的有效时间怎么算？」

## A
**基本回答。** 用 N=5 个互相独立的 Redis 主节点，不做主从。流程：记下开始时间 T1；对 5 个节点用同一个 key 和随机值执行 `SET NX PX`，每个请求的超时远小于 TTL；至少 3 个成功，且有效时间 = TTL − 加锁耗时（T2−T1）− 时钟漂移补偿 > 0，才算拿到锁。失败就向所有节点发释放，包括以为没锁成功的。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对 5 个互相独立的主节点依次 SET NX PX</text>
<rect x="6" y="24" width="62" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 1</text>
<text x="37" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OK ✓</text>
<rect x="70" y="24" width="62" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="101" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 2</text>
<text x="101" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OK ✓</text>
<rect x="134" y="24" width="62" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="165" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 3</text>
<text x="165" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OK ✓</text>
<rect x="198" y="24" width="62" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="229" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 4</text>
<text x="229" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超时 ✗</text>
<rect x="262" y="24" width="62" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="293" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 5</text>
<text x="293" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OK ✓</text>
<text x="8" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4 个成功 ≥ 多数派 3</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TTL = 10 秒；T1 开始，T2 加锁完成</text>
<rect x="6" y="122" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">耗时</text>
<rect x="46" y="122" width="254" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="173" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有效时间</text>
<rect x="300" y="122" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="317" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">漂移</text>
<text x="6" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T1</text>
<text x="46" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T2</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">有效时间 = TTL − (T2−T1) − 时钟漂移补偿 > 0</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">失败：向所有节点发释放，包括以为没成功的</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">随机延迟后再重试，避免同步冲突</text>
</svg>
上半是客户端对 5 个独立节点逐个加锁，4 个成功，超过 3 个的多数派。下半是时间条：从总的 TTL 里扣掉加锁耗时和时钟漂移补偿，剩下才是真正能用的有效时间。
**容易错。**
- **以为 RedLock 是 5 个主从：** 它用的是 5 个互相独立的主节点，不做主从。
- **有效时间直接用 TTL：** 要扣掉加锁耗时和时钟漂移补偿，因为第一个节点的 key 最早设置也最早过期；业务必须在有效时间内做完。
- **单个请求的超时和 TTL 一样长：** 会被宕机的节点拖住，TTL 为 10 秒时取 5 到 50 毫秒；失败后随机延迟再重试，免得多个客户端同步重试都拿不到多数。
- **失败后只释放成功的那几个：** 要向所有节点发释放，包括以为没成功的。

**业务场景。** 座位锁 TTL 为 10 秒，向 5 个节点加锁共耗时 30 毫秒，3 个以上成功，有效时间约 9.97 秒再扣一点时钟补偿；如果耗时已接近 TTL，则视为失败并立即释放。
