---
id: tlc-diameter-of-binary-tree-4-followup
node: p4.diameter-of-binary-tree
type: qa
step: 4
---
## Q
**LC 543 二叉树的直径**｜追问

面试官接着问：（1）树是 `10^4` 层的链，递归会出问题，怎么写迭代版本？（2）递归版本为什么会出问题，能只靠调高递归上限吗？（3）改成求最大路径和（LC 124），结构怎么变？

## A
1. **迭代版（显式栈）。** 栈里放 `(节点, 是否已处理孩子)`：第一次弹出时把自己以「已访问」压回，再压孩子；第二次弹出时孩子的高度都已存进字典，计算自己的高度并更新答案：

```python
def diameter_stack(root: TreeNode | None) -> int:
    if root is None:
        return 0
    height: dict[TreeNode, int] = {}             # 结点 -> 以它为根的子树高度（按结点数）
    best = 0
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:                                 # 迭代后序：孩子都算完再算自己，避免深树时递归爆栈
        node, visited = stack.pop()
        if not visited:
            stack.append((node, True))
            if node.left:
                stack.append((node.left, False))
            if node.right:
                stack.append((node.right, False))
        else:
            lh = height.get(node.left, 0)        # 空孩子不在字典里，高度记 0
            rh = height.get(node.right, 0)
            height[node] = 1 + max(lh, rh)
            best = max(best, lh + rh)            # 经过 node 的最长路径的边数 = 左高 + 右高
    return best
```

`10^4` 层的左斜链 → `9999`，不会 `RecursionError`；`TreeNode` 按对象身份哈希，可以直接做字典的键。

2. **深链。** `10^4` 层的左斜链会让递归版抛 `RecursionError`（默认递归上限约 1000）。可以 `sys.setrecursionlimit(20000)`，但每层 Python 帧较大，更深的树可能直接崩溃；稳妥做法是上面的迭代后序。
3. **最大路径和（LC 124）。** 同样自底向上：函数返回"从该节点向下、只走一侧能得到的最大和"，即 `node.val + max(0, 左返回值, 右返回值)`；经过该节点的候选答案是 `node.val + max(0, 左) + max(0, 右)`。把"高度"换成"带符号的收益"，其余结构不变。

**Python 提醒**：嵌套函数里要修改外层的整数变量，必须声明 `nonlocal`，否则 `best = …` 会创建新的局部变量，外层的 `best` 始终是 `0`；用列表 `best = [0]` 绕过也可以，但 `nonlocal` 更直接。
