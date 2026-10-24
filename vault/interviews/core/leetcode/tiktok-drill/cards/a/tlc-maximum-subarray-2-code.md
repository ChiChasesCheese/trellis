---
id: tlc-maximum-subarray-2-code
node: a.maximum-subarray
type: qa
step: 2
---
## Q
**LC 53 最大子数组和**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`），返回和最大的连续子数组（至少一个元素）的和，要求 `O(n)` 时间。

## A
**思路。** `cur` 是以当前元素结尾的最大子数组和，`best` 是目前见过的最大值。两者都从第一个元素开始；之后每读到 `x`，`cur` 取「自己单独成段」和「接在前面后面」中较大的，再用 `cur` 刷新 `best`。

```python
from itertools import islice


def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]                # cur：以当前元素结尾的最大子数组和
    for x in islice(nums, 1, None):     # 跳过首元素，又不拷贝切片
        cur = max(x, cur + x)           # 接在前面后面，或者从 x 重新开始
        best = max(best, cur)
    return best
```

运行：`[-2,1,-3,4,-1,2,1,-5,4]` → `6`，`[1]` → `1`，`[5,4,-1,7,8]` → `23`，`[-3,-1,-2]` → `-1`。

**复杂度。** 时间 `O(n)`：每个元素常数次操作；空间 `O(1)`：两个变量。

**写法要点。** 用 `nums[0]` 而不是 `0` 或 `-inf` 初始化，保证至少选一个元素，也不需要 `float` 的无穷大；`islice(nums, 1, None)` 惰性地跳过第 0 项，`nums[1:]` 则会拷贝 `O(n)` 的新列表；`best = cur = nums[0]` 链式赋值只适合整数这类不可变值；`max(x, cur + x)` 把「要不要接上前面」写成一次比较，比 `if cur < 0` 的分支更短。
