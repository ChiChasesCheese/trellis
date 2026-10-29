---
id: tlc-minimum-swaps-to-group-all-1s-together-ii-4-followup
node: a.minimum-swaps-to-group-all-1s-together-ii
type: qa
step: 4
---
## Q
**LC 2134 最少交换次数来组合所有的 1 II**｜追问

面试官接着问：（1）数组不是环形的（LC 1151）？（2）想用前缀和写，代码怎么写？（3）要求把所有 `0` 聚集，答案会变吗？

## A
1. **非环形**：去掉取模，窗口起点只取 `0..n-k`，其余完全一样。

```python
def min_swaps_linear(nums: list[int]) -> int:
    n, ones = len(nums), sum(nums)
    window = sum(nums[:ones])
    best = window
    for i in range(ones, n):               # 右端 i 不越界，起点 1..n-ones
        window += nums[i] - nums[i - ones]
        best = max(best, window)
    return ones - best
```

   `[1,1,0,0,1]` → `1`，`[0,1,0,1,1,0,0]` → `1`。
2. **前缀和**：把数组拼两遍，起点 `i` 的窗口里 `1` 的个数是 `pref[i + ones] - pref[i]`。

```python
from itertools import accumulate


def min_swaps_prefix(nums: list[int]) -> int:
    n, ones = len(nums), sum(nums)
    pref = list(accumulate(nums + nums, initial=0))
    return ones - max(pref[i + ones] - pref[i] for i in range(n))
```

   `[0,1,0,1,1,0,0]` → `1`，`[1,1,0,0,1]` → `0`。`accumulate(…, initial=0)` 让 `pref[0] = 0`，窗口和不需要特判起点。空间 `O(n)`，时间 `O(n)`。
3. **聚集所有 `0`**：答案不变。在环上，`1` 连成一段当且仅当 `0` 也连成一段，两个目标状态完全相同，所以最少交换数相同。

**Python 提醒**：`nums + nums` 创建一份新的 `2n` 列表，`10^5` 的规模可以接受；更省内存的写法是用 `itertools.chain` 或直接 `% n` 取下标。`sum(nums[:ones])` 切片会复制 `ones` 个元素，`ones = 0` 时是空切片，`sum` 得 `0`，无需特判。
