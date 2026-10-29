---
id: uth-gaps-union-find-2-ena
node: gaps.union-find
type: qa
step: 2
---
## Q
**合并小组怎样几乎不花时间**｜Rust 编译器 · rustc 1.90

编译器给每个还不知道的类型起一个名字（`?A`、`?B`…），遇到「这两个必须是同一个类型」就要把它们合并。变量成千上万时，合并和查询怎样都不慢？

## A
**背景。** 直觉做法：每个变量存一份「同组成员」名单，合并就把两份名单拷成一份，名单越长越慢。并查集（union-find）换个想法：每个变量只记一个父指针，指向同组的另一个变量；根指向自己，整组共享根上的信息。

**结构。** rustc 把每个未知类型变量放进 `ena` 这个并查集库。`find` 顺父指针走到根，`union` 把一个根挂到另一个根下面。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="85" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">find 之前</text>
<text x="255" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">find(?C) 之后</text>
<line x1="170" y1="8" x2="170" y2="176" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<line x1="85" y1="92" x2="85" y2="68" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M85,62 L88,68 L82,68 Z" fill="currentColor" stroke="none"/>
<line x1="85" y1="146" x2="85" y2="124" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M85,118 L88,124 L82,124 Z" fill="currentColor" stroke="none"/>
<rect x="57" y="36" width="56" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?A</text>
<rect x="57" y="92" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?B</text>
<rect x="57" y="146" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?C</text>
<text x="122" y="53" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">根: u8</text>
<line x1="218" y1="96" x2="236.7" y2="67" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M240,62 L239.3,68.7 L234.2,65.4 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="292" y1="96" x2="273.3" y2="67" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M270,62 L275.8,65.4 L270.7,68.7 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="227" y="36" width="56" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?A</text>
<rect x="190" y="98" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="218" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?B</text>
<rect x="264" y="98" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">?C</text>
<text x="292" y="53" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">根: u8</text>
<text x="255" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">下次一步到位</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">find(?C) 走到根 并把 ?C 改成直接指向根</text>
</svg>
```

**细节。**

- `find` 走完后，沿途的点改成直接指向根：路径压缩（path compression）
- `union` 默认把秩（rank，树高的上界）小的根挂到大的下面，树不会长高
- 根上存「未知」或「已知是 u8」：给 `?C` 定下 `u8`，同组的 `?A`、`?B` 马上都知道

**为什么。** 两招合起来，每次操作的均摊时间接近常数；名单做法每次合并都要拷贝。

**例题：** LC 305 数岛屿 II

`m x n` 的网格一开始全是水。依次给出 `positions`，每个 `[r, c]` 把该格变成陆地（可能重复）。每次变化后返回当前的岛屿数（四连通）。不能每次重扫整张图。

```python
def num_islands_ii(m, n, positions):
    parent = {}                                       # only land cells exist in the structure (sparse, O(#adds) memory)
    size = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    islands, answer = 0, []
    for r, c in positions:
        cell = (r, c)
        if cell in parent:                            # duplicate addLand: nothing changes
            answer.append(islands)
            continue
        parent[cell], size[cell] = cell, 1
        islands += 1                                  # a brand-new island ...
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (r + dr, c + dc)
            if nb in parent:
                ra, rb = find(cell), find(nb)
                if ra != rb:                          # ... which every successful merge reduces by one
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    islands -= 1
        answer.append(islands)
    return answer
```
