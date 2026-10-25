---
id: tlc-check-completeness-of-a-binary-tree-4-followup
node: b.check-completeness-of-a-binary-tree
type: qa
step: 4
---
## Q
**LC 958 二叉树的完全性检验**｜追问

面试官接着问：（1）不用 BFS，能不能用深度优先（DFS）判断？（2）如果这棵树是完全二叉树，怎样在低于 `O(n)` 的时间数出节点数（LC 222）？（3）树很高、很窄时，BFS 和 DFS 的内存各是多少？

## A
1. **堆式编号 + DFS**：根编号 `1`，左孩子 `2i`，右孩子 `2i+1`。完全二叉树当且仅当「节点数 == 最大编号」。用显式栈避免递归深度问题。

```python
def is_complete_by_index(root: TreeNode | None) -> bool:
    count = last = 0
    stack = [(root, 1)]                        # 堆式编号：左孩子 2i，右孩子 2i+1
    while stack:
        node, i = stack.pop()
        if node is None:
            continue
        count += 1
        last = max(last, i)
        stack.append((node.left, 2 * i))
        stack.append((node.right, 2 * i + 1))
    return count == last                       # 编号 1..count 恰好各用一次
```

`[1,2,3,4,5,6]` → `True`，深度 100 的单链 → `False`。

2. **完全二叉树的节点数**：沿最左路径和最右路径量高度；两者相等说明是满树，节点数 `2^h - 1`；否则递归左右子树。每层最多有一侧要继续展开，总共 `O(log^2 n)`。
3. **内存**：BFS 的队列最多装一层，完全二叉树最宽的一层有 `~n/2` 个节点；DFS 的栈只装一条路径，平衡时 `O(log n)`，退化成链时 `O(n)`。

**Python 提醒**：堆式编号在 Python 里不会溢出（整数无限精度），在 Java / C++ 里深度超过 31 层的链会让编号溢出 `int`，要改用 `long` 或者只用 BFS 的空位法。
