---
slug: max-consecutive-ones-iii
---
## Q
**LC 1004 最大连续1的个数 III**｜Medium

二进制数组 `nums` 最多可把 `k` 个 `0` 翻成 `1`，求连续 `1` 的最大个数。

## A
**一句话。** 等价于找至多含 `k` 个 `0` 的最长子数组：滑动窗口，`0` 超过 `k` 就收缩左端。

```python
def longest_ones(nums, k):
    best = left = zeros = 0    # zeros：窗口内 0 的个数
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:       # 0 太多，缩左端
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `while zeros > k` 写成 `>= k`：少算一个，示例 `[1,1,1,0,0,0,1,1,1,1,0]`、`k=2` 得 `5`，应为 `6`。
- 缩左端时直接 `zeros -= 1`：要先判断被移出的元素是不是 `0`，否则计数错位。

**追问。**
- 数据流、不能回看旧元素？：只存窗口里 `0` 的下标（`deque`，至多 `k` 个），超出时 `left = popleft() + 1`。
- 删掉一个元素后最长全 1 子数组（LC 1493）？：窗口至多含一个 `0`，答案取窗口长度减一。

**同模式。** LC 487 最大连续1的个数 II、LC 1493 删掉一个元素以后全为1的最长子数组、LC 424 替换后的最长重复字符、LC 3 无重复字符的最长子串
