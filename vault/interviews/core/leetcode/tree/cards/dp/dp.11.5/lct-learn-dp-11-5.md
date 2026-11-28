---
id: lct-learn-dp-11-5
node: dp.11.5
type: qa
step: 1
---
## Q
**动态规划 › 优化 DP › 字典树优化 DP**｜学习卡

套路是什么？

## A
**一句话。** Word Break 的 `f[i]` 转移要枚举所有 `j`，把词典建成前缀树后，从每个可行的 `j` 沿树往下走，失配立刻停，词尾处标记 `f[i+1]`。

下图：`f` 写在切点上；从可达的切点出发沿字典树走一遍，就枚举完所有以它开头的词。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="30" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="49.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="68" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="106" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<rect x="144" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="163.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s</text>
<rect x="182" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="201.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="220" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="239.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="258" y="20" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="277.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g</text>
<rect x="17" y="92" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="30" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="30" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<line x1="30" y1="46" x2="30" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="55" y="92" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="68" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="68" y1="46" x2="68" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="93" y="92" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="106" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<line x1="106" y1="46" x2="106" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="131" y="92" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="144" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="144" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<line x1="144" y1="46" x2="144" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="169" y="92" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="182" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="182" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="182" y1="46" x2="182" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="207" y="92" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="220" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="220" y1="46" x2="220" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="245" y="92" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="258" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<line x1="258" y1="46" x2="258" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="283" y="92" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="296" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="296" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="296" y1="46" x2="296" y2="90" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<path d="M 30 92 Q 85.0 70 140 92" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140.0,92.0 133.0,91.3 136.1,86.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 30 92 Q 104.0 52 178 92" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="178.0,92.0 171.2,90.3 175.0,85.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 182 92 Q 237.0 62 292 92" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="292.0,92.0 285.2,90.3 289.0,85.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="76" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">cat</text>
<text x="120" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">cats</text>
<text x="220" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dog</text>
<text x="170" y="147" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从每个为真的 j 沿树走，遇词尾标 f[i+1]，失配即停</text>
</svg>

```python
def find_all_concatenated_words(words):
    trie = {}                        # 嵌套字典，"#" 标词尾
    for w in words:
        node = trie
        for c in w:
            node = node.setdefault(c, {})
        node["#"] = 1
    def ok(w):
        n = len(w)
        f = [True] + [False] * n     # f[i]：w[:i] 能拆成若干词
        for j in range(n):
            node = trie if f[j] else {}   # 不可达的 j 直接失配
            for i in range(j, n):    # 从 j 沿树走，失配即停
                node = node.get(w[i])
                if node is None:
                    break
                if "#" in node and (j or i < n - 1):
                    f[i + 1] = True  # 整词本身不算一块
        return f[n]
    return [w for w in words if ok(w)]
```

**要点。**
- 为什么对？：只有 `f[j]` 为真才需要往后找词，沿树走的步数不超过最长词长，省掉了大量切片和哈希。
- LC 139 怎么改？：词典换成给定词典，去掉「整词不算一块」的条件，返回 `f[n]`。

**易错点。**
- 忘了排除整词：每个词都能拆成它自己，结果变成全部 `words`。
- 把「至少两个词」当成「两个不同的词」：`["a","aa"]` 里 `"aa" = "a" + "a"` 也是连接词。

**对应题目。** LC 472 连接词
