---
id: bagu-timeout-1-layered-deadline
node: b.protect.timeout
type: qa
step: 1
---
## Q
**超时 · 取值、逐层递减与截止时间传递**｜追问

面试官：「调用支付渠道的超时你设多少？三层服务调用，每层超时怎么配？」

## A
**基本回答。** 每次远程调用都必须设超时，不能默认无限等（线程被占光是雪崩起点）；连接超时（通常 1 到 3 秒）和读超时分开设。取值看下游延迟分布 p99 到 p99.9 再加余量（下游 p99 是 200ms 就设 500ms），上线后按监控调；太长占资源，太短误伤并触发重试放大。上游超时必须大于下游超时加重试之和，所以逐层递减：网关 3s > 服务 A 2s > 服务 B 1s > 数据库 500ms，三层都设 3s 则内层超时后外层还在等、下游白做工。更好的做法是传递 deadline（gRPC deadline 或请求头带剩余时间），下游发现剩余时间不够直接放弃。超时不等于没执行，写操作必须幂等；取消信号（Go `context`、gRPC cancel）让下游中止没做完的工作。组合：超时发现故障 → 有限次退避重试 → 熔断 → 限流。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">超时层层递减（条的长度 = 超时时间）</text>
<rect x="8" y="26" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关  3 s</text>
<rect x="8" y="62" width="216" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务 A  2 s</text>
<rect x="8" y="98" width="108" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务 B  1 s</text>
<rect x="8" y="134" width="54" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="35" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="70" y="153" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数据库  500 ms</text>
<text x="8" y="188" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">下游的超时 + 重试之和 < 上游的超时</text>
<text x="8" y="206" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">三层都设 3 s：内层超时后外层还在等</text>
</svg>
条长是超时时间，越往里越短，每层必须比下一层长才装得下它的重试。
**业务场景。** 网关 deadline 3 秒：服务 A 剩 2.9 秒、自己上限 2 秒取 2；服务 B 取 1 秒；数据库超时 500ms，B 在 1 秒内还能重试一次；若 B 收到时只剩 0.05 秒，直接放弃。调支付渠道超时 500ms 但渠道可能已扣款，重试要带同一个幂等键或先查询。
**容易错。**
- **只设一个总超时，或每层设成一样。**
- **上游超时小于下游加重试：** 下游重试全白费。
- **把超时当成没执行。**
