---
id: lct-learn-dp-7-4
node: dp.7.4
type: qa
step: 1
---
## Q
**动态规划 › 其他线性 DP › 合法子序列 DP**｜学习卡

套路是什么？

## A
**一句话。** 合法子序列 DP：用 `f[x]` 表示「以元素值 `x` 结尾」的最长长度（或个数、和），新元素 `x` 只从倒数第二个元素 `y` 转移；值域大或不是整数时 `f` 用哈希表。

下图：LC 1048，`f` 以「结尾元素」为键，新元素只看它可能的前一个元素。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 120">
<rect x="20" y="30" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<text x="50" y="78" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f = 1</text>
<rect x="100" y="30" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ba</text>
<text x="130" y="78" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f = 2</text>
<line x1="80" y1="45" x2="98" y2="45" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="98.0,45.0 91.7,48.0 91.7,42.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180" y="30" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="210" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bda</text>
<text x="210" y="78" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f = 3</text>
<line x1="160" y1="45" x2="178" y2="45" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="178.0,45.0 171.7,48.0 171.7,42.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="260" y="30" width="60" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="290" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">bdca</text>
<text x="290" y="78" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f = 4</text>
<line x1="240" y1="45" x2="258" y2="45" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258.0,45.0 251.7,48.0 251.7,42.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按长度排序；删去一个字母得到前驱</text>
<text x="170" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f[w] = max(f[前驱] + 1)；f 用哈希表，键是元素值</text>
</svg>

```python
def longest_str_chain(words):
    words.sort(key=len)              # 短的先处理
    f = {}                           # f[w]：以 w 结尾的最长链
    for w in words:
        f[w] = 1
        for i in range(len(w)):      # 删去一个字母得到前驱
            pre = w[:i] + w[i + 1:]
            if pre in f:
                f[w] = max(f[w], f[pre] + 1)
    return max(f.values())
```

**要点。**
- 为什么对？：排序后，`w` 的所有可能前驱（长度少一）都已处理完，`f[w]` 取它们的最大值加一，状态数等于单词数，转移 `O(L)`。
- LC 940 怎么改？：状态改成「以字母 `c` 结尾的不同子序列数」`f[c]`，读到 `c` 时 `f[c] = 1 + sum(f)`（所有已有子序列后接 `c`，加上单独的 `c`），答案是 `sum(f)`；旧的 `f[c]` 被整体替换，所以不会重复计数。

**易错点。**
- 没按长度排序：前驱可能还没算出来，`f` 里查不到会漏转移。
- 940 写成 `f[c] += 1 + sum(f)`：旧的以 `c` 结尾的子序列被重复计数，`"aaa"` 应得 `3`，会得 `7`；必须赋值 `f[c] = 1 + sum(f)`。
- 940 忘了取模：每步对 `10^9 + 7` 取模，`sum(f)` 也要取模。

**对应题目。** LC 940 不同的子序列 II、LC 1048 最长字符串链
