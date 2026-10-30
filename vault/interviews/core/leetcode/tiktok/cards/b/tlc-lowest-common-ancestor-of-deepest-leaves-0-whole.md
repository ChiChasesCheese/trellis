---
id: tlc-lowest-common-ancestor-of-deepest-leaves-0-whole
node: b.lowest-common-ancestor-of-deepest-leaves
type: qa
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium · CodeTop 国内累计 1 次 · 最近 2026-03-31（国内 CodeTop）

给一棵二叉树的根结点 `root`，返回它**最深的叶结点们**的最近公共祖先。叶结点是没有子结点的结点；根的深度是 `0`，深度为 `d` 的结点的子结点深度为 `d + 1`。一组结点 `S` 的最近公共祖先 `A` 满足：`S` 中每个结点都在以 `A` 为根的子树里，且 `A` 的深度在此条件下尽可能大。树中结点数在 `[1, 1000]` 范围内，`0 <= Node.val <= 1000`，每个结点的值都不相同。例：`root = [3,5,1,6,2,0,8,null,null,7,4]` → 值为 `2` 的结点（子树 `[2,7,4]`；最深的叶子是 `7` 和 `4`，深度 `3`）；`root = [1]` → `[1]`；`root = [0,1,3,null,2]` → `[2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 自底向上，对每个结点求「它子树里最深叶子的深度」和「这些最深叶子的最近公共祖先」：左右子树一样深，答案就是这个结点本身；否则沿用更深那一侧的答案。根结点上的结果就是题目的答案。`O(n)`。

**识别。** 「最深叶子」+「最近公共祖先」是树形 DP 的信号：每个结点只需要从两个孩子拿到 `(深度, 答案)` 两个量，就能合并出自己的。同一族的题还有 LC 236（任意两个结点的 LCA）。后序递归最直观；结点数最多 `1000`，但链状树的深度可达 `1000`，正好碰到 Python 默认的递归上限，见易错点。

**推导。** 暴力：先遍历记录每个结点的深度，找出最深一层的所有叶子，再两两求 LCA，或者逐个比较根到叶子的路径，`O(n * h)`。浪费：深度和 LCA 分两遍算。洞察：设结点 `x` 左右子树里最深叶子的深度是 `ld` 和 `rd`。`ld > rd`：所有最深叶子都在左边，`x` 子树里的答案等于左子树的答案；`rd > ld` 对称；`ld == rd`：最深叶子分居两边（或者 `x` 自己是叶子），`x` 就是它们的汇合点。写成后序递归：函数返回 `(深度, 答案)`，每个结点处理一次。

```python
def lca_deepest_leaves(root: TreeNode | None) -> TreeNode | None:
    def dfs(node: TreeNode | None) -> tuple[int, TreeNode | None]:
        # 返回 (node 子树里最深叶子的深度（以 node 为 1）, 这些最深叶子的最近公共祖先)
        if node is None:
            return 0, None                     # 空子树
        ld, lca_l = dfs(node.left)
        rd, lca_r = dfs(node.right)
        if ld > rd:
            return ld + 1, lca_l               # 最深的叶子都在左边
        if rd > ld:
            return rd + 1, lca_r               # 最深的叶子都在右边
        return ld + 1, node                    # 左右一样深（含叶子本身）：node 就是汇合点

    return dfs(root)[1]
```

运行（返回结点的值）：`[3,5,1,6,2,0,8,null,null,7,4]` → `2`，`[1]` → `1`，`[0,1,3,null,2]` → `2`，`[1,2,3]` → `1`，`[1,2,null,3]` → `3`；`1000` 个结点的链状树 → `999`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个结点处理一次；空间 `O(h)`：递归栈，链状树时为 `O(n)`。

**易错点。**
- 平局时沿用左边的答案（把 `ld > rd` 写成 `ld >= rd`，叶子处退回自己）：`[1,2,3]` 得到结点 `2`，正确是结点 `1`，因为两片最深的叶子 `2` 和 `3` 分居两侧，汇合点是根。
- 返回「最深叶子的父结点」：`[0,1,3,null,2]` 得到结点 `1`，正确是结点 `2`，只有一片最深叶子时它自己就是 LCA。
- 递归深度：`1000` 个结点的链状树，递归深度 `1000` 层以上，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。

**追问。**
- 不想动递归上限：BFS 序倒着处理，孩子先于父亲，等价于后序：
```python
def lca_deepest_leaves_iter(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    order = [root]                     # BFS 序：父结点一定排在子结点前面
    for node in order:                 # 遍历列表的同时往后追加，等价于队列
        order.extend(child for child in (node.left, node.right) if child)
    info: dict[TreeNode, tuple[int, TreeNode | None]] = {}   # (最深叶子的深度, 它们的最近公共祖先)
    empty = (0, None)                  # 空子树
    for node in reversed(order):       # 逆 BFS 序：孩子先于父亲，等价于后序遍历
        (ld, lca_l), (rd, lca_r) = info.get(node.left, empty), info.get(node.right, empty)
        if ld > rd:
            info[node] = (ld + 1, lca_l)
        elif rd > ld:
            info[node] = (rd + 1, lca_r)
        else:
            info[node] = (ld + 1, node)
    return info[root][1]
```
- 带父指针的另一种做法：先找到最深一层的全部结点，整体向上提一层，去重，直到只剩一个结点。
- 一组任意给定结点的 LCA（LC 1676）：后序递归，统计子树里命中了几个目标，到达总数的最低位置就是答案。

**同模式。** LC 865 具有所有最深节点的最小子树（同一道题）、LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 543 二叉树的直径。
