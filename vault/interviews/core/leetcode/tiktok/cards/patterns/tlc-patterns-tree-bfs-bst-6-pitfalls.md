---
id: tlc-patterns-tree-bfs-bst-6-pitfalls
node: patterns.tree-bfs-bst
type: qa
step: 6
---
## Q
**二叉树 BFS 与 BST 性质｜常见陷阱**

BFS 与 BST 题最容易在哪里出错？

## A
1. **空树**：`root is None` 时直接返回空结果；`deque([root])` 会放进一个 `None`，第一次弹出就报 `AttributeError`。
2. **按层处理没有固定 `len(q)`**：在 `for` 里边弹边加，`range(len(q))` 必须在循环前求值；写成 `while q:` 嵌套会把不同层混在一起。
3. **用 `list.pop(0)`** 做队列：`O(n)`；用 `deque.popleft()`。
4. **验证 BST 只比较父子**：`[5,1,6,null,null,3,7]` 误判为 `True`。
5. **BST 允许相等吗**：LC 98 要严格不等（`[2,2,2]` 为 `False`）；先问清楚。
6. **初始上下界用 `INT_MIN / INT_MAX`**：节点值恰好是边界时出错；用 `float("-inf")` / `float("inf")`。
7. **序列化漏掉空节点**：`[1,2]` 与 `[1,null,2]` 无法区分。
8. **反序列化顺序与序列化不一致**：前序序列化必须前序还原，先左后右。
9. **BST 删除两个孩子的情况**：替换后要在右子树里**再删除后继**，否则出现重复值。
10. **最大宽度的编号**：空位也要占编号（`2*i`、`2*i+1`），不是只给非空节点连续编号；不减 `base` 在 Python 里不会溢出，但会让数字变得很大。
11. **父指针图里的回头路**：LC 863 的 BFS 要用 `seen` 集合，否则会从子节点走回父节点再走回子节点。
12. **层序遍历用递归**：需要传 `depth`，并保证 `res[depth]` 存在；迭代更直观。
