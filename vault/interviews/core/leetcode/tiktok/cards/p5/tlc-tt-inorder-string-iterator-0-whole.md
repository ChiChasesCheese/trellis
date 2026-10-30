---
id: tlc-tt-inorder-string-iterator-0-whole
node: p5.tt-inorder-string-iterator
type: qa
---
## Q
**二叉树中序字符迭代器**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2025-10-31（面试记录）

二叉树的每个节点存一个字符串 `val`（可以是空串）。实现迭代器 `InorderCharIterator(root)`：`next()` 每次按中序遍历的顺序返回下一个字符（逐字符，不是逐节点），没有字符时抛 `StopIteration`；`hasNext()` 判断是否还有字符。要求懒加载：不能在构造时把整棵树展开成一个大字符串，额外空间与树高成正比；空串节点要被跳过。节点数不超过 `10^5`，每个字符串长度不超过 `100`。例：根 `"ab"`，左孩子 `"c"`，右孩子 `""`，右孩子的右孩子 `"de"` → 依次返回 `c, a, b, d, e`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用显式栈模拟中序遍历（和 LC 173 二叉搜索树迭代器一样），再多记一个「当前字符串和已读位置」。`hasNext()` 在当前字符串读完时，弹出下一个节点、把它右子树的整条左链压栈、载入它的字符串，空串就继续弹；`next()` 返回当前位置的字符。`next` 摊还 `O(1)`，空间 `O(h)`。

**识别。** 「中序 + 迭代器 + 不预先展开」就是栈模拟中序的标准题；「逐字符」只是在节点这一层外面套一层位置游标；「空串要跳过」说明换节点的逻辑必须是个循环，不能只换一次。

**推导。** 暴力：构造时做一次中序遍历，把所有字符拼成一个字符串或列表，`next` 就是下标自增，`O(N)` 时间和空间在构造时一次性花掉 → 浪费：违背懒加载，树很大时即使只读几个字符也要付出全部代价 → 洞察：中序遍历的递归状态就是「祖先栈」，栈里只需要保存还没访问自己的祖先，最多一条左链，`O(h)`；节点内的位置是一个整数游标。把「换下一个节点」放进 `hasNext()`，`next()` 只负责读字符，两个方法的状态始终一致，`hasNext()` 重复调用不会改变结果。

```python
class InorderCharIterator:
    def __init__(self, root: TreeNode | None) -> None:
        self._stack: list[TreeNode] = []        # 栈里是“还没访问自己和右子树”的祖先
        self._s, self._i = "", 0                # 当前节点的字符串和已读到的位置
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node:
            self._stack.append(node)
            node = node.left

    def hasNext(self) -> bool:
        while self._i >= len(self._s) and self._stack:   # 当前字符串读完（或是空串）：换下一个节点
            node = self._stack.pop()
            self._push_left(node.right)
            self._s, self._i = node.val, 0
        return self._i < len(self._s)

    def next(self) -> str:
        if not self.hasNext():
            raise StopIteration
        ch = self._s[self._i]
        self._i += 1
        return ch
```

运行：根 `"ab"`、左 `"c"`、右 `""` 带右孩子 `"de"` → `['c', 'a', 'b', 'd', 'e']`；空树 `hasNext()` → `False`；单个空串节点 `hasNext()` → `False`；一条 `10^5` 个节点的左斜链、每个节点 `"x"` → 依次读出 `100000` 个字符，没有递归，不会溢出。

**复杂度。** 构造 `O(h)`；每个节点只入栈、出栈各一次，所以 `n` 次 `next` 总计 `O(N)`（节点数加字符数），单次摊还 `O(1)`；空间 `O(h)`，与字符总数无关。

**易错点。**
- `hasNext()` 只检查栈是否非空：遇到只有空串的节点，`hasNext()` 返回 `True` 但 `next()` 没有字符可读。单个空串节点的树上，应该是 `False`。
- 弹出节点时忘了压它右子树的左链：根 `"ab"`、左 `"c"`、右 `"de"` 只会读出 `c, a, b`，漏掉 `d, e`。
- 在构造函数里递归展开整棵树再逐个返回：功能对，但违反懒加载；而且递归在 `10^5` 层的斜树上会 `RecursionError`。

**追问。**
- 用生成器实现：一个函数里 `yield from node.val`，短，但要自己用栈迭代，才能避免递归深度问题。
- 实现 Python 的迭代器协议：加 `__iter__` 返回自己，`__next__` 调用 `next`，这样可以 `for ch in it`。
- 想要 `peek()`：先调用 `hasNext()` 保证当前游标指向一个字符，再返回 `self._s[self._i]` 而不前进。

**同模式。** LC 173 二叉搜索树迭代器、LC 94 二叉树的中序遍历、LC 341 扁平化嵌套列表迭代器、LC 284 窥探迭代器。
