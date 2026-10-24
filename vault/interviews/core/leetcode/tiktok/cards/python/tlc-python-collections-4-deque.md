---
id: tlc-python-collections-4-deque
node: python.collections
type: qa
step: 4
---
## Q
**Python 工具箱｜`deque`**

BFS 队列和滑动窗口为什么用 `collections.deque` 而不是 `list`？`maxlen`、`rotate` 的行为是什么？哪个操作在 `deque` 上反而慢？

## A
`deque` 是双向链块结构：两端 `append` / `appendleft` / `pop` / `popleft` 都是 `O(1)`；`list.pop(0)` 要把后面所有元素前移，是 `O(n)`。

```python
from collections import deque
q = deque([1, 2, 3])
print(q.popleft(), q)             # 1 deque([2, 3])
dq = deque([1, 2, 3], maxlen=3)   # 定长：满了再加会从另一端挤掉一个
dq.append(4);     print(dq)       # deque([2, 3, 4], maxlen=3)
dq.appendleft(0); print(dq)       # deque([0, 2, 3], maxlen=3)
dq.rotate(1);     print(dq)       # deque([3, 0, 2], maxlen=3)：向右转 1 位
print(deque(range(5))[2])         # 2：能按下标取，但中间随机访问是 O(n)
```

- 适用：BFS 的队列（LC 200、994、127）、单调队列（LC 239 滑动窗口最大值，队首弹出过期下标）、`maxlen=k` 只保留最近 `k` 个（LC 346 数据流移动平均）。
- `rotate(k)` 向右转 `k` 位，`k` 为负则向左，`O(k)`。
- **坑**：中间下标访问和切片不支持（`dq[1:3]` 报 `TypeError`），下标访问在中部是 `O(n)`；需要随机访问就别用 `deque`。

`list.pop(0)` 在 `10^5` 个元素上循环调用会多出一个 `n` 的因子，是 BFS 超时的常见原因。
