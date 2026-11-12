---
slug: tt-inorder-string-iterator
---
## Q
**二叉树中序字符迭代器**｜Medium

二叉树每个节点存一个字符串 `val`（可为空串）。实现 `InorderCharIterator(root)`：`next()` 按中序逐字符返回，没有字符时抛 `StopIteration`；`hasNext()` 判断是否还有字符。要懒加载，额外空间与树高成正比。

## A
**一句话。** 显式栈模拟中序遍历（同 LC 173），再记「当前字符串和已读位置」，读完就弹下一个节点，空串继续弹。

```python
class InorderCharIterator:
    def __init__(self, root):
        self.stack = []        # 还没访问自己和右子树的祖先
        self.s, self.i = "", 0 # 当前字符串和已读位置
        self.push_left(root)

    def push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def hasNext(self):
        while self.i >= len(self.s) and self.stack:
            node = self.stack.pop()      # 读完或空串：换下一个节点
            self.push_left(node.right)
            self.s, self.i = node.val, 0
        return self.i < len(self.s)

    def next(self):
        if not self.hasNext():
            raise StopIteration
        ch = self.s[self.i]
        self.i += 1
        return ch
```

**复杂度。** 时间 单次摊还 `O(1)`，空间 `O(h)`。

**易错点。**
- `hasNext()` 只看栈是否非空：只有空串的节点会让它返回 `True` 却无字符可读。
- 弹出节点忘了压右子树的左链：根 `"ab"`、左 `"c"`、右 `"de"` 只读出 `c, a, b`。
- 构造时递归展开整棵树：违反懒加载，斜树还会 `RecursionError`。

**追问。**
- 想要 `peek()`？：先调 `hasNext()` 保证游标指向字符，再返回 `s[i]` 不前进。
- 实现 Python 迭代器协议？：加 `__iter__` 返回自己，`__next__` 调用 `next`。

**同模式。** LC 173 二叉搜索树迭代器、LC 94 二叉树的中序遍历、LC 341 扁平化嵌套列表迭代器、LC 284 窥探迭代器
