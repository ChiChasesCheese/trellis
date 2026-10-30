---
id: tlc-tt-fixed-array-deque-o1-4-followup
node: p3.tt-fixed-array-deque-o1
type: qa
step: 4
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜追问

定长环形缓冲区实现的双端队列已经让 `push_head`、`push_tail`、`pop_head`、`pop_tail`、`index` 都是 `O(1)`。面试官接着问：（1）「search」如果是**按值**判断存在，也要 `O(1)`？（2）容量不够时自动扩容？（3）多线程使用？（4）想要覆盖最旧元素而不是拒绝？

## A
1. **按值 `O(1)` 查找**：额外维护 `Counter[int]`（值 → 个数），入队加一、出队减一，`contains(x)` 是 `count[x] > 0`。

```python
from collections import Counter


class CountedDeque:
    """包一层：转发给 FixedDeque，同时维护 值 -> 个数，让 contains 变成 O(1)。"""

    def __init__(self, inner: FixedDeque) -> None:
        self.inner = inner
        self.count: Counter[int] = Counter()

    def push_head(self, x: int) -> bool:
        ok = self.inner.push_head(x)
        if ok:
            self.count[x] += 1
        return ok

    def push_tail(self, x: int) -> bool:
        ok = self.inner.push_tail(x)
        if ok:
            self.count[x] += 1
        return ok

    def pop_head(self) -> int | None:
        x = self.inner.pop_head()
        if x is not None:
            self.count[x] -= 1
        return x

    def pop_tail(self) -> int | None:
        x = self.inner.pop_tail()
        if x is not None:
            self.count[x] -= 1
        return x

    def contains(self, x: int) -> bool:
        return self.count[x] > 0
```

   要得到值所在的位置则困难得多，因为两端入队会让所有元素的序号整体偏移，一般只提供存在性判断。
2. **自动扩容**：满时分配 `2 * cap` 的新数组，按逻辑顺序（从 `head` 起绕一圈）拷贝 `size` 个元素，`head` 重置为 `0`；单次 `O(n)`，均摊 `O(1)`。
3. **线程安全**：每个公开方法持同一把 `threading.Lock`；生产者消费者场景用 `Condition` 在满、空时等待。
4. **覆盖最旧元素**：满时 `push_tail` 先 `pop_head` 再写入（`collections.deque(maxlen=k)` 的行为）。

**Python 提醒**：`Counter` 读不存在的键返回 `0` 且不插入，`count[x] -= 1` 可以减到 `0`，键仍然保留，不影响 `contains`；包装类里每个会改变元素集合的方法都必须同步更新计数，漏掉一个就会让 `contains` 悄悄出错。
