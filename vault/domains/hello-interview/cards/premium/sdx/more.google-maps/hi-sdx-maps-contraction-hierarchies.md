---
id: hi-sdx-maps-contraction-hierarchies
node: more.google-maps
type: qa
step: 1
---
## Q
**收缩层次：路网点到点最短路**｜补充 · 地图与导航（Google Maps） · 必会

面试官：「全国级路网上做点到点最短路径，纯 Dijkstra 要先扫过一大片图，延迟扛不住。你怎么让查询只探索很小一部分图？」

## A
**结论。** 用收缩层次（Contraction Hierarchies，CH）：离线按重要度给节点排序，从最不重要的路口开始逐个「收缩」，只在确实经过它的邻居对之间补一条捷径边；查询时起点和终点各做一次只往更重要节点走的双向搜索，在高速层汇合。

**要点。**
- **收缩时补捷径：** 移除节点 B 时，对每对邻居 A、C，若 A→B→C 就是 A 到 C 的最短路（先做见证搜索，排除更短的绕路），就加捷径 A→C，权重为两段之和。
- **双向上行搜索：** 两侧都只沿指向更高层级的边走，相遇处给出最短距离，再把捷径展开成真实路段，几乎不碰本地小路。
- **为什么 Dijkstra 不行：** 它按距离向外扩张，随机两点之间平均要扫过全图约一半的节点（约 1800 万节点的西欧路网上平均约 930 万个）。
- **成本搬到离线：** 代价集中在一次预处理，查询降到毫秒级，捷径边让图略增大。

**为什么。** 最短路里的绝大部分节点是本地小路，而长途路线必然会爬到高速和干线。排序之后，每一端只需向上爬，两边的搜索空间都很小。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 324">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 收缩 B：A 到 C 的最短路经过 B</text>
<rect x="20" y="30" width="56" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="48" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="142" y="30" width="56" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="264" y="30" width="56" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="292" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<polyline points="76,44 142,44" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="142,44 135.0,47.2 135.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="76,44 83.0,40.8 83.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="109" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<polyline points="198,44 264,44" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="264,44 257.0,47.2 257.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="198,44 205.0,40.8 205.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="231" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="20" y="92" width="56" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="48" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="264" y="92" width="56" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="292" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<polyline points="76,106 264,106" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="264,106 257.0,109.2 257.0,102.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="76,106 83.0,102.8 83.0,109.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">捷径 7（B 被移除）</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 查询：两端各自只往更重要的节点走</text>
<rect x="20" y="166" width="70" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="55" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高速 H1</text>
<rect x="250" y="166" width="70" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="285" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高速 H2</text>
<polyline points="90,180 250,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,180 243.0,183.2 243.0,176.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="90,180 97.0,176.8 97.0,183.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">汇合</text>
<rect x="20" y="222" width="70" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="55" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">干线 M1</text>
<rect x="250" y="222" width="70" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="285" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">干线 M2</text>
<rect x="20" y="278" width="70" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="55" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">起点 S</text>
<rect x="250" y="278" width="70" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="285" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">终点 T</text>
<polyline points="55,278 55,250" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="55,250 58.2,257.0 51.8,257.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="55,222 55,194" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="55,194 58.2,201.0 51.8,201.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="285,278 285,250" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="285,250 288.2,257.0 281.8,257.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="285,222 285,194" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="285,194 288.2,201.0 281.8,201.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本地小路几乎不碰</text>
</svg>

**面试里这样说。** 「我会用收缩层次：离线按重要度给路口排序，从最不重要的开始收缩，只在最短路确实经过它的邻居之间加捷径；查询时从起点和终点各做一次只走向更高层的双向搜索，在高速层汇合，所以毫秒级就能出结果。」

**易错。**
- **以为捷径可以随便加：** 收缩时不做见证搜索，会补出无用的捷径，图越来越稠密。
- **忽略预处理依赖边权：** 捷径权重是行程时间之和，路况变了就失效，这是后面要处理实时路况的原因。
