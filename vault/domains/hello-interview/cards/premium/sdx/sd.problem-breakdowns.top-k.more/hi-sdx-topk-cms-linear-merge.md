---
id: hi-sdx-topk-cms-linear-merge
node: sd.problem-breakdowns.top-k.more
type: qa
step: 2
---
## Q
**CMS 的线性合并：窗口汇总与树形合并**｜补充 · YouTube 热门 Top K · 追问

面试官：「Top K 要同时提供 1 分钟、1 小时、1 天、全部时间四种窗口。较粗的窗口怎么得到，不用每个都重读原始流？流量涨 10 倍，草图的内存和合并又会怎样？」

## A
**结论。** 只有最细的 1 分钟桶读原始流，较粗的窗口靠汇总：1 小时 = 60 张分钟草图逐格相加，1 天 = 24 张小时草图，全部时间 = 按天累加。这依赖 CMS 的线性：草图相加等价于对合并后的流建草图。流量涨 10 倍，内存只线性增长，真正的瓶颈是合并的扇入，要改成树形合并。

**要点。**
- **窗口汇总：** 分钟 → 小时 → 天 → 全部时间，每层只对草图做逐格加法，不再读事件。
- **Space-Saving 不行：** 较粗窗口的候选集取各细窗口候选集的并集，再用汇总后的 CMS 重新排序。
- **10 倍的内存：** 要把绝对误差 ε × N 保持不变，流量涨 10 倍就要把 ε 缩小 10 倍，宽度 w = e/ε 随之约涨 10 倍。ε = 10⁻⁶、δ = 10⁻³、4 字节计数器时，约 76 MB 涨到约 760 MB，是可控的线性成本。
- **新的瓶颈是扇入：** 要合并的草图数随分片数增长。64 张 76 MB 的草图扁平汇到一个节点，约 4.9 GB；640 张就是约 49 GB。
- **树形合并：** 先在机架或可用区内两两合并，再逐层上推。每个节点只接收少数几份，例如扇入 8，只接收约 610 MB。

**为什么。** 草图的逐格加法满足结合律，所以怎么分组、分几层都不影响结果。先局部合并，让流经最终节点的数据量随层数而不是随分片数增长。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 254">
<rect x="100" y="10" width="140" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根：最终合并</text>
<text x="170" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐格相加</text>
<rect x="30" y="86" width="120" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="90" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机架 1 合并</text>
<text x="90" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐格相加</text>
<rect x="190" y="86" width="120" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机架 2 合并</text>
<text x="250" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐格相加</text>
<rect x="6" y="162" width="76" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 1</text>
<text x="44" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">草图</text>
<rect x="90" y="162" width="76" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 2</text>
<text x="128" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">草图</text>
<rect x="174" y="162" width="76" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 3</text>
<text x="212" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">草图</text>
<rect x="258" y="162" width="76" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="296" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 4</text>
<text x="296" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">草图</text>
<polyline points="90,86 150,46" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150,46 146.0,52.5 142.4,47.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="250,86 190,46" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,46 197.6,47.2 194.0,52.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="44,162 70,122" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="70,122 68.9,129.6 63.5,126.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="128,162 110,122" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="110,122 115.8,127.1 110.0,129.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="212,162 230,122" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="230,122 230.0,129.7 224.2,127.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="296,162 270,122" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="270,122 276.5,126.1 271.1,129.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扁平：所有分片的草图都汇到一个节点</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">树形：每个节点只接收少数几份</text>
</svg>

**面试里这样说。** 「只有 1 分钟桶读原始流，小时和天都是对 CMS 逐格相加，因为更新是线性的。流量涨 10 倍，我把 ε 缩小 10 倍，内存约 76 MB 涨到 760 MB，还是线性的。真正的瓶颈是合并扇入，所以我按机架先合并、再往上汇总，不让所有草图汇到一个节点。」

**易错。**
- **想对 Space-Saving 也逐格相加：** 它没有这个性质，要用候选集并集再配合 CMS。
- **扁平扇入到单点：** 分片数增长后，合并节点最先撑不住。
