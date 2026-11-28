---
id: hi-sdx-metrics-field-index-pruning
node: sd.problem-breakdowns.metrics-monitoring.more
type: qa
step: 3
---
## Q
**查询扇出：用标签索引剪枝**｜补充 · 指标监控（Datadog） · 加分

面试官：「查询广播给所有存储叶子节点，集群越大越慢。怎么让成本跟着查询的选择性走，而不是跟着集群规模走？剪枝会不会漏掉结果？」

## A
**结论。** 在每个区（zone）和根这两层放一个小的标签索引，记录哪些区、哪些叶子可能含有满足某个标签条件的序列，发查询前先剪枝，只问可能有的。索引可以多放行（误报），但不能漏放行（漏报），因为叶子最后仍做精确匹配，正确性不依赖索引精确，只要它保守。

**要点。**
- **广播的问题：** 查询成本随集群节点总数增长，哪怕只查一个服务的数据，也要问所有叶子。
- **两层索引：** 根层的索引挑区，区层的索引挑叶子。
- **数字：** Google 的 Monarch 报告区级扇出减少约 99.5%，根级约 80%。20 个区 × 每区 500 个叶子 = 10,000 个叶子，根层只留 20 × 0.2 = 4 个区，每区只留 500 × 0.005 = 2.5 个叶子，共约 10 个，减少约 1000 倍。
- **偏保守：** 误报只是多问几个叶子；漏报等于漏数据，不允许。
- **索引要小：** 只存标签值的摘要，放在内存里，保持很小。

**为什么。** 把「这个查询可能落在哪些节点」变成一次廉价的内存查找，成本就取决于数据的分布，而不是节点数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="20" y="10" width="300" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全部叶子 10,000</text>
<text x="170" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">20 区 × 每区 500 个</text>
<rect x="70" y="92" width="200" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 个区</text>
<text x="170" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">根层索引剪掉约 80%</text>
<rect x="110" y="174" width="120" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="190.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 10 个叶子</text>
<text x="170" y="205.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">区层剪掉约 99.5%</text>
<polyline points="170,50 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 166.8,85.0 173.2,85.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="178" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">根层字段索引</text>
<polyline points="170,132 170,174" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,174 166.8,167.0 173.2,167.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="178" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">区层字段索引</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">索引可以多放行，不能漏放行：</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">叶子最后仍做精确匹配</text>
</svg>

**面试里这样说。** 「我在每个区和根放一个标签索引，查询前先剪掉不可能有数据的区和叶子，10,000 个叶子剪到约 10 个。索引只能误报不能漏报，叶子最后还是精确匹配，所以结果始终正确。」

**易错。**
- **索引追求精确：** 精确索引又大又难维护，保守的小索引就够。
- **允许漏报：** 剪枝漏掉含数据的叶子，查询结果静默缺失。
