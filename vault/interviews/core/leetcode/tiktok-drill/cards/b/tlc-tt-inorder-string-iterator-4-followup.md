---
id: tlc-tt-inorder-string-iterator-4-followup
node: b.tt-inorder-string-iterator
type: qa
step: 4
---
## Q
**二叉树中序字符迭代器**｜追问

面试官接着问：（1）能不能用生成器写得更短；（2）怎样让它支持 `for ch in it`；（3）再加一个 `peek()`，只看下一个字符而不前进。

## A
1. **生成器**：把栈留在函数内部，每读到节点就 `yield from node.val`，空串自然什么也不产出。仍然要用显式栈，递归版会在深树上栈溢出。

```python
from collections.abc import Iterator


def inorder_chars(root: TreeNode | None) -> Iterator[str]:
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:                       # 一路向左，把祖先压栈
            stack.append(node)
            node = node.left
        node = stack.pop()
        yield from node.val               # 逐字符产出；空串什么也不产出
        node = node.right
```

根 `"ab"`、左 `"c"`、右 `""` 带右孩子 `"de"` → `['c', 'a', 'b', 'd', 'e']`；`10^5` 个节点的左斜链读出 `100000` 个字符。生成器没有 `hasNext()`，如果接口必须有，要像上面那样用类。
2. **迭代器协议**：在类里加 `__iter__`（返回 `self`）和 `__next__`（调用 `next()`，读完时抛 `StopIteration`）。我们的 `next()` 已经在没有字符时抛 `StopIteration`，`__next__` 可以直接复用它。
3. **`peek()`**：先调用 `hasNext()` 保证游标指向一个字符，再返回 `self._s[self._i]`，不增加游标；没有字符时抛 `StopIteration`。因为 `hasNext()` 重复调用不改变状态，`peek()` 之后再 `next()` 得到同一个字符。

**Python 提醒**：`yield from 字符串` 会逐字符产出，`yield from` 对任意可迭代对象都有效；类里叫 `next` 的方法不会遮住内置函数 `next`（方法在类的命名空间里，要通过 `self.next()` 调用），所以两者可以共存。
