---
id: tlc-maximum-value-at-a-given-index-in-a-bounded-array-2-code
node: b.maximum-value-at-a-given-index-in-a-bounded-array
type: qa
step: 2
---
## Q
**LC 1802 有界数组中指定下标处的最大值**｜写出 Python 实现

整数 `n`、`index`、`max_sum`（`1 <= n <= max_sum <= 10^9`，`0 <= index < n`）。构造长为 `n` 的正整数数组，相邻元素差的绝对值不超过 `1`，元素和不超过 `max_sum`，使 `nums[index]` 最大。返回这个最大值。

## A
**思路。** 二分峰值 `v`。`total(v)` 是峰值取 `v` 时数组的最小和：峰 + 左侧最小和 + 右侧最小和，每侧是从 `v-1` 逐格递减、到 `1` 后补 `1` 的数列；找满足 `total(v) <= max_sum` 的最大 `v`。

```python
def max_value(n: int, index: int, max_sum: int) -> int:
    def side(peak: int, length: int) -> int:
        # 峰值一侧 length 个位置的最小和：从 peak-1 逐格降 1，降到 1 后全补 1
        if length >= peak - 1:
            return peak * (peak - 1) // 2 + (length - (peak - 1))
        return (peak - 1 + peak - length) * length // 2

    def total(peak: int) -> int:               # 峰值取 peak 时整个数组的最小和
        return peak + side(peak, index) + side(peak, n - 1 - index)

    lo, hi = 1, max_sum                        # 单调：peak 越大 total 越大
    while lo < hi:
        mid = (lo + hi + 1) // 2               # 上取整，避免 lo = mid 时死循环
        if total(mid) <= max_sum:
            lo = mid                           # mid 放得下，答案至少是 mid
        else:
            hi = mid - 1
    return lo
```

运行：`(4, 2, 6)` → `2`，`(6, 1, 10)` → `3`，`(1, 0, 1)` → `1`，`(3, 0, 3)` → `1`，`(5 * 10^8, 0, 10^9)` → `31623`，`(10^9, 0, 10^9)` → `1`。

**复杂度。** 时间 `O(log max_sum)`；空间 `O(1)`。

**写法要点。** 内层函数 `side` / `total` 直接读取外层的 `n`、`index`，二分主体只剩一个单调判定。求“最大可行”的二分模板：`mid` 上取整、可行就 `lo = mid`、不可行就 `hi = mid - 1`，循环条件 `lo < hi`。Python 整数不会溢出，`peak * (peak - 1)` 在 `10^9` 量级也没问题；用 `//` 做整数除法，乘积一定是偶数所以不丢精度。`total(1)` 恰为 `n`，题目保证 `n <= max_sum`，所以 `lo = 1` 永远可行。
