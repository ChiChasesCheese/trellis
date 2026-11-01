---
id: tlc-tops-maximum-depth-of-binary-tree-0-whole
node: trees.maximum-depth-of-binary-tree
type: qa
---
## Q
**LC 104 二叉树的最大深度**｜Easy · 全公司热度第 124 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150、LeetCode 75

给定一个二叉树的根节点 `root`，返回其最大深度。最大深度是从根节点到最远叶子节点的最长路径上的**节点数**。树中节点数在 `[0, 10^4]`，`-100 <= Node.val <= 100`。例：`root = [3,9,20,null,null,15,7]` → `3`；`root = [1,null,2]` → `2`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树递归（DFS，后序：先拿到子树的答案再合并自己）。

**一句话。** 一棵树的深度 = 1 + 左右子树深度的较大者，空树深度为 0。

**识别。** 树的问题先问「这个问题能不能由左右子树的答案合并出来」：深度、高度、是否平衡、直径都是这个形状。`n <= 10^4`，每个节点访问一次的 `O(n)` 足够。

**推导。** 层序遍历（BFS）数层数也对，但要队列；递归直接把定义翻译成代码：空树是 `0`，否则先问左子树多深、右子树多深，取大的再加上自己这一层。

```python
def max_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0                                   # 空树深度为 0：递归出口，也覆盖叶子的空孩子
    left = max_depth(root.left)                    # 后序：先得到左右子树的答案
    right = max_depth(root.right)
    return 1 + max(left, right)                    # 加上自己这一层；按节点数计，不是边数
```

运行：`[3,9,20,null,null,15,7]` → `3`；`[1,null,2]` → `2`；`[]` → `0`；`[5]` → `1`。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`，`h` 是递归栈深度，平衡树 `O(log n)`，链状 `O(n)`。

**拓展优化。**
- 不想递归：层序遍历，数层数。
```python
from collections import deque

def max_depth_bfs(root: TreeNode | None) -> int:
    if root is None:
        return 0
    depth, queue = 0, deque([root])
    while queue:
        depth += 1                                 # 每处理完一整层，深度加 1
        for _ in range(len(queue)):                # 只弹出当前层的节点
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
```

**易错点。**
- `1 + max(...)` 漏掉 `1`：每层都不加自己，永远返回 `0`，`[3,9,20,null,null,15,7]` 得 `0`，正确是 `3`。
- 单链树的递归深度：`10^4` 个节点的链，深度到 `10^4`，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit`，要么用上面的 BFS。
- BFS 里每弹出一个节点就 `depth += 1`，数到的是节点数而不是层数：`[3,9,20,null,null,15,7]` 得 `5`，正确是 `3`。要用 `for _ in range(len(queue))` 把一层切开。

**同模式。** LC 111 二叉树的最小深度（注意缺一侧孩子时不能取 `min`）、LC 110 平衡二叉树、LC 543 二叉树的直径、LC 226 翻转二叉树。
