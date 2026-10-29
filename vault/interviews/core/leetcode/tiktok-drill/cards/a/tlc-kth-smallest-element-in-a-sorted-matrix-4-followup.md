---
id: tlc-kth-smallest-element-in-a-sorted-matrix-4-followup
node: a.kth-smallest-element-in-a-sorted-matrix
type: qa
step: 4
---
## Q
**LC 378 有序矩阵中第 K 小的元素**｜追问

面试官接着问：（1）用堆怎么写，什么时候比二分更好？（2）矩阵只保证每行有序，列不保证？（3）数据是流式的或矩阵太大放不进内存？

## A
1. **堆 / 归并**：每行是一条有序链，惰性 `n` 路归并，取第 `k` 个。
```python
import heapq
from itertools import islice

def kth_smallest_merge(matrix: list[list[int]], k: int) -> int:
    return next(islice(heapq.merge(*matrix), k - 1, None))     # n 个有序行的惰性归并
```
`[[1,5,9],[10,11,13],[12,13,15]], k = 8` → `13`。时间 `O(k log n)`，空间 `O(n)`。`k` 很小（比如前几小）时比二分快，`k` 接近 `n^2` 时二分更快。
2. **只有行有序**：阶梯扫描依赖列也有序，失效。改成每行用 `bisect_right(row, mid)` 数个数，`count_le` 变成 `O(n log n)`，总计 `O(n log n · log V)`。
3. **放不进内存**：二分答案天然适合——每轮对数据做一遍扫描计数，只占 `O(1)` 内存；多次扫描的代价是 I/O，可以把 `log V` 轮减少到分位数估计的几轮。

**Python 提醒**：`heapq.merge` 返回的是惰性迭代器，不能直接下标取值；用 `islice` 跳过前 `k − 1` 个再 `next`。`heapq.merge(*matrix)` 要求每个输入已经有序，这里行本身有序所以成立。
