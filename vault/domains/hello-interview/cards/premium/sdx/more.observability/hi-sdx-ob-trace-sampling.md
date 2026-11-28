---
id: hi-sdx-ob-trace-sampling
node: more.observability
type: qa
step: 3
---
## Q
**追踪采样：头部还是尾部**｜补充 · 可观测性 · 追问

面试官：「追踪数据太多，只能采样。头部采样和尾部采样分别在什么时候决定？事故期间哪一种更能留下你要的那条追踪？」

## A
**结论。** 头部采样在第一跳就决定（比如留 1%），随追踪上下文传到所有跨度，便宜简单，但出错和很慢的请求本来就稀少，很容易被丢掉。尾部采样等整条追踪结束再决定：所有错误和慢请求全留，普通请求抽样，事故时更有用，代价是需要缓冲层。

**要点。**
- **头部采样：** 在入口随机决定，决定写进追踪上下文，所有服务保持一致，整条追踪完整保留或整条丢弃。
- **头部的弱点：** 万分之一的出错追踪大概率被丢弃。
- **尾部采样：** 收集器缓冲整条追踪的所有跨度，结束后按规则决定：错误、超过阈值的慢请求全留，其余抽样。
- **尾部的代价：** 需要缓冲层，并且同一条追踪的所有跨度必须到达同一个收集器，需要按追踪 ID 做路由。
- **常见做法：** 头部先做粗抽样控制量，再在尾部保留有价值的追踪。

**为什么。** 有价值的追踪恰恰是少数，随机抽样天然会丢掉它们。尾部采样用缓冲换来了「看过全貌再决定」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">头部采样</text>
<text x="180" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">尾部采样</text>
<rect x="8" y="28" width="152" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">入口随机留 1%</text>
<polyline points="84,68 84,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="84,96 81.0,89.7 87.0,89.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="96" width="152" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">决定写进上下文</text>
<polyline points="84,136 84,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="84,164 81.0,157.7 87.0,157.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="164" width="152" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">出错追踪多半丢</text>
<rect x="180" y="28" width="152" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="256" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上报全部跨度</text>
<polyline points="256,68 256,96" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="256,96 253.0,89.7 259.0,89.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="96" width="152" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按追踪 ID 缓冲</text>
<polyline points="256,136 256,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="256,164 253.0,157.7 259.0,157.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="164" width="152" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结束后再决定</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">错误和慢请求全留，其余抽样</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：需要缓冲层</text>
</svg>

**面试里这样说。** 「我会用尾部采样：收集器按追踪 ID 聚合，追踪结束后保留所有出错和 p99 以上的，其余按 1% 抽样。头部采样便宜，但事故里最想要的那条追踪多半已经被丢了。」

**易错。**
- **只做头部采样：** 出错追踪大量丢失。
- **跨度分散到不同收集器：** 尾部决策时看不到完整追踪。
- **缓冲不设上限：** 流量高峰把收集器撑爆。
