---
id: uth-os-net-rate-limit-2-leaky
node: os-net.rate-limit
type: qa
step: 2
---
## Q
**漏桶只存 excess 一个数**｜Nginx · limit_req · 1.31

配置 `rate=1r/s burst=5`，Nginx 对每个客户端只存什么，就能判断放行、延迟还是拒绝？

## A
**背景。** 令牌桶允许突发；有些场景反而要输出匀速，保护后端。漏桶（leaky bucket）的比喻：请求像水倒进桶，桶底以固定速率漏水；水超过桶口就溢出，也就是拒绝。`rate=1r/s burst=5` 的意思是每秒漏 1 个，最多让 5 个在桶里排队。

**结构。** 每个客户端只存两样：`excess`（桶里的水，单位是千分之一个请求）和上次到达的时间。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="170" y="12" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每个请求 excess +1000</text>
<line x1="140" y1="20" x2="140" y2="49" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M140.0,54.0 L136.7,47.2 L143.3,47.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="170" y1="20" x2="170" y2="49" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,54.0 L166.7,47.2 L173.3,47.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="200" y1="20" x2="200" y2="49" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M200.0,54.0 L196.7,47.2 L203.3,47.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="121" y="98" width="98" height="42" rx="0" stroke="none" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<polyline points="120,50 120,140 220,140 220,50" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="114" y1="66" x2="222" y2="66" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="230" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">burst x 1000</text>
<text x="230" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">超过就拒绝</text>
<text x="114" y="112" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">excess</text>
<line x1="170" y1="142" x2="170" y2="171" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,176.0 L166.7,169.2 L173.3,169.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">按 rate 漏出</text>
</svg>
```

**细节。**

- 每个请求到达：`excess = excess - rate × 经过毫秒数 / 1000 + 1000`，下限 0，意思是先漏掉一段时间的水，再倒进一个请求
- `excess` 超过 `burst × 1000` 就拒绝
- 没超过就按 `excess` 折算成延迟排队，加 `nodelay` 则立即放行

**为什么。** 输出速率恒定，对后端最平滑；代价是突发被排队，而令牌桶允许突发直通。

**对应 LeetCode：** 无直接对应的题
