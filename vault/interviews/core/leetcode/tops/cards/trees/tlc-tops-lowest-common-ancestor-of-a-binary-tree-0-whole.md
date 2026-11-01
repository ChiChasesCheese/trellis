---
id: tlc-tops-lowest-common-ancestor-of-a-binary-tree-0-whole
node: trees.lowest-common-ancestor-of-a-binary-tree
type: qa
---
## Q
**LC 236 二叉树的最近公共祖先**｜Medium · 全公司热度第 117 名 · Hot 100、Top Interview 150、LeetCode 75

给定一个二叉树，找到该树中两个指定节点 `p`、`q` 的最近公共祖先（LCA）：满足「是 `p`、`q` 的祖先」且深度尽可能大的节点，**一个节点也可以是它自己的祖先**。节点数在 `[2, 10^5]`，`-10^9 <= Node.val <= 10^9`，所有 `Node.val` 互不相同，`p != q`，且 `p` 和 `q` 均存在于树中。例：`root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1` → `3`；`p = 5, q = 4` → `5`（节点本身）；`root = [1,2], p = 1, q = 2` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树后序 DFS：递归返回「这棵子树里找到了什么」，在左右结果的汇合点得到答案。

**一句话。** 在子树里找 `p`、`q`：遇到 `p` 或 `q` 就直接返回它；左右子树都有返回值，说明 `p`、`q` 分居两侧，当前节点就是 LCA；否则返回非空的那一侧。

**识别。** 「两个节点的最近公共祖先」且不是 BST（不能比大小走）：用后序 DFS 汇总。保证 `p`、`q` 都在树里，才允许遇到其中一个就提前返回。`n <= 10^5`：`O(n)` 一次遍历；注意递归深度。

**推导。** 先找到 `p` 和 `q` 各自的根路径再找最后一个相同节点，要存路径，`O(n)` 空间。递归把「路径」藏进返回值：`lca(node)` 的含义是「`node` 子树中 `p` 或 `q` 的最高出现位置」。左右都找到 → 分居两侧 → 当前节点是 LCA；只有一边找到 → 把那一边的结果向上传（可能是 `p`、`q` 之一，也可能是已经确定的 LCA）。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root                                # 空，或找到了其中一个：直接返回（它已经是这棵子树里最高的那个）
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root                                # p、q 分居两侧：root 就是最近公共祖先
    return left or right                           # 只有一侧有：把那一侧的结果往上传
```

运行：`[3,5,1,6,2,0,8,null,null,7,4]`，`p=5, q=1` → `3`；`p=5, q=4` → `5`；`[1,2]`，`p=1, q=2` → `1`；`p=6, q=4` → `5`。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`，递归栈。

**拓展优化。**
- 深链输入（`n = 10^5`）不能递归：先用栈遍历记录每个节点的父亲，再让 `p` 的所有祖先入集合，`q` 向上走到第一个在集合里的节点。
```python
def lca_parent(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while p not in parent or q not in parent:      # 找到 p、q 就可以停
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    ancestors = set()
    while p:                                       # p 的所有祖先（含自己）
        ancestors.add(p)
        p = parent[p]
    while q not in ancestors:                      # q 向上走，第一个落在集合里的就是 LCA
        q = parent[q]
    return q
```
- 多次查询同一棵树：预处理父亲数组做倍增（binary lifting），每次查询 `O(log n)`。

**易错点。**
- 去掉「遇到 `p` 或 `q` 就返回」，只在左右都找到时才返回：`p = 5, q = 4` 时，`5` 之下才有 `4`，永远凑不齐两侧，得到 `None`，正确是 `5`。
- 这个「提前返回」依赖「`p`、`q` 一定都在树里」：如果其中一个可能不存在（LC 1644），遇到一个就返回会把「另一个不存在」误判成 LCA，需要再数一遍两者都出现。
- 链状树深度 `10^5`，远超 CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要调高上限或用上面的父指针迭代版。

**同模式。** LC 235 二叉搜索树的最近公共祖先、LC 1676 二叉树的最近公共祖先 IV、LC 1644 二叉树的最近公共祖先 II、LC 1123 最深叶节点的最近公共祖先。
