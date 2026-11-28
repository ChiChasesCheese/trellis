---
id: bagu-spike-10x-5-postmortem
node: a.protect.spike-10x
type: qa
step: 5
---
## Q
**QPS 突增十倍 · 事后怎么复盘和预防**｜追问

面试官：「这次扛过去了。你怎么保证下次十倍流量来时不用再靠人肉救火？」

## A
**基本回答。** 只修这次的直接原因没用，下次突增形状不同，要知道系统自己的极限。三件事：找拐点，全链路压测逐步加压到延迟开始陡增的 QPS，生产容量取其约 70%，容量规划再留 2 到 3 倍峰值余量；压测用影子库、测试标记隔离流量，否则污染线上数据；做预案，已知活动提前扩容预热缓存，把「撑不住时拒绝哪些请求」写成预案（先拒次要接口保核心），降级和限流开关要定期演练，否则用时发现配置过期；建监控，盯 QPS、错误率、饱和度（CPU、连接池、队列长度），告警设在容量 70% 而不是 100%，留出反应时间。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<line x1="36" y1="20" x2="36" y2="160" stroke-width="1.2" stroke="currentColor"/>
<line x1="36" y1="160" x2="326" y2="160" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟</text>
<text x="326" y="180" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">QPS</text>
<polyline points="36,148 110,146 170,142 210,130 240,96 258,52 266,24" fill="none" stroke-width="1.6" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="160" y1="24" x2="160" y2="160" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="240" y1="24" x2="240" y2="160" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="160" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 万</text>
<text x="240" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6 万</text>
<text x="156" y="38" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">限流、告警</text>
<text x="156" y="54" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">设在这里</text>
<text x="236" y="38" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拐点</text>
<text x="236" y="54" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">延迟陡增</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">压测找拐点，生产只用约 70%</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再留 2 到 3 倍峰值余量做容量规划</text>
</svg>
延迟在低负载时几乎平，到拐点突然陡增；限流和告警要设在拐点之前。
**业务场景。** 大促前压测，订单库从 2 万 QPS 加到 7 万，6 万时延迟陡增；限流阈值设在约 4 万（拐点的约 70%），预案写明超过后先关推荐和积分接口保下单支付，大促前把降级开关真的拨一遍，当天按预案操作，没有临时决策。
**容易错。**
- **拿 100% 当容量。**
- **压测打在真实库上。**
- **开关不演练。**
