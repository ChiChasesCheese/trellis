---
slug: longest-subarray-of-1s-after-deleting-one-element
---
## Q
**LC 1493 删掉一个元素以后全为 1 的最长子数组**｜Medium

二进制数组 `nums` 必须删除一个元素，返回删除后仅含 `1` 的最长子数组长度。

## A
**一句话。** 滑动窗口最多容纳一个 `0`（被删的那个），答案是窗口长度减 1。

```python
def longest_subarray(nums):
    left = zeros = best = 0
    for r, x in enumerate(nums):
        zeros += x == 0
        while zeros > 1:               # 超过一个 0，左端前进
            zeros -= nums[left] == 0
            left += 1
        best = max(best, r - left)     # 窗口长度减去被删的一个
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 忘了「必须删一个」：写 `r - left + 1`，`[1,1,1]` 得 `3`，应为 `2`。
- 条件写成 `zeros > 0`：窗口里一个 `0` 都不容，`[1,1,0,1]` 得 `1`，应为 `3`。
- 收缩左端只改 `left` 不更新 `zeros`：计数和窗口脱节。

**追问。**
- 最多删 `k` 个？：条件改成 `zeros > k`，答案取窗口里 `1` 的个数。
- 流式读入怎么做？：只记前一段 `1` 和当前段 `1` 两个数，遇 `0` 时交接，`O(1)` 空间。

**同模式。** LC 1004 最大连续 1 的个数 III、LC 487 最大连续 1 的个数 II、LC 424 替换后的最长重复字符、LC 3 无重复字符的最长子串
