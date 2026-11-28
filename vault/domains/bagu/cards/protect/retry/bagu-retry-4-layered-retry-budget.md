---
id: bagu-retry-4-layered-retry-budget
node: a.protect.retry
type: qa
step: 4
---
## Q
**重试 · 多层调用每层都重试会怎样，重试预算是什么**｜追问

面试官：「调用链是网关到上传服务到转码服务再到存储，每一层都配了重试 3 次。存储抖动一下，会发生什么？」

## A
**基本回答。** 重试逐层相乘。每层最多调用 3 次（原请求加 2 次重试），三层嵌套时存储最坏收到 3×3×3=27 倍的请求。对策：只在最靠近故障的一层重试，上层失败直接返回；再加重试预算（retry budget），重试请求不超过总请求的 10%，超出就只发首次请求。
**一句话记住。** 三级传话：总经理让经理「办不成就再问三次」，经理让主管「办不成就再问三次」，主管让员工「办不成就再问三次」，员工一次失败，最后会被问 27 次。每层的「再试」不是相加，是相乘。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<rect x="8" y="30" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关</text>
<line x1="68" y1="45" x2="89" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="96.0,45.0 89.0,48.2 89.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="82" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×3</text>
<rect x="96" y="30" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上传</text>
<line x1="156" y1="45" x2="177" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="184.0,45.0 177.0,48.2 177.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×3</text>
<rect x="184" y="30" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="214" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">转码</text>
<line x1="244" y1="45" x2="265" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="272.0,45.0 265.0,48.2 265.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="258" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×3</text>
<rect x="272" y="30" width="60" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="302" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存储</text>
<text x="38" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 次</text>
<text x="126" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 次</text>
<text x="214" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9 次</text>
<text x="302" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">27 次</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每层最多调 3 次：存储最坏收到 3×3×3 = 27 倍</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对策一：只在最靠近故障的一层重试</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">对策二：重试预算 ≤ 总请求的 10%</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000 次首次请求，最多再带 100 次重试，约 1.1 倍</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求头带「这是重试」，下游就不再重试</text>
</svg>
网关调用上传 3 次，每次上传又调用转码 3 次，每次转码又调用存储 3 次：到存储这里，最坏是 27 次。
**讲明白。**
- **为什么相乘：** 下层的每次失败都会让上层把整个下层调用重来一遍，所以放大倍数是各层次数的乘积。
- **算一下：** 每层最多调用 3 次（原请求加 2 次重试），三层嵌套时存储最坏收到 3×3×3=27 倍的请求，抖动变成宕机。
- **对策一，只在一层重试：** 只在最靠近故障的一层重试，上层失败直接返回。
- **对策二，重试预算：** 限制重试请求不超过总请求的某个比例，例如 10%，超出就只发首次请求。
- **预算的效果：** 整体故障时的额外负载封顶约 1.1 倍：1000 个首次请求最多再带 100 个重试，而不是几倍。
- **告诉下游「这是重试」：** 请求头里带「这是重试」的标记，下游看到就不再重试。
- **要监控：** 原始请求 QPS、重试 QPS 和重试比例，重试比例突增就是风暴前兆。
**举个例子。** 视频上传链路：网关 → 上传服务 → 转码服务 → 存储，每一层都配了重试 3 次，存储短暂抖动、一直失败：
1. **转码调存储：** 存储失败，转码把存储调 3 次。
2. **上传调转码：** 转码返回失败，上传把转码重新调 3 次，每次转码又调存储 3 次，存储累计 9 次。
3. **网关调上传：** 上传失败，网关重试 3 次，存储累计 27 次。
4. **改进：** 只让上传服务调存储这一层重试，并带预算；其他层失败直接返回。每秒 1000 个首次请求，最多再带 100 个重试，存储收到约 1100 个，几秒内就自行恢复。
**容易错。**
- **以为每层重试都是保险：** 层层叠加会把请求放大到 27 倍。
- **只加预算不去掉多余的重试层：** 能在一层完成的，不要每层都重试。
- **看不到重试流量：** 不单独监控重试 QPS 和比例，风暴到了才发现。
- **以为预算是限制重试次数：** 预算限制的是重试占总请求的比例。
**业务场景。** 视频上传链路中存储短暂抖动，每层都重试，存储收到 27 倍请求，从抖动变成宕机；改成只有上传服务到存储这一层重试并配预算后，同样的抖动几秒内自行恢复。
**系统设计。** [[links.youtube|视频平台（YouTube）]]：上传、转码、存储的多级调用链。面试官追问「存储抖动时怎么避免级联放大」，答：只在最靠近存储的一层重试，配重试预算（重试不超过总请求 10%），请求头标记「这是重试」让下游不再重试。
**可能问法。**
- 多层重试会有什么问题？ → 重试逐层相乘。每层最多调用 3 次（原请求加 2 次重试），三层嵌套时存储最坏收到 3×3×3=27 倍的请求，抖动变成宕机。因为下层的每次失败都会让上层把整个下层调用重来一遍。
- 重试预算是什么？ → 限制重试请求不超过总请求的某个比例，例如 10%，超出就只发首次请求。这样整体故障时的额外负载封顶约 1.1 倍：1000 个首次请求最多再带 100 个重试，而不是几倍。
- 重试应该放在哪一层？ → 只在最靠近故障的一层重试，上层失败直接返回。请求头里带「这是重试」的标记，下游看到就不再重试；监控原始 QPS、重试 QPS 和重试比例，重试比例突增就是风暴前兆。
