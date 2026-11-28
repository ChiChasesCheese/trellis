---
id: lct-learn-dp-4-1-2
node: dp.4.1.2
type: qa
step: 1
---
## Q
**动态规划 › 经典线性 DP › 最长公共子序列（LCS） › 进阶**｜学习卡

套路是什么？

## A
**一句话。** LCS 进阶仍是前缀对前缀的二维 DP，只是转移多了「匹配 / 不匹配 / 通配」的分支；先想末尾字符各自怎么被消化。

下图：LC 115，同一张前缀表，转移换成「不用 / 用」两支相加。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="20" y="24" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42.0" y="42.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="24" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="108" y="24" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="152" y="24" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="52" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42.0" y="70.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="52" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="86.0" y="70.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">左上</text>
<rect x="108" y="52" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130.0" y="70.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">上</text>
<rect x="152" y="52" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="80" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42.0" y="98.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="80" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="108" y="80" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="98.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">本格</text>
<rect x="152" y="80" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="108" width="44" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42.0" y="126.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="108" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="108" y="108" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="152" y="108" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="130.0" y1="72.0" x2="130.0" y2="81.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,81.0 127.0,74.7 133.0,74.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="100.0" y1="74.0" x2="112.0" y2="84.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112.0,84.0 105.2,82.2 109.1,77.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="20" y="16" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t 前缀 →</text>
<text x="210" y="40" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">不用 s[i]：上</text>
<text x="210" y="60" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s[i] == t[j]：再加左上</text>
<text x="210" y="92" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 列 = 1：</text>
<text x="210" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空的 t 恰有一种取法</text>
<text x="170" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先想 s、t 的末尾字符各自怎么被消化</text>
</svg>

```python
def num_distinct(s, t):          # s 的子序列中 t 出现的次数
    m, n = len(s), len(t)
    # f[i][j]：s[:i] 的子序列中 t[:j] 出现的次数
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        f[i][0] = 1              # 空串 t：恰一种取法
    for i, x in enumerate(s):
        pre, cur = f[i], f[i + 1]
        for j, y in enumerate(t):
            cur[j + 1] = pre[j + 1]              # 不用 s[i]
            if x == y:
                cur[j + 1] += pre[j]       # 用 s[i] 配 t[j]
    return f[m][n]
```

**要点。**
- 为什么对？：`s[i]` 要么不用（沿用 `f[i][j+1]`），要么用来匹配 `t[j]`（`f[i][j]`），两类互不重叠所以相加。
- LC 97 怎么改？：`f[i][j]` 表示 `s1[:i]`、`s2[:j]` 能否交错成 `s3[:i+j]`，末字符来自 `s1` 或 `s2` 二选一；先比总长度。
- LC 44 怎么改？：`*` 取「匹配空 `f[i][j-1]`」或「多吞一个 `f[i-1][j]`」，`?` 和普通字符取斜上；第 `0` 行只有连续的 `*` 才为真。
- LC 10 怎么改？：`*` 绑定前一个字符：零次 `f[i][j-2]`，或前字符能匹配 `s[i]` 时 `f[i-1][j]`；`.` 匹配任意字符。

**易错点。**
- 只置 `f[0][0] = 1`：第 `0` 列每一行都要是 `1`，`("babgbag", "bag")` 得 `3`，应为 `5`。
- 相等时丢掉「不用」那一项：`("rabbbit", "rabbit")` 得 `1`，应为 `3`。
- LC 44 第 `0` 列设成 `True`：`("a", "")` 得 `True`，应为 `False`。

**对应题目。** LC 115 不同的子序列、LC 97 交错字符串、LC 10 正则表达式匹配、LC 44 通配符匹配
