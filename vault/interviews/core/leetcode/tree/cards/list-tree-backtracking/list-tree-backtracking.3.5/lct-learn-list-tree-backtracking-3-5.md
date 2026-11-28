---
id: lct-learn-list-tree-backtracking-3-5
node: list-tree-backtracking.3.5
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 一般树 › 树的直径**｜学习卡

套路是什么？

## A
**一句话。** 每条路径都有唯一的最高点：后序 DFS 求每个节点向下最长的两条分支，两者之和就是以它为最高点的最长路径，全局取最大；返回给父亲的只有最长的一条。

下图：在每个节点取向下最长、次长两条分支；两者之和是以它为最高点的最长路径。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<circle cx="120" cy="30" r="14" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x</text>
<line x1="109.5" y1="44" x2="50" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="50" cy="70" r="8" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<line x1="50" y1="78" x2="50" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="50" cy="100" r="8" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<line x1="50" y1="108" x2="50" y2="122" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="50" cy="130" r="8" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">m1 = 3</text>
<line x1="120.0" y1="44" x2="120" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="70" r="8" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<line x1="120" y1="78" x2="120" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="100" r="8" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">m2 = 2</text>
<line x1="130.5" y1="44" x2="190" y2="62" stroke-width="1.2" stroke="currentColor"/>
<circle cx="190" cy="70" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="220" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans = m1 + m2 = 5</text>
<text x="220" y="56" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">返回给父亲：m1</text>
<text x="220" y="72" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">只带最长一条</text>
<text x="220" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">边数 = 子高度 + 1</text>
</svg>

```python
def tree_diameter(edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    ans = 0

    def height(x, p):                # x 向下最长的边数
        nonlocal ans
        m1 = m2 = 0              # 最长、次长分支
        for y in g[x]:
            if y != p:
                h = height(y, x) + 1
                m1, m2 = max(m1, h), max(m2, min(m1, h))
        ans = max(ans, m1 + m2)  # 以 x 为最高点
        return m1                  # 对父亲只给一条分支

    height(0, -1)
    return ans
```

**要点。**
- 为什么对？：最长路径的最高点是某个节点，路径是它向下的两条不相交分支拼成的，枚举所有最高点取最大即可，`O(n)`。
- 不想递归怎么改？：两次 BFS：从任意点找最远点 `u`，再从 `u` 找最远距离就是直径（边权非负）。
- 二叉树怎么改？：LC 543 直接用左右子树高度，`ans = max(ans, left + right)`。

**易错点。**
- 把 `m1 + m2` 返回给父亲：两条分支相加不是向下的路径，`[[0,1],[1,2],[1,3]]` 得 `3`，应为 `2`。
- `m1`、`m2` 初值设为负无穷：缺的分支算 `0`，`[[0,1]]` 才得 `1`。
- 链状树很深：递归会超过 CPython 默认上限，改迭代或调高递归上限。

**对应题目。** LC 1245 树的直径
