---
id: tlc-lowest-common-ancestor-of-a-binary-search-tree-0-whole
node: b.lowest-common-ancestor-of-a-binary-search-tree
type: qa
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Easy · CodeTop 国内累计 7 次 · 最近 2026-03-19（CodeTop）

给一棵二叉搜索树（BST）的根结点 `root` 和其中两个不同的结点 `p`、`q`，返回它们的最近公共祖先（LCA）：既是 `p` 的祖先又是 `q` 的祖先、且深度尽可能大的结点。**一个结点也可以是它自己的祖先**。所有结点的值都唯一；`p`、`q` 是不同的结点，且都在这棵树里。例：`root = [6,2,8,0,4,7,9,null,null,3,5]`，`p = 2, q = 8` → `6`；`p = 2, q = 4` → `2`（`2` 是 `4` 的祖先，也是它自己的祖先）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 从根往下走：当前结点的值比 `p`、`q` 都小就走右子树，比两者都大就走左子树，否则当前结点就是答案（两者分居左右，或当前结点本身是其一）。`O(h)` 时间、`O(1)` 空间，`h` 是树高。

**识别。** BST 的有序性（左子树 < 根 < 右子树）让每一步都能整棵子树地排除一边。LCA 就是**第一个值落在闭区间 `[min(p, q), max(p, q)]` 里的结点**。普通二叉树的 LCA（LC 236）要遍历整棵树，BST 版不需要。

**推导。** 暴力：分别记下根到 `p`、根到 `q` 的路径，取最后一个相同的结点，`O(h)` 时间和空间；或者忽略 BST 性质，用 LC 236 的后序遍历，`O(n)`。浪费：BST 已经告诉我们 `p`、`q` 在哪一侧，没必要搜索它们。洞察：在结点 `x`，若 `p`、`q` 都小于 `x.val`，二者都在左子树，LCA 必在左子树里；都大于则在右子树；否则二者被 `x` 分开，或 `x` 就是其中之一，此时 `x` 的任何孩子都不是共同祖先，所以 `x` 就是答案。写成循环，不需要递归栈。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    lo, hi = min(p.val, q.val), max(p.val, q.val)    # 不假设 p 比 q 小
    node = root
    while node:
        if node.val < lo:              # 两个目标都在右子树
            node = node.right
        elif node.val > hi:            # 两个目标都在左子树
            node = node.left
        else:                          # lo <= node.val <= hi：两路在此分叉（或 node 本身就是其一）
            return node
    return None
```

运行（`root = [6,2,8,0,4,7,9,null,null,3,5]`，返回结点的值）：`p = 2, q = 8` → `6`，`p = 2, q = 4` → `2`，`p = 8, q = 2` → `6`，`p = 3, q = 5` → `4`，`p = 6, q = 0` → `6`。

**复杂度。** 时间 `O(h)`，平衡时 `O(log n)`，链状时 `O(n)`；空间 `O(1)`。

**易错点。**
- 区间必须是**闭**的：`p = 2, q = 4` 时答案是 `2`，它的值等于 `lo`。写成严格的 `p.val < node.val < q.val`，会越过 `2`，最后返回 `None`（正确 `2`）。
- 别假设 `p.val < q.val`：`p = 8, q = 2` 时严格写法同样返回 `None`。先取 `min` 和 `max`，或两边都判断。
- 结点值唯一，所以直接比较 `val`；允许重复值时，BST 的左右划分不再确定，这个解法失效。

**追问。**
- 普通二叉树（LC 236）：后序递归，左右都找到目标就返回当前结点，否则返回非空的一边，`O(n)`。
- `p`、`q` 不一定在树里（LC 1644）：先在 BST 里各自二分验证存在，再求 LCA。
- 很多次查询：BST 版每次 `O(h)` 已经够快；普通树用倍增（binary lifting）预处理 `O(n log n)`，每次查询 `O(log n)`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 701 二叉搜索树中的插入操作、LC 700 二叉搜索树中的搜索、LC 1123 最深叶节点的最近公共祖先。
