---
id: hi-sdx-mr-async-rpo
node: more.multi-region
type: qa
step: 1
---
## Q
**异步复制：灾难时丢多少写入**｜补充 · 多区域部署 · 追问

面试官：「主区域异步复制到备用区域。主区域整体宕机，你切到备用区域，会丢多少数据？这个数怎么估、怎么盯？」

## A
**结论。** 实际 RPO 等于灾难那一刻的复制延迟，丢失写入约等于延迟乘以写吞吐：延迟 5 秒、每秒 2000 次写，约丢 1 万次。要把复制延迟当 SLI 监控，超过 RPO 目标就告警。

**要点。**
- **RPO 等于延迟：** 异步时备用区域落后多久，切过去就少多久的数据。
- **算一笔账：** 5 秒×2000 写/秒=10000 次写入；延迟 30 秒就是 6 万次。
- **越忙越落后：** 流量高峰和故障期间，复制通道最容易积压，所以延迟恰好在最需要时最大。
- **监控：** 把复制延迟作为 SLI，超过 RPO 目标即告警，并在切换前显示将丢多少。
- **要 RPO 为零：** 必须同步多数派复制，每次写入多等一次跨区域往返。
- **2026 亮点：** 工作流引擎的容灾也是这笔账：Temporal Cloud 的多区域是异步复制，文档给的是 RPO 不足 1 分钟、RTO 20 分钟（可用性目标 99.99%，单区域 99.9%），切换后最近的事件可能丢失，个别 Activity 可能被重新执行，所以外部调用必须带幂等键；要零丢失只能同步多数派，代价是跨区域写延迟。

**为什么。** RPO 不是一个配置值，是运行时测量值。承诺的 RPO 只有在延迟被持续测量并受控时才可信。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">异步复制的时间线</text>
<line x1="20" y1="80" x2="320" y2="80" stroke-width="1.2" stroke="currentColor"/>
<rect x="140" y="62" width="120" height="36" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="200" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">复制延迟 5 s</text>
<circle cx="140" cy="80" r="3.5" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="260" cy="80" r="3.5" style="fill:var(--accent,#3b6fd4)"/>
<text x="140" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">备用区域已有</text>
<text x="260" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主区域宕机</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">丢失 ≈ 5 s × 2000 写/秒</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 10,000 次写入</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">高峰和故障时延迟更大</text>
</svg>

**面试里这样说。** 「异步复制下我的 RPO 就是灾难时刻的复制延迟：5 秒、每秒 2000 写，约丢 1 万次写。所以我把复制延迟当 SLI，超过目标就告警；业务要零丢失就改成同步多数派，接受跨区域写延迟。」

**易错。**
- **把 RPO 当常数：** 平时延迟 200 毫秒，事故时涨到分钟级，承诺作废。
- **丢失写入没有对账：** 外部副作用（已扣的钱）没有记录，需要用幂等键和对账补齐。
- **只测平均延迟：** 高峰期的尾部延迟才决定灾难时丢多少。
