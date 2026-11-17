---
id: performance-ds-deque
node: performance.data-structures
type: qa
step: 3
---
## Q
用 list 当队列，从头取任务写成 `queue.pop(0)`，任务数从一万涨到十万，处理时间为什么涨了 150 倍？该换成什么？

## A
**从头部取要用 `deque`，list 只适合从尾部操作**

- **`list.pop(0)` 要把后面所有元素前移一格**：每次 O(n)，取完 n 个就是 O(n²)；
- **`deque.popleft()` 是 O(1)**：它是分块的双向链表，两端都便宜；
- **代价**：`deque` 按下标访问中间元素是 O(n)，不能当随机访问的数组；
- **要限长度**：`deque(maxlen=100)` 满了自动丢最老的，做“最近 100 条”不用手写；
- **要按优先级取**：不是 FIFO，换 `heapq`（见同领域的堆那张卡）。

实测（3.11，本机，把 n 个元素全部从头取完）：

| n | `list.pop(0)` | `deque.popleft()` |
|---|---|---|
| 10,000 | 3.49 ms | 0.13 ms |
| 100,000 | 535 ms | 1.37 ms |

n 扩大 10 倍，list 版慢了约 153 倍（接近平方），deque 版只慢了约 11 倍。

```python
from collections import deque

def drain(items):
    q = deque(items)
    out = []
    while q:
        out.append(q.popleft())      # O(1)；用 list.pop(0) 这里就是 O(n)
    return out

recent = deque(maxlen=3)
for x in range(5):
    recent.append(x)
print(drain(range(4)), list(recent))   # [0, 1, 2, 3] [2, 3, 4]
```

<details class="pt"><summary>延伸</summary>

多线程之间传任务用 `queue.Queue`：它内部就是 `deque` 加锁和条件变量。单线程里直接用 `deque` 更快，别为了“队列”这个名字引入锁。

</details>

**知识点：**按访问模式选结构（Choosing Structures）
