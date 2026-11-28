---
id: bagu-limiter-handwrite-1-sliding-window
node: b.protect.limiter-handwrite
type: qa
step: 1
---
## Q
**手写限流器 · 滑动窗口怎么写、并发和内存怎么处理**｜必会

面试官：「现场写一个『10 秒内最多 3 次』的限流器，要线程安全。再说说它和令牌桶怎么选？」

## A
**基本回答。** 滑动窗口日志：队列存窗口内每次放行的时间戳；请求来时先从队头淘汰过期的，再看长度是否小于上限，小于就放行并记录。淘汰、判断、记录必须在一把锁里：否则两个线程都看到长度 2，同时放行，实际放进 4 个。它总是统计「现在往前一个窗口」，不像固定窗口在边界两侧各满额、2 秒内放近两倍。日志版内存 O(limit) × key 数，空闲 key 要淘汰；省内存用滑动窗口计数器，相邻两窗口加权：当前计数 + 上窗口计数 × (1 − 当前窗口已过比例)，是近似值。令牌桶只存令牌数和上次补充时间，请求来时惰性补：`tokens = min(容量, tokens + 经过时间 × 速率)`，不用为每个 key 起定时线程，百万 key 也省内存；它允许突发（桶容量），滑动窗口严格平滑。时间用单调时钟并可注入，单测用假时钟验证边界。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="6" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">滑动窗口日志：限额 3、窗口 10 秒，队列里存放行时刻</text>
<text x="6" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t=8 来</text>
<rect x="70" y="26" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="26" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="158" y="26" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="178" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="206" y="44" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已满 3 个 → 拒绝</text>
<text x="6" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t=11 来</text>
<rect x="70" y="70" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="90" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="114" y="70" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="158" y="70" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="178" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="202" y="70" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<text x="250" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">淘汰 1 → 放行</text>
<text x="70" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队头过期（1 ≤ 11−10）被淘汰</text>
<text x="6" y="146" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">固定窗口的边界突刺：0–10 秒、10–20 秒各限 3 次</text>
<line x1="10" y1="180" x2="330" y2="180" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="160" x2="170" y2="190" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="140" y1="166" x2="140" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="150" y1="166" x2="150" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="160" y1="166" x2="160" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="180" y1="166" x2="180" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="190" y1="166" x2="190" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="166" x2="200" y2="180" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="120" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 秒内放行 6 次</text>
<text x="10" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t=0</text>
<text x="172" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t=10</text>
</svg>
t=8 队列已有 3 个，拒绝；t=11 淘汰队头的 1（1 ≤ 11−10）再放行。下半是固定窗口的边界突刺。
**代码。**
```python
import threading, time
from collections import deque

class SlidingWindowLog:
    def __init__(self, limit, window, now=time.monotonic):
        self.limit, self.window, self.now = limit, window, now
        self.ts, self.lock = deque(), threading.Lock()   # ts 最多 limit 个

    def allow(self):
        with self.lock:                      # 淘汰 + 判断 + 记录是一步
            t = self.now()
            while self.ts and self.ts[0] <= t - self.window:
                self.ts.popleft()            # 只从队头淘汰
            if len(self.ts) < self.limit:
                self.ts.append(t)
                return True
            return False
```
**业务场景。** 「10 秒最多 3 次」：t=1、2、5 放行，t=8 拒绝，t=11 淘汰 1 后放行。令牌桶（容量 3、速率 0.3/秒、初始满）下 t=8 桶里约 2.1 个，第 4 次也放行；这就是突发，滑动窗口会拒绝。
**容易错。**
- **用墙上时钟：** 系统改时间会让窗口错乱。
- **不加锁。**
- **令牌桶起定时线程。**
