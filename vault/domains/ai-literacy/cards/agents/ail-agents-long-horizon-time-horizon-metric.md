---
id: ail-agents-long-horizon-time-horizon-metric
node: agents.long-horizon
type: qa
step: 1
---
## Q
"智能体能独立工作多久"这个指标是怎么量出来的？"50% 时间跨度"（time horizon）是什么意思？

## A
**拿一批任务，按"人类专家做完要多久"分档，测模型在每档的成功率；成功率掉到 50% 的那一档的人类用时，就是它的 50% 时间跨度。**

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="50" y1="20" x2="50" y2="150"/>
<line x1="50" y1="150" x2="320" y2="150"/>
<path d="M50 32 C120 32 150 62 190 85 S 260 138 315 146" stroke-width="2"/>
</g>
<g fill="none" stroke="currentColor" stroke-dasharray="4 3" opacity="0.7">
<line x1="50" y1="85" x2="190" y2="85"/>
<line x1="190" y1="85" x2="190" y2="150"/>
</g>
<g fill="currentColor">
<text x="26" y="36">100%</text>
<text x="26" y="89">50%</text>
<text x="190" y="168">跨度 H</text>
<text x="185" y="190">任务的人类用时（分钟到小时）</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="268" y="70">成功率 vs 难度</text>
</g>
</g>
</svg>

**怎么得到这条曲线：** 任务集里每个任务都标了人类专家的完成用时（几分钟到十几小时）。让模型做，统计每档的成功率，拟合一条随用时变长而下降的曲线，读出 50% 处的横坐标。

**怎么读：**
- 跨度 2 小时，意思是"人类要做 2 小时的这类任务，它大约一半能做成"；更短的多数能成，更长的多数失败。
- **单位是人类用时，不是模型运行时间。** 模型可能 10 分钟就干完一个人类要 2 小时的任务。
- 还可以量 80% 成功率的跨度，它比 50% 的更短，更接近"可以放心交出去"。

**为什么有意义：** 之前的基准只说"答对 X% 的题"，这个指标说的是"能接多长的活"，单位直观，又能画出随时间变化的趋势。
