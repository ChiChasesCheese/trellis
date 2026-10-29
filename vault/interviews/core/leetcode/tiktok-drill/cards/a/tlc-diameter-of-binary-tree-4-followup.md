---
id: tlc-diameter-of-binary-tree-4-followup
node: a.diameter-of-binary-tree
type: qa
step: 4
---
## Q
**LC 543 二叉树的直径**｜追问

面试官接着问：（1）写个递归版本？（2）递归版本在什么情况下会出问题？（3）改成求最大路径和（LC 124），结构怎么变？

## A
1. **递归版。** 嵌套函数返回高度，`nonlocal` 更新答案：

```python
def diameter_recursive(root: TreeNode | None) -> int:
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)                  # 经过 node 的最长路径的边数
        return 1 + max(l, r)

    height(root)
    return best
```

2. **深链。** `10^4` 层的左斜链会抛 `RecursionError`（默认递归上限 1000）。可以 `sys.setrecursionlimit(20000)`，但每层 Python 帧较大，更深的树可能直接崩溃；稳妥做法是改成迭代后序。
3. **最大路径和（LC 124）。** 同样自底向上：函数返回"从该节点向下、只走一侧能得到的最大和"，即 `node.val + max(0, 左返回值, 右返回值)`；经过该节点的候选答案是 `node.val + max(0, 左) + max(0, 右)`。把"高度"换成"带符号的收益"，其余结构不变。

**Python 提醒**：嵌套函数里要修改外层的整数变量，必须声明 `nonlocal`，否则 `best = …` 会创建新的局部变量，外层的 `best` 始终是 `0`；用列表 `best = [0]` 绕过也可以，但 `nonlocal` 更直接。
