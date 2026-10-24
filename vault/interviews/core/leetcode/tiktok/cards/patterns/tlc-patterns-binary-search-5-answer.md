---
id: tlc-patterns-binary-search-5-answer
node: patterns.binary-search
type: qa
step: 5
---
## Q
**二分查找（Binary Search）｜对答案二分的变形**

「最低运载能力」「有界数组中指定下标处的最大值」「第 k 个缺失的正整数」「矩阵中第 k 小」怎样转化为「找第一个 True」？

## A
步骤：**① 确定答案范围 → ② 写判定函数 `ok(x)` → ③ 套 `first_true`**。

**LC 1011 最低运载能力**（`ok` = 在 `days` 天内能运完）：范围 `[max(weights), sum(weights)]`。

```python
from typing import Callable
def first_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    while lo < hi:                         # [lo, hi) 上第一个 ok 为 True 的位置
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def ship_within_days(weights: list[int], days: int) -> int:
    def ok(cap: int) -> bool:
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:              # 装不下，新开一天
                d += 1
                cur = 0
            cur += w
        return d <= days
    return first_true(max(weights), sum(weights) + 1, ok)
print(ship_within_days([1,2,3,4,5,6,7,8,9,10], 5), ship_within_days([3,2,2,4,1,4], 3))   # 15 6
```

**其他题的转化：**
- **LC 1802**：`ok(v) = 以 v 为峰、两边每步减 1（不低于 1）的数组之和 <= maxSum`，要找最大的 `v`：先找第一个**不可行**的 `v`，再减 1。两侧之和用等差数列公式 `O(1)` 计算。`(n, index, maxSum) = (4, 2, 6)` → `2`。
- **LC 1539**：`arr[i] - (i + 1)` 是 `arr[i]` 之前缺失的个数，单调不减。找第一个 `>= k` 的 `i`，答案 `i + k`。`([2,3,4,7,11], 5)` → `9`。
- **LC 69**：第一个 `m * m > x` 的 `m` 减 1。`8` → `2`。
- **LC 378**：值域 `[matrix[0][0], matrix[-1][-1]]`，`ok(x) = 矩阵中 <= x 的个数 >= k`；计数从左下角走，`O(n)`；总 `O(n log 值域)`，空间 `O(1)`。`([[1,5,9],[10,11,13],[12,13,15]], 8)` → `13`。

识别：一个整数范围 + 一个能在 `O(n)` 内回答「x 行不行」的函数 → 对答案二分。
