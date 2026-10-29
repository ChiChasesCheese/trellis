---
id: tlc-sort-an-array-4-followup
node: b.sort-an-array
type: qa
step: 4
---
## Q
**LC 912 排序数组**｜追问

面试官接着问：（1）写一个快排，怎样避免最坏情况？（2）需要稳定排序怎么办？（3）值域只有 `10^5` 种有没有更快的办法？（4）数据放不进内存？

## A
1. **三路快排 + 随机基准**：随机选基准避开固定输入的最坏情况；三路划分（小于 / 等于 / 大于）一次把所有等于基准的元素放好，重复值多时不退化；循环加显式栈，先压较大的一段，栈深度 `O(log n)`。

```python
import random


def quick_sort(nums: list[int]) -> list[int]:
    stack = [(0, len(nums) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot = nums[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi          # nums[lo:lt] < pivot, nums[lt:i] == pivot, nums[gt+1:] > pivot
        while i <= gt:
            if nums[i] < pivot:
                nums[lt], nums[i] = nums[i], nums[lt]
                lt += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1
            else:
                i += 1
        left, right = (lo, lt - 1), (gt + 1, hi)
        if left[1] - left[0] > right[1] - right[0]:
            stack += [left, right]      # 较大的一段先入栈，后处理
        else:
            stack += [right, left]
    return nums
```

`5 * 10^4` 个全相同的数约 `0.001` 秒。
2. **稳定排序**：归并排序，相等时取左边的元素；额外空间 `O(n)`。
3. **计数排序**：值域 `V = 10^5 + 1`，时间 `O(n + V)`，不基于比较，所以可以快过 `n log n` 的下界。

```python
def counting_sort(nums: list[int]) -> list[int]:
    offset = 50000
    cnt = [0] * (2 * offset + 1)
    for x in nums:
        cnt[x + offset] += 1
    return [v - offset for v, c in enumerate(cnt) for _ in range(c)]
```

`counting_sort([5,2,3,1,-1])` → `[-1,1,2,3,5]`。
4. **外部排序**：分块读入内存、各自排序写成有序文件，再用 k 路归并（堆）合并。

**Python 提醒**：`list.sort()` 和 `sorted()` 用的是 Timsort（稳定、对部分有序数据接近线性），生产代码就用它们；题面禁用内置排序，所以手写；递归写法要留意默认递归上限 `1000`，`sys.setrecursionlimit` 只是推迟问题，改成循环才是根治。
