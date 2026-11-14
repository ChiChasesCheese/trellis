---
slug: maximize-the-confusion-of-an-exam
---
## Q
**LC 2024 考试的最大困扰度**｜Medium

`T/F` 串 `answerKey`，最多改 `k` 个字符，求最长连续相同字符的长度。

## A
**一句话。** 分别以全 `T`、全 `F` 为目标做不定长滑窗：窗口里非目标字符超过 `k` 个就移左端。

```python
def max_consecutive_answers(answer_key, k):
    def longest(target):
        left = bad = ans = 0
        for right, ch in enumerate(answer_key):
            bad += ch != target          # 需要改的个数
            while bad > k:
                bad -= answer_key[left] != target
                left += 1
            ans = max(ans, right - left + 1)
        return ans

    return max(longest('T'), longest('F'))
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只算一种目标：`"FFT"`、`k = 0` 时全 `T` 只得 `1`，应为 `2`。
- 收缩时减错：要减去「左端是否是非目标字符」，不是无条件减一。

**追问。**
- 一遍扫完？：窗口里 `T`、`F` 计数，`min(cntT, cntF) > k` 就收缩。
- 26 个字母（LC 424）？：窗口长 - 窗口内最多字符次数 `> k` 时收缩。

**同模式。** LC 424 替换后的最长重复字符、LC 1004 最大连续1的个数 III、LC 3 无重复字符的最长子串
