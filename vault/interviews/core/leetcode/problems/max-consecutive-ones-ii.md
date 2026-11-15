---
slug: max-consecutive-ones-ii
---
## Q
**LC 487 最大连续1的个数 II**｜Medium

给二进制数组 `nums`，最多可以把一个 `0` 翻成 `1`，求翻转后最长的连续 `1` 的个数。

## A
**一句话。** 滑动窗口：窗口内至多容纳一个 `0`，右端扩张、`0` 多于一个时左端收缩，窗口最大长度就是答案。

```python
def find_max_consecutive_ones(nums):
    ans = left = zeros = 0
    for right, x in enumerate(nums):
        zeros += x == 0              # 进窗口：数 0 的个数
        while zeros > 1:             # 超过一个 0：左端出窗口
            zeros -= nums[left] == 0
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把窗口收缩写成 `if`：一次可能要弹多个元素才能让 `zeros` 回到 1，必须 `while`。
- 左端出窗口时不判断是不是 `0`：`zeros` 会算错，要 `zeros -= nums[left] == 0`。
- 全是 `1` 的数组：没有 `0` 可翻，窗口一直扩张，答案就是 `n`。

**追问。**
- 数据流、不能回看历史怎么办？：只记前一段 `1` 的长度 `prev` 与当前段 `cur`，遇 `0` 时 `prev, cur = cur, 0`，答案是 `prev + cur + 1` 的最大值。
- 最多翻 `k` 个 `0` 呢？：把 `1` 改成 `k`，即 LC 1004。

**同模式。** LC 1004 最大连续1的个数 III、LC 485 最大连续 1 的个数、LC 1493 删掉一个元素以后全为 1 的最长子数组、LC 424 替换后的最长重复字符
