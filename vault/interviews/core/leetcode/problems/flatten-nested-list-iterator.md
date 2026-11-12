---
slug: flatten-nested-list-iterator
---
## Q
**LC 341 扁平化嵌套列表迭代器**｜Medium

`nestedList` 的元素是整数或嵌套列表（`isInteger()`、`getInteger()`、`getList()`）。实现迭代器 `next()` / `hasNext()`，按顺序产出所有整数。

## A
**一句话。** 递归生成器 `yield from` 惰性展开，预取一个值来回答 `hasNext`。

```python
class NestedIterator:
    def __init__(self, nestedList):
        def walk(items):
            for x in items:
                if x.isInteger():
                    yield x.getInteger()
                else:
                    yield from walk(x.getList())
        self.it = walk(nestedList)
        self.nxt = next(self.it, None)   # 预取一个

    def next(self):
        v, self.nxt = self.nxt, next(self.it, None)
        return v

    def hasNext(self):
        return self.nxt is not None
```

**复杂度。** 每次 `next` 均摊 `O(d)`，空间 `O(d)`（`d` 为嵌套深度）。

**易错点。**
- 空列表：`[[], [[]]]` 没有整数，`hasNext` 必须返回 `False`，只看最外层是否为空会错。
- `hasNext` 依赖调用顺序：预取放在 `__init__` 与 `next` 里，连续调用 `next` 也不出错。
- 嵌套超过约 1000 层：递归生成器触顶，抛 `RecursionError`。

**追问。**
- 嵌套很深怎么办？：改用显式栈，存各层的迭代器，栈顶耗尽就弹出。
- 为什么要预取？：`hasNext` 要先知道后面是否真有整数，而空列表只能靠往前展开才能发现。

**同模式。** LC 339 嵌套列表权重和、LC 385 迷你语法分析器、LC 173 二叉搜索树迭代器、LC 284 窥视迭代器
