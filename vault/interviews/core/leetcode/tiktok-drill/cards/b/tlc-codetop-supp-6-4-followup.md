---
id: tlc-codetop-supp-6-4-followup
node: b.codetop-supp-6
type: qa
step: 4
---
## Q
**补充题 6 手撕堆排序**｜追问

面试官接着问：（1）建堆为什么是 `O(n)`？（2）堆排序稳定吗，和快速排序比怎么选？（3）用 Python 标准库怎么写，Top-K 又怎么办？

## A
1. **建堆 `O(n)`**：高度为 `h` 的节点至多 `n / 2^(h+1)` 个，各下沉至多 `h` 步，总和 `Σ h * n / 2^(h+1) = O(n)`。
2. **稳定性**：不稳定，堆顶与末尾的交换会打乱相等元素的次序。对比快排：堆排序最坏也是 `O(n log n)` 且 `O(1)` 空间，但访问跳跃、缓存不友好，实际常数更大；快排平均更快但最坏 `O(n^2)`。
3. **标准库**：
```python
from heapq import heapify, heappop

def heap_sort_heapq(nums: list[int]) -> list[int]:
    heap = nums[:]
    heapify(heap)                                   # O(n)，小根堆
    return [heappop(heap) for _ in range(len(heap))]
```
时间同样是 `O(n log n)`，额外空间 `O(n)`。Top-K 不必全排序：`heapq.nlargest(k, nums)`，`O(n log k)`。

**Python 提醒**：`heapq` 只有小根堆；要大根堆，把元素取负再放入。
