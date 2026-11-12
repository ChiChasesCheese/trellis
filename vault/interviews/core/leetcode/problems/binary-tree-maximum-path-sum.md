---
slug: binary-tree-maximum-path-sum
---
## Q
**LC 124 二叉树中的最大路径和**｜Hard

求二叉树中任意一条路径（至少一个节点，不必过根，节点不重复）的最大节点值之和。

## A
**一句话。** 后序递归，每个节点返回向下的最大单链和，负的一侧舍弃，并以它为最高点更新全局答案。

```python
def max_path_sum(root):
    best = root.val              # 不能用 0：全负树答案为负
    def gain(node):              # 从 node 向下的最大单链和
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)     # 负收益不要
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # 顶
        return node.val + max(left, right)  # 对父只能选一边
    gain(root)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 没舍弃负增益：`[1,-2,3]` 得 `3`，应为 `4`。
- 返回 `val + left + right`：拼出分叉路径，`[1,2,3,null,null,4,5]` 得 `15`，应为 `12`。
- `best` 初值取 `0`：`[-3]` 应得 `-3`。

**追问。**
- 链状树深 `3*10^4` 会爆栈吗？：会，CPython 递归上限约 1000，要调大上限或改显式栈（逆先序处理，孩子先于父亲）。
- 路径必须从根出发？：只剩单链，去掉「左右合并」那一步。

**同模式。** LC 543 二叉树的直径、LC 687 最长同值路径、LC 337 打家劫舍 III、LC 968 监控二叉树
