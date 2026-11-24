---
id: ail-agents-long-horizon-doubling-trend
node: agents.long-horizon
type: qa
step: 2
---
## Q
50% 时间跨度增长得有多快？现在大概到了多少？

## A
**长期趋势是每约 7 个月翻一番；2024 年以来更快，约每 3 个月翻一番。**

METR（研究模型能力的非营利机构）在 2026 年 1 月更新的任务集上给出的数字：

| 统计窗口 | 翻倍时间 |
|---|---|
| 2019 年以来 | 约 196 天（约 6.5 个月） |
| 2023 年以来 | 约 131 天 |
| 2024 年以来 | 约 89 天 |

**几个点（同一任务集上的 50% 跨度）：**
- GPT-4（2023 年初）：约 3.5 分钟。
- GPT-5：约 3.6 小时（214 分钟）。
- Claude Opus 4.5：约 5.3 小时（320 分钟），区间 170 到 729 分钟，也就是 2.8 到 12 小时。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<g font-size="12" font-family="sans-serif" fill="currentColor">
<text x="0" y="12">50% 时间跨度（条长按对数刻度）</text>
<rect x="100" y="24" width="33" height="14" opacity="0.55"/>
<text x="0" y="36">GPT-4</text>
<text x="139" y="36">约 3.5 分钟</text>
<rect x="100" y="54" width="140" height="14" opacity="0.55"/>
<text x="0" y="66">GPT-5</text>
<text x="246" y="66">约 3.6 小时</text>
<rect x="100" y="84" width="150" height="14" opacity="0.55"/>
<text x="0" y="96">Opus 4.5</text>
<text x="256" y="96">约 5.3 小时</text>
<rect x="100" y="114" width="176" height="14" opacity="0.55"/>
<text x="0" y="126">Opus 4.6</text>
<text x="282" y="126">约 14.5 小时</text>
</g>
</svg>

**读数时的三个提醒：**
- 区间很宽：8 小时以上的任务只有 31 个，其中只有 5 个有真人实测的用时。
- 只量了软件、安全、推理类任务，不能直接推到所有职业。
- 翻倍时间随统计窗口和任务集变化，不要把某一个数当定律。

**新进展（2026 年 2 月）。** METR 估计 Claude Opus 4.6 的 50% 跨度约 14.5 小时，区间 6 到 98 小时。他们同时警告：超过 16 小时的测量，用现有任务集已经不可靠。

<details class="pt"><summary>想一想：点估计 14.5 小时，区间却是 6 到 98 小时，为什么这么宽？</summary>模型已经接近任务集的上限，最长的任务很少，且多数没有真人实测用时，几个任务的成败就能让拟合曲线大幅移动，所以估计的不确定性主要出现在高端。</details>
