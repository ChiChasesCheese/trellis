---
slug: flatten-nested-list-iterator
---
## Q
**LC 341 扁平化嵌套列表迭代器**｜Medium

给你一个嵌套的整数列表 `nestedList`。每个元素要么是一个整数，要么是一个列表，列表的元素也可能是整数或其他列表。实现扁平迭代器类 `NestedIterator`：`NestedIterator(nestedList)` 初始化；`int next()` 返回下一个整数；`boolean hasNext()` 如果仍有待迭代的整数返回 `true`。`NestedInteger` 接口提供 `isInteger()`、`getInteger()`、`getList()`。重复调用 `hasNext()` 为真时 `next()`，得到的序列必须等于扁平化后的列表。`1 <= nestedList.length <= 500`，整数值在 `[-10^6, 10^6]`。例：`nestedList = [[1,1],2,[1,1]]` → `[1,1,2,1,1]`；`nestedList = [1,[4,[6]]]` → `[1,4,6]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 迭代器设计（iterator）：惰性（lazy）展开 + 预取（peek）一个元素；嵌套结构的 DFS。

**一句话。** 用递归生成器 `yield from` 惰性地深度优先展开嵌套列表，构造时预取第一个整数，`hasNext` 看有没有预取值，`next` 返回它并再预取下一个。

**识别。** 「嵌套结构 + 顺序遍历 + 要做成迭代器」：展开顺序就是 DFS 先序；迭代器要求按需产出，不能一次展开（嵌套很大或无限时不可行）。`hasNext` 必须能自己判断「后面还有没有整数」，因为列表可以是空的、可以层层嵌套空列表。

**推导。** 最直接：构造时递归把所有整数收进一个平铺列表，再用下标迭代（见下）。浪费在于一次展开全部、占 `O(总元素数)` 内存，且在迭代器只用前几个元素时白做了功。惰性做法把递归「暂停」在每个整数处：生成器天然保存了 DFS 的位置。`hasNext` 的难点是空列表，只有真正取出下一个整数才知道有没有，所以预取一个。

**简单解法。** 构造时一次展开：

```python
class NestedIteratorEager:
    def __init__(self, nestedList: list[NestedInteger]) -> None:
        self.flat: list[int] = []
        def dfs(items: list[NestedInteger]) -> None:
            for item in items:
                if item.isInteger():
                    self.flat.append(item.getInteger())
                else:
                    dfs(item.getList())
        dfs(nestedList)
        self.i = 0

    def next(self) -> int:
        self.i += 1
        return self.flat[self.i - 1]

    def hasNext(self) -> bool:
        return self.i < len(self.flat)
```

构造 `O(N)` 时间和空间（`N` 为整数个数加列表个数），每次调用 `O(1)`。

最优解（惰性）：

```python
class NestedIterator:
    def __init__(self, nestedList: list[NestedInteger]) -> None:
        self.gen = self._walk(nestedList)        # 生成器：暂停处就是 DFS 当前所在位置
        self.head: int | None = next(self.gen, None)   # 预取下一个整数，None 表示已经没有

    def _walk(self, items: list[NestedInteger]) -> Iterator[int]:
        for item in items:
            if item.isInteger():
                yield item.getInteger()
            else:
                yield from self._walk(item.getList())   # 递归展开子列表；空列表什么也不产出

    def next(self) -> int:
        val = self.head
        self.head = next(self.gen, None)         # 取出后立刻预取下一个，hasNext 才不依赖调用顺序
        return val

    def hasNext(self) -> bool:
        return self.head is not None
```

运行：`[[1,1],2,[1,1]]` → `[1, 1, 2, 1, 1]`，`[1,[4,[6]]]` → `[1, 4, 6]`，`[[], [[]]]` → `[]`，`[[], 5, [[], 6]]` → `[5, 6]`。

**复杂度。** 构造只预取一个整数；每个整数经过一条 `yield from` 链产出，总时间 `O(N · d)`（`d` 为嵌套深度，通常很小），空间 `O(d)`。

**拓展优化。**
- 嵌套很深时生成器链有递归深度限制（见易错点）。改成显式栈，栈里放「列表的迭代器」，行为与递归版一致：

```python
class NestedIteratorStack:
    def __init__(self, nestedList: list[NestedInteger]) -> None:
        self.stack: list[Iterator[NestedInteger]] = [iter(nestedList)]   # 栈顶是正在遍历的那一层
        self.head: int | None = None
        self._advance()

    def _advance(self) -> None:
        self.head = None
        while self.stack:
            item = next(self.stack[-1], None)
            if item is None:
                self.stack.pop()                   # 这一层遍历完，回到上一层
            elif item.isInteger():
                self.head = item.getInteger()      # 找到下一个整数，停下
                return
            else:
                self.stack.append(iter(item.getList()))   # 进入子列表

    def next(self) -> int:
        val = self.head
        self._advance()
        return val

    def hasNext(self) -> bool:
        return self.head is not None
```

**易错点。**
- 空列表：`[[], [[]]]` 里没有整数，`hasNext` 必须返回 `False`。只检查「最外层列表是否为空」的实现会返回 `True`，然后 `next` 失败。
- `hasNext` 依赖「先调用 `hasNext` 再 `next`」才能展开：直接连续调用 `next` 就会出错；预取放在 `__init__` 与 `next` 里，两个方法都不依赖调用顺序。
- 最坏深度：嵌套 `n` 层的列表，递归生成器深度为 `n`，CPython 默认递归上限约 1000，层数超过它会抛 `RecursionError`，需要 `sys.setrecursionlimit` 或用上面的显式栈。

**同模式。** LC 339 嵌套列表权重和、LC 385 迷你语法分析器、LC 173 二叉搜索树迭代器、LC 284 窥视迭代器、LC 251 展开二维向量。
