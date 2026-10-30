---
id: tlc-minimum-depth-of-binary-tree-0-whole
node: b.minimum-depth-of-binary-tree
type: qa
---
## Q
**LC 111 二叉树的最小深度**｜Easy · CodeTop 国内累计 8 次 · 最近 2025-12-02（国内 CodeTop）

给二叉树的根 `root`，求它的最小深度：从根节点到**最近的叶子节点**的最短路径上的节点数。叶子节点是没有子节点的节点。树中节点数在 `[0, 10^5]` 内，`-1000 <= Node.val <= 1000`。例：`[3,9,20,null,null,15,7]` → `2`（`3 → 9`）；`[2,null,3,null,4,null,5,null,6]` → `5`（一条向右的链，唯一的叶子是 `6`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** BFS 按层往下走，遇到的**第一个叶子**所在的层数就是答案，可以立刻返回；比 DFS 少访问大量节点，也没有递归深度问题。

**识别。** 「最小深度」=「离根最近的叶子」= 无权图上的**最短路** → BFS 的信号：按层推进，先到的就是最近的。节点数到 `10^5`，退化成链时递归深度也是 `10^5`，Python 默认递归上限约 `1000`，所以优先迭代写法。

**推导。** DFS 要遍历所有根到叶的路径取最小，`O(n)` 且必须走完整棵树。浪费在于：最浅的叶子可能就在第 2 层，DFS 却还要钻到最深处。BFS 一层层扩展，第一次碰到叶子时，所有更浅的层都已检查完，这个深度就是最小值，直接返回；最坏（最浅叶子在最底层）仍是 `O(n)`，但通常提前结束。

```python
from collections import deque


def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue = deque([(root, 1)])                    # (节点, 它的深度)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                          # BFS 按层推进：第一个叶子就是最浅的
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0
```

运行：`[3,9,20,null,null,15,7]` → `2`，`[2,null,3,null,4,null,5,null,6]` → `5`，`[]` → `0`，`[1]` → `1`，`[1,2]` → `2`，`10^5` 个节点的链 → `100000`。

**复杂度。** 时间 `O(n)`，遇到第一个叶子即停；空间 `O(w)`，`w` 是树的最大宽度（队列里至多两层）。

**易错点。**
- 照搬最大深度写 `1 + min(左深度, 右深度)`：只有一个孩子的节点，空孩子返回 `0`，被 `min` 选中，可空孩子那边**没有叶子**。`[1,2]` 会错成 `1`（正确 `2`），样例 2 的链会错成 `1`（正确 `5`）。
- 递归 DFS 在 `10^5` 个节点的链上触发 `RecursionError`；BFS 或显式栈没有这个问题。
- 空树返回 `0`，要在入队前处理。

**追问。**
- 返回到最近叶子的路径：BFS 时记 `parent[child] = node`，找到叶子后沿 `parent` 回溯再反转；样例 1 → `[3, 9]`。
- 递归写法：只有一个孩子时只递归那一侧，`if not root.left: return 1 + f(root.right)`，两个孩子都在才取 `min`。
- 最大深度（LC 104）没有这个陷阱：空孩子的 `0` 不会被 `max` 选中。

**同模式。** LC 104 二叉树的最大深度、LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 752 打开转盘锁。
