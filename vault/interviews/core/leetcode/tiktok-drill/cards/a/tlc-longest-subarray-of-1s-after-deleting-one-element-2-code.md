---
id: tlc-longest-subarray-of-1s-after-deleting-one-element-2-code
node: a.longest-subarray-of-1s-after-deleting-one-element
type: qa
step: 2
---
## Q
**LC 1493 删掉一个元素以后全为 1 的最长子数组**｜写出 Python 实现

`0/1` 数组 `nums`（长度 `1 ~ 10^5`），必须恰好删掉一个元素，求删完之后全是 `1` 的最长连续子数组的长度。要求 `O(n)`。

## A
**思路。** 维护窗口 `nums[left..right]`，保证其中至多一个 `0`。右端每吃进一个 `0`，计数加一；计数超过 `1` 时，左端前进，直到吐出一个 `0`。每步窗口长度是 `right - left + 1`，必须删掉一个元素，所以用 `right - left` 更新答案。

```python
def longest_subarray(nums: list[int]) -> int:
    left = zeros = best = 0                   # 窗口 nums[left..right] 里最多容纳 1 个 0
    for right, x in enumerate(nums):
        zeros += x == 0                       # bool 当 0/1 加
        while zeros > 1:                      # 超过一个 0：左端前进直到吐出一个 0
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left)        # 窗口长度 right-left+1，必须删掉一个元素，所以减 1
    return best
```

运行：`[1,1,0,1]` → `3`，`[0,1,1,1,0,1,1,0,1]` → `5`，`[1,1,1]` → `2`，`[0,0]` → `0`，`[1]` → `0`。

**复杂度。** 时间 `O(n)`：右端走 `n` 步，左端总共最多前进 `n` 步；空间 `O(1)`。

**写法要点。** `zeros += x == 0` 利用 `bool` 是 `int` 的子类，比 `if` 更紧凑；`zeros -= nums[left] == 0` 同理。`left = zeros = best = 0` 链式赋值只用于不可变的整数。用 `right - left` 直接把「删一个」折进长度，不另设变量。`for right, x in enumerate(nums)` 同时拿下标与值，避免 `nums[right]` 重复索引。
