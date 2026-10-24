---
id: tlc-longest-palindromic-substring-4-followup
node: a.longest-palindromic-substring
type: qa
step: 4
---
## Q
**LC 5 最长回文子串**｜追问

面试官接着问：（1）能不能做到 `O(n)`（Manacher）？（2）统计回文子串的个数（LC 647）怎么改？（3）`n` 很大时中心扩展的最坏情况是什么？

## A
1. **Manacher**：先在字符之间和两端插入分隔符 `#`，让所有回文都变成奇数长度。`radius[i]` 是以 `t[i]` 为中心的回文半径；维护覆盖最靠右的回文 `(center, right)`。处理 `i` 时，若 `i < right`，它关于 `center` 的镜像点 `2 * center - i` 的半径给出 `radius[i]` 的下界（不能超过 `right - i`），再继续向外扩展；每次扩展都会推进 `right`，所以总共 `O(n)`。

```python
def longest_palindrome_manacher(s: str) -> str:
    t = "#" + "#".join(s) + "#"                    # 插入分隔符，奇偶长度统一成奇数
    n = len(t)
    radius = [0] * n                               # radius[i] = 以 t[i] 为中心的回文半径（不含中心）
    center = right = 0                             # 已知覆盖到最右的回文：中心 center，右边界 right
    for i in range(n):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])   # 镜像点的半径是下界
        while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n and t[i - radius[i] - 1] == t[i + radius[i] + 1]:
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    best = max(range(n), key=radius.__getitem__)
    start = (best - radius[best]) // 2
    return s[start : start + radius[best]]
```

`"babad"` → `"bab"`，`"cbbd"` → `"bb"`，与中心扩展一致；`"a" * 100000` 也能很快完成。
2. **统计回文子串（LC 647）**：中心扩展里每成功比较一步（`s[l] == s[r]`）就是一个新的回文子串，计数加一；`"abc"` → `3`，`"aaa"` → `6`。

```python
def count_palindromes(s: str) -> int:
    n, total = len(s), 0
    for center in range(2 * n - 1):
        l = center // 2
        r = l + center % 2
        while l >= 0 and r < n and s[l] == s[r]:
            total += 1
            l -= 1
            r += 1
    return total
```
3. **最坏情况**：全是同一个字符（如 `"a" * 1000`）时每个中心都能扩到边界，总计约 `n^2 / 2` 次比较；`n = 1000` 约 `5 * 10^5` 步，Python 里不到一秒。`n` 到 `10^5` 就必须用 Manacher。

**Python 提醒**：`"#".join(s)` 在 `s` 的每两个字符之间插入 `#`；`max(range(n), key=radius.__getitem__)` 并列时返回第一个最大值，对应最靠左的回文。
