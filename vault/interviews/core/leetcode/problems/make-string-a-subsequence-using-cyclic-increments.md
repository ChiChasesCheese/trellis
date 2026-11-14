---
slug: make-string-a-subsequence-using-cyclic-increments
---
## Q
**LC 2825 循环增长使字符串子序列等于另一个字符串**｜Medium

一次操作可选 `str1` 的任意一组下标，把这些字符各自循环加一（`z` 变 `a`），至多做一次。问能否让 `str2` 成为 `str1` 的子序列。

## A
**一句话。** 双指针贪心判子序列：`str1` 的字符本身或它的下一个字母等于 `str2[j]` 就匹配，`j` 前进。

**图解。** `str1` 每个字符可用本身或 `+1` 后的字母去配 `str2[j]`，配上就让 `j` 前进。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 160">
<rect x="70" y="16" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="33.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="106" y="16" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="33.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="142" y="16" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="33.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">c</text>
<rect x="70" y="50" width="36" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="88.0" y="64.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">b</text>
<rect x="106" y="50" width="36" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="124.0" y="64.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">c</text>
<rect x="142" y="50" width="36" height="22" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160.0" y="64.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="70" y="116" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="133.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="106" y="116" width="36" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="133.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<text x="62" y="33" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">str1</text>
<text x="62" y="65" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">+1</text>
<text x="62" y="133" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">str2</text>
<polyline points="78.0,42 78.0,116" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="78.0,116.0 75.0,110.0 81.0,110.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="160.0,72 124.0,116" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="124.0,116.0 125.5,109.5 130.1,113.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="190" y="33" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a = a，j → 1</text>
<text x="190" y="65" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c+1 = d，j → 2</text>
<text x="190" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b、b+1 都不是 d，跳过</text>
</svg>

```python
def can_make_subsequence(str1, str2):
    j = 0
    for c in str1:
        if j == len(str2):
            break
        nxt = chr((ord(c) - 97 + 1) % 26 + 97)  # z 绕回 a
        if str2[j] in (c, nxt):  # 能匹配就贪心地用掉
            j += 1
    return j == len(str2)
```

**复杂度。** 时间 `O(n + m)`，空间 `O(1)`。

**易错点。**
- `z` 的下一个：忘了 `% 26`，`"zc"` 配 `"ad"` 会判错。
- 以为只能整体加一：操作是任选下标各自加一，所以每个字符独立决定加不加。

**追问。**
- 为什么贪心对？：越早匹配 `str2[j]`，留给后面的 `str1` 越长，不会更差。
- 允许加任意次（加 k）？：判断条件换成 `(ord(t) - ord(c)) % 26 <= k`。

**同模式。** LC 392 判断子序列、LC 524 通过删除字母匹配到字典里最长单词、LC 792 匹配子序列的单词数
