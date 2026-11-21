---
slug: find-subtree-sizes-after-changes
---
## Q
**LC 3331 修改后子树的大小**｜Medium

以 0 为根的树用 `parent` 数组给出，节点 `i` 的字符是 `s[i]`。每个节点同时改挂到离它最近的同字符祖先下（没有就不动），求新树里每个节点的子树大小。

## A
**一句话。** DFS 时按字符记「路径上最近的该字符祖先」，就是新父节点；后序把自己的子树大小加给新父节点。

**图解。** 3a 往上最近的 a 是 0a，于是改挂到 0 下；1 的子树从 4 变成 3。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 150">
<line x1="63.2" y1="33.9" x2="46.8" y2="58.1" stroke="currentColor" stroke-width="1.2"/>
<line x1="76.8" y1="33.9" x2="93.2" y2="58.1" stroke="currentColor" stroke-width="1.2"/>
<line x1="34.1" y1="78.4" x2="20.9" y2="101.6" stroke="currentColor" stroke-width="1.2"/>
<line x1="40.0" y1="80.0" x2="40.0" y2="100.0" stroke="currentColor" stroke-width="1.2"/>
<line x1="45.9" y1="78.4" x2="59.1" y2="101.6" stroke="currentColor" stroke-width="1.2"/>
<line x1="242.5" y1="33.4" x2="222.5" y2="58.6" stroke="currentColor" stroke-width="1.2"/>
<line x1="250.0" y1="36.0" x2="250.0" y2="56.0" stroke="currentColor" stroke-width="1.2"/>
<line x1="257.5" y1="33.4" x2="277.5" y2="58.6" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.8"/>
<line x1="210.0" y1="78.9" x2="200.0" y2="101.1" stroke="currentColor" stroke-width="1.2"/>
<line x1="220.0" y1="78.9" x2="230.0" y2="101.1" stroke="currentColor" stroke-width="1.2"/>
<circle cx="70" cy="24" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="27.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">0a</text>
<circle cx="40" cy="68" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="71.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1b</text>
<circle cx="100" cy="68" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="71.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2a</text>
<circle cx="15" cy="112" r="12" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="15" y="115.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">3a</text>
<circle cx="40" cy="112" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="115.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">4b</text>
<circle cx="65" cy="112" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="115.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5c</text>
<circle cx="250" cy="24" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="27.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">0a</text>
<circle cx="215" cy="68" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="215" y="71.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1b</text>
<circle cx="250" cy="68" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="71.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">2a</text>
<circle cx="285" cy="68" r="12" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="285" y="71.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">3a</text>
<circle cx="195" cy="112" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="195" y="115.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">4b</text>
<circle cx="235" cy="112" r="12" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="115.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">5c</text>
<text x="152" y="72" text-anchor="middle" font-size="16" font-family="sans-serif" fill="currentColor">→</text>
<text x="152" y="54" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3a 往上找 a</text>
<text x="55" y="142" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">原树</text>
<text x="240" y="142" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新树：size[1] = 3</text>
</svg>

```python
def find_subtree_sizes(parent, s):
    n = len(parent)
    g = [[] for _ in range(n)]
    for i in range(1, n):
        g[parent[i]].append(i)
    size = [1] * n
    last = {}      # 字符 -> 当前路径上最近的该字符节点

    def dfs(x):
        y = last.get(s[x])   # x 的新父节点，可能没有
        last[s[x]] = x
        for c in g[x]:
            dfs(c)
        last[s[x]] = y       # 回溯：恢复给兄弟子树用
        # 后序：新子节点都在 x 之下，已加完
        p = parent[x] if y is None else y
        if p >= 0:
            size[p] += size[x]

    dfs(0)
    return size
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 忘了回溯 `last`：兄弟子树会把别的分支上的节点当成祖先。
- 按原树先算子树再改：改挂是同时发生的，新父节点只能是原祖先，所以一次后序就够，不必真的重建树。

**追问。**
- 为什么后序累加是对的？：新父节点一定是原树祖先，比 `x` 晚结束；`x` 的新子节点都是原树后代，比 `x` 早结束。
- `n = 10^5` 递归会爆栈？：Python 要 `sys.setrecursionlimit`，或改成显式栈，先算新父节点再按逆序累加。

**同模式。** LC 437 路径总和 III、LC 1519 子树中标签相同的节点数、LC 2246 相邻字符不同的最长路径
