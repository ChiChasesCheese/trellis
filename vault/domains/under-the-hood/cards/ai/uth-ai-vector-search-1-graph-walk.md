---
id: uth-ai-vector-search-1-graph-walk
node: ai.vector-search
type: qa
step: 1
---
## Q
**百万个向量里怎么快速找最近的几个**｜pgvector · 0.8.0 HNSW

`ORDER BY embedding <-> $1 LIMIT 5` 在百万行向量上，为什么建了 HNSW 索引后快得多？

## A
**背景。** 向量（vector）是一串数，意思相近的文本、图片，数也靠得近。找最近的几个，最直接是把查询和每一行都算一次距离：百万行就是百万次计算，每次查询都这样太慢。换个想法像问路：让每个点只记住几个最近的邻居，连成一张图；查询从某个点出发，每步走向离查询更近的邻居，走不动就停。但图只有一层时，起点可能很远，要走很多步。

**结构。** 分层近邻图（HNSW，Hierarchical Navigable Small World）：所有点都在最底层，少数点还出现在上一层，层越高点越少。先在稀疏的上层大步走，再下到底层细找，和跳表（skip list）的快车道是同一个思路。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<text x="6" y="20" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">上层 稀疏</text>
<text x="60" y="98" text-anchor="start" style="stroke:none;fill:var(--dim,#6b7280)">底层 全部点</text>
<line x1="41" y1="52" x2="203" y2="52" style="stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<line x1="229" y1="52" x2="297" y2="52" style="stroke-width:1"/>
<line x1="28" y1="65" x2="28" y2="119" style="stroke-width:1;stroke-dasharray:3,3"/>
<line x1="216" y1="65" x2="216" y2="119" style="stroke:var(--accent,#3b6fd4);stroke-width:2;stroke-dasharray:3,3"/>
<line x1="310" y1="65" x2="310" y2="119" style="stroke-width:1;stroke-dasharray:3,3"/>
<line x1="41" y1="132" x2="62" y2="132" style="stroke-width:1"/>
<line x1="88" y1="132" x2="109" y2="132" style="stroke-width:1"/>
<line x1="135" y1="132" x2="156" y2="132" style="stroke-width:1"/>
<line x1="182" y1="132" x2="203" y2="132" style="stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<line x1="229" y1="132" x2="250" y2="132" style="stroke-width:1"/>
<line x1="276" y1="132" x2="297" y2="132" style="stroke-width:1"/>
<circle cx="28" cy="52" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="28" y="56.2" stroke="none">5</text>
<circle cx="216" cy="52" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="216" y="56.2" stroke="none">40</text>
<circle cx="310" cy="52" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="310" y="56.2" stroke="none">90</text>
<circle cx="28" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="28" y="136.2" stroke="none">5</text>
<circle cx="75" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="75" y="136.2" stroke="none">12</text>
<circle cx="122" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="122" y="136.2" stroke="none">25</text>
<circle cx="169" cy="132" r="13" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="169" y="136.2" style="stroke:none;fill:#fff">33</text>
<circle cx="216" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="216" y="136.2" stroke="none">40</text>
<circle cx="263" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="263" y="136.2" stroke="none">52</text>
<circle cx="310" cy="132" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="310" y="136.2" stroke="none">90</text>
<polygon points="141,148 135,159 147,159" style="fill:var(--accent,#3b6fd4)"/>
<text x="141" y="174" style="stroke:none;fill:var(--accent,#3b6fd4)">查询30</text>
<text x="170" y="200" stroke="none">从5出发: 上层1步到40, 底层1步到33</text>
<text x="170" y="218" style="stroke:none;fill:var(--dim,#6b7280)">只走底层要5到12到25到33, 共3步</text>
</g>
</svg>
```

**细节。**

- 图里找最接近 30 的点：上层 1 步到 40，底层再 1 步到 33
- pgvector 默认 `m = 16`：每个点最多连 16 个邻居，底层放宽到 32 个
- 结果是近似的：贪心可能走进死胡同，漏掉真正最近的

**为什么。** 暴力查询每次是 O(n)，分层图的搜索步数随数据量近似按对数增长。代价是：多占内存存邻居线，召回率（recall，找回了几成真正最近的）不是 100%。

**对应 LeetCode：** 无直接对应的题
