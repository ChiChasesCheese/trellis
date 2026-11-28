---
id: lct-learn-list-tree-backtracking-2-6
node: list-tree-backtracking.2.6
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 二叉树的直径**｜学习卡

套路是什么？

## A
**一句话。** 树上任何一条路径都有唯一的最高点，路径就是「向左下的一条链 + 向右下的一条链」；后序 DFS 返回向下的单链（给父亲继续延伸），答案则在每个节点处用左链加右链更新全局变量。

下图：每条路径在最高点处拆成左链加右链；返回值只带一侧链给父亲。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<line x1="91.3" y1="34.7" x2="63.7" y2="65.3" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="109.2" y1="34.2" x2="140.8" y2="65.8" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="48.3" y1="86.1" x2="31.7" y2="113.9" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="61.7" y1="86.1" x2="78.3" y2="113.9" stroke-width="1.2" stroke="currentColor"/>
<circle cx="100" cy="25" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="100" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<circle cx="55" cy="75" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="55" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="150" cy="75" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="25" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="25" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="85" cy="125" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="40" y="48" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">l = 2</text>
<text x="160" y="48" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">r = 1</text>
<text x="200" y="28" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最高点 1：</text>
<text x="200" y="44" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans = l + r = 3</text>
<text x="200" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">向上只返回一侧：</text>
<text x="200" y="100" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">max(l, r) + 1</text>
<text x="170" y="155" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">路径 4-2-1-3 = 左链 + 右链，在最高点处结算</text>
</svg>

```python
def diameter(root):                  # LC 543
    ans = 0                          # 答案放在外面，和返回值分开
    def dfs(node):                   # 返回向下最长链的节点数
        nonlocal ans
        if node is None:
            return 0
        l, r = dfs(node.left), dfs(node.right)
        ans = max(ans, l + r)        # 以 node 为最高点的路径边数
        return max(l, r) + 1         # 向上只能带一侧，不能分叉
    dfs(root)
    return ans
```

**要点。**
- 为什么对？：路径与「（最高点，左链，右链）」一一对应，最长路径必在某个节点取到 `l + r`；返回值与答案必须分开，因为延伸时只能选一侧，结算时可以用两侧。
- LC 124 怎么改？：链带权，`l = max(dfs(left), 0)`（负链不如不走），结算 `node.val + l + r`，返回 `node.val + max(l, r)`，`ans` 初值负无穷。
- LC 2385 怎么改？：把树变成无向图（DFS 记父亲），从 `start` 做 BFS，层数减一就是分钟数。

**易错点。**
- 把 `l + r` 当返回值：`[1,2,3]` 直径是 `2`，已分叉的路径不能再被父亲接长。
- 读 `dfs(root)` 当答案：`[1,2,3,4,5]` 直径应得 `3`，返回值只是向下最长链。
- LC 124 的 `ans` 初值设成 `0`：`[-3]` 应得 `-3`；不舍负链：`[1,-2,3]` 应得 `4`。

**对应题目。** LC 2385 感染二叉树需要的总时间、LC 124 二叉树中的最大路径和、LC 543 二叉树的直径
