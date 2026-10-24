---
id: tlc-python-bisect-sorted-2-boundary-queries
node: python.bisect-sorted
type: qa
step: 2
---
## Q
**Python 工具箱｜用 `bisect` 一次写对四种边界查询**

在有序数组中：第一个 `>= x`、第一个 `> x`、最后一个 `<= x`、最后一个 `< x`，分别怎样用 `bisect` 表达？LC 34「排序数组中查找元素的第一个和最后一个位置」怎样写？

## A
| 要找的 | 下标 |
|---|---|
| 第一个 `>= x`（下界 lower bound） | `bisect_left(a, x)` |
| 第一个 `> x`（上界 upper bound） | `bisect_right(a, x)` |
| 最后一个 `<= x` | `bisect_right(a, x) - 1` |
| 最后一个 `< x` | `bisect_left(a, x) - 1` |

前两个可能得到 `len(a)`，后两个可能得到 `-1`，取值前都要判断。

```python
from bisect import bisect_left, bisect_right
def search_range(nums: list[int], target: int) -> list[int]:
    i = bisect_left(nums, target)                       # 第一个 >= target
    if i == len(nums) or nums[i] != target:             # 越界或不相等：不存在
        return [-1, -1]
    return [i, bisect_right(nums, target) - 1]          # 最后一个 <= target
print(search_range([5, 7, 7, 8, 8, 10], 8))   # [3, 4]
print(search_range([5, 7, 7, 8, 8, 10], 6))   # [-1, -1]
print(search_range([], 0))                    # [-1, -1]
```

- 「存在性」永远是两步：先 `bisect_left` 得到下标，再检查 `i < len` 且 `a[i] == x`。
- 向下取整（floor）/ 向上取整（ceiling）：`a[bisect_right(a, x) - 1]` 是不超过 `x` 的最大值，`a[bisect_left(a, x)]` 是不小于 `x` 的最小值。
- 手写二分容易在循环边界和 `+1/-1` 上出错；库函数把「找第一个满足条件的位置」封装好，面试里可以先用它写出正确答案，再被要求时手写。

**坑**：`bisect_right(a, x) - 1` 在 `x` 比所有元素都小时是 `-1`，而 Python 下标 `a[-1]` 不会报错、会取到最后一个元素，必须显式判断 `>= 0`。
