---
slug: peeking-iterator
---
## Q
**LC 284 窥视迭代器**｜Medium

给一个只有 `next()` 和 `hasNext()` 的迭代器，设计 `PeekingIterator`，再支持 `peek()`：返回下一个元素但不移动指针。

## A
**一句话。** 永远提前取一个放进缓存：`peek` 直接返回缓存，`next` 返回缓存并立刻再预取下一个。

```python
class PeekingIterator:
    def __init__(self, iterator):
        self.it = iterator
        self.has = iterator.hasNext()          # 缓存里有没有值
        self.cache = iterator.next() if self.has else None

    def peek(self):
        return self.cache

    def next(self):
        res = self.cache
        self.has = self.it.hasNext()           # 预取下一个
        self.cache = self.it.next() if self.has else None
        return res

    def hasNext(self):
        return self.has
```

**复杂度。** 时间每个操作 `O(1)`，空间 `O(1)`。

**易错点。**
- `peek` 里调用 `it.next()`：会真的消耗元素，窥视必须读缓存。
- 用 `cache is None` 判断是否还有元素：元素本身可能是 `None`，要单独记一个标志。
- `next` 返回前才预取：要先把旧缓存存进 `res`，否则返回的是新值。

**追问。**
- 不预取，改成惰性缓存呢？：`peek` 时才取一个并标记「已缓存」，`next` 先看有无缓存，省掉构造时的取值。
- 想支持任意长度的窥视？：缓存换成队列，`peek(k)` 取够 `k` 个。

**同模式。** LC 173 二叉搜索树迭代器、LC 341 扁平化嵌套列表迭代器
