---
id: lct-learn-data-structures-6-3
node: data-structures.6.3
type: qa
step: 1
---
## Q
**常用数据结构 › 字典树（trie） › 字典树优化 DP**｜学习卡

套路是什么？

## A
**一句话。** 拆分成字典词是划分型 DP，字典树让从位置 `i` 出发沿树走一遍就枚举出所有以 `s[i]` 开头的词（遇 `$` 就是一个可用的词，断路立刻停）；要列出所有拆法就对后缀记忆化。

下图：从位置 `i` 沿字典树走一遍，路上每个 `$` 就是一个可用的词，断路立刻停；剩下的后缀交给记忆化的 `dfs`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="30" y="40" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="50.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="70" y="40" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="90.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="110" y="40" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<rect x="150" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s</text>
<rect x="190" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="230" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">n</text>
<rect x="270" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="50.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="90.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="130.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="170.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="210.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="250.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="290.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="50.0" y="28" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="30" y1="98" x2="30" y2="104" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="150" y1="98" x2="150" y2="104" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="98" x2="150" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="90.0" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">"cat" 遇 $ → dfs(3)</text>
<line x1="30" y1="126" x2="30" y2="132" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="190" y1="126" x2="190" y2="132" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="126" x2="190" y2="126" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="110.0" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">"cats" 遇 $ → dfs(4)</text>
<text x="270" y="28" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从 i 出发沿树走</text>
<text x="270" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">"catsa" 断路：停</text>
</svg>

```python
def word_break_ii(s, word_dict):     # LC 140
    root = {}
    for w in word_dict:
        node = root
        for c in w:
            node = node.setdefault(c, {})
        node['$'] = True             # 词在此结束
    @cache
    def dfs(i):                      # s[i:] 的所有拆法
        res = [''] if i == len(s) else []   # 末尾：一种空拆法
        node = root
        for j in range(i, len(s)):
            node = node.get(s[j])
            if node is None:
                break                # 断路：更长的段也不是词
            if '$' in node:          # 第一个词是 s[i..j]
                for rest in dfs(j + 1):
                    res.append(f'{s[i:j+1]} {rest}'.strip())
        return res
    return dfs(0)
```

**要点。**
- 为什么对？：字典树保证从 `i` 出发沿 `s[i], s[i+1], …` 走出的路径覆盖所有以 `s[i..j]` 为前缀的词，途中遇到的 `$` 就恰是所有词，不重不漏；断路说明没有词以这一段开头，更长的也不可能。
- 为什么要记忆化？：`dfs(i)` 只依赖 `i`，无解的后缀会被不同前缀反复走进，不记忆就指数增长；输出本身可能指数多，复杂度是输出敏感的。
- LC 139 怎么改？：布尔 `f[i]`，`f[0] = True`，对可达的 `i` 沿树走，遇 `$` 在 `j` 处置 `f[j + 1] = True`，答案 `f[n]`；`f[i]` 不可达就别走。

**易错点。**
- 不加记忆化：`22` 个 `a` 加 `b`、字典 `["a","aa","aaa"]` 无解，应返回 `[]`，不记忆会超时。
- 断路后写 `continue`：`node` 已是 `None`，下一轮 `AttributeError`；应 `break`。
- 拼句子时末尾多空格：`dfs(n)` 返回 `['']`，要判断 `rest` 是否为空。

**对应题目。** LC 140 单词拆分 II
