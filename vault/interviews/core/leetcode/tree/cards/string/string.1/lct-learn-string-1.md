---
id: lct-learn-string-1
node: string.1
type: qa
step: 1
---
## Q
**字符串 › KMP（前缀的后缀）**｜学习卡

套路是什么？

## A
**一句话。** KMP：先算模式串每个前缀的最长相等前后缀（`fail`），失配时只回退模式串的指针，主串指针永不回头。

下图：失配时只把模式串回退到 `fail[k-1]`，主串指针永不回头。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="10" y="36" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<rect x="40" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="76" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="112" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="148" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="184" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="220" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">.</text>
<rect x="256" y="20" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">.</text>
<text x="10" y="72" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">p</text>
<rect x="40" y="56" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="76" y="56" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="112" y="56" width="36" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="148" y="56" width="36" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="166.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="184" y="56" width="36" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="202.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<text x="10" y="128" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回退</text>
<rect x="112" y="112" width="36" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="148" y="112" width="36" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="166.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="184" y="112" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="202.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<rect x="220" y="112" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="256" y="112" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="202" y1="48" x2="202" y2="54" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="210" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d ≠ c：k = fail[3] = 2</text>
<text x="170" y="162" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">p 的已匹配部分 "abab" 的最长相等前后缀 "ab" 直接对上；s 指针不动</text>
</svg>

```python
def kmp(s, p):                       # p 在 s 中首次出现的下标
    m = len(p)
    fail = [0] * m                   # p[:i+1] 的最长相等前后缀长度
    k = 0
    for i in range(1, m):            # 模式串自己匹配自己
        while k and p[i] != p[k]:
            k = fail[k - 1]
        k += p[i] == p[k]
        fail[i] = k
    k = 0                            # 已匹配 p 的前 k 个字符
    for i, ch in enumerate(s):       # s 的指针永不回退
        while k and ch != p[k]:
            k = fail[k - 1]
        k += ch == p[k]
        if k == m:
            return i - m + 1
    return -1
```

**要点。**
- 为什么对？：已匹配 `p[:k]` 时失配，`p[:k]` 的最长相等前后缀 `fail[k-1]` 已经和 `s` 当前位置之前对上了，可以直接从它继续，不必回头。
- LC 796 怎么改？：长度相等且 `goal` 在 `s + s` 里：`len(s) == len(goal) and goal in s + s`；要保证线性就用本模板。

**易错点。**
- 失配回退写成 `k - 1`：`s = "abba"`、`p = "aba"` 会错返回 `1`，要用 `fail[k - 1]`。
- 建表时 `i` 从 `0` 开始：`p[0]` 与自己比，`fail[0]` 变 `1`，真前缀定义被破坏。
- LC 796 漏掉长度判断：`s = "a"`、`goal = "aa"` 时 `"aa" in "aa"` 为真，应为 `false`。

**对应题目。** LC 28 找出字符串中第一个匹配项的下标、LC 796 旋转字符串
