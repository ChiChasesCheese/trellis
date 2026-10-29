---
id: uth-gaps-tree-dfs-1-post-order
node: gaps.tree-dfs
type: qa
step: 1
---
## Q
**du 怎样算出每个目录有多大**｜GNU coreutils · du 9.12

`du` 一次列出每个子目录的大小。一个目录的大小取决于里面的所有东西，它先算谁、后算谁，又怎样不把同一个文件数很多遍？

## A
**背景。** 目录大小 = 自己占的空间 + 里面每个文件 + 每个子目录的总大小。直觉做法：对每个目录各自把底下所有文件重新扫一遍再相加。可是每个文件在它的每一层祖先那里都被扫一次，越深数得越多。

**结构。** 后序遍历（post-order）：先走进子目录，等里面全算完得到一个总数，回到父目录时把总数加进来，自己最后算。每个文件只读一次，每个目录离开时恰好报一次大小，所以 `du` 的输出里子目录总在父目录之前。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<line x1="170" y1="38" x2="95" y2="80" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="38" x2="245" y2="80" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="95" y1="104" x2="55" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="95" y1="104" x2="135" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="245" y1="104" x2="245" y2="152" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="140" y="14" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">/  4</text>
<rect x="65" y="80" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="95" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a  4</text>
<rect x="215" y="80" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="245" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b  4</text>
<rect x="27" y="152" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">x  10</text>
<rect x="107" y="152" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">y  20</text>
<rect x="217" y="152" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">z  5</text>
<text x="206" y="30" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">合计 47</text>
<text x="131" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">合计 34</text>
<text x="281" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">合计 9</text>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">方框里是自己占的大小 先算完子目录再加到父目录</text>
</svg>
```

**细节。**

- 遍历库 `fts` 逐个吐出条目：进入目录（`FTS_D`）时什么都不做，离开（`FTS_DP`）时才统计、打印
- 数的是磁盘块 `st_blocks`；加 `--apparent-size` 才数内容字节

**为什么。** 每个节点只处理一次，总时间与条目数成正比；重复扫描要乘以深度。

**例题：** LC 508 出现次数最多的子树元素和（同类：LC 110 平衡二叉树）

给二叉树根结点 `root`，返回出现次数最多的子树元素和（以某结点为根的整棵子树所有结点值之和）；并列时全部返回，顺序不限。结点数 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`。例：`[5,2,-3]` → `[2,-3,4]`。

```python
from collections import Counter


def find_frequent_tree_sum(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    order: list[TreeNode] = []
    stack = [root]
    while stack:                               # 先序：父总在子之前
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    total: dict[TreeNode, int] = {}            # 每个节点的子树和
    freq: Counter[int] = Counter()
    for node in reversed(order):               # 倒着扫 = 孩子先于父亲
        s = node.val + total.get(node.left, 0) + total.get(node.right, 0)
        total[node] = s
        freq[s] += 1
    top = max(freq.values())
    return [s for s, c in freq.items() if c == top]
```
