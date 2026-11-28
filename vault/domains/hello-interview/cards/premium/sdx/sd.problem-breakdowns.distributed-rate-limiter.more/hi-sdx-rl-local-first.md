---
id: hi-sdx-rl-local-first
node: sd.problem-breakdowns.distributed-rate-limiter.more
type: qa
step: 5
---
## Q
**本地优先的限流：份额随用量重分**｜补充 · 分布式限流器 · 加分

面试官：「20 台网关，某个 key 的全局限额是 1000 次/秒。最简单的做法是每台分 50 次/秒，各自本地判断、互不通信。这样为什么会误拒？有没有既不每次访问中心、又更准的做法？」

## A
**结论。** 静态均分在流量不均时会误拒；改成各节点定期上报实际用量，由中心按占比重算每台的份额，平时全在本地判断，接近份额时才同步问中心。

**要点。**
- **误拒场景：** 客户端连接粘性使这个 key 只落在 4 台网关上，每台上限 50，合计最多 200 次/秒，远低于全局 1000，却已经在拒绝。
- **上报：** 每个节点每约 100 ms 异步上报本周期的用量，多个 key 可合并成一条消息。
- **重新分配：** 中心按用量占比重算份额，如 4 台各约 250 次/秒。份额之和始终不超过全局限额，所以不会超发。
- **平时本地：** 每次检查只读本地计数器，没有网络调用。中心的负载是「节点数 × 每秒上报次数」，不再随请求数增长。
- **接近份额再同步：** 用掉约八成时同步向中心借额度。中心不可用就沿用上一轮份额。
- **代价：** 一个周期内的突发可能小幅超过份额。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">这个 key 的流量只落在 4 台网关上</text>
<rect x="10" y="22" width="74" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="47.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 1</text>
<text x="47.0" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 250/s</text>
<polyline points="47,62 47,98" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="47.0,98.0 50.2,91.0 43.8,91.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="92" y="22" width="74" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="129.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 2</text>
<text x="129.0" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 250/s</text>
<polyline points="129,62 129,98" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="129.0,98.0 132.2,91.0 125.8,91.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="174" y="22" width="74" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="211.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 3</text>
<text x="211.0" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 250/s</text>
<polyline points="211,62 211,98" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="211.0,98.0 214.2,91.0 207.8,91.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="256" y="22" width="74" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="293.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 4</text>
<text x="293.0" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 250/s</text>
<polyline points="293,62 293,98" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="293.0,98.0 296.2,91.0 289.8,91.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="98" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中心存储</text>
<text x="170.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每 100 ms 收用量，按占比重算各台份额</text>
<text x="10" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">静态均分：每台 50/s，4 台最多 200/s</text>
<text x="10" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全局 1000/s 远没用完，却已在拒绝</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">本地优先：份额随用量重分，平时只查本地</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用到份额的八成左右，再同步问中心</text>
</svg>

**面试里这样说。** 「我不做静态 limit/20，那样流量集中在几台时会误拒。每台本地判断，每 100 ms 把用量报给中心，中心按占比重新分配份额，总和不超过全局限额；接近份额时才同步核对，中心挂了就沿用上一轮份额。」

**易错。**
- **把静态均分当成精确限流：** 只有流量完全均匀时才成立。
- **份额之和超过全局限额：** 会放过多于限额的流量，失去了限流的意义。
