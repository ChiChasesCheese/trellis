---
id: tlc-patterns-tree-bfs-bst-3-why-bst
node: patterns.tree-bfs-bst
type: qa
step: 3
---
## Q
**二叉树 BFS 与 BST 性质｜正确性：验证 BST 为什么不能只比较父子**

验证二叉搜索树（LC 98）时，只检查「左孩子 < 根 < 右孩子」会错在哪里？正确的不变量是什么？

## A
BST 的定义是：**整棵左子树**的所有值都小于根，**整棵右子树**的所有值都大于根；不是只有直接孩子。

**不变量**：递归到节点 `node` 时，它必须落在一个开区间 `(lo, hi)` 内；进入左孩子时上界收窄为 `node.val`，进入右孩子时下界收窄为 `node.val`。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    def ok(node: TreeNode | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        if not lo < node.val < hi:         # 严格不等：BST 里不允许相等的值
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))
```

**反例**：树 `[5,1,6,null,null,3,7]`——根 `5`，右孩子 `6`，`6` 的左孩子 `3`。
- 只比较父子：`1 < 5 < 6`、`3 < 6 < 7` 都成立，返回 `True`。
- 实际上 `3` 在根 `5` 的右子树里，却小于 `5`，违反 BST，正确答案是 `False`。
- 区间写法：`3` 处于 `(5, 6)` 内？不在，返回 `False`。

运行：`[2,1,3]` → `True`；`[5,1,4,null,null,3,6]` → `False`；`[2,2,2]` → `False`（不允许相等）；`[-2147483648]` → `True`（用 `-inf` 而不是 `INT_MIN` 做初始下界）。

等价做法：中序遍历，检查前一个值始终**严格小于**当前值。时间 `O(n)`，空间 `O(h)`。
