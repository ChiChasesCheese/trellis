---
slug: codetop-supp-4
---
## Q
**补充题4 手撕快速排序**｜Medium

不用内置排序，原地把整数数组升序排列，平均 `O(n log n)`，可能有大量重复元素。

## A
**一句话。** 快速排序：随机基准做三路划分，等于基准的段已就位，只递归较短一侧、循环较长一侧。

```python
def sort_array(nums):
    def quicksort(lo, hi):             # 排序 nums[lo:hi]
        while hi - lo > 1:
            pivot = nums[random.randrange(lo, hi)]
            lt, i, gt = lo, lo, hi   # <p | ==p | >p
            while i < gt:
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1
                    i += 1
                elif nums[i] > pivot:
                    gt -= 1
                    nums[i], nums[gt] = nums[gt], nums[i]
                else:
                    i += 1
            if lt - lo < hi - gt:      # 短的递归，栈深 O(log n)
                quicksort(lo, lt)
                lo = gt
            else:
                quicksort(gt, hi)
                hi = lt

    quicksort(0, len(nums))
    return nums
```

**复杂度。** 期望时间 `O(n log n)`，空间 `O(log n)`。

**易错点。**
- 末尾元素当基准的两路划分：升序输入 `RecursionError`，全相同的数退化为 `O(n^2)`。
- 换来 `gt` 位置的数后 `i` 也加一：换来的数还没检查，`[2,3,1]` 得 `[2,1,3]`。
- 区间开闭混用：半开区间 `[lo, hi)` 递归 `(lo, lt)`，写成 `lt - 1` 会漏元素。

**追问。**
- 第 K 大（LC 215）怎么做？：同样三路划分，只进入含目标下标的一侧，期望 `O(n)`。
- 怎么保证最坏情况？：递归过深切换堆排序（introsort）。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 75 颜色分类、LC 912 排序数组、LC 347 前 K 个高频元素
