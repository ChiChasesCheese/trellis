---
id: tlc-maximum-product-of-three-numbers-0-whole
node: c.maximum-product-of-three-numbers
type: qa
---
## Q
**LC 628 三个数的最大乘积**｜Easy · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2021-08-24（国内 CodeTop）

给你一个整型数组 `nums`，在数组中找出由三个数组成的最大乘积并返回。`3 <= nums.length <= 10^4`，`-1000 <= nums[i] <= 1000`。例：`nums = [1,2,-3]` → `-6`；`nums = [1,2,3,4]` → `24`；`nums = [-1,-2,-3]` → `-6`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 最大乘积只可能是「最大的三个数」或「最小的两个数（两个负数）乘最大的一个数」，取两者较大者；用堆工具函数一趟找出这 5 个数，`O(n)`。

**识别。** 「选 k 个数使乘积最大 + 有负数」：负负得正，极端值只会出现在数组的两端。看到负数和乘积，先想「两个最小的负数」这条分支。

**推导。** 暴力：三重循环枚举，`O(n³)`。排序后乘积的候选只有两个：末尾三个，或开头两个与末尾一个；`n = 10^4` 排序就够，但只需要 5 个极值，不必全排序。`heapq.nlargest(3, nums)` 与 `heapq.nsmallest(2, nums)` 内部维护大小为 `k` 的堆，对固定的 `k` 是 `O(n)`。

**简单解法。** 排序后在两个候选里取大者。

```python
def maximum_product_sort(nums: list[int]) -> int:
    nums = sorted(nums)
    return max(nums[-1] * nums[-2] * nums[-3],   # 三个最大的数
               nums[0] * nums[1] * nums[-1])     # 两个最小的（可能是负数）乘最大的
```

`O(n log n)`，空间 `O(n)`；已经足够通过，是首选开场答案，面试官通常追问不排序怎么做。

最优解：

```python
from heapq import nlargest, nsmallest


def maximum_product(nums: list[int]) -> int:
    big = nlargest(3, nums)                      # 降序：big[0] 最大
    small = nsmallest(2, nums)                   # 升序：small[0] 最小
    return max(big[0] * big[1] * big[2],         # 全取最大的三个
               small[0] * small[1] * big[0])     # 两个最小的负数相乘变成正数，再配最大的一个
```

运行：`[1,2,-3]` → `-6`，`[1,2,3,4]` → `24`，`[-1,-2,-3]` → `-6`；`[-10,-10,1,3,2]` → `300`，`[0,0,0]` → `0`，`[-1000,-1000,1000]` → `1000000000`。

**复杂度。** 时间 `O(n)`（`k` 为常数），空间 `O(1)`。

**拓展优化。**
- 手写一趟扫描，不借助堆，常数更小。

```python
from math import inf


def maximum_product_scan(nums: list[int]) -> int:
    mx1 = mx2 = mx3 = -inf                       # 最大、次大、第三大
    mn1 = mn2 = inf                              # 最小、次小
    for x in nums:
        if x > mx1:
            mx1, mx2, mx3 = x, mx1, mx2          # 新的最大值把旧的依次挤下去
        elif x > mx2:
            mx2, mx3 = x, mx2
        elif x > mx3:
            mx3 = x
        if x < mn1:
            mn1, mn2 = x, mn1
        elif x < mn2:
            mn2 = x
    return int(max(mx1 * mx2 * mx3, mn1 * mn2 * mx1))
```

**易错点。**
- 只取最大的三个：`[-10,-10,1,3,2]` 得到 `6`，正确是 `300`。
- `nums` 恰好 3 个数时，两个分支是同一个乘积，不要因为「最小的两个」与「最大的三个」重叠而去重。
- 扫描法里最大值的初值设成 `0`：全是负数时 `0` 永远赢，`[-1,-2,-3]` 得到 `0`，正确是 `-6`。

**追问。**
- 选 `k` 个数：排序后每次从两端各取一个相乘，枚举从左取多少对（偶数个）。
- 求最大乘积的子数组（LC 152）：换成同时维护最大与最小值的 DP。

**同模式。** LC 152 乘积最大子数组、LC 215 数组中的第K个最大元素、LC 414 第三大的数、LC 1464 数组中两元素的最大乘积、LC 1913 两个数对之间的最大乘积差。
