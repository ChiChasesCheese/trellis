---
id: uth-ai-vector-search-4-ivf
node: ai.vector-search
type: qa
step: 4
---
## Q
**IVF：先分桶再查**｜pgvector · 0.8.0 IVFFlat

不用图的另一种向量索引：IVFFlat 怎么把百万向量变成「只扫几个桶」？

## A
**背景。** 更朴素的想法：先把向量按位置分成若干堆，像把城市分成几个区；查询时只去最近的几个区找，其余区整个跳过。

**结构。** 倒排表（inverted file，IVF）：建索引时用 k-means（反复把点分给最近的中心，再把中心移到这一堆的平均位置）算出 `lists` 个中心，每个向量归入最近中心的桶。查询先比中心，再扫最近 `probes` 个桶里的向量。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<circle cx="70" cy="70" r="46" style="fill:none;stroke-width:1;stroke-dasharray:4,3"/>
<circle cx="200" cy="60" r="46" style="fill:none;stroke:var(--accent,#3b6fd4);stroke-width:2;stroke-dasharray:4,3"/>
<circle cx="150" cy="150" r="46" style="fill:none;stroke:var(--accent,#3b6fd4);stroke-width:2;stroke-dasharray:4,3"/>
<g>
<circle cx="46.5" cy="77.2" r="3"/>
<circle cx="89.6" cy="59.9" r="3"/>
<circle cx="44.8" cy="68.8" r="3"/>
<circle cx="79.3" cy="91.4" r="3"/>
<circle cx="49" cy="47.7" r="3"/>
</g>
<g style="fill:var(--accent,#3b6fd4);stroke:none">
<circle cx="214.9" cy="70" r="3"/>
<circle cx="226.1" cy="76.7" r="3"/>
<circle cx="196.1" cy="49.6" r="3"/>
<circle cx="234.9" cy="56.1" r="3"/>
<circle cx="185.2" cy="38.6" r="3"/>
<circle cx="155.7" cy="158.7" r="3"/>
<circle cx="138.6" cy="148" r="3"/>
<circle cx="156" cy="165.2" r="3"/>
<circle cx="171.7" cy="154.1" r="3"/>
<circle cx="120.3" cy="161.6" r="3"/>
</g>
<path d="M65 65l10 10m0-10l-10 10" style="stroke-width:2"/>
<path d="M195 55l10 10m0-10l-10 10" style="stroke-width:2"/>
<path d="M145 145l10 10m0-10l-10 10" style="stroke-width:2"/>
<polygon points="170,100 163,113 177,113" style="fill:none;stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="158" y="112" text-anchor="end" style="stroke:none;fill:var(--accent,#3b6fd4)">查询</text>
<text x="170" y="215" style="stroke:none;fill:var(--dim,#6b7280)">x是质心, 蓝圈是离查询最近的2个桶</text>
<text x="170" y="233" stroke="none">只在蓝圈里的点中找, 其余桶跳过</text>
</g>
</svg>
```

**细节。**

- `lists` 起步：1M 行以内用 `rows / 1000`，更多用 `sqrt(rows)`
- `ivfflat.probes` 默认 1，起步可设 `sqrt(lists)`；设成 `lists` 就是精确搜索，规划器不再用索引

**为什么。** 与 HNSW 比：建得快、占内存少，但速度和召回的平衡更差。

**坑。** 必须等表里已有数据再建索引：中心按建索引时的数据算，数据太少，桶分得差，查询返回的行会变少。

**对应 LeetCode：** 无直接对应的题
