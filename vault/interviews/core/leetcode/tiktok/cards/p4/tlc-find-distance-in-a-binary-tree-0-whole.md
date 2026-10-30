---
id: tlc-find-distance-in-a-binary-tree-0-whole
node: p4.find-distance-in-a-binary-tree
type: qa
---
## Q
**LC 1740 找到二叉树中的距离**｜Medium · 近一年被问：美国 0 次、国内 1 次 · 最近 2026-09-18（面试记录）

给二叉树的根节点 `root` 和两个整数 `p`、`q`，返回树中值为 `p` 的结点与值为 `q` 的结点之间的**距离**，即路径上边的数目。结点个数在 `[1, 10^4]`，`0 <= Node.val <= 10^9`，所有结点的值唯一，`p` 和 `q` 都是树中结点的值。例：`root = [3,5,1,6,2,0,8,null,null,7,4]`：`p=5, q=0` → `3`（5-3-1-0）；`p=5, q=7` → `2`（5-2-7）；`p=5, q=5` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树中两点的路径一定经过它们的最近公共祖先（LCA，lowest common ancestor），所以 `距离 = depth[p] + depth[q] - 2*depth[LCA]`。迭代遍历一遍记下每个结点的父结点和深度，再让较深的结点往上爬、直到两者相遇，爬的步数就是距离。`O(n)`。

**识别。** 「树上两点的路径长度」→ 路径 = 上行到 LCA + 下行到另一点；树没有指向父结点的指针，所以先补出父指针（或把树当无向图）。`n = 10^4` 且树可能退化成一条 `10^4` 层的链，Python 递归默认深度约 1000，必须用迭代遍历。

**推导。** 暴力：分别求根到 `p`、根到 `q` 的路径，去掉公共前缀，剩余长度之和就是答案，`O(n)`，但要存两条路径。等价地把树转成无向图再 BFS，也是 `O(n)` 但空间更大。浪费在存整条路径：只需要深度和父指针。记 `parent` 和 `depth` 后，两个指针按「深度大的先爬一步」的规则同步上行，必然在 LCA 相遇，期间每爬一步距离加 1。

```python
def find_distance(root: TreeNode | None, p: int, q: int) -> int:
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

运行：示例 `p=5, q=0` → `3`，`p=5, q=7` → `2`，`p=5, q=5` → `0`；单结点树 `p=q=7` → `0`；`10^4` 个结点的左链上 `p=0, q=9999` → `9999`，`p=5000, q=9999` → `4999`。

**复杂度。** 时间 `O(n)`：遍历一次，爬升最多 `O(n)` 步；空间 `O(n)`：`parent`、`depth`、`by_val` 三个字典。

**易错点。**
- 用递归求 LCA：单边链 `10^4` 层会 `RecursionError`；要么迭代，要么调高递归上限并说明理由。
- `p == q` 时 `a is b` 立刻成立，返回 `0`；不要对这种情况硬走 LCA 的「两边都找到」分支。
- 把「深度相同」当成「相遇」：同一层的两个不同结点还没到 LCA。示例树里 `p=6, q=2` 都在第 2 层，只比深度会得到 `0`，正确答案是 `2`（6-5-2）；循环条件必须是 `a is not b`。

**追问。**
- 返回路径本身：爬升时把经过的结点分别存入两个列表，再把右侧反转拼接。
- 同一棵树上查询很多对 `(p, q)`：预处理倍增表（binary lifting），每次查询 `O(log n)`；或离线用 Tarjan LCA。
- 只给根、没有 `p`、`q` 的值保证存在：先判断是否在 `by_val` 中，不存在时返回 `-1`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 863 二叉树中所有距离为 K 的结点、LC 2096 从二叉树一个结点到另一个结点的每步方向。
