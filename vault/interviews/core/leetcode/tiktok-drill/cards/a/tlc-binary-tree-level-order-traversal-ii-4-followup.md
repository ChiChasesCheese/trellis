---
id: tlc-binary-tree-level-order-traversal-ii-4-followup
node: a.binary-tree-level-order-traversal-ii
type: qa
step: 4
---
## Q
**LC 107 二叉树的层序遍历 II**｜追问

面试官接着问：（1）能不能不做最后的反转？（2）想用 DFS 做，要注意什么？（3）改成之字形层序（LC 103）或右视图（LC 199）？

## A
1. **不反转**：用 `deque`，每收集一层就 `appendleft`，最后转成列表：

```python
from collections import deque


def level_order_bottom_deque(root: TreeNode | None) -> list[list[int]]:
    ans: deque[list[int]] = deque()
    level = [root] if root else []
    while level:
        ans.appendleft([node.val for node in level])      # 新的一层插到最前面，省掉最后的反转
        level = [child for node in level for child in (node.left, node.right) if child]
    return list(ans)
```
   运行：`[3,9,20,null,null,15,7]` → `[[15, 7], [9, 20], [3]]`。两种写法都是 `O(n)`，反转只涉及层数，差别可以忽略。
2. **DFS**：递归时带 `depth`，`depth == len(levels)` 时新开一层，把值追加到 `levels[depth]`，最后 `levels[::-1]`。先左后右的前序遍历保证层内从左到右。注意递归深度可达 `2000`，超过默认上限，需要 `sys.setrecursionlimit` 或改成显式栈。
3. **之字形（LC 103）**：同样 BFS，给每层一个下标，奇数层把值列表反转：`vals[::-1] if depth % 2 else vals`。**右视图（LC 199）**：每层只取最后一个结点的值，`level[-1].val`。

**Python 提醒**：嵌套列表推导式 `[c for n in level for c in (n.left, n.right) if c]` 的 `for` 子句顺序与等价的两层循环完全相同；而条件 `if c` 判断的是结点对象的真值，自定义类默认为真、`None` 为假，所以能直接过滤空孩子。
