---
id: tlc-make-costs-of-paths-equal-in-a-binary-tree-4-followup
node: p3.make-costs-of-paths-equal-in-a-binary-tree
type: qa
step: 4
---
## Q
**LC 2673 使二叉树所有路径值相等的最小代价**｜追问

满二叉树（堆式下标）上，每次把一个节点加 `1`，让根到所有叶子的路径值相等，已经用自底向上的差值累加求出最少次数。面试官接着问：（1）要输出具体给哪些节点加多少？（2）如果每个节点加一次的代价不同呢？（3）能不能省掉拷贝？（4）树不是用数组给，而是 `TreeNode`，怎么写？

## A
1. **输出方案**：在每个非叶子节点 `i`，较小的那个孩子编号 `child = 2 * i if left < right else 2 * i + 1` 加上 `abs(left - right)` 就是一次操作，记进列表，总共不超过 `n // 2` 条。
2. **代价不同**：补在较小一侧的根上仍然最省次数，但“省次数”不再等价于“省代价”；需要比较「补在根」和「补在其下更便宜的节点」，这时是真正的树形 DP，状态是子树内部的目标路径值，复杂度明显更高，面试里先说明题目没有这个条件。
3. **省空间**：直接在 `cost` 上累加，下标换成 `i - 1`、`2 * i - 1`、`2 * i`，额外空间 `O(1)`，代价是改动了输入；面试里要说明这一点。
4. **`TreeNode` 版**：后序遍历返回「子树的路径值」，同时用外层变量累加差值；深度只有 `log n`，递归安全。

```python
def min_increments_tree(root: TreeNode | None) -> int:
    ans = 0

    def dfs(node: TreeNode | None) -> int:
        nonlocal ans
        if node is None:
            return 0
        left, right = dfs(node.left), dfs(node.right)
        ans += abs(left - right)
        return node.val + max(left, right)

    dfs(root)
    return ans
```

**Python 提醒**：内层函数要修改外层的计数变量，必须写 `nonlocal ans`；不写的话 `ans += ...` 会把 `ans` 当成局部变量，直接 `UnboundLocalError`。
