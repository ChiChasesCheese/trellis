---
id: lct-learn-dp-5-1
node: dp.5.1
type: qa
step: 1
---
## Q
**动态规划 › 划分型 DP › 判定能否划分**｜学习卡

套路是什么？

## A
**一句话。** 判定能否划分：`f[i]` 表示前 `i` 个字符能否划分，枚举最后一段 `s[j:i]`，要求 `f[j]` 为真且这段合法。

下图：`f[i]` 写在第 `i` 个切点上；从一个为真的切点跳过一个单词，就到达下一个为真的切点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="26" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<rect x="62" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="98" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="134" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<rect x="170" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="206" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<rect x="242" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="278" y="20" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="13" y="90" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="26" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="26" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<line x1="26" y1="46" x2="26" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="49" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="62" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="62" y1="46" x2="62" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="85" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="98" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="98" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<line x1="98" y1="46" x2="98" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="121" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="134" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<line x1="134" y1="46" x2="134" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="157" y="90" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="170" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="170" y1="46" x2="170" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="193" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="206" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="206" y1="46" x2="206" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="229" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="242" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<line x1="242" y1="46" x2="242" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="265" y="90" width="26" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F</text>
<text x="278" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="278" y1="46" x2="278" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="301" y="90" width="26" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="314" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<text x="314" y="128" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<line x1="314" y1="46" x2="314" y2="88" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<path d="M 26 90 Q 96.0 64 166 90" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="166.0,90.0 159.0,89.5 161.9,84.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 170 90 Q 240.0 64 310 90" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="310.0,90.0 303.0,89.5 305.9,84.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="98" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">"leet"</text>
<text x="242" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">"code"</text>
<text x="170" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i] = 存在 j：f[j] 且 s[j:i] 是单词</text>
</svg>

```python
def word_break(s, words):
    words = set(words)           # 集合查找 O(1)
    L = max(map(len, words))     # 最长单词：更远的切点不用看
    f = [True] + [False] * len(s)    # 空串可划分
    for i in range(1, len(s) + 1):
        f[i] = any(f[j] and s[j:i] in words
                   for j in range(max(0, i - L), i))
    return f[-1]
```

**要点。**
- 为什么对？：把串划分成若干合法段，最后一段 `s[j:i]` 确定后，前面 `s[:j]` 是独立的子问题，所以枚举 `j` 即可。
- 为什么只看最近 `L` 位？：最后一段长度不会超过最长单词，`i - j > L` 的切点一定不合法，复杂度降到 `O(n·L)` 次查表。
- 要输出所有拆分（LC 140）或字典很大怎么办？：自顶向下 `@cache` 返回后缀的所有拆分（方案数可能指数级）；字典很大时建 Trie，从每个起点沿 `s` 往下走。

**易错点。**
- `f[0]` 不设 `True`：整张表全 `False`。
- 字典用 `list` 查找：每次 `O(|dict|)`，先转 `set`。
- 贪心遇词就切：`"aaaaaaa"`、`["aaaa","aaa"]` 先切 `aaa` 会失败，应为 `True`。

**对应题目。** LC 139 单词拆分
