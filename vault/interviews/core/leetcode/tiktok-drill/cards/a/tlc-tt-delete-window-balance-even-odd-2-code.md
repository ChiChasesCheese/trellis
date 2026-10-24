---
id: tlc-tt-delete-window-balance-even-odd-2-code
node: a.tt-delete-window-balance-even-odd
type: qa
step: 2
---
## Q
**删除一个长度为 k 的窗口，使奇偶下标之和相等**｜写出 Python 实现

写 `min_balanced_deletion(nums, k)`：删除一段长度为 `k` 的连续子数组，剩余元素保持顺序并重新编号，使偶数下标元素之和等于奇数下标元素之和；返回最小起点，没有则返回 `-1`，删空时算满足。`1 <= k <= len(nums) <= 10^5`，`-10^4 <= nums[i] <= 10^4`。

## A
**思路。** 构造带符号的前缀和 `pre`（偶数下标加、奇数下标减，带 `initial=0`）。枚举起点 `i`：左边贡献 `pre[i]`，右边贡献 `±(pre[n] - pre[i+k])`，`k` 为奇数时取负号；两者之和为 `0` 即满足。

```python
from itertools import accumulate


def min_balanced_deletion(nums: list[int], k: int) -> int:
    """删除一段长度 k 的连续子数组，使剩余数组偶数下标之和等于奇数下标之和；返回最小起点，没有则返回 -1。"""
    n = len(nums)
    # pre[i]：nums[:i] 按原下标奇偶加符号的和（偶 +，奇 -）。pre[n] 是整个数组的「偶数下标和 - 奇数下标和」
    pre = list(accumulate((x if i % 2 == 0 else -x for i, x in enumerate(nums)), initial=0))
    flip = -1 if k % 2 else 1                    # 窗口右边的元素整体左移 k 位：k 为奇数时奇偶互换，符号翻转
    for i in range(n - k + 1):
        left = pre[i]                            # 窗口左边：下标不变
        right = flip * (pre[n] - pre[i + k])     # 窗口右边：下标减 k
        if left + right == 0:
            return i
    return -1
```

运行：`([1,1,2,3,4,4], 2)` → `2`，`([1,1,2,1,1], 1)` → `2`，`([1,2], 2)` → `0`，`([3,1,4,1,5], 1)` → `-1`，`([1,1,2,2,3], 1)` → `4`，`([1,1,1,2,1], 1)` → `3`，`([1,1,1,2,1], 3)` → `1`；`10^5` 个元素瞬间完成。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**写法要点。**
- `itertools.accumulate(生成器, initial=0)`：一行得到带 `0` 开头的前缀和，`pre[i]` 恰好是前 `i` 个元素的和，不需要手写循环；`initial` 参数 3.8 起可用。
- 生成器表达式 `(x if i % 2 == 0 else -x for i, x in enumerate(nums))` 直接把符号编进去，不建中间列表。
- `flip = -1 if k % 2 else 1`：奇偶翻转只取决于 `k`，循环外算一次。
- `range(n - k + 1)`：起点最大是 `n - k`（删掉末尾），包含它。
