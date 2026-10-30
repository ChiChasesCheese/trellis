---
id: tlc-maximum-subarray-4-followup
node: p3.maximum-subarray
type: qa
step: 4
---
## Q
**LC 53 最大子数组和**｜追问

面试官接着问：（1）要返回最大子数组的**位置**（起止下标）？（2）进阶要求的**分治**解法怎么做？（3）数组是**环形**的（首尾相连）怎么办？

## A
1. **返回位置**：`cur < 0` 时丢掉前面，记下新的起点 `start`；每次刷新 `best` 时同时记下 `start` 和当前下标。

```python
def max_sub_array_range(nums: list[int]) -> tuple[int, int, int]:
    best = cur = nums[0]
    start = best_l = best_r = 0
    for i in range(1, len(nums)):
        if cur < 0:                     # 前面的和是负担：丢掉，从 i 重新开始
            cur, start = nums[i], i
        else:
            cur += nums[i]
        if cur > best:
            best, best_l, best_r = cur, start, i
    return best, best_l, best_r
```

   `[-2,1,-3,4,-1,2,1,-5,4]` → `(6, 3, 6)`，即 `nums[3:7] = [4,-1,2,1]`。
2. **分治**：每段返回四元组（总和、最大前缀、最大后缀、最大子段）。合并时最大子段取 `max(左.最大子段, 右.最大子段, 左.最大后缀 + 右.最大前缀)`。总时间 `O(n)`，递归深度 `O(log n)`；它的价值是可以并行，也是线段树维护区间最大子段和的做法。
3. **环形（LC 918）**：答案是 `max(普通最大子段和, 总和 - 最小子段和)`；后者对应「跨越首尾」的情形。若所有数都是负数，`总和 - 最小子段和` 会得到空集 `0`，要特判：普通最大子段和为负时直接返回它。`[5,-3,5]` → `10`。

**Python 提醒**：`itertools.accumulate(nums)` 直接给出前缀和序列，配合「到目前为止的最小前缀」可以写成前缀和版本；`max(nums)` 在全负数组上就是答案，可以用来快速特判。
