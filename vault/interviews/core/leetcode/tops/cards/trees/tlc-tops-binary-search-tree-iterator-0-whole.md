---
id: tlc-tops-binary-search-tree-iterator-0-whole
node: trees.binary-search-tree-iterator
type: qa
---
## Q
**LC 173 二叉搜索树迭代器**｜Medium · 全公司热度第 704 名 · Top Interview 150

实现 `BSTIterator`，它是二叉搜索树（BST）**中序遍历**的迭代器：`BSTIterator(root)` 用树根初始化，指针起初指在一个比树中所有数都小的位置；`hasNext()` 指针右侧还有数就返回 `true`；`next()` 把指针右移并返回指针处的数，首次调用返回最小元素。保证 `next()` 的调用总是有效。树中结点数在 `[1, 10^5]`，`0 <= Node.val <= 10^6`，最多调用 `10^5` 次 `hasNext` 和 `next`。进阶：`next()` 和 `hasNext()` 均摊 `O(1)`，只用 `O(h)` 内存（`h` 为树高）。例：树 `[7,3,15,null,null,9,20]`，依次调用 `next()` → `3`，`next()` → `7`，`hasNext()` → `true`，`next()` → `9`，`next()` → `15`，`next()` → `20`，`hasNext()` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** BST 的中序遍历是升序；把递归遍历"摊开"成可暂停的迭代器（受控递归 / 显式栈）。

**一句话。** 初始化时中序遍历把所有值收进列表，`next` 和 `hasNext` 就是移动一个下标。

**识别。** 「BST + 中序 + 逐个取」= 升序序列上的指针；"迭代器"意味着一次只吐一个，进阶要求 `O(h)` 内存，说明不能把整棵树摊平，要用栈保存"还没访问的左链"。

**推导。** 最直接的做法是递归中序遍历存成列表，构造 `O(n)` 时间、`O(n)` 内存，之后每个操作 `O(1)`。进阶把内存压到 `O(h)`：中序遍历的递归栈本来就只有 `h` 层，让栈自己保存，每次 `next` 只"推进"到下一个结点，见拓展。

```python
class BSTIterator:
    def __init__(self, root: TreeNode | None) -> None:
        self.vals: list[int] = []

        def inorder(node: TreeNode | None) -> None:
            if node:
                inorder(node.left)
                self.vals.append(node.val)  # BST 的中序遍历结果就是升序
                inorder(node.right)

        inorder(root)
        self.i = -1  # 指针在最小值之前

    def next(self) -> int:
        self.i += 1
        return self.vals[self.i]

    def hasNext(self) -> bool:
        return self.i + 1 < len(self.vals)
```

运行：树 `[7,3,15,null,null,9,20]` 上依次得到 `3`、`7`、`True`、`9`、`True`、`15`、`True`、`20`、`False`，与示例一致；单结点树调用一次 `next()` 后 `hasNext()` → `False`。

**复杂度。** 构造 `O(n)` 时间和空间，`next`、`hasNext` 各 `O(1)`。

**拓展优化。**
- 进阶要求的 `O(h)` 内存：栈里只放"已经走到、但自己和右子树都还没访问"的结点——从根一路向左入栈；`next` 弹出栈顶（就是当前最小），再把它右子树的整条左链压栈。每个结点入栈出栈各一次，所以 `next` 均摊 `O(1)`，栈深不超过 `h`；这是面试官真正想看的版本：

```python
class BSTIteratorStack:
    def __init__(self, root: TreeNode | None) -> None:
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node:  # 一路向左：最左的结点是当前子树的最小值
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()  # 栈顶 = 下一个最小值
        self._push_left(node.right)  # 它的右子树里的数都比它大、比栈里其余的小：左链压栈
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)
```

**易错点。**
- 最坏的深度：树退化成一条 `10^5` 个结点的链时，递归中序的深度是 `10^5`，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit`，要么用上面的显式栈版本（栈在堆上，不受影响）。
- 栈版本 `next` 里忘了压右子树的左链：树 `[7,3,15,null,null,9,20]` 弹出 `3`、`7` 后栈就空了，`hasNext()` 变成 `false`，漏掉 `9`、`15`、`20`。
- 指针从 `-1` 开始却把 `hasNext` 写成 `self.i < len(self.vals)`：取完最后一个数后仍返回 `True`，示例最后一次 `hasNext()` 应为 `false`；正确是 `self.i + 1 < len(self.vals)`。

**同模式。** LC 94 二叉树的中序遍历、LC 230 二叉搜索树中第 K 小的元素、LC 98 验证二叉搜索树、LC 284 窥视迭代器。
