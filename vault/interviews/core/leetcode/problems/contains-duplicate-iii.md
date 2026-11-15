---
slug: contains-duplicate-iii
---
## Q
**LC 220 存在重复元素 III**｜Hard

给整数数组 `nums` 和 `k`（下标差上限）、`t`（值差上限）。是否存在下标 `i != j`，使 `|i-j| <= k` 且 `|nums[i]-nums[j]| <= t`？

## A
**一句话。** 桶排序：桶宽 `t+1`，同桶的两个数必满足，只需再看相邻两个桶；窗口外的下标对应的桶随时删掉。

```python
def contains_nearby_almost_duplicate(nums, k, t):
    w = t + 1                     # 同桶 => 差 <= t
    box = {}                      # 桶号 -> 桶里唯一的值
    for i, x in enumerate(nums):
        b = x // w                    # 向下取整，负数也对
        if b in box:
            return True
        if b - 1 in box and x - box[b - 1] <= t:
            return True
        if b + 1 in box and box[b + 1] - x <= t:
            return True
        box[b] = x
        if i >= k:                    # 滑出窗口的删掉
            del box[nums[i - k] // w]
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(min(n, k))`。

**易错点。**
- 桶宽取 `t`：`t = 0` 时除以零；宽度 `t + 1` 才保证同桶两数的差不超过 `t`。
- 用 `int(x / w)` 取整：负数朝零取整，`-1` 与 `1` 会落进同一个桶，要用 `//` 向下取整。
- 只查本桶：相邻桶里的数也可能满足，两侧要比较差值。

**追问。**
- 不用桶怎么做？：窗口内维护有序集合，查 `x` 的前驱和后继是否在 `t` 内，`O(n log k)`。
- 为什么桶里最多一个数？：窗口内同桶有两个数时早已返回 `True`。

**同模式。** LC 217 存在重复元素、LC 219 存在重复元素 II、LC 164 最大间距
