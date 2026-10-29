---
id: uth-gaps-union-find-1-equivalence-class
node: gaps.union-find
type: qa
step: 1
---
## Q
**a=b、b=c，规划器怎样自己得到 a=c**｜PostgreSQL · 17

查询写了 `a.x = b.y AND b.y = c.z AND c.z = 5`，没有写 `a.x = c.z`，也没有写 `a.x = 5`。数据库怎样自己得出它们，又为什么要得出？

## A
**背景。** 最笨的办法是照字面执行：三条条件各管各的，没人告诉 `a` 表它的 `x` 必须是 5，只好把 `a` 整张表读出来再连接。聪明的办法：把「已知相等」的东西放进同一组，组内任意两个之间的比较都不用再写。新来一条 `p = q`：一边已有组，就把另一边加进去；两边各有一组，就把两组并成一组。

**结构。** PostgreSQL 把这样的一组叫等价类（EquivalenceClass）。例：`{a.x, b.y}` 和 `{c.z, 5}` 被 `b.y = c.z` 并成一组。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="170" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">WHERE a.x = b.y AND b.y = c.z AND c.z = 5</text>
<rect x="20" y="26" width="130" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="28" y="35" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="55" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.x</text>
<rect x="88" y="35" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="115" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.y</text>
<rect x="190" y="26" width="130" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="198" y="35" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="225" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c.z</text>
<rect x="258" y="35" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="285" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<line x1="85" y1="70" x2="114.2" y2="105.4" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M118,110 L111.9,107.3 L116.5,103.5 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="255" y1="70" x2="225.8" y2="105.4" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M222,110 L223.5,103.5 L228.1,107.3 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">b.y = c.z</text>
<rect x="20" y="112" width="300" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="30" y="120" width="62" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="61" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.x</text>
<rect x="102" y="120" width="62" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="133" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.y</text>
<rect x="174" y="120" width="62" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="205" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c.z</text>
<rect x="246" y="120" width="62" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="277" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<line x1="70" y1="154" x2="70" y2="178" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M70,184 L67,178 L73,178 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="170" y1="154" x2="170" y2="178" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170,184 L167,178 L173,178 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="270" y1="154" x2="270" y2="178" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M270,184 L267,178 L273,178 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="24" y="186" width="92" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.x = 5</text>
<rect x="124" y="186" width="92" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.y = 5</text>
<rect x="224" y="186" width="92" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c.z = 5</text>
<text x="170" y="230" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每张表扫描时就只读等于 5 的行</text>
</svg>
```

**细节。**

- 组里有常量 5：给每个成员各生成一条 `列 = 5`，扫描各自的表时就过滤
- 组里没有常量：要连 `a` 和 `c` 时现造 `a.x = c.z`，不会因为没写条件就被迫做笛卡尔积（Cartesian product，两张表的行两两配对）

**为什么。** 相等能传递，让规划器自己推导，比靠人写全可靠，还多出可选的连接顺序。

**例题：** LC 547 省份数量（同类：LC 1319 连通网络的操作次数）

`n x n` 的邻接矩阵 `isConnected`，`isConnected[i][j] = 1` 表示城市 `i`、`j` 直接相连。直接或间接相连的城市构成一个省份，返回省份总数。`1 <= n <= 200`。

```python
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # 路径减半
            x = parent[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                root_i, root_j = find(i), find(j)
                if root_i != root_j:
                    parent[root_i] = root_j
    return len({find(i) for i in range(n)})
```
