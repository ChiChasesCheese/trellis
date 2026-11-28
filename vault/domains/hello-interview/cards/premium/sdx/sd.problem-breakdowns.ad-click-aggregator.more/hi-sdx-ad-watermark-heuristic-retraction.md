---
id: hi-sdx-ad-watermark-heuristic-retraction
node: sd.problem-breakdowns.ad-click-aggregator.more
type: qa
step: 2
---
## Q
**水位线只是估计，重触发要撤回**｜补充 · 广告点击聚合 · 加分

面试官：「水位线能保证某个事件时间之前的数据都已经到齐吗？窗口输出之后又来了迟到数据，重新触发时旧结果怎么处理？」

## A
**结论。** 不能保证。水位线是对「事件时间大概推进到哪」的启发式估计，不是数据已到齐的证明，所以窗口输出之后仍可能因迟到数据重新触发。如果下游还有第二层聚合，只用新值覆盖旧值会让下游把新旧两个值都加进去；正确做法是「累加并撤回」：先发一条撤回旧值的记录，再发新值。

**要点。**
- **水位线是估计：** 它按「目前见到的最大事件时间减去允许的乱序」推进，没有数学保证。
- **重触发：** 在允许迟到期内，迟到事件让窗口再次输出结果。
- **只写 OLAP 时：** 终点是按确定性键的覆盖写，覆盖本身就是更正，不需要撤回。
- **下游还有二次聚合时：** 比如先按（广告, 分钟）聚合，再按（广告主, 小时）聚合。旧值不撤回，下游会把同一个窗口算两次；撤回让下游先减旧值，再加新值。
- **流的结果永远不是最终账单：** 调水位线和宽限期都无法证明完整，最终账单以每日批对账为准：重算前一天，逐（ad_id, 天）比对，完全一致才标记已对账。

**为什么。** 完整性在流里是概率问题，不是确定性问题。所以要么靠撤回保证每次更新语义正确，要么靠批对账兜底。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<rect x="30" y="8" width="100" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">窗口算子</text>
<rect x="200" y="8" width="100" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="250" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游二次聚合</text>
<text x="84" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">窗口结果 100</text>
<polyline points="80,84 250,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="250,84 243.0,87.2 243.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8.2" y="98" width="143.6" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">迟到事件，窗口重触发</text>
<text x="84" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">撤回 100</text>
<polyline points="80,146 250,146" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,146 243.0,149.2 243.0,142.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="84" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">更正后 105</text>
<polyline points="80,180 250,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,180 243.0,183.2 243.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下游：−100 + 105，净增 5</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只覆盖不撤回：100 + 105 = 205</text>
<line x1="80" y1="48" x2="80" y2="96" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="80" y1="120" x2="80" y2="195" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="80" y1="210" x2="80" y2="215" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="80" y1="230" x2="80" y2="234" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="250" y1="48" x2="250" y2="234" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

**面试里这样说。** 「水位线只是启发式估计，窗口输出后可能重触发。只写 OLAP、键确定的话，覆盖就是更正；下游还有二次聚合，就要用累加并撤回，先撤旧值再发新值。流的结果不是最终账单，最后以夜间批对账为准。」

**易错。**
- **把水位线当成保证：** 窗口一关就认为数据到齐，迟到数据被悄悄丢弃。
- **下游有二次聚合还只覆盖：** 新旧值同时被计入，下游偏大。
