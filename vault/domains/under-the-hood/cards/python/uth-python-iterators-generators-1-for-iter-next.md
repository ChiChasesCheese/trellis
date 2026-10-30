---
id: uth-python-iterators-generators-1-for-iter-next
node: python.iterators-generators
type: qa
step: 1
---
## Q
**for 循环是怎么一个个取元素的**｜Python · CPython 3.14

`for x in [10, 20, 30]` 在底层是怎么走完列表的？「可迭代对象」和「迭代器」有什么区别？

## A
**背景。** 列表按下标走，字典按哈希表的槽位走，文件按行走。每种容器的遍历方式不同，但 `for` 需要一种统一的写法。办法是让容器交出一个「游标」，游标只会做一件事：每次给出下一个元素，没有了就报告结束。

**结构。** 只有两个动作：`iter(x)` 拿到游标（迭代器，iterator）；对游标反复调用 `next()`，直到它抛出 `StopIteration`，`for` 接住这个异常，循环就结束。能被 `iter()` 的东西叫可迭代对象（iterable，有 `__iter__`）；游标自己有 `__next__`，并且 `iter(游标)` 返回它自己。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="60" y="40" width="70" height="32" rx="3"/>
<rect x="200" y="40" width="70" height="32" rx="3"/>
<rect x="75" y="120" width="180" height="56" rx="3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="130" y="40" width="70" height="32" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="165" y1="120" x2="165" y2="74"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="165.0,74.0 168.0,80.0 162.0,80.0"/>
</g>
<g fill="currentColor">
<text x="95" y="60">10</text>
<text x="165" y="60">20</text>
<text x="235" y="60">30</text>
<text x="165" y="158" font-size="11">seq: 指向 L</text>
<text x="165" y="171" font-size="11">it_index = 1</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="95" y="32" font-size="11">0</text>
<text x="165" y="32" font-size="11">1</text>
<text x="235" y="32" font-size="11">2</text>
<text x="30" y="61">L</text>
<text x="172" y="98" text-anchor="start" font-size="11">下一个取这格</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="165" y="140">list_iterator</text>
</g>
</g>
</svg>
```

```python
it = iter([10, 20, 30])
next(it)   # 10
next(it)   # 20
next(it)   # 30
next(it)   # 抛出 StopIteration
```

**细节。**

- 列表的游标 `list_iterator` 只存两样：指向列表的引用和下一个下标 `it_index`；走完之后它把引用清空。
- 字节码里 `for` 就是 `GET_ITER`（调 `iter`）加循环里的 `FOR_ITER`（调 `next`，遇到 `StopIteration` 就跳出循环）。

**为什么。** 游标把「怎么走」留给容器自己，`for`、`sum`、`list()`、解包都只认这两个动作，所以任何类型只要交出游标，就能被它们使用。

**例题：** 二叉树中序字符迭代器（TikTok 变体题）

二叉树每个节点存一个字符串 `val`（可以是空串）。实现迭代器 `InorderCharIterator(root)`：`next()` 按中序遍历的顺序逐字符返回，没有字符时抛 `StopIteration`，`hasNext()` 判断是否还有字符。要懒加载，额外空间与树高成正比，空串节点要跳过。例：根 `"ab"`，左孩子 `"c"`，右孩子 `""`，右孩子的右孩子 `"de"`，依次返回 `c, a, b, d, e`。

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
