---
id: tlc-balanced-binary-tree-4-followup
node: p4.balanced-binary-tree
type: qa
step: 4
---
## Q
**LC 110 平衡二叉树**｜追问

面试官接着问：（1）树退化成 5000 层的链，递归会爆栈，怎么改成迭代？（2）自顶向下的写法复杂度是多少、为什么慢？（3）怎样把一棵不平衡的二叉搜索树变平衡（LC 1382）？

## A
1. **迭代后序。** 显式栈，每个节点入栈两次：第一次展开孩子，第二次（孩子都处理完）用字典里孩子的高度判断：
```python
def is_balanced_iter(root: TreeNode | None) -> bool:
    height: dict[TreeNode, int] = {}
    stack: list[tuple[TreeNode, bool]] = [(root, False)] if root else []
    while stack:
        node, done = stack.pop()
        if not done:
            stack.append((node, True))      # 孩子处理完之后再回来处理自己
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
        else:
            lh, rh = height.get(node.left, 0), height.get(node.right, 0)   # 空孩子查不到，默认 0
            if abs(lh - rh) > 1:
                return False
            height[node] = max(lh, rh) + 1
    return True
```
`[3,9,20,null,null,15,7]` → `True`，`[1,2,2,3,3,null,null,4,4]` → `False`，5000 层的左链 → `False`，不再有递归深度问题。
2. **自顶向下。** 对每个节点调用一次“求高度”再递归检查孩子，每个节点的高度被重复算很多次；平衡树大约 `O(n log n)`，链状树最坏 `O(n^2)`。自底向上把高度和判断合在一次遍历里，降为 `O(n)`。
3. **平衡一棵 BST（LC 1382）。** 中序遍历得到有序数组，再取中点作根、左右半段递归建树，左右子树大小至多差 `1`，高度也就平衡了：`O(n)` 时间。

**Python 提醒**：自定义类 `TreeNode` 没有重写 `__eq__` / `__hash__` 时，实例按对象身份哈希，可以直接做字典的键；一旦给类加了 `__eq__`，默认 `__hash__` 会被置空，需要同时定义 `__hash__` 才能继续当键。
