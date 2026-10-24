---
id: tlc-python-heapq-1-basics
node: python.heapq
type: qa
step: 1
---
## Q
**Python 工具箱｜`heapq` 的基本盘**

`heapq` 是怎样把一个普通 `list` 当成堆用的？`heappush`、`heappop`、`heapify`、取堆顶各自的复杂度是多少？为什么 `print(h)` 看起来不是有序的？

## A
`heapq` 没有堆类，只有一组函数，操作的是一个普通 `list`，维护「`h[i] <= h[2i+1]` 且 `h[i] <= h[2i+2]`」的最小堆性质。

```python
import heapq
h = [5, 1, 4, 2, 3]
heapq.heapify(h)            # 原地建堆，O(n)
print(h, h[0])              # [1, 2, 4, 5, 3] 1：堆顶永远是 h[0]
heapq.heappush(h, 0)        # O(log n)
print(heapq.heappop(h), h[0])   # 0 1：弹出最小值，O(log n)
print(sorted(h), h)         # [1,2,3,4,5] [1,2,4,5,3]：堆数组本身不是有序的
```

- 取最小值 `h[0]` 是 `O(1)`；只有堆顶保证最小，其余位置只满足父不大于子，不要对 `h[1]`、`h[-1]` 做任何假设。
- `heapify` 是 `O(n)`，比逐个 `heappush` 的 `O(n log n)` 快，已有一批数据时先用它。
- `heapq` **只有最小堆**。要最大堆，把值取负存进去（元组入堆时第一项是优先级，第二项起只在平局时比较）。
- **坑**：对堆数组直接 `h.sort()` 虽然仍是合法堆，但对 `h` 做任意下标赋值、`h.remove(x)` 会破坏堆性质，`remove` 之后必须再 `heapify`（`O(n)`）。

典型题型：Top-K（LC 215、347）、合并 K 个有序链表（LC 23）、会议室（LC 253）、数据流中位数（LC 295）。
