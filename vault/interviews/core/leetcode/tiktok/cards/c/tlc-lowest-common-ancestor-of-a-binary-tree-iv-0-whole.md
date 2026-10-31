---
id: tlc-lowest-common-ancestor-of-a-binary-tree-iv-0-whole
node: c.lowest-common-ancestor-of-a-binary-tree-iv
type: qa
---
## Q
**LC 1676 二叉树的最近公共祖先 IV**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2024-11-13（国内 CodeTop）

给定二叉树的根节点 `root` 和 `TreeNode` 对象列表 `nodes`，返回 `nodes` 中所有节点的最近公共祖先（LCA）：后代中包含所有这些节点的最深节点（允许节点是自己的后代）。列表中的节点都在树中，且树中所有节点值互不相同。树中节点个数范围 `[1, 10^4]`，`-10^9 <= Node.val <= 10^9`，`nodes[i]` 互不相同。例：`root = [3,5,1,6,2,0,8,null,null,7,4]`，`nodes = [4,7]` → `2`；`nodes = [1]` → `1`；`nodes = [7,6,2,4]` → `5`；`nodes` 为全部节点 → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 经典 LCA 递归的推广：把「等于 `p` 或 `q`」换成「属于目标集合」，一次后序遍历，左右两侧都返回非空的节点就是答案。

**识别。** 「多个节点的最近公共祖先」仍是自底向上的树形递归：每个节点只需要知道左右子树里有没有目标。题目保证目标都在树中，所以不用核实「是否都找到了」。

**推导。** 暴力：为每个目标求根路径，再取公共前缀，`O(n * k)`。洞察：遇到目标直接返回（它的子树里即使还有目标，该目标也就是那一支的汇合点）；若左右各返回非空，当前节点就是所有目标的分叉点；只有一侧非空就把那一侧的结果上传。

```python
def lowest_common_ancestor(root: TreeNode | None, nodes: list[TreeNode]) -> TreeNode | None:
    targets = set(nodes)                         # TreeNode 按对象身份哈希

    def dfs(node: TreeNode | None) -> TreeNode | None:
        if node is None or node in targets:      # 遇到目标就不用往下找了：它自己就是这条分支的代表
            return node
        left = dfs(node.left)
        right = dfs(node.right)
        if left and right:                       # 两侧各有目标：当前节点是它们的汇合点
            return node
        return left or right                     # 只有一侧有目标，向上传递

    return dfs(root)
```

运行：示例四个依次返回值为 `2`、`1`、`5`、`3` 的节点；随机树上的结果与逐目标求根路径取公共前缀一致。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈，`h` 为树高）。

**拓展优化。**
- 链状树深度可达 `10^4`，递归会超限：先用显式栈得到先序序列和父指针，再倒序累加每个子树里的目标数，第一个累计到 `len(targets)` 的节点就是 LCA：

```python
def lowest_common_ancestor_iterative(root: TreeNode | None, nodes: list[TreeNode]) -> TreeNode | None:
    targets = set(nodes)
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    order: list[TreeNode] = []                   # 先序遍历序，逆序处理就是自底向上
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    found: dict[TreeNode, int] = {}              # 子树里包含的目标数（以及目标本身）
    for node in reversed(order):
        total = found.get(node, 0) + (node in targets)
        if total == len(targets):                # 第一次达到全部目标数的最深节点
            return node
        if parent[node] is not None:
            found[parent[node]] = found.get(parent[node], 0) + total
    return None
```

**易错点。**
- 目标集合用列表而不是 `set`：每个节点做 `in` 判断都是 `O(k)`，总时间退化为 `O(n * k)`。
- 遇到目标后继续往下递归：多余，且会让「目标在目标之下」的情形返回更深的节点；`nodes = [5, 4]`（4 在 5 的子树里）应返回 `5`。
- 最坏深度：链状树 `10^4` 个节点，递归深度 `10^4`，CPython 默认递归上限约 1000，会抛 `RecursionError`，需要 `sys.setrecursionlimit` 或改为迭代。

**追问。**
- 目标可能不在树中（LC 1644）：需要额外统计找到了几个目标，不足就返回 `None`。
- 有父指针（LC 1650）：沿父指针向上走，类似链表相交。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 1644 二叉树的最近公共祖先 II、LC 1650 二叉树的最近公共祖先 III、LC 865 具有所有最深节点的最小子树。
