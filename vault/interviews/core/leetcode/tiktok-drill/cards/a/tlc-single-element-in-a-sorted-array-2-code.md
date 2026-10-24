---
id: tlc-single-element-in-a-sorted-array-2-code
node: a.single-element-in-a-sorted-array
type: qa
step: 2
---
## Q
**LC 540 有序数组中的单一元素**｜写出 Python 实现

有序整数数组 `nums`（长度 `1` 到 `10^5`，元素 `0` 到 `10^5`），除了一个数只出现一次之外，其余每个数恰好出现两次。返回那个只出现一次的数。要求 `O(log n)` 时间、`O(1)` 空间。

## A
**思路。** 在偶数下标上二分。`mid` 对齐到偶数后，若 `nums[mid] == nums[mid + 1]`，这一对完整，单一元素在右边（`lo = mid + 2`）；否则在 `mid` 或左边（`hi = mid`）。循环结束时 `lo == hi` 就是单一元素的下标。

```python
def single_non_duplicate(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1               # lo、hi 始终是偶数下标
    while lo < hi:
        mid = (lo + hi) // 2
        mid -= mid & 1                      # 对齐到偶数下标：mid 必是某一对的左端（或单一元素）
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2                    # 这一对完整：单一元素在右边
        else:
            hi = mid                        # 这一对已被打破：单一元素在 mid 或更左
    return nums[lo]
```

运行：`[1,1,2,3,3,4,4,8,8]` → `2`，`[3,3,7,7,10,11,11]` → `10`，`[5]` → `5`，`[1,2,2]` → `1`，`[1,1,2]` → `2`。

**复杂度。** 时间 `O(log n)`：每轮区间减半；空间 `O(1)`。

**写法要点。**
- `mid -= mid & 1`：`mid & 1` 是最低位（奇数为 `1`），一步把奇数 `mid` 退到前一个偶数，比 `if mid % 2: mid -= 1` 短。
- `mid + 1` 不会越界：`lo < hi` 且二者都是偶数，所以 `mid < hi`，`mid + 1 <= hi`。
- `lo = mid + 2` 跨过一整对，保持 `lo` 为偶数；`hi = mid` 保持 `hi` 为偶数。
- 等价的无对齐写法：`if nums[mid] == nums[mid ^ 1]: lo = mid + 1 else: hi = mid`，`mid ^ 1` 取同一对里的另一个下标。
- 标准库写法：`i = bisect_left(range(len(nums) // 2), True, key=lambda i: nums[2 * i] != nums[2 * i + 1])`，返回 `nums[2 * i]`；`range` 支持随机访问，所以能直接传给 `bisect`（`key` 需要 Python 3.10 以上）。
