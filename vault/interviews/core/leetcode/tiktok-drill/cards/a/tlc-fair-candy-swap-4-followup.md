---
id: tlc-fair-candy-swap-4-followup
node: a.fair-candy-swap
type: qa
step: 4
---
## Q
**LC 888 公平的糖果交换**｜追问

面试官接着问：（1）内存很紧，不想开集合怎么办？（2）如果题目不保证有解，边界要怎么处理？（3）能交换多盒吗？

## A
1. **不开集合**：两个数组各自排序，双指针按目标差移动，额外空间 `O(1)`，时间 `O(n log n + m log m)`。
```python
def fair_candy_swap_sorted(a: list[int], b: list[int]) -> list[int]:
    delta = (sum(a) - sum(b)) // 2
    a, b = sorted(a), sorted(b)
    i = j = 0
    while i < len(a) and j < len(b):
        diff = a[i] - b[j] - delta        # 为 0 时 b[j] == a[i] - delta
        if diff == 0:
            return [a[i], b[j]]
        if diff < 0:
            i += 1
        else:
            j += 1
    return []
```
2. **不保证有解**：先判断 `(sumA - sumB) % 2`，奇数直接返回 `[]`。否则整除向下取整会算出一个错误的 `delta`，可能返回一个其实不公平的交换。
3. **交换多盒**：等价于从两边各选一个子集，使子集和之差等于 `delta`，是子集和（subset sum）类问题，不再是简单查表。

**Python 提醒**：`-3 // 2 == -2`（向下取整），`sumA < sumB` 时 `delta` 为负，整除的取整方向和 C++/Java 的向零取整不同，所以奇偶判断要先做。
