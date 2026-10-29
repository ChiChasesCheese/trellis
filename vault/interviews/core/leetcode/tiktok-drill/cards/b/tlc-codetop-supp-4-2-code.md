---
id: tlc-codetop-supp-4-2-code
node: b.codetop-supp-4
type: qa
step: 2
---
## Q
**补充题4 手撕快速排序**｜写出 Python 实现

整数数组 `nums`（长度 `1..50000`，值在 `[-50000, 50000]`，可能有大量重复）。不调用内置排序，用快速排序原地升序排列并返回，要求不会因为有序或全相同的输入而退化。

## A
**思路。** `quicksort(lo, hi)` 排序半开区间 `nums[lo:hi]`。随机取一个基准值，三路划分：`[lo, lt)` 小于基准，`[lt, i)` 等于基准，`[gt, hi)` 大于基准，`i` 扫描中间未知的部分。划分完，等于基准的那段已经就位，只需要处理 `[lo, lt)` 和 `[gt, hi)`。递归较短的一侧，对较长的一侧更新 `lo` 或 `hi` 后继续 `while` 循环。

```python
import random


def sort_array(nums: list[int]) -> list[int]:
    def quicksort(lo: int, hi: int) -> None:        # 原地排序 nums[lo:hi]
        while hi - lo > 1:
            pivot = nums[random.randrange(lo, hi)]  # 随机基准：不怕有序输入
            lt, i, gt = lo, lo, hi      # 三路划分：[lo,lt) < pivot，[lt,i) == pivot，[gt,hi) > pivot
            while i < gt:
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1
                    i += 1
                elif nums[i] > pivot:
                    gt -= 1
                    nums[i], nums[gt] = nums[gt], nums[i]   # 换来的数还没看过，i 不动
                else:
                    i += 1
            if lt - lo < hi - gt:       # 递归较短的一侧，循环处理较长的一侧：栈深 O(log n)
                quicksort(lo, lt)
                lo = gt
            else:
                quicksort(gt, hi)
                hi = lt

    quicksort(0, len(nums))
    return nums
```

运行：`[5,2,3,1]` → `[1, 2, 3, 5]`，`[5,1,1,2,0,0]` → `[0, 0, 1, 1, 2, 5]`，`[1]` → `[1]`，`[2,2,2]` → `[2, 2, 2]`；`5 * 10^4` 个元素的随机、全相同、升序、降序、先升后降、只有 4 种取值的数组都能正确排序，每个都在零点几秒内完成。

**复杂度。** 期望时间 `O(n log n)`：随机基准下，每轮划分的期望规模是均匀分布的；最坏 `O(n^2)`，概率极小。空间 `O(log n)`：递归栈。

**写法要点。** `random.randrange(lo, hi)` 在 `[lo, hi)` 里取下标，与半开区间一致；三路划分只做一趟扫描，每个元素最多交换一次；`nums[i], nums[gt] = nums[gt], nums[i]` 在 `gt -= 1` 之后写，才能取到最后一个未处理的位置；`while hi - lo > 1` 里改变 `lo` 或 `hi` 来代替对较长一侧的递归，是手动做的尾递归消除；函数返回 `nums` 自身，原地修改的同时满足「返回排序后数组」的要求。
