---
id: tlc-core-maximum-depth-of-binary-tree
node: p4.maximum-depth-of-binary-tree
type: qa
---
## Q
**LC 104 二叉树的最大深度**｜Easy · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 29 次 · 最近 2026-09-13（国内 CodeTop） · 也在：LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给二叉树的根节点 `root`，返回它的最大深度：从根节点到最远叶子节点的最长路径上的**节点数**。节点数在 `[0, 10^4]`，`-100 <= Node.val <= 100`。例：`[3,9,20,null,null,15,7]` → `3`；`[1,null,2]` → `2`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归定义：`depth(node) = 1 + max(depth(左), depth(右))`，空树深度为 `0`。`O(n)`；也可以按层数轮数（见追问）。

**识别。** 「深度 / 高度 / 最长路径」是树上的自底向上汇总：一个节点的答案由两个孩子的答案合并而来。递归最直观；`n` 到 `10^4` 意味着退化成链的树深度可达 `10^4`，而 CPython 的默认递归上限约 `1000`，见易错点。

**推导。** 暴力思路是枚举所有根到叶路径取最长，`O(n)` 条路径、每条 `O(h)`，浪费在共享的前缀上 → 洞察：子树的深度彼此独立，根的深度只依赖两个子树的深度，递归 `1 + max(左, 右)` 每个节点算一次，递归深度等于树高。

```python
def max_depth(root: TreeNode | None) -> int:
    if root is None:                               # 空树深度为 0
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

运行：`[3,9,20,null,null,15,7]` → `3`，`[1,null,2]` → `2`，空树 → `0`，`[0]` → `1`，`10^4` 个节点的单链 → `10000`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`，递归栈深度等于树高 `h`，最坏 `O(n)`。

**易错点。**
- 空树的基准值是 `0`，不是 `1`。把 `None` 当成深度 `1`，示例 1 会算出 `4`，正确是 `3`。
- 深度按**节点数**算，不是边数；单个节点深度为 `1`。
- 递归深度：`10^4` 节点的单链，调用深度 `10^4`，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。

**追问。**
- 不想动递归上限：逐层展开，轮数就是深度：
```python
def max_depth_bfs(root: TreeNode | None) -> int:
    depth = 0
    level = [root] if root else []
    while level:                                   # 每轮处理完整的一层
        depth += 1
        level = [child for node in level
                 for child in (node.left, node.right) if child]
    return depth
```
- 最小深度（LC 111）：不能直接把 `max` 改成 `min`——只有一个孩子的节点，空的那一侧不算叶子。`[1,null,2]` 用 `min` 会得到 `1`，正确是 `2`。
- N 叉树的最大深度（LC 559）：同样按层，下一层是 `node.children` 的并集。
- 平衡二叉树（LC 110）：每个节点同时返回高度，高度差大于 `1` 就提前标记失败。

**同模式。** LC 111 最小深度、LC 110 平衡二叉树、LC 559 N 叉树的最大深度、LC 543 二叉树的直径、LC 102 层序遍历。
