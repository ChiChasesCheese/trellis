---
id: tlc-palindromic-substrings-2-code
node: b.palindromic-substrings
type: qa
step: 2
---
## Q
**LC 647 回文子串**｜写出 Python 实现

统计小写字符串 `s`（长度 1 到 1000）中回文子串的个数，位置不同的相同子串分别计数。要求 `O(n^2)` 时间、`O(1)` 额外空间。

## A
**思路。** 每个回文有唯一中心：字符本身（奇数长度）或两个相邻字符之间（偶数长度），共 `2n - 1` 个。从每个中心向两边扩，两端相等就计数并继续，不等就停。

```python
def count_substrings(s: str) -> int:
    n = len(s)
    total = 0
    for center in range(2 * n - 1):         # 2n-1 个中心：n 个字符 + n-1 个相邻字符之间的空隙
        left = center // 2
        right = left + center % 2           # 偶数编号：奇数长度回文；奇数编号：偶数长度回文
        while left >= 0 and right < n and s[left] == s[right]:
            total += 1                      # 每次成功外扩都对应一个新的回文子串
            left -= 1
            right += 1
    return total
```

运行：`"abc"` → `3`，`"aaa"` → `6`，`"a"` → `1`，`"abba"` → `6`，`"a" * 1000` → `500500`。

**复杂度。** 时间 `O(n^2)`：`2n - 1` 个中心，每个至多扩 `O(n)` 步，全相同字符时达到上界；空间 `O(1)`。

**写法要点。** 用一个编号 `center` 统一两类中心：`center // 2` 是左端，`center % 2` 决定右端是否错开一位，避免写两遍几乎相同的扩展循环；`while` 条件里越界判断放在取字符之前，靠 `and` 短路保护索引。
