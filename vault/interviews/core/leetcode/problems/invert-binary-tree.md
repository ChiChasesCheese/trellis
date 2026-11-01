---
slug: invert-binary-tree
---
## Q
**LC 226 翻转二叉树**｜Easy

给你一棵二叉树的根节点 `root`，翻转这棵二叉树（每个节点的左右子树互换），并返回其根节点。节点数在 `[0, 100]`，`-100 <= Node.val <= 100`。例：`root = [4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`；`root = [2,1,3]` → `[2,3,1]`；`root = []` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树递归（DFS）：对每个节点做同一个局部操作，再交给子树。

**一句话。** 翻转整棵树 = 先把左右子树各自翻转好，再让当前节点的左右指针互换。

**识别。** 「对树里每个节点做同一件事」的变换题，递归最短。`n <= 100`，任何遍历顺序都够；前序、后序都对，因为每个节点只需要互换自己的两个指针。

**推导。** 要把树镜像，等价于每个节点的两个孩子互换。先递归翻转子树，再交换指针；Python 的元组赋值让「翻转右子树、翻转左子树、一起赋值」只占一行。

```python
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None                                # 空树翻转后还是空树
    # 右边翻好的子树放到左边，左边翻好的放到右边；等号右边先全部求值，不会互相覆盖
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

运行：`[4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`；`[2,1,3]` → `[2,3,1]`；`[]` → `[]`；`[1,2]` → `[1,null,2]`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，递归栈深度，平衡树 `O(log n)`，链状 `O(n)`。

**拓展优化。**
- 迭代：栈（或队列）里放待处理节点，弹出一个就交换它的孩子再把孩子压进去，顺序无所谓。
```python
def invert_tree_iter(root: TreeNode | None) -> TreeNode | None:
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        node.left, node.right = node.right, node.left   # 局部互换，不依赖子树是否已处理
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return root
```

**易错点。**
- 分两行赋值：`root.left = invert_tree(root.right)` 之后再写 `root.right = invert_tree(root.left)`，此时 `root.left` 已经被覆盖成翻转后的右子树，两边变成同一棵子树。`[2,1,3]` 得到 `[2,3,3]`，正确是 `[2,3,1]`。要么用元组一次赋值，要么先用临时变量存下旧的 `left`。
- 只交换了值不交换节点，或只交换根的两个孩子而不递归：`[4,2,7,1,3,6,9]` 得到 `[4,7,2,6,9,1,3]`，下面几层没翻。
- 递归深度：链状树最深 `n` 层，CPython 默认上限约 `1000`；这里 `n <= 100` 安全，换成大输入要调高上限或用上面的迭代版。

**同模式。** LC 101 对称二叉树、LC 100 相同的树、LC 617 合并二叉树、LC 104 二叉树的最大深度。
