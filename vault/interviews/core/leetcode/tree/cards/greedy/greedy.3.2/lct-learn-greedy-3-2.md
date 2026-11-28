---
id: lct-learn-greedy-3-2
node: greedy.3.2
type: qa
step: 1
---
## Q
**贪心算法 › 字符串贪心 › 回文串贪心**｜学习卡

套路是什么？

## A
**一句话。** 回文串贪心：回文是成对字符加正中间至多一个；双指针对撞，第一次失配时只有「删左」「删右」两个出路，各验证一次剩下的区间。

下图：LC 680，双指针对撞，失配时只试「删左」和「删右」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="70" y="40" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="120" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="145.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<rect x="170" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="195.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<rect x="220" y="40" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="245.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="145.0" y1="24" x2="145.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="145.0,38.0 142.0,31.7 148.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="145.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="195.0" y1="24" x2="195.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="195.0,38.0 192.0,31.7 198.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="195.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<text x="170" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">外层已配成对；第一次失配 s[i] ≠ s[j]：</text>
<text x="170" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">删左：验 s[i+1..j]　或　删右：验 s[i..j-1]</text>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有这两条出路，各验一次 O(n)</text>
</svg>

```python
def valid_palindrome(s):         # 至多删一个字符
    def ok(i, j):                # s[i..j] 是否回文
        while i < j:
            if s[i] != s[j]:
                return False
            i, j = i + 1, j - 1
        return True

    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:         # 第一次失配：删左或删右
            return ok(i + 1, j) or ok(i, j - 1)
        i, j = i + 1, j - 1
    return True
```

**要点。**
- 为什么对？：失配的两个字符里必须删掉一个才可能回文，删哪个不确定就两个都试；之后不允许再失配，所以各验证一次剩余区间即可，总 `O(n)`。
- LC 409 怎么改？：可重排：每种字母取 `次数 // 2 * 2` 个成对放，若有剩余字母再在中间放一个，答案 `pairs + (pairs < len(s))`。
- 最多删 `k` 个（LC 1216）怎么办？：求最长回文子序列 `lps`，判断 `len(s) - lps <= k`，`O(n^2)` DP。

**易错点。**
- 只试删左：`"aab"` 删左得 `"ab"` 不是回文，误判 `False`；删右才对。
- 失配后两边都删（`ok(i+1, j-1)`）：`"abc"` 误判 `True`，只能删一个。
- LC 409 每个奇数次字母都加 `1`：`"abc"` 得 `3`，应为 `1`，中间只能放一个。

**对应题目。** LC 409 最长回文串、LC 680 验证回文串 II
