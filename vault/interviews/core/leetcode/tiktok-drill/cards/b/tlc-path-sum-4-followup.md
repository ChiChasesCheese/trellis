---
id: tlc-path-sum-4-followup
node: b.path-sum
type: qa
step: 4
---
## Q
**LC 112 路径总和**｜追问

面试官接着问：（1）树退化成 `5000` 层的链，递归会怎样，怎么改成显式栈？（2）返回所有满足条件的路径（LC 113）？（3）路径可以从任意结点开始、到任意结点结束（LC 437）？

## A
1. **显式栈**：递归深度等于树高，`5000` 层的单链会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`；`sys.setrecursionlimit` 可以调高，但栈太深有让解释器崩溃的风险。改成栈，里面存 `(结点, 走到这里后还差多少)`：

```python
def has_path_sum_stack(root: TreeNode | None, target_sum: int) -> bool:
    if root is None:
        return False                   # 空树没有任何根到叶子的路径
    stack = [(root, target_sum - root.val)]   # (结点, 走到这里后还差多少)
    while stack:
        node, remain = stack.pop()
        if node.left is None and node.right is None and remain == 0:
            return True                # 必须是叶子，并且恰好凑够
        for child in (node.right, node.left):
            if child:
                stack.append((child, remain - child.val))
    return False
```

2. **所有路径**：DFS 时维护当前路径 `path`，进入结点 `path.append(val)`，叶子且 `remain == 0` 时 `ans.append(path[:])`（必须拷贝），离开结点时 `path.pop()` 回溯。显式栈版本需要把路径一并存进栈元素，或存父指针事后回溯。
3. **任意起点终点（LC 437）**：不再是「根到叶子」，用前缀和哈希表：记录根到当前结点链上的前缀和出现次数，查 `当前和 - target`；见那一题。

**Python 提醒**：`or` 的短路求值让递归版找到一条路径后不再探索另一侧；`any(...)` 搭配生成器也可以；不要写成 `rec(l) + rec(r) > 0`，布尔值相加会失去短路。另外调试时别用 `print(root)` 打印 `TreeNode` 对象（没有 `__repr__`），打印 `root.val`。
