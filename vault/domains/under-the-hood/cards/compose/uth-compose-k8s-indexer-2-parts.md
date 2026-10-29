---
id: uth-compose-k8s-indexer-2-parts
node: compose.k8s-indexer
type: qa
step: 2
---
## Q
**主表加二级索引**｜Kubernetes · client-go v0.37

`Indexer` 由哪几张表组成？一次写入和一次按索引查询分别碰哪几张？

## A
**结构。** 三张表：`items`（key → 对象，唯一存放对象的地方）、`indexers`（索引名 → 索引函数，从对象算出它属于哪些分组）、`indices`（索引名 → 分组值 → key 集合）。索引里只存 key，不存对象。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<rect x="10" y="22" width="320" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="38" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">items: key -> 对象 (对象只存这一份)</text>
<rect x="18" y="46" width="96" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="66" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">a</text>
<text x="66" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">default / n1</text>
<rect x="122" y="46" width="96" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="170" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">b</text>
<text x="170" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">default / n2</text>
<rect x="226" y="46" width="96" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="274" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">c</text>
<text x="274" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">kube / n1</text>
<rect x="10" y="120" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="136" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">索引 namespace</text>
<text x="18" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">default -> {a, b}</text>
<text x="18" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">kube -> {c}</text>
<rect x="180" y="120" width="150" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="188" y="136" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">索引 node</text>
<text x="188" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">n1 -> {a, c}</text>
<text x="188" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">n2 -> {b}</text>
<line x1="85" y1="120" x2="85" y2="92" stroke="currentColor" stroke-width="1"/>
<polygon points="85,92 81,100 89,100" fill="currentColor"/>
<line x1="255" y1="120" x2="255" y2="92" stroke="currentColor" stroke-width="1"/>
<polygon points="255,92 251,100 259,100" fill="currentColor"/>
<text x="93" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key</text>
<text x="263" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引只存 key: 先拿到 key 集合, 再回主表取对象</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写一个对象: 主表和每个索引都要改</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `Get(k)` | `items` | O(1) |
| `ByIndex(名, 值)` | `indices[名][值]` 得 key 集合，再逐个查 `items` | O(结果个数) |
| 增、改、删 | `items` + 每个索引：摘旧、挂新 | O(索引个数) |

**为什么。** 索引只存 key：对象只有一份，改对象不必同步多份拷贝。代价是每多一个索引，每次写入多一轮摘旧挂新。

**对应 LeetCode：** 无直接对应的题
