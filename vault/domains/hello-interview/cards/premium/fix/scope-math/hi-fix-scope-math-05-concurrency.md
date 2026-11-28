---
id: hi-fix-scope-math-05-concurrency
node: fix.scope-math
type: qa
step: 5
---
## Q
**限时捐款 · 并发等于速率乘时延**｜补强

面试官：「你说支付服务商（Payment Service Provider，PSP）的调用大约 0.5 秒，那同一时刻有多少个请求在等它？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **公式：** 「同时在飞的数量 = 每秒进来多少 × 每个请求停留多少秒。」
- **PSP 调用：** 「2,000 笔/秒 × 0.5 秒 = 1,000 个同时在等 PSP。」
- **它推出什么：** 「这个数是我的并发上限，也是我要和 PSP 提前谈的额度；超出的排队，不直接失败。」
- **页面读：** 「峰值 15,000 次/秒，缓存命中约 0.02 秒：15,000 × 0.02 = 300 个在飞，几台应用服务器就够，不是瓶颈。」
- **直播连接：** 「每秒进来 1,000 人，平均停留 600 秒：1,000 × 600 = 60 万个连接；每台撑 5 万，60 万 ÷ 5 万 = 12 台。」
- **别混单位：** 「速率是次每秒，并发是个。」说错单位，数就没有意义。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 275">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同时在飞的数量 = 每秒进来 × 每个停留多久</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">PSP 调用</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2,000 笔/秒 × 0.5 秒 = 1,000 个</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">给 PSP 调用设并发上限，谈额度</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">页面读（缓存命中）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">15,000 次/秒 × 0.02 秒 = 300 个</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">几台应用服务器就够，不是瓶颈</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">直播连接</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1,000 人/秒 × 600 秒 = 60 万个连接</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每台 5 万 → 60 万 ÷ 5 万 = 12 台</text>
<text x="8" y="237" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">速率的单位是「次/秒」，并发的单位是「个」</text>
<text x="8" y="255" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个不要混着说</text>
</svg>
白板上：三行算式，每行的单位都能对上；第一行直接变成设计里的一个并发闸。
**为什么这样说。** （约 1 分钟。）面试官看你能不能把速率变成资源数：线程、连接、对外调用的额度。强的回答用「速率 × 时延」一步算出并发，并说它决定了什么。弱的回答是只说「要高并发」，没有数字。
**面试官可能接着问。**
- 时延变成 5 秒呢？ → 2,000 × 5 = 10,000 个在飞。这是 PSP 变慢时最先出问题的数，所以要有超时和熔断，不让在飞的数无限涨。
- 并发上限设成 1,000，超出的请求呢？ → 排队，队列有长度和等待上限；再超就返回「稍后重试」，不是悄悄丢掉。
- 这个公式叫什么？ → 排队论里的利特尔法则（Little's Law）：平均在系统里的数量等于到达率乘平均停留时间。面试里只要会算。
**常见失分。**
- **只说「高并发」：** 没有数，面试官无法判断你要的是什么系统。
- **把速率当并发：** 2,000 笔/秒不是 2,000 个同时在飞。
- **算了不用：** 1,000 个在飞推不出一个闸，估算就成了表演。
