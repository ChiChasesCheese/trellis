---
slug: maximum-length-substring-with-two-occurrences
---
## Q
**LC 3090 每个字符最多出现两次的最长子字符串**｜Easy

求最长子串，使其中每个字符最多出现两次。

## A
**一句话。** 不定长滑窗：右端加入 `ch` 后只有 `ch` 可能超过 2 次，移左端直到它回到 2 次。

```python
def maximum_length_substring(s):
    cnt = Counter()
    left = ans = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while cnt[ch] > 2:       # 只盯刚加入的字符
            cnt[s[left]] -= 1
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(26)`。

**易错点。**
- 用 `if` 代替 `while`：左端可能要移好几格才能把 `ch` 的次数降下来。
- 收缩时减的是 `cnt[ch]`：要减左端字符 `s[left]` 的次数。

**追问。**
- 每个字符最多 `k` 次？：把 `2` 换成 `k`，即 LC 2958。
- 统计满足条件的子串个数？：每个右端点贡献 `right - left + 1`。

**同模式。** LC 3 无重复字符的最长子串、LC 2958 最多 K 个重复元素的最长子数组、LC 904 水果成篮
