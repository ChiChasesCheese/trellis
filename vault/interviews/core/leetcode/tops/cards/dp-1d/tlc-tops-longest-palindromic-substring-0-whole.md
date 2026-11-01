---
id: tlc-tops-longest-palindromic-substring-0-whole
node: dp-1d.longest-palindromic-substring
type: qa
---
## Q
**LC 5 最长回文子串**｜Medium · 全公司热度第 10 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你字符串 `s`，找到 `s` 中最长的回文子串。`1 <= s.length <= 1000`，`s` 仅由数字和英文字母组成。例：`"babad"` → `"bab"`（`"aba"` 同样合法）；`"cbbd"` → `"bb"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 中心扩展（expand around center）；回文子串 DP；Manacher 算法。

**一句话。** 每个回文都由一个中心决定，枚举全部 `2n - 1` 个中心（字符或相邻字符间的缝）向两侧扩展，取最长。

**识别。** 「最长回文子串」「回文对中心对称」：`n = 1000` 允许 `O(n^2)`；面试里先写中心扩展（代码最短、空间 `O(1)`），被追问线性时间再说 Manacher。

**推导。** 暴力：枚举所有子串并判断回文，`O(n^3)`。回文有对称结构：已知 `s[l..r]` 是回文，只需看 `s[l-1]` 与 `s[r+1]` 是否相等就知道能不能扩展，所以从每个中心出发扩展，每个中心最多 `O(n)`，总共 `O(n^2)`。DP 的做法是 `dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]`，同样 `O(n^2)` 但要 `O(n^2)` 空间，中心扩展更省。

```python
def longest_palindrome(s: str) -> str:
    def expand(left: int, right: int) -> tuple[int, int]:  # 从中心向两侧扩，返回最长回文的半开区间 [l, r)
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right

    best_l, best_r = 0, 1
    for i in range(len(s)):
        # 回文由中心决定：奇数长度以字符 i 为中心，偶数长度以 i 与 i+1 之间的缝为中心
        for l, r in (expand(i, i), expand(i, i + 1)):
            if r - l > best_r - best_l:
                best_l, best_r = l, r
    return s[best_l:best_r]
```

运行：`"babad"` → `"bab"`；`"cbbd"` → `"bb"`；`"a"` → `"a"`；`"ac"` → `"a"`。

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`（不计结果）。

**拓展优化。**
- 线性时间 Manacher：在字符间插入分隔符统一奇偶，维护当前向右延伸最远的回文 `(center, right)`，用镜像点的半径当作新中心半径的下界，只在超出右边界时才继续比较，右边界单调右移，总计 `O(n)`。

```python
def longest_palindrome(s: str) -> str:
    t = "#" + "#".join(s) + "#"  # 每个字符之间插入分隔符，奇偶长度的回文统一成以某个位置为中心
    n = len(t)
    radius = [0] * n  # radius[i]：以 t[i] 为中心的回文半径（不含中心），恰好等于它在 s 中的长度
    center = right = 0  # 当前向右延伸最远的回文：中心 center，右边界 right
    for i in range(n):
        if i < right:  # 落在大回文里：镜像点 2*center-i 的半径是现成的下界
            radius[i] = min(right - i, radius[2 * center - i])
        while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n and t[i - radius[i] - 1] == t[i + radius[i] + 1]:
            radius[i] += 1  # 只在右边界之外才会继续成功扩，右边界单调右移，总共 O(n)
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    length, mid = max((r, i) for i, r in enumerate(radius))
    start = (mid - length) // 2  # t 中下标折回 s 的下标
    return s[start:start + length]
```

**易错点。**
- 只枚举奇数长度中心：`"cbbd"` 会得到 `"c"`（长度 1），漏掉偶数长度回文 `"bb"`。
- `expand` 返回的是越界后的 `left`、`right`，真正的回文区间是 `[left + 1, right)`，直接用 `[left, right]` 会多带两端的字符。
- 把「`s` 与 `s[::-1]` 的最长公共子串」当作答案是错的：`"abcdecba"` 会得到 `"abc"`，它不是回文（正确答案长度为 `1`）；必须额外检查下标是否对应。

**同模式。** LC 647 回文子串、LC 516 最长回文子序列、LC 131 分割回文串、LC 125 验证回文串。
