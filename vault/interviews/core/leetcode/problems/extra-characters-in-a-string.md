---
slug: extra-characters-in-a-string
---
## Q
**LC 2707 字符串中的额外字符**｜Medium

把字符串 `s` 切出若干互不重叠、都在字典里的子串，剩下的字符是额外字符。求额外字符的最少个数。

## A
**一句话。** 划分型 DP：`f[i]` 是前缀 `s[:i]` 的最少额外字符；要么 `s[i-1]` 当额外字符（`f[i-1] + 1`），要么某个字典词正好以 `i` 结尾（`f[j]`）。

**图解。** `"leetscode"` 的 `f`：`leet` 让 `f[4] = 0`，`code` 让 `f[9] = f[5] = 1`，多出来的是 `s`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 351 144">
<text x="27" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<text x="80.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">l</text>
<text x="110.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">e</text>
<text x="140.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">e</text>
<text x="170.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">t</text>
<text x="200.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s</text>
<text x="230.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<text x="260.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">o</text>
<text x="290.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d</text>
<text x="320.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">e</text>
<text x="27" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f</text>
<rect x="35" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="65" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="95" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="125" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="155" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="185" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="215" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="245" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="275" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="305" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="320.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[4] = 0：leet 是词</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">f[5] = 1：s 是额外字符</text>
<text x="16" y="126" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[9] = f[5] = 1：code 是词</text>
</svg>

```python
def min_extra_char(s, dictionary):
    words = set(dictionary)
    n = len(s)
    f = [0] * (n + 1)          # f[i]：s[:i] 最少剩几个字符
    for i in range(1, n + 1):
        f[i] = f[i - 1] + 1    # s[i-1] 当额外字符
        for j in range(i):
            if s[j:i] in words:
                f[i] = min(f[i], f[j])   # s[j:i] 是一个词
    return f[n]
```

**复杂度。** 时间 `O(n³)`（切片和哈希），空间 `O(n + 字典大小)`。

**易错点。**
- 只考虑「贪心匹配最长词」：`leetcode` 和 `leet + code` 都行，但别的串里贪心会错，必须 DP。
- 忘了 `f[i-1] + 1` 这条转移：字符不在任何词里时 `f[i]` 停在 0。

**追问。**
- 去掉切片开销？：把字典词倒序插进字典树，从 `i-1` 往左走，路过的词尾都是转移点。
- 和单词拆分的关系？：LC 139 问能否 0 额外字符切完，就是这里 `f[n] == 0`。

**同模式。** LC 139 单词拆分、LC 140 单词拆分 II、LC 472 连接词
