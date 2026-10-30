---
id: tlc-find-distance-in-a-binary-tree-0-whole
node: p4.find-distance-in-a-binary-tree
type: qa
---
## Q
**LC 1740 找到二叉树中的距离**｜Medium · 近一年被问：美国 0 次、国内 1 次 · 最近 2026-09-18（国内面试记录）

给二叉树的根节点 `root` 和两个整数 `p`、`q`，返回树中值为 `p` 的结点与值为 `q` 的结点之间的**距离**，即路径上边的数目。结点个数在 `[1, 10^4]`，`0 <= Node.val <= 10^9`，所有结点的值唯一，`p` 和 `q` 都是树中结点的值。例：`root = [3,5,1,6,2,0,8,null,null,7,4]`：`p=5, q=0` → `3`（5-3-1-0）；`p=5, q=7` → `2`（5-2-7）；`p=5, q=5` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树中两点的路径一定经过它们的最近公共祖先（LCA，lowest common ancestor），所以 `距离 = LCA 到 p 的边数 + LCA 到 q 的边数`。先用 LC 236 的递归找到 LCA，再各写一个递归「从 LCA 往下找某个值，返回边数」，两段相加。`O(n)`。

**识别。** 「树上两点的路径长度」→ 路径 = 上行到 LCA + 下行到另一点；树没有指向父结点的指针，递归自然地从下往上汇报，不需要父指针。`lca` 的递归形状是固定套路：空或命中 `p` / `q` 就返回自己，两边各返回一个就是 LCA，否则返回非空的那边。

**推导。** 暴力：分别求根到 `p`、根到 `q` 的路径，去掉公共前缀，剩余长度之和就是答案，`O(n)`，但要存两条路径。等价地把树转成无向图再 BFS，也是 `O(n)` 但空间更大。浪费在存整条路径：只需要 LCA 的位置 → LC 236 的递归一次找到 LCA → 从 LCA 起各做一次「往下找值并计数」，两个数相加。三次遍历，每次最多 `n` 个结点，仍是 `O(n)`。

```python
def find_distance(root: TreeNode | None, p: int, q: int) -> int:
    def lca(node: TreeNode | None) -> TreeNode | None:
        if node is None or node.val in (p, q):
            return node                        # 空，或者碰到 p / q 本身：向上报告
        left, right = lca(node.left), lca(node.right)
        return node if left and right else left or right   # 两边各有一个：自己就是 LCA

    def down(node: TreeNode, target: int) -> int:
        if node.val == target:
            return 0
        for child in (node.left, node.right):
            if child and (d := down(child, target)) >= 0:
                return d + 1                   # 在这个孩子的子树里找到了
        return -1                              # 这棵子树里没有 target

    top = lca(root)                            # p、q 的最近公共祖先
    return down(top, p) + down(top, q)         # 路径 = LCA 到 p + LCA 到 q
```

运行：示例 `p=5, q=0` → `3`，`p=5, q=7` → `2`，`p=5, q=5` → `0`，`p=6, q=2` → `2`；单结点树 `p=q=7` → `0`；`10^4` 个结点的左链（值 `0` 到 `9999`，调高递归上限后）`p=0, q=9999` → `9999`，`p=5000, q=9999` → `4999`；默认递归上限下同一棵链抛 `RecursionError`。

**复杂度。** 时间 `O(n)`：`lca` 一次，两次 `down` 各最多访问 `n` 个结点；空间 `O(h)`，是递归栈，链状树上为 `O(n)`。

**易错点。**
- 只加深度、不扣 LCA：示例树里 `p=6, q=2` 都在第 2 层，`depth[p] + depth[q] = 4`，正确答案是 `2`（6-5-2），要用从 LCA 往下的边数，不是从根起的深度。
- `lca` 命中 `p` 就立刻返回、不再往下找：这是对的，因为 `q` 若在它下面，它自己就是 LCA；`p == q` 时同样返回该结点，`down` 得到 `0 + 0`，不要为这种情况另写分支。
- `down` 在找不到时必须返回 `-1`，不能返回 `0`，否则会把「没找到」当成「就是这个结点」，走错子树。
- 递归深度：树可能退化成 `10^4` 层的链，CPython 默认递归上限约 `1000`，`lca` 和 `down` 都会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成迭代（见追问）。

**追问。**
- 树很深、递归会超限：迭代遍历一次记下每个结点的父结点和深度，再让较深的结点往上爬、直到两者相遇，爬的步数就是距离，`O(n)` 时间、三个字典 `O(n)` 空间。

```python
def find_distance_iter(root: TreeNode | None, p: int, q: int) -> int:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    depth: dict[TreeNode, int] = {root: 0}
    by_val: dict[int, TreeNode] = {}
    stack = [root]
    while stack:                       # 迭代遍历：树可能退化成 10^4 层的链，递归会爆栈
        node = stack.pop()
        by_val[node.val] = node
        for child in (node.left, node.right):
            if child:
                parent[child], depth[child] = node, depth[node] + 1
                stack.append(child)
    a, b = by_val[p], by_val[q]
    dist = 0
    while a is not b:                  # 总是让更深的那个往上爬一步，直到在 LCA 相遇
        if depth[a] < depth[b]:
            a, b = b, a
        a = parent[a]
        dist += 1
    return dist
```

- 返回路径本身：爬升时把经过的结点分别存入两个列表，再把右侧反转拼接。
- 同一棵树上查询很多对 `(p, q)`：预处理倍增表（binary lifting），每次查询 `O(log n)`；或离线用 Tarjan LCA。
- `p`、`q` 不保证在树中：先判断是否在 `by_val` 中，不存在时返回 `-1`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 863 二叉树中所有距离为 K 的结点、LC 2096 从二叉树一个结点到另一个结点的每步方向。
