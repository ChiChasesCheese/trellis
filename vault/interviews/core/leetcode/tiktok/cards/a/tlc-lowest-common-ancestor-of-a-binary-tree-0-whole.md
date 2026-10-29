---
id: tlc-lowest-common-ancestor-of-a-binary-tree-0-whole
node: a.lowest-common-ancestor-of-a-binary-tree
type: qa
---
## Q
**LC 236 二叉树的最近公共祖先**｜Medium · LC TikTok 热度 53/100 · 近一年被问：美国 2 次、国内 5 次 · CodeTop 国内累计 134 次 · 最近 2026-10-19（面试记录）

给一棵二叉树和其中两个节点 `p`、`q`，找出它们的**最近公共祖先**（LCA）：既是 `p` 的祖先又是 `q` 的祖先、且深度尽可能大的节点；一个节点也可以是它自己的祖先。树中节点数在 `[2, 10^5]` 内，`-10^9 <= Node.val <= 10^9`，所有节点值互不相同，`p != q`，`p` 和 `q` 都在树中。例：`root = [3,5,1,6,2,0,8,null,null,7,4]`，`p = 5, q = 1` → `3`；`p = 5, q = 4` → `5`；`root = [1,2], p = 1, q = 2` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先用一次迭代 DFS 给每个节点记下父节点；把 `p` 自己和它的全部祖先放进集合，再让 `q` 沿父指针往上爬，第一个落进集合的节点就是最近公共祖先。`O(n)`。

**识别。** 「最近公共祖先」且题目没说二叉搜索树，就不能用值的大小来导航（那是 LC 235）。一般二叉树有两条路：自底向上的递归（后序）返回「子树里找到了谁」，或者建好父指针后把问题变成「两条向上的链在哪里汇合」，后者和相交链表（LC 160）完全同构。`n` 到 `10^5`，单链树深度可达 `10^5`，Python 递归会触发 `RecursionError`，所以主解法用显式栈。

**推导。** 暴力：分别求出根到 `p`、根到 `q` 的路径，取最长公共前缀的最后一个节点 → `O(n)` 时间，但要写路径回溯，且路径要完整保存。洞察：祖先关系只需要「向上走」，向上走只需要父指针；两个节点的祖先链都在根处汇合，第一个公共点就是最近公共祖先。给每个节点记下父节点后，`p` 的链放进集合，`q` 向上爬，命中集合即停。建父指针时，`p`、`q` 的父指针都登记完就可以提前停止遍历。

```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while p not in parent or q not in parent:      # p、q 的父指针都登记好就停
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    ancestors: set[TreeNode] = set()
    node: TreeNode | None = p
    while node:                                    # p 自己和它的全部祖先
        ancestors.add(node)
        node = parent[node]
    node = q
    while node not in ancestors:                   # q 往上爬，第一个撞上的就是答案
        node = parent[node]
    return node
```

运行：`p = 5, q = 1` → `3`，`p = 5, q = 4` → `5`，`[1,2]` 中 `p = 1, q = 2` → `1`；`10^5` 个节点的单链树，取最深的两个节点 → 较浅的那个，没有 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（父指针表、栈、祖先集合）。

**易错点。**
- 祖先集合必须从 `p` **自己**开始：一个节点也是自己的祖先。从 `p` 的父节点开始，示例二 `p = 5, q = 4` 会返回 `3`，正确答案是 `5`。
- 遍历的循环条件是 `p not in parent or q not in parent`（有一个没登记就继续）。写成 `and`，只登记了一个就停，后面查另一个会 `KeyError`。
- `p`、`q` 是树里的节点对象，不是数值：字典和集合的键用节点本身（按身份比较）。把 `p` 当数值去和别的节点值比大小，是把题目误当成二叉搜索树。

**追问。**
- 递归后序写法：`if root is None or root is p or root is q: return root`；左右各递归一次，两边都找到就返回 `root`，否则返回非空的一边。代码最短，但深度等于树高，单链树会 `RecursionError`。
- 同一棵树要回答很多对查询：预处理深度和倍增表（binary lifting）`up[k][v]`，每次查询 `O(log n)`。
- `p`、`q` 不保证在树中（LC 1644）：要额外确认两个都被找到。

**同模式。** LC 235 二叉搜索树的最近公共祖先、LC 160 相交链表、LC 1650 含父指针的最近公共祖先、LC 1644 最近公共祖先 II、LC 1123 最深叶节点的最近公共祖先。
