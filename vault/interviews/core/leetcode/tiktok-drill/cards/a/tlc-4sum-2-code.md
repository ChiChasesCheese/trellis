---
id: tlc-4sum-2-code
node: a.4sum
type: qa
step: 2
---
## Q
**LC 18 四数之和**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 200`，`-10^9 <= nums[i] <= 10^9`）和 `target`（`-10^9 <= target <= 10^9`），返回所有和为 `target` 且不重复的四元组，顺序不限。

## A
**思路。** 排序后用两层循环固定前两个数，第三、第四个数用对撞双指针找。排序让相同值相邻：前两层遇到与前一个相同的值就跳过，找到解后左指针跳过重复值。再用有序性做两个剪枝，常数更小。

```python
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:           # 第一个数去重
            continue
        if sum(nums[i:i + 4]) > target:                # 最小的四数之和已超过：之后只会更大
            break
        if nums[i] + sum(nums[-3:]) < target:          # 与最大的三个数相加仍不够：换更大的 i
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:   # 第二个数去重：注意是 j > i + 1
                continue
            if nums[i] + sum(nums[j:j + 3]) > target:
                break
            if nums[i] + nums[j] + sum(nums[-2:]) < target:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[j] + nums[lo] + nums[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    result.append([nums[i], nums[j], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:   # 跳过重复的第三个数
                        lo += 1
    return result
```

运行：`[1,0,-1,0,-2,2], 0` → `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`，`[2,2,2,2,2], 8` → `[[2,2,2,2]]`，`[0,0,0,0], 0` → `[[0,0,0,0]]`，`[1,2,3], 6` → `[]`，`[10^9,10^9,-10^9,-10^9], 0` → `[[-1000000000,-1000000000,1000000000,1000000000]]`。

**复杂度。** 时间 `O(n^3)`，`n = 200` 约 `8 * 10^6` 步；空间 `O(1)` 额外。

**写法要点。** `sorted(nums)` 不改动输入；`sum(nums[i:i + 4])`、`sum(nums[-3:])` 用切片写剪枝，比手写四项相加好读；去重一律「和前一个比较」而不是用 `set`，既省空间又保证输出有序；`range(n - 3)` 和 `range(i + 1, n - 2)` 的上界直接保证后面还有足够多的数。
