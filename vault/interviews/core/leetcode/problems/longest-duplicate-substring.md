---
slug: longest-duplicate-substring
---
## Q
**LC 1044 最长重复子串**｜Hard

求 `s` 中出现至少两次（可重叠）的最长子串，没有返回 `""`。

## A
**一句话。** 二分长度 `L`，每个 `L` 用滚动哈希（Rabin-Karp）在 `O(n)` 内查有没有重复窗口。

```python
def longest_dup_substring(s):
    n = len(s)
    nums = [ord(c) - 96 for c in s]
    mod = (1 << 61) - 1
    base = random.randrange(1 << 20, mod)   # 随机底数防卡哈希

    def find(L):               # 返回重复窗口的起点，没有 -1
        top = pow(base, L, mod)
        h = 0
        for x in nums[:L]:
            h = (h * base + x) % mod
        seen = {h: [0]}
        for i in range(1, n - L + 1):
            h = h * base - nums[i-1] * top + nums[i+L-1]
            h %= mod
            for j in seen.get(h, ()):
                if s[j:j+L] == s[i:i+L]:    # 哈希同再逐字比对
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi, start, best = 1, n - 1, 0, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        idx = find(mid)
        if idx != -1:
            start, best, lo = idx, mid, mid + 1
        else:
            hi = mid - 1
    return s[start:start + best]
```

**复杂度。** 时间 `O(n log n)`（期望），空间 `O(n)`。

**易错点。**
- 以为两次出现不能重叠：`"banana"` 的 `"ana"` 就共用一个 `a`，答案会少 `1`。
- 哈希相同就返回：有假阳性，必须逐字比对。
- `find` 只返回布尔值：二分结束时取不出子串，要返回起点。

**追问。**
- 不想用哈希？：后缀数组 + 最长公共前缀（LCP），取相邻后缀 LCP 的最大值。
- 为什么能二分？：有长度 `L` 的重复子串，必有长度 `L-1` 的，判定单调。

**同模式。** LC 1062 最长重复子串、LC 718 最长重复子数组、LC 187 重复的DNA序列、LC 28 找出字符串中第一个匹配项的下标
