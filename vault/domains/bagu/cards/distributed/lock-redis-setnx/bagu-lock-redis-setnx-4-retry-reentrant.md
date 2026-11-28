---
id: bagu-lock-redis-setnx-4-retry-reentrant
node: a.distributed.lock-redis-setnx
type: qa
step: 6
---
## Q
**加锁失败与可重入 · Redisson 怎么做**｜追问

面试官：「加锁失败了怎么办？同一线程持锁时又调用了需要同一把锁的方法，会不会把自己锁死？」

## A
**基本回答。** 加锁失败有三种处理：快速失败，直接返回；带超时的自旋重试，间隔加随机退避；订阅释放通知（Redisson 用 Pub/Sub，即发布订阅）。不要无限忙等。可重入用 Hash：key 是锁名，field 是「客户端 ID:线程 ID」，value 是重入次数；同一线程再加锁，次数加一，释放减一，减到 0 才删 key。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="6" y="8" width="328" height="66" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Hash：key = 锁名</text>
<text x="170" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">field = 客户端 ID:线程 ID</text>
<text x="170" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">value = 重入次数</text>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个线程进进出出，计数这样变：</text>
<rect x="6" y="108" width="76" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">外层加锁</text>
<text x="44" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">count = 1</text>
<line x1="82" y1="129" x2="83" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90,129 83,132.2 83,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="108" width="76" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内层加锁</text>
<text x="128" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">count = 2</text>
<line x1="166" y1="129" x2="167" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174,129 167,132.2 167,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="174" y="108" width="76" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内层释放</text>
<text x="212" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">count = 1</text>
<line x1="250" y1="129" x2="251" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="258,129 251,132.2 251,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="258" y="108" width="76" height="42" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="296" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">外层释放</text>
<text x="296" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 → 删 key</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">别的线程来加锁：拿到剩余 TTL，只能等或放弃</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只在计数减到 0 时才真正放锁</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内层方法返回，不会把外层的锁提前放开</text>
</svg>
同一个线程嵌套加锁时，Hash 里的计数一路加到 2，再一层层减回 0；只有减到 0 才把 key 删掉，别的线程这时才拿得到锁。
**代码。** 按 Redisson 的思路写的加锁脚本：
```lua
-- KEYS[1]=锁名  ARGV[1]=过期毫秒  ARGV[2]=客户端ID:线程ID
if redis.call('exists', KEYS[1]) == 0 or redis.call('hexists', KEYS[1], ARGV[2]) == 1 then
  redis.call('hincrby', KEYS[1], ARGV[2], 1)   -- 次数加一
  redis.call('pexpire', KEYS[1], ARGV[1])      -- 刷新过期时间
  return nil                                   -- 加锁成功
end
return redis.call('pttl', KEYS[1])             -- 别人持有：返回剩余 TTL
```
**容易错。**
- **以为自己会被自己锁死不用管：** 不可重入时，内层方法对同一把锁再加锁，会等外层释放，请求卡到超时。
- **内层释放就删 key：** 要减到 0 才删，否则内层返回时外层的锁被提前放开。
- **自旋不加随机退避：** 大量客户端同时重试，一起冲向 Redis，又一起失败。
- **无限忙等或无超时阻塞：** 要有超时，等不到就放弃。

**业务场景。** 提现主流程对用户加锁后，内部又调用「校验并扣减」方法，该方法同样对同一用户加锁。若不可重入，同一线程等自己释放，请求卡到超时。
