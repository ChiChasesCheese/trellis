---
id: tlc-find-all-anagrams-in-a-string-2-code
node: p2.find-all-anagrams-in-a-string
type: qa
step: 2
---
## Q
**LC 438 找到字符串中所有字母异位词**｜写出 Python 实现

字符串 `s`、`p`（长度均在 `1..3·10^4`，仅小写字母）。返回 `s` 中所有与 `p` 互为字母异位词的子串的起始下标（顺序任意）。要求 `O(n)`。

## A
**思路。** `need[c]` 表示窗口内字母 `c` 还缺几个（初始是 `p` 的计数，窗口为空）。右端字符进窗口就 `need[c] -= 1`，窗口超过 `m` 时左端字符出窗口 `need[c] += 1`。同时维护 `unbalanced`：`need` 中非 0 的字母种数。`unbalanced == 0` 说明窗口和 `p` 字母重数完全相同，记录起点 `right - m + 1`。

```python
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need = Counter(p)             # need[c]：窗口里还缺几个 c；负数表示多了
    unbalanced = len(need)        # need[c] != 0 的字母种数；为 0 就是异位词
    ans: list[int] = []

    def shift(c: str, d: int) -> int:
        """窗口增减一个 c，返回 unbalanced 的变化量。"""
        was = need[c] != 0
        need[c] += d
        return (need[c] != 0) - was

    for right, ch in enumerate(s):
        unbalanced += shift(ch, -1)               # 右端进窗口：少缺一个 ch
        if right >= m:
            unbalanced += shift(s[right - m], +1)  # 左端出窗口：多缺一个
        if unbalanced == 0:
            ans.append(right - m + 1)
    return ans
```

运行：`s="cbaebabacd", p="abc"` → `[0, 6]`，`s="abab", p="ab"` → `[0, 1, 2]`，`s="a", p="ab"（p 比 s 长）` → `[]`，`s="aabaabaa", p="aab"` → `[0, 1, 2, 3, 4, 5]`。

**复杂度。** 时间 `O(n)`：右端走 `n` 步，每步两次 `O(1)` 的计数更新；空间 `O(Σ)`，`Σ = 26` 是字母表大小（`Counter` 至多 26 个键）。

**写法要点。** `Counter(p)` 一行建计数表，读不存在的键返回 `0` 且不插入；嵌套函数 `shift` 把「改计数并返回不平衡种数的变化」封装起来，进出窗口两处共用，布尔相减 `(need[c] != 0) - was` 得到 `-1 / 0 / +1`；`unbalanced += shift(...)` 让更新和判断分开；`enumerate(s)` 同时拿下标和字符。固定 26 个字母时可用 `[0] * 26` 加 `ord(c) - 97` 提速，但 `Counter` 版对任意字符集成立。
