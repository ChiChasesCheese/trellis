---
id: psy-career-overwork
node: career.work.overwork
type: qa
step: 1
tags: [证据中]
---
## Q
发版前你每周干 70 个小时，觉得这样比 55 小时多出一大截产出。数据里，工时拉长到 70 小时，产出真的随工时涨吗？

## A
**长工时的产出封顶（diminishing returns to hours）：每周工时过了约 49 小时，多干一小时的产出越来越少；70 小时的产出和 56 小时差不多。**

**故事。** 1914 年战争爆发后，英国政府暂停了军工厂的工时规定，「每周工作 70 到 90 小时很常见」。1915 年 9 月政府设立军工工人健康委员会（HMWC），派调查员进厂记录工时和产出。Pencavel 重新分析这些记录，大多是 1916 年的女工，以周为单位：不到 49 小时时，产出与工时成正比；49 小时以上，产出增长越来越慢，在约 63 小时达到最大；70 小时的产出和 56 小时相差很小。

<svg viewBox="0 0 340 210" xmlns="http://www.w3.org/2000/svg" font-size="12" fill="currentColor">
<line x1="40" y1="180" x2="320" y2="180" stroke="currentColor"/>
<line x1="40" y1="180" x2="40" y2="20" stroke="currentColor"/>
<polyline points="40,180 112,108 136,87 168,66 200,55 224,52 248,55 280,66 304,81 320,93" fill="none" stroke="currentColor" stroke-width="2"/>
<line x1="112" y1="108" x2="112" y2="180" stroke="currentColor" stroke-dasharray="3 3"/>
<line x1="224" y1="52" x2="224" y2="180" stroke="currentColor" stroke-dasharray="3 3"/>
<text x="112" y="196" text-anchor="middle">49</text>
<text x="224" y="196" text-anchor="middle">63</text>
<text x="168" y="196" text-anchor="middle">56</text>
<text x="280" y="196" text-anchor="middle">70</text>
<text x="46" y="32">产出</text>
<text x="180" y="40">示意：按论文的 49、63 小时画</text>
<text x="300" y="208" text-anchor="end">每周工时</text>
</svg>

- **证据 · 中：** 产出封顶的结论只来自 122 个周观察值，是 100 多年前的军工厂，计件的体力工作，不能直接套到写代码上。工时越长，医学上的风险也越清楚：2015 年 Kivimäki 等人汇总 25 项研究，每周 55 小时以上对比 35 到 40 小时，中风风险高 33%（RR 1.33），冠心病高 13%。
- **动手：** 下次想靠加班赶进度的时候，先把本周总工时压在 49 小时以内，算一下：超出的每一小时，是否换来了额外的合并代码。连续 2 周超过 55 小时就要砍需求或要人。
