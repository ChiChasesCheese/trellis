---
id: hi-sdx-rel-server-backoff
node: more.reliability
type: qa
step: 7
---
## Q
**每个客户端都退避了，服务还是被打垮**｜补充 · 可靠性 · 追问

面试官：「每个客户端都做了指数退避加抖动，最多重试 3 次。服务仍然被重试压垮。为什么？有哪两个机制可以修？」

## A
**结论。** 客户端的退避只掌握本地信息，看不到另外一万个客户端也在重试，总重试量依然超出服务承受力。修法是服务端驱动退避（Retry-After）和客户端自适应节流。

**要点。**
- **本地信息的局限：** 每个客户端只知道自己失败了，不知道服务整体过载了多久。
- **Retry-After：** 服务返回 429 或 503 并带上等待时间，只有服务知道恢复需要多久，还能给不同客户端不同的随机值把它们分散。
- **拒绝要便宜：** 在入口直接拒绝，不要进到数据库再拒绝，否则拒绝路径本身变成故障。
- **自适应节流：** 客户端统计近两分钟的请求数与被接受数，以概率 max(0,(请求−K×接受)/(请求+1)) 主动丢弃自己的请求，K 取 2。
- **效果：** 服务接受率越低，客户端越自觉限制，总负载收敛到服务能处理的量。

**为什么。** 这两个机制是重试预算（重试不超过请求的 10%）的执行手段；没有它们，预算只是一个没人遵守的愿望。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="10" width="120" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="212" y="10" width="120" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过载的服务</text>
<polyline points="128,24 212,24" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,24 205.7,27.0 205.7,21.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="135" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">请求</text>
<polyline points="212,44 128,44" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,44 134.3,41.0 134.3,47.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="138" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">429</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务端驱动：回 Retry-After</text>
<rect x="8" y="98" width="324" height="70" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端自适应节流（近 2 分钟）</text>
<text x="170" y="144.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">丢弃概率 = max(0,(请求−2×接受)/(请求+1))</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">例：请求 100，接受 20</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(100 − 40) / 101 ≈ 59% 自己先丢掉</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">接受率越低，客户端越自觉收敛。</text>
</svg>

**面试里这样说。** 「光靠客户端退避不够，它看不到全局。我让服务在入口直接回 429 加 Retry-After，值带抖动，同时客户端按近两分钟的接受率自适应丢请求，K 取 2，把重试总量压在服务能承受的范围。」

**易错。**
- **拒绝要查库：** 每个被拒请求仍消耗数据库，拒绝路径变成故障。
- **忽略 Retry-After：** 客户端自己猜间隔，仍然同步重试。
- **每层都重试：** 节流只管一层，多层嵌套照样成倍放大。
