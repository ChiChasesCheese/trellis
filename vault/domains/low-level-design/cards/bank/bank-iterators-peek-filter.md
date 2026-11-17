---
id: bank-iterators-peek-filter
node: bank.structures.iterators
type: qa
step: 3
---
## Q
要做一个带 `peek()` 和 `has_next()` 的迭代器，或者「只产出满足条件的元素」的过滤迭代器。`has_next()` 为什么必须真的往前读一个？这个预读什么时候读最合适？

## A
**缓存一个元素，被问到才读**

- **`has_next` 要回答「还有没有」**：不读下一个就答不出来。过滤迭代器同理，后面有没有满足条件的，要一路读到它才知道；
- **一个缓存槽加一个哨兵**：`_buf` 为 `_EMPTY` 表示没读；`peek` 才读并存下，`next` 取走并清空。哨兵用 `object()`，不用 `None`，因为 `None` 可能是合法元素；
- **惰性预读**：构造时不读，第一次 `peek` 才读。构造函数里就预读一个，对「读一个就有副作用」的源（网络、产生事件的流）是提前消费。下面的源只在第一次 `peek` 时打印 `read 1`，`peek` 两次也不多读；
- **过滤迭代器 = 窥视加条件**：`Peekable(x for x in src() if cond)` 就够了，被过滤掉的元素在 `next` 往后找下一个的时候才被读掉；
- **耗尽的写法**：`peek` 让 `StopIteration` 原样抛出；`has_next` 就是 `try: self.peek(); return True`，`except StopIteration: return False`。

```python
_EMPTY = object()                                    # 「还没读」的标记
class Peekable:
    def __init__(self, it): self._it, self._buf = iter(it), _EMPTY
    def peek(self):
        if self._buf is _EMPTY: self._buf = next(self._it)   # 被问到才读；耗尽抛 StopIteration
        return self._buf
    def __next__(self):
        v = self.peek(); self._buf = _EMPTY
        return v

def src():
    for i in range(1, 4): print("read", i); yield i
p = Peekable(x for x in src() if x != 2)             # 过滤迭代器 = 窥视 + 条件
print(p.peek(), p.peek(), next(p))                   # 只读了 1；peek 两次不多读
print(next(p))                                       # 读 2（被过滤）、3
```

<details class="pt"><summary>延伸</summary>

和它并列的另一种选择是「提前把全部元素读进列表，再在列表上写 `has_next`」：写起来最简单，但源是无限流或读取有副作用时直接失败，内存也随输入增长。窥视迭代器只多占一个元素的内存，这才是它存在的理由。

</details>

**知识点：**迭代器设计（Iterator Design）
