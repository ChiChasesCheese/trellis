---
id: python-data-model-total-ordering
node: python.data-model
type: qa
step: 5
tags: [grown]
---
## Q
机器编码题里要把自定义对象放进一个最小堆（`heapq`）按优先级排序，`functools.total_ordering` 在这里省了什么？

## A
`heapq` 只需要元素支持 `<`（`__lt__`）。但如果代码里别处还想用 `<=`、`>`、`>=` 比较，手写全部 6 个比较方法很啰嗦。`@functools.total_ordering` 只要求实现 `__eq__` 和其中一个（例如 `__lt__`），就能自动补全其余的比较方法；代价是它用组合调用实现，比手写全套方法稍慢。
```python
from functools import total_ordering

@total_ordering
class Task:
    def __init__(self, priority):
        self.priority = priority
    def __eq__(self, other):
        return self.priority == other.priority
    def __lt__(self, other):
        return self.priority < other.priority
```
