---
id: bagu-rate-limit-algorithms-6-hand-written-bucket
node: a.protect.rate-limit-algorithms
type: qa
step: 5
---
## Q
**限流实现 · 手写令牌桶：核心状态、惰性补充和线程安全**｜必会

面试官：「现场写一个令牌桶限流器。核心状态是什么？令牌怎么补充？多线程下怎么保证正确？」

## A
**基本回答。** 状态只有两个：tokens 和 last，令牌数是时间的函数，用到才算（惰性补充），不起定时线程，空闲时零开销，也比定时线程更准。每次请求在锁里一步完成：`tokens = min(burst, tokens + (t − last) × rate)`，`last = t`，够扣就扣并放行。封顶很重要：空闲一分钟不能攒出六万个令牌，否则恢复后一次放行巨大突发。要加锁，因为读、算、写不是原子的，两个线程都看到剩 1 个会都放行。计时用单调时钟，冷启动桶是满的。分布式版本把两个状态存 Redis 哈希，用 Lua 一次完成读、算、写，时间在脚本里用 `TIME` 取避免各机时钟不一致（Redis 5.0 起脚本按效果复制，允许先读 `TIME` 再写）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="324" height="200" rx="4" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="14" y="22" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">allow() 持锁：补充 + 扣减是一步</text>
<rect x="20" y="32" width="300" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 读时间 t（单调时钟）</text>
<rect x="20" y="68" width="300" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 补令牌，封顶到容量</text>
<text x="170" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tokens = min(burst, tokens + (t−last)×rate)</text>
<rect x="20" y="116" width="300" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ last = t</text>
<rect x="20" y="152" width="300" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ tokens ≥ n ？</text>
<text x="170" y="185.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">够：tokens −= n，放行　不够：拒绝</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不起定时线程：令牌数是时间的函数，用到才算</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">冷启动桶是满的，空闲再久也不超过 burst</text>
</svg>
`allow()` 里读时间、补令牌、记时间、判断并扣减是一个整体，全在锁里。
**代码。**
```python
import threading, time

class TokenBucket:
    def __init__(self, rate, burst, now=time.monotonic):
        self.rate, self.burst, self.now = rate, burst, now
        self.tokens, self.last = burst, now()   # 冷启动时桶是满的
        self.lock = threading.Lock()

    def allow(self, n=1):
        with self.lock:                          # 补充 + 扣减是一步
            t = self.now()
            self.tokens = min(self.burst, self.tokens + (t - self.last) * self.rate)
            self.last = t
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False
```
**业务场景。** rate = 2/秒、burst = 4：t=0 四次放行（4→0），第 5 次拒绝；t=0.5 补 (0.5−0)×2 = 1 个，放行。空闲到 t=100 理论补 199 个，封顶到 4；没封顶就一次放行 199 个。商户开放接口每商户一个桶（每秒 50、突发 100），某商户重试风暴只取空自己的桶，其他商户不受影响。
**容易错。**
- **起定时线程放令牌。**
- **补充不封顶。**
- **补充和扣减分开加锁，或不加锁。**
- **用系统时钟：** 回拨会算出负间隔。
