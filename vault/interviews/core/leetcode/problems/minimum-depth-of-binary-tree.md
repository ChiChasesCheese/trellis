---
slug: minimum-depth-of-binary-tree
---
## Q
**LC 111 二叉树的最小深度**｜Easy

求根到最近叶子的路径上的节点数。

## A
**一句话。** BFS 按层走，遇到的第一个叶子所在层就是答案，立刻返回。

```python
def min_depth(root):
    if root is None:
        return 0
    queue = deque([(root, 1)])  # (节点, 深度)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth        # 第一个叶子最浅
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 照搬最大深度写 `1 + min(左, 右)`：只有一个孩子时空侧返回 `0` 被选中，`[1,2]` 得 `1`，应为 `2`。
- 递归 DFS 遇到 `10^5` 个节点的链会 `RecursionError`：BFS 没有这个问题。

**追问。**
- 递归写法怎么避开陷阱？：只有一个孩子时只递归那一侧，两个孩子都在才取 `min`。
- 为什么最大深度没有这个陷阱？：空侧的 `0` 不会被 `max` 选中。

**同模式。** LC 104 二叉树的最大深度、LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 752 打开转盘锁
