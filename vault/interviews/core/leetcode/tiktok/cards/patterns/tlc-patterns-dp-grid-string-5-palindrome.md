---
id: tlc-patterns-dp-grid-string-5-palindrome
node: patterns.dp-grid-string
type: qa
step: 5
---
## Q
**动态规划：网格、双串与区间｜最长回文子串（LC 5）：中心扩展与区间 DP**

为什么中心扩展不需要二维表？要枚举哪些中心？

## A
回文串以中心对称。中心有 `2n - 1` 个：`n` 个字符本身（奇数长度）和 `n - 1` 个相邻字符之间（偶数长度）。从每个中心向两边扩展，直到不匹配。

```python
def longest_palindrome(s: str) -> str:
    start, best = 0, 1
    def expand(l: int, r: int) -> None:
        nonlocal start, best
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        if r - l - 1 > best:               # 退出时 (l, r) 是第一个不匹配的位置
            start, best = l + 1, r - l - 1
    for i in range(len(s)):
        expand(i, i)                       # 奇数长度：以 s[i] 为中心
        expand(i, i + 1)                   # 偶数长度：以 s[i], s[i+1] 之间为中心
    return s[start:start + best]
print(longest_palindrome("babad"), longest_palindrome("cbbd"), longest_palindrome("a"), longest_palindrome("ac"))   # bab bb a a
```

时间 `O(n^2)`（`n <= 1000`，约 `10^6` 次），空间 `O(1)`。`"a" * 1000` 是最坏输入，仍在毫秒级。

**漏掉偶数中心的反例**：只枚举 `expand(i, i)`，`"cbbd"` 得到 `"c"`（长度 1），正确答案是 `"bb"`。

**区间 DP 版本**：`dp[i][j] = (s[i] == s[j]) and (j - i < 3 or dp[i+1][j-1])`，按区间长度从小到大填，时间、空间都是 `O(n^2)`。能找出所有回文子串，但空间比中心扩展大。

**Manacher 算法**：利用已知回文的对称性把时间降到 `O(n)`，面试里点到为止；`n <= 1000` 没必要写。

- 变形：回文子串个数（LC 647）——每次扩展成功就计数 `+1`；分割回文串（LC 131）——先用区间 DP 预处理 `is_pal[i][j]`，再回溯。
