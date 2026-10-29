---
id: tlc-find-largest-value-in-each-tree-row-4-followup
node: a.find-largest-value-in-each-tree-row
type: qa
step: 4
---
## Q
**LC 515 在每个树行中找最大值**｜追问

面试官接着问：（1）用 DFS 写，并且不能递归（树可能是一条 `10^4` 的链）？（2）改成返回每层的**右视图**或**平均值**，代码改哪一行？（3）DFS 和 BFS 哪个内存更省？

## A
1. **迭代 DFS**：栈里放 `(节点, 深度)`。`depth == len(ans)` 说明第一次到达这一层，追加；否则更新 `ans[depth]`。

```python
def largest_values_dfs(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    stack = [(root, 0)] if root else []
    while stack:
        node, depth = stack.pop()
        if depth == len(ans):                     # 第一次到达这一层
            ans.append(node.val)
        else:
            ans[depth] = max(ans[depth], node.val)
        for child in (node.right, node.left):     # 先压右再压左，先处理左子树
            if child:
                stack.append((child, depth + 1))
    return ans
```

运行：`[1,3,2,5,3,null,9]` → `[1, 3, 9]`，`10^4` 个节点的链 → 长度 `10000` 的列表。正确性依赖「DFS 到达深度 `d` 之前一定已经到达过 `0..d-1`」，所以 `depth` 最多比 `len(ans)` 大 0。
2. **换统计量**：只改 `ans.append(...)` 那一行。右视图（LC 199）：`level[-1].val`；平均值（LC 637）：`sum(n.val for n in level) / len(level)`；锯齿形（LC 103）：奇数层把值列表反转。
3. **内存**：BFS 同时保存一层，宽度 `w` 在完全二叉树里约 `n/2`；DFS 的栈约为「树高 × 每层压入的兄弟数」，平衡树是 `O(log n)`。宽而浅的树 DFS 省，窄而深的树 BFS 省。

**Python 提醒**：`max()` 作用在空序列上抛 `ValueError`；需要时用 `max(iterable, default=...)`。
