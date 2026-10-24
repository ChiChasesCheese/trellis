---
id: tlc-python-heapq-6-lazy-delete
node: python.heapq
type: qa
step: 6
---
## Q
**Python 工具箱｜堆的懒删除（lazy deletion）**

`heapq` 不能删除任意元素。滑动窗口里元素过期、Dijkstra 里同一个点被多次入堆时，应该怎么处理？

## A
堆里删除中间元素要 `O(n)`。办法是**不删**：记下「这个值已失效」，等它浮到堆顶再丢掉，每个元素最多入堆一次、出堆一次，总成本仍是 `O(log n)` 摊销。

```python
import heapq
from collections import Counter
h: list[int] = []
dead: Counter[int] = Counter()           # 值 -> 还欠几次删除
for x in [5, 2, 8]:
    heapq.heappush(h, x)
dead[2] += 1                              # 标记删除一个 2
while h and dead[h[0]]:                   # 堆顶若已失效就弹掉，直到堆顶有效
    dead[heapq.heappop(h)] -= 1
print(h[0])                               # 5
```

三个常见场景：
- **Dijkstra**：同一节点可能带不同距离多次入堆；弹出时若 `d > dist[u]` 说明是旧记录，直接 `continue`（LC 787、743）。
- **滑动窗口最大值**（用堆的版本）：堆里存 `(-值, 下标)`，弹出时若 `下标 <= i - k` 就丢（LC 239）。
- **滑动窗口中位数 / 数据流**：两个堆各记一个失效计数，并同步「有效元素个数」。

注意：堆的 `len(h)` 含失效元素，判断「还剩几个有效」要单独维护一个计数；否则容易在「堆非空」时拿到失效的堆顶。
