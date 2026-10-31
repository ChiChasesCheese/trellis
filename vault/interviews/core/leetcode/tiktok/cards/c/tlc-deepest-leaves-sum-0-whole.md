---
id: tlc-deepest-leaves-sum-0-whole
node: c.deepest-leaves-sum
type: qa
---
## Q
**LC 1302 层数最深叶子节点的和**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 2 次 · 最近 2021-09-09（国内 CodeTop）

给你一棵二叉树的根节点 `root`，返回层数最深的叶子节点的和。树中节点数目在 `[1, 10^4]`，`1 <= Node.val <= 100`。例：`root = [1,2,3,4,5,null,6,7,null,null,null,null,8]` → `15`（最深一层的叶子是 7 和 8）；`root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]` → `19`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前序遍历（DFS）带着深度，遇到更深的层就把累加和清零重来，遇到同一深度就累加，遍历结束时就是最深一层的和，`O(n)`。

**识别。** 「最深一层」类问题有两种标准解：按层遍历（BFS）取最后一层，或 DFS 带深度。最深一层的节点一定是叶子（再有孩子就更深了），所以不用判断「是不是叶子」。

**推导。** 先求树高再第二次遍历累加，要走两遍。洞察：一遍 DFS 里维护 `(最大深度, 该深度的和)`，访问到深度 `d`：`d` 更大则重置为 `(d, val)`，相等则累加，更小则忽略。

```python
def deepest_leaves_sum(root: TreeNode | None) -> int:
    best_depth = -1                              # 目前见过的最大深度
    total = 0                                    # 该深度所有节点的和

    def dfs(node: TreeNode | None, depth: int) -> None:
        nonlocal best_depth, total
        if node is None:
            return
        if depth > best_depth:                   # 发现更深的一层：之前的和作废
            best_depth, total = depth, node.val
        elif depth == best_depth:                # 同一层：累加
            total += node.val
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total
```

运行：`[1,2,3,4,5,null,6,7,null,null,null,null,8]` → `15`，`[6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]` → `19`；`[5]` → `5`；`10^4` 个节点的左链在默认递归上限下抛 `RecursionError`，上限调到 `20000` 后输出 `1`（每个节点值为 1 时）。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈，`h` 为树高，链状时 `h = n`）。

**拓展优化。**
- 逐层 BFS，没有递归深度问题：下一层为空时，当前层的和就是答案。

```python
def deepest_leaves_sum_bfs(root: TreeNode | None) -> int:
    level = [root]
    while True:
        nxt = [c for node in level for c in (node.left, node.right) if c]
        if not nxt:                              # 没有下一层：当前层就是最深一层
            return sum(node.val for node in level)
        level = nxt
```

- 递归深度超限又想保留 DFS 时改成显式栈，逻辑完全相同。

```python
def deepest_leaves_sum_stack(root: TreeNode | None) -> int:
    best_depth, total = -1, 0
    stack = [(root, 0)]                          # (节点, 深度)
    while stack:
        node, depth = stack.pop()
        if depth > best_depth:
            best_depth, total = depth, node.val
        elif depth == best_depth:
            total += node.val
        for child in (node.left, node.right):
            if child:
                stack.append((child, depth + 1))
    return total
```

**易错点。**
- 更深时只把 `best_depth` 更新而忘了把 `total` 重置为当前值：会把浅层的和带进答案。
- 最坏深度：10^4 个节点的链状树深度 10^4，CPython 默认递归上限约 1000，会抛 `RecursionError`，要 `sys.setrecursionlimit` 调高或改用显式栈（BFS 没有这个问题）。
- 误以为要判断叶子：最深一层的节点一定是叶子，多加判断只会增加出错的位置。

**追问。**
- 最深叶子的最近公共祖先（LC 865）：后序返回 `(深度, 节点)`，左右深度相同则当前节点是答案。
- 求树的最大深度（LC 104）：同一个遍历，只保留深度。

**同模式。** LC 104 二叉树的最大深度、LC 102 二叉树的层序遍历、LC 513 找树左下角的值、LC 865 具有所有最深节点的最小子树、LC 515 在每个树行中找最大值。
