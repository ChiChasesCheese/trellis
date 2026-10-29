---
id: tlc-binary-search-4-followup
node: a.binary-search
type: qa
step: 4
---
## Q
**LC 704 二分查找**｜追问

面试官接着问：（1）数组里有重复元素，怎么找第一个 / 最后一个出现的位置？（2）标准库有现成的吗，怎么用？（3）如果数组是「旋转过的有序数组」？

## A
1. **重复元素**：循环里只判断 `nums[mid] < target`，退出时 `lo` 就是第一个 `>= target` 的位置（`bisect_left`）。最后一个出现的位置是「第一个 `> target` 的位置减一」，即把条件改成 `nums[mid] <= target`（`bisect_right`），再减一。
2. **标准库 `bisect`**：`bisect_left(a, x)` 返回第一个 `>= x` 的插入点，`bisect_right(a, x)` 返回第一个 `> x` 的插入点，都是 `O(log n)`。

```python
from bisect import bisect_left

def search_bisect(nums: list[int], target: int) -> int:
    i = bisect_left(nums, target)          # 第一个 >= target 的位置
    return i if i < len(nums) and nums[i] == target else -1
```

结果与手写版一致：`([-1,0,3,5,9,12], 9)` → `4`，`([-1,0,3,5,9,12], 2)` → `-1`。Python 3.10 起还可以传 `key=`，比如 `bisect_left(range(n), x, key=lambda i: f(i))`，把"单调的判定函数"当作虚拟数组二分。
3. **旋转有序数组（LC 33）**：每次用中点把区间分成一段有序、一段无序；判断 `target` 是否落在有序那一段，是就去那一段，否则去另一段，仍是 `O(log n)`。

**Python 提醒**：`bisect` 不检查输入是否有序，对无序列表也会返回一个值而不报错；`bisect_left` 返回的是**插入点**，不保证元素存在，要自己再验证 `a[i] == x`。
