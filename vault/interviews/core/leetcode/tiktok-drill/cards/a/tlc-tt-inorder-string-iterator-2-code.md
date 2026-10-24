---
id: tlc-tt-inorder-string-iterator-2-code
node: a.tt-inorder-string-iterator
type: qa
step: 2
---
## Q
**二叉树中序字符迭代器**｜写出 Python 实现

二叉树节点 `TreeNode(val, left, right)` 的 `val` 是字符串（可以为空串）。实现类 `InorderCharIterator(root)`：`next()` 按中序顺序逐字符返回，没有字符时抛 `StopIteration`；`hasNext()` 判断是否还有字符。不能在构造时展开整棵树，额外空间 `O(h)`，空串节点跳过。节点数不超过 `10^5`。

## A
**思路。** 栈保存还没访问的祖先（构造时压入根的整条左链）。`hasNext()` 在当前字符串读完时循环：弹出栈顶、压入其右子树的左链、载入它的字符串并把游标置零，直到找到有字符的节点或栈空。`next()` 先调用 `hasNext()`，再返回游标处的字符并前进。

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

运行：根 `"ab"`、左 `"c"`、右 `""` 带右孩子 `"de"` → `['c', 'a', 'b', 'd', 'e']`；空树 `hasNext()` → `False`；读完后再调用 `next()` 抛 `StopIteration`；`10^5` 个节点的左斜链 → 读出 `100000` 个字符。

**复杂度。** 构造 `O(h)`；`next` 摊还 `O(1)`；空间 `O(h)`。

**写法要点。** `hasNext()` 里用 `while`，一次可以连续跳过多个空串节点；`_push_left` 把「压入整条左链」抽成一个方法，构造和换节点两处共用；`self._s, self._i = node.val, 0` 一次完成载入字符串和复位游标；`next()` 复用 `hasNext()` 保证两个方法状态一致，且 `hasNext()` 重复调用不会改变状态；以下划线开头的成员表示内部状态，不属于对外接口。
