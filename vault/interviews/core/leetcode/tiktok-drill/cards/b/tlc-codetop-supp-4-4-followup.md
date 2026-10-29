---
id: tlc-codetop-supp-4-4-followup
node: b.codetop-supp-4
type: qa
step: 4
---
## Q
**补充题4 手撕快速排序**｜追问

面试官接着问：（1）只要第 `K` 大的元素，不需要全部排序（LC 215）？（2）快排是稳定的吗，怎么做到稳定？（3）最坏情况能不能保证 `O(n log n)`？

## A
1. **快速选择**：同样的三路划分，但只进入包含目标下标的那一侧；若目标落在「等于基准」的那段，直接返回基准。期望 `O(n)`。

```python
import random


def find_kth_largest(nums: list[int], k: int) -> int:
    target = len(nums) - k              # 升序排好后第 k 大所在的下标
    lo, hi = 0, len(nums)
    while True:
        pivot = nums[random.randrange(lo, hi)]
        lt, i, gt = lo, lo, hi
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
        if target < lt:
            hi = lt
        elif target >= gt:
            lo = gt
        else:
            return pivot
```

2. **稳定性**：快排的交换会打乱相同值的先后顺序，不稳定。要稳定就用归并排序，或者给元素加上原始下标当第二关键字。Python 的 `list.sort()` 是稳定的 Timsort。
3. **最坏情况**：随机基准只是让最坏情况概率极小。要硬性保证，可用「中位数的中位数」选基准（常数大），或像 introsort 那样，递归深度超过 `2 log n` 时切换到堆排序。

**Python 提醒**：`list.sort()` 原地排序并返回 `None`，`sorted(x)` 返回新列表；`nums = nums.sort()` 会把 `nums` 变成 `None`。手撕题里函数返回排好序的 `nums` 自身。递归深度默认上限约 `1000`，快排不控制深度时容易触顶。
