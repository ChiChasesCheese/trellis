---
id: hi-sdx-rel-burn-rate
node: more.reliability
type: qa
step: 5
---
## Q
**燃烧率告警：多窗口怎么配**｜补充 · 可靠性 · 追问

面试官：「SLO 99.9%，月度窗口。为什么不直接对错误率设一个固定阈值告警，而用错误预算燃烧率？多窗口怎么配才既不误报又不漏报？」

## A
**结论。** 燃烧率是消耗预算的速度，正常速度为 1。固定阈值要么被毛刺吵醒，要么对慢性泄漏无感。做法是长窗口加短窗口同时超限才告警：1 小时 14.4 倍加 5 分钟，页面告警；3 天 1 倍加 6 小时，只开工单。

**要点。**
- **燃烧率：** 当前错误率除以预算比例（99.9% 时为 0.1%）；等于 1 表示恰好在月底花完。
- **14.4 倍：** 1 小时内消耗约 2% 的月预算（14.4×1/720）；照此速度约 50 小时烧光，立刻呼叫。
- **6 倍：** 6 小时窗口，消耗 5%，也是页面告警。
- **1 倍：** 3 天窗口，消耗 10%，只开工单，不半夜叫人。
- **长加短：** 长窗口保证真有大量预算被花，短窗口（长窗口的约十二分之一）保证问题还在发生，故障修好后告警很快自己熄灭。

**为什么。** 告警的目标是预算花得太快才叫人。把速度换算成「多久烧光」，不同速度就对应不同紧急程度，页面和工单自然分开。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9% SLO，30 天预算</text>
<rect x="8" y="30" width="324" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页面  14.4 倍</text>
<text x="170" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长 1 小时 且 短 5 分钟 · 耗预算 2%</text>
<rect x="8" y="86" width="324" height="48" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页面  6 倍</text>
<text x="170" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长 6 小时 且 短 30 分钟 · 耗预算 5%</text>
<rect x="8" y="142" width="324" height="48" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工单  1 倍</text>
<text x="170" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长 3 天 且 短 6 小时 · 耗预算 10%</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个窗口都超限才告警</text>
</svg>

**面试里这样说。** 「我用多窗口多燃烧率：1 小时超过 14.4 倍并且 5 分钟也超过，立即呼叫；6 小时 6 倍同理；3 天 1 倍只开工单。这样毛刺不会叫醒人，慢性泄漏也不会漏掉。」

**易错。**
- **只设一个窗口：** 短窗口噪声大，长窗口故障修好后还在响。
- **全部都发页面：** 慢速消耗半夜叫人，值班疲劳。
- **按绝对错误数告警：** 流量低谷和高峰的含义完全不同。
