---
id: lct-learn-sliding-window-4-2
node: sliding-window.4.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 双序列双指针 › 判断子序列**｜学习卡

套路是什么？

## A
**一句话。** 判断 `s` 是不是 `t` 的子序列：一个指针指着 `s` 中等待匹配的字符，另一个扫过 `t`，遇到就匹配、前进；`s` 走完即是。

下图：`s` 的指针只在匹配时前进，`t` 的指针每步都前进。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<text x="14" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<rect x="60" y="20" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="100" y="20" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="140" y="20" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="160.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<text x="14" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t</text>
<rect x="40" y="100" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="60.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="80" y="100" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h</text>
<rect x="120" y="100" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="140.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="160" y="100" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g</text>
<rect x="200" y="100" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="240" y="100" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<line x1="80.0" y1="48" x2="60.0" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,98.0 59.6,91.0 65.1,93.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="120.0" y1="48" x2="140.0" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,98.0 134.9,93.2 140.4,91.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="160.0" y1="48" x2="260.0" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260.0,98.0 253.0,97.8 255.7,92.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="220" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">i：s 中下一个待匹配</text>
<text x="220" y="52" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">扫 t，相等就 i += 1</text>
<text x="220" y="70" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i == len(s)：是</text>
</svg>

```python
def is_subsequence(s, t):           # LC 392
    i = 0                           # s 中下一个待匹配的位置
    for c in t:
        if i < len(s) and s[i] == c:    # 先判 i 没有越界
            i += 1
    return i == len(s)
```

**要点。**
- 为什么对？：尽早匹配永远不会更差，贪心地用 `t` 里最靠前的字符来匹配。
- 海量查询的进阶怎么改？：`t` 固定时，预处理每个字符在 `t` 里的下标升序列表，匹配时对当前位置二分找第一个更大的出现位置，每个查询 `O(|s| log |t|)`。

**易错点。**
- 指针越界：`s = "a"`、`t = "aa"` 应得 `True`，匹配完 `i == len(s)` 后再读 `s[i]` 会越界。
- 把子序列当子串：`s = "ace"`、`t = "abcde"` 应得 `True`。
- 空串：`s = ""` 恒为 `True`，`s` 非空而 `t` 为空为 `False`。

**对应题目。** LC 392 判断子序列
