---
slug: moving-average-from-data-stream
---
## Q
**LC 346 数据流中的移动平均值**｜Easy

设计 `MovingAverage(size)`：`next(val)` 读入一个数，返回最近至多 `size` 个数的平均值。

## A
**一句话。** 队列装窗口，另维护一个窗口和：新数入队加上，超出 `size` 就弹队头并减掉。

```python
class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.q = deque()
        self.total = 0

    def next(self, val):
        self.q.append(val)
        self.total += val
        if len(self.q) > self.size:
            self.total -= self.q.popleft()   # 滑出窗口
        return self.total / len(self.q)
```

**复杂度。** 时间每次 `O(1)`，空间 `O(size)`。

**易错点。**
- 每次重新对队列求和：变成 `O(size)`，要维护 `total`。
- 除以 `size`：窗口没满时要除以当前个数 `len(q)`。
- 先弹再入队：容量为 1 时队列会短暂为空，先入队再弹更安全。

**追问。**
- 浮点误差累积怎么办？：长时间运行后 `total` 会漂移，可定期重算，或整数存和、取均值时才除。
- 想要中位数而不是平均数？：用双堆或有序结构，见数据流的中位数。

**同模式。** LC 933 最近的请求次数、LC 362 敲击计数器、LC 239 滑动窗口最大值、LC 643 子数组最大平均数 I
