---
id: tlc-diameter-of-binary-tree-2-code
node: p4.diameter-of-binary-tree
type: qa
step: 2
---
## Q
**LC 543 二叉树的直径**｜写出 Python 实现

二叉树根节点 `root`（节点数 `1..10^4`，值 `-100..100`）。返回直径：树中任意两节点之间最长路径的边数，路径可以不经过根。注意树可能是 `10^4` 层的链，要避免递归爆栈。

## A
**思路。** 迭代后序。栈里放 `(节点, 是否已处理孩子)`：第一次弹出时把自己以"已访问"重新压回，再压左右孩子；第二次弹出时孩子的高度都已存进字典，计算自己的高度，并用 `左高 + 右高` 更新答案。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
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

**运行。** `[1,2,3,4,5]` → `3`；`[1,2]` → `1`；`[1]` → `0`；`None` → `0`；`10^4` 层的左斜链 → `9999`。

**复杂度。** 时间 `O(n)`：每个节点入栈两次、各处理一次；空间 `O(n)`。

**写法要点。** `TreeNode` 没有重写 `__eq__` / `__hash__`，按对象身份哈希，可以直接做字典的键；`height.get(node.left, 0)` 借助"`None` 不在字典里"一步处理空孩子，省去判断；`(node, visited)` 两阶段栈是迭代后序的通用模板；`best` 是普通局部变量，迭代写法里不需要 `nonlocal`。
