---
id: hi-sdx-prox-shard-boundary
node: sd.problem-breakdowns.yelp.more
type: qa
step: 2
---
## Q
**地理分片的边界查询**｜补充 · 商户点评（Yelp） · 追问

面试官：「索引按地理区域分片以后，用户站在两个分片的交界处，附近的店有一部分在另一个分片。怎么保证不漏？为什么用 S2 或 H3 的分层单元做分片键比按国家分更省？」

## A
**结论。** 边界附近的查询要同时问相邻分片再合并，不能只信一个分片的答案。按国家分片时，「相邻」可能是整个邻国的一个大分片，只为捞边境的几家店；用 S2 或 H3 的较粗一级单元做分片键，边界查询只需多问相邻的几个粗单元。

**要点。**
- **只问一个分片会漏：** 单个分片的结果在边缘处不完整，必须广播给相邻分片。
- **行政区分片的代价：** 各分片大小不均，邻居形状不规则，一次边界查询可能打到一个很大的邻片。
- **粗单元做分片键：** 一个单元里的店归同一分片，邻居就是固定的相邻单元（H3 取一圈，S2 取相邻单元），扇出数小而确定。
- **合并：** 各分片返回候选，合并后统一按精确距离排序，按商户 id 去重。
- **另一种做法：** 在边缘把店在两侧都存一份，查询只问一个分片，代价是写放大和去重。

**为什么。** 分层单元让「相邻」变成一个便宜的纯计算：给定一个单元，能直接算出周围的单元 ID，不必依赖行政边界。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片键 = 较粗一级的单元（S2 / H3）</text>
<rect x="50" y="30" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="90" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="130" y="30" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="210" y="30" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="250" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="50" y="76" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="90" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="130" y="76" width="80" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本格</text>
<rect x="210" y="76" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">相邻格</text>
<rect x="50" y="122" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="90" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="130" y="122" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<rect x="210" y="122" width="80" height="46" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="250" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">·</text>
<circle cx="202" cy="99" r="5" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">● 用户在本格右边缘：近处的店可能在右邻格</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只多问相邻的几个粗单元，不用问整个邻国</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各分片返回候选，合并后统一按精确距离排序</text>
</svg>

**面试里这样说。** 「我用 S2 较粗一级的单元做分片键，用户在边缘时，多问相邻的几个单元，再合并结果统一按精确距离排序、按 id 去重。这样比按国家分片扇出小，邻居也是算出来的。」

**易错。**
- **只查本分片：** 边缘处漏掉近在咫尺的店。
- **把分片键取得太细：** 单元越小，边界上要多问的相邻单元越多，合并开销越大。
