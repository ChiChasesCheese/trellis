---
id: tlc-longest-palindromic-substring-2-code
node: a.longest-palindromic-substring
type: qa
step: 2
---
## Q
**LC 5 最长回文子串**｜写出 Python 实现

`s` 仅由数字和英文字母组成，`1 <= s.length <= 1000`。返回 `s` 中最长的回文子串（连续）。用 `O(1)` 额外空间的中心扩展。

## A
**思路。** 枚举 `2n - 1` 个中心：下标 `center` 为偶数时以字符 `center // 2` 为中心，为奇数时以它与下一个字符之间的缝为中心。从中心向两边扩展直到越界或字符不等，退出时 `s[l+1 : r]` 就是这个中心的最长回文，和已有最优比较。

```python
def longest_palindrome(s: str) -> str:
    n = len(s)
    best_l = best_r = 0                            # 当前最长回文是 s[best_l : best_r + 1]
    for center in range(2 * n - 1):                # 2n-1 个中心：n 个字符 + n-1 个缝
        l = center // 2
        r = l + center % 2                         # center 偶数：以字符为中心（l == r）；奇数：以缝为中心（r = l + 1）
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        # 循环结束时 s[l+1 : r] 是以这个中心扩出的最长回文
        if r - l - 1 > best_r - best_l + 1:
            best_l, best_r = l + 1, r - 1
    return s[best_l : best_r + 1]
```

运行：`"babad"` → `"bab"`；`"cbbd"` → `"bb"`；`"a"` → `"a"`；`"ac"` → `"a"`；`"aaaa"` → `"aaaa"`；`"abacdfgdcaba"` → `"aba"`；`"a" * 1000` → 长度 `1000`。

**复杂度。** 时间 `O(n^2)`，最坏出现在全是同一个字母时；空间 `O(1)`。

**写法要点。** 用一个循环变量 `center` 统一处理奇偶两种中心，比写两个 `expand(l, r)` 调用少一半代码；`l = center // 2`、`r = l + center % 2` 一行区分字符中心和缝中心；`while` 的条件把越界检查放在字符比较之前，短路求值避免下标越界；只保存左右端点，最后切片一次，避免在循环里反复拼接字符串。
