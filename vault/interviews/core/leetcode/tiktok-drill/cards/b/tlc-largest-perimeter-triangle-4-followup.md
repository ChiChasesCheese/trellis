---
id: tlc-largest-perimeter-triangle-4-followup
node: b.largest-perimeter-triangle
type: qa
step: 4
---
## Q
**LC 976 三角形的最大周长**｜追问

面试官接着问：（1）要数能组成多少个三角形（LC 611）？（2）数组非常大、甚至是数据流，还要排序全部数据吗？（3）要返回三条边？

## A
1. **数个数（LC 611）**：升序排序，固定最长边下标 `k`，左右指针 `i = 0, j = k - 1`：若 `nums[i] + nums[j] > nums[k]`，`i..j-1` 都能和 `j` 配对，计数加 `j - i` 后 `j -= 1`；否则 `i += 1`。`O(n^2)`。
2. **只取前 32 大**：若相邻三元组连续失败，`a >= b + c` 让长度从小往大至少按斐波那契数增长；长度 `>= 1` 时第 32 个斐波那契数已超过 `10^6`，所以答案必然出现在最大的 32 个数里。

```python
import heapq


def largest_perimeter_top(nums: list[int]) -> int:
    top = heapq.nlargest(32, nums)                    # 降序的前 32 个，O(n log 32)
    for a, b, c in zip(top, top[1:], top[2:]):
        if b + c > a:
            return a + b + c
    return 0
```

数据流里维护一个大小 32 的最小堆即可。
3. **返回三条边**：返回 `(a, b, c)`，或 `[]` 表示不存在。

**Python 提醒**：`nums.sort()` 返回 `None` 并改动原列表，写成 `nums = nums.sort()` 会把 `nums` 变成 `None`；要新列表就用 `sorted`。
