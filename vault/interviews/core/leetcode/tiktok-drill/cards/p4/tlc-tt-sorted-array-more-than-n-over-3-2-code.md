---
id: tlc-tt-sorted-array-more-than-n-over-3-2-code
node: p4.tt-sorted-array-more-than-n-over-3
type: qa
step: 2
---
## Q
**有序数组中出现次数超过 n/3 的数**｜写出 Python 实现

非递减有序整数数组 `nums`（`3 <= n <= 10^6`），返回所有出现次数大于 `n / 3` 的数字，升序，时间低于 `O(n)`。

## A
**思路。** 次数大于 `n/3` 等价于至少 `step + 1` 次，`step = n // 3`。这样的值必然覆盖下标 `0, step, 2*step, ...` 之一，取这些下标上的值作为候选，对每个候选用 `bisect_right - bisect_left` 求出现次数，保留 `3 * 次数 > n` 的。

```python
from bisect import bisect_left, bisect_right


def more_than_third(nums: list[int]) -> list[int]:
    n = len(nums)
    step = n // 3                                        # 出现次数 > n/3，即至少 step + 1 次
    ans: list[int] = []
    for v in sorted({nums[i] for i in range(0, n, step)}):   # 候选：每隔 step 取一个下标上的值，至多 5 个
        if 3 * (bisect_right(nums, v) - bisect_left(nums, v)) > n:   # 整数比较避免 n / 3 的浮点
            ans.append(v)
    return ans
```

运行：`[1,2,3]` → `[]`；`[1,1,2,3,4]` → `[1]`；`[1,1,2,4,4]` → `[1, 4]`；`[1,2,3,4,5,6,7]` → `[]`；`[5,5,5]` → `[5]`；`[1,1,1,2,2,2]` → `[1, 2]`；`[1,1,2,2,3,3]` → `[]`。

**复杂度。** 时间 `O(log n)`；空间 `O(1)`（候选集合至多 `5` 个元素）。

**写法要点。** 集合推导式 `{nums[i] for i in range(0, n, step)}` 对重复的候选去重，避免对同一个值二分多次；`sorted(...)` 让结果升序；`bisect_right(nums, v) - bisect_left(nums, v)` 是 `v` 的出现次数，两次二分各 `O(log n)`；`3 * 次数 > n` 用整数乘法替代 `次数 > n / 3`，没有浮点误差；`n >= 3` 保证 `step >= 1`，`range` 的步长不会是 `0`。
