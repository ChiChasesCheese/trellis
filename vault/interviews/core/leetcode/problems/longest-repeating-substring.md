---
slug: longest-repeating-substring
---
## Q
**LC 1062 最长重复子串**｜Medium

求字符串 `s` 中出现至少两次（可重叠）的最长子串的长度，没有则为 `0`。

## A
**一句话。** 对长度二分（有长 `L` 的重复子串则有长 `L-1` 的），用集合判断某个长度的窗口是否出现过两次。

```python
def longest_repeating_substring(s):
    def has_repeat(length):
        seen = set()
        for i in range(len(s) - length + 1):
            sub = s[i:i + length]
            if sub in seen:
                return True
            seen.add(sub)
        return False

    lo, hi = 0, len(s) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2  # 上取整，防死循环
        if has_repeat(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(n² log n)`，空间 `O(n²)`。

**易错点。**
- 中点下取整：`lo=2, hi=3` 且长度 `2` 可行时 `mid` 恒为 `2`，死循环。
- 按「不能重叠」处理：`"aaaa"` 应为 `3`，会得 `2`。
- 把 `hi` 设成 `n`：长度 `n` 的子串只有一个，多算一轮。

**追问。**
- `n` 到 `3×10^4`（LC 1044）怎么办？：切片和集合太慢，用滚动哈希把判定降到 `O(n)`。
- 不用二分怎么做？：`dp[i][j]` 记以 `s[i-1]`、`s[j-1]` 结尾（`i<j`）的最长公共后缀，取全表最大值。

**同模式。** LC 1044 最长重复子串、LC 718 最长重复子数组、LC 1143 最长公共子序列、LC 187 重复的DNA序列
