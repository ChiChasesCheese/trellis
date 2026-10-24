---
id: tlc-patterns-two-pointers-2-template
node: patterns.two-pointers
type: qa
step: 2
---
## Q
**双指针（Two Pointers）｜模板**

写出「排序后固定一个数、对剩下部分相向双指针」的三数之和（LC 15），以及接雨水（LC 42）的双指针版。

## A
```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res: list[list[int]] = []
    n = len(nums)
    for i in range(n - 2):
        if i and nums[i] == nums[i - 1]:
            continue                       # 第一个数去重
        if nums[i] > 0:
            break                          # 最小的数已 > 0，不可能再凑出 0
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1                     # 和太小：左端换更大的
            elif s > 0:
                r -= 1                     # 和太大：右端换更小的
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1                 # 第二个数去重
    return res
```

运行：`[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`；`[0,1,1]` → `[]`；`[0,0,0,0]` → `[[0,0,0]]`。时间 `O(n^2)`（排序 `O(n log n)` 可忽略），空间 `O(1)`（不计输出）。

```python
def trap(height: list[int]) -> int:
    l, r = 0, len(height) - 1
    lmax = rmax = water = 0
    while l < r:
        if height[l] < height[r]:          # 左边更矮：左边的水位只取决于 lmax
            lmax = max(lmax, height[l])
            water += lmax - height[l]
            l += 1
        else:
            rmax = max(rmax, height[r])
            water += rmax - height[r]
            r -= 1
    return water
```

运行：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`；`[4,2,0,3,2,5]` → `9`；`[]` → `0`。时间 `O(n)`，空间 `O(1)`。
