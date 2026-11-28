---
id: bagu-retry-3-why-not-unlimited
node: a.protect.retry
type: qa
step: 3
---
## Q
**重试 · 为什么不能无限重试**｜必会

面试官：「下游挂了，你的代码一直重试直到成功，有什么问题？」

## A
**基本回答。** 下游过载时每个失败请求再重试，下游收到的流量变成原来的 2 到 4 倍（各层各自重试还会相乘），更过载，是失败导致重试、重试导致更过载的正反馈循环（重试风暴 retry storm），只有外力（限流、熔断、停止重试）能打断；重试期间线程、连接一直被占，上游也被拖垮，用户永远等不到结果，快速失败更友好。要有限次数、退避、预算，超限就快速失败或降级，失败率超阈值直接熔断。消息消费失败：有限次数加退避，超限转死信队列（DLQ），别让毒消息卡住后面所有消息，死信保留现场、修复后再重投。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重试风暴（retry storm）</text>
<rect x="8" y="28" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游已过载</text>
<line x1="148" y1="45" x2="185" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="192.0,45.0 185.0,48.2 185.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="192" y="28" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求失败</text>
<line x1="262" y1="62" x2="262" y2="109" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,116.0 258.8,109.0 265.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="192" y="116" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端重试</text>
<line x1="192" y1="133" x2="155" y2="133" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,133.0 155.0,129.8 155.0,136.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="116" width="140" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流量变 2~4 倍</text>
<line x1="78" y1="116" x2="78" y2="69" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,62.0 81.2,69.0 74.8,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">正反馈</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只有外力能打断：限流、熔断、停止重试</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快速失败比无限等待更友好</text>
</svg>
闭环：下游过载导致失败，失败的客户端重试，流量变 2~4 倍，下游更过载；圈里没有东西能自己停下来。
**业务场景。** 下游本能处理 1000/秒，抖动后只能处理 600：第一轮 400 个失败；无限重试时下一秒收到 1000 + 400 = 1400，失败涨到 800，再下一秒 1800……一次小抖动变成持续宕机。每个请求最多重试 3 次并退避，再配熔断，下游几秒内恢复。
**容易错。**
- **以为多重试一次总有好处。**
- **毒消息不转死信。**
- **没有熔断配合。**
