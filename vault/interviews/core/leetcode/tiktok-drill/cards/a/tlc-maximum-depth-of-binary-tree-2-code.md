---
id: tlc-maximum-depth-of-binary-tree-2-code
node: a.maximum-depth-of-binary-tree
type: qa
step: 2
---
## Q
**LC 104 二叉树的最大深度**｜写出 Python 实现

二叉树节点数在 `[0, 10^4]`，返回根到最远叶子的路径上的节点数（空树为 `0`）。要求不因树退化成链而栈溢出。

## A
**思路。** 逐层展开：`level` 存当前层所有节点，每轮深度加一，再用列表推导把这层所有非空孩子收成下一层；`level` 为空时停止。轮数就是深度，没有递归。

```python
def max_depth(root: TreeNode | None) -> int:
    depth = 0
    level = [root] if root else []
    while level:                                   # 每轮处理完整的一层
        depth += 1
        level = [child for node in level
                 for child in (node.left, node.right) if child]
    return depth
```

运行：`[3,9,20,null,null,15,7]` → `3`，`[1,null,2]` → `2`，空树 → `0`，`[0]` → `1`，`10^4` 个节点的单链 → `10000`。

**复杂度。** 时间 `O(n)`：每个节点恰好进入一次某一层；空间 `O(w)`，`w` 为最大层宽，最坏 `O(n)`。

**写法要点。** 用「列表一层一层换」代替 `deque` + 记层大小，少一个内层循环；嵌套推导 `for node in level for child in (...)` 先外后内，和两层 `for` 的顺序一致；`if child` 过滤空孩子；`[root] if root else []` 处理空树。递归版 `1 + max(f(left), f(right))` 更短，但在 `10^4` 的单链上会 `RecursionError`。
