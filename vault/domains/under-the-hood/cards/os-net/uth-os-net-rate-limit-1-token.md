---
id: uth-os-net-rate-limit-1-token
node: os-net.rate-limit
type: qa
step: 1
---
## Q
**令牌桶：不用定时器补令牌**｜Guava · RateLimiter · 33.7

Guava 的 `RateLimiter` 没有后台线程往桶里加令牌，它怎么知道桶里还剩多少？

## A
**背景。** 限流就是控制“每秒最多放行多少请求”。令牌桶的说法：桶里最多放 B 个令牌，每秒补 R 个；请求拿走一个令牌，拿不到就等或被拒；桶满时多余的令牌作废，所以允许至多 B 个的突发。照字面实现，需要一个定时器不停补令牌。

**结构。** 令牌数其实是时间的函数：只要记住“上次是什么时候”，来请求时按流逝的时间一次算出该补多少（惰性补充）。`SmoothBursty` 只存两个值：`storedPermits`（桶里的令牌）和 `nextFreeTicketMicros`（下一张票最早能发放的时间）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="40" y1="20" x2="40" y2="156" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="156" x2="322" y2="156" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">令牌数</text>
<text x="322" y="176" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">时间</text>
<line x1="40" y1="44" x2="300" y2="44" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="46" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">maxPermits</text>
<polyline points="40,130 120,44 180,44" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="180" y1="44" x2="180" y2="110" fill="none" stroke="currentColor" stroke-width="1.2"/>
<polyline points="180,110 240,44 290,44" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="180" cy="44" r="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<circle cx="180" cy="110" r="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="174" y="84" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">请求扣 5 个</text>
<text x="150" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">没有定时器 用到时才按时间补</text>
<text x="100" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">按速率回升</text>
</svg>
```

**细节。**

- 每次请求先 `resync`：若现在晚于 `nextFreeTicketMicros`，按空闲了多久一次算出新令牌，上限 `maxPermits`，默认是 1 秒的量
- 令牌够就直接扣；不够的部分，按 `1/速率` 把 `nextFreeTicketMicros` 往后推
- 先放行后付账：大请求立刻通过，是下一个请求为它等待

**为什么。** 令牌数用到时再算，不需要定时器，状态只有两个数字。

**对应 LeetCode：** 无直接对应的题
