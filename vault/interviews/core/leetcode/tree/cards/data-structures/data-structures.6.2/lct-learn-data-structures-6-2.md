---
id: lct-learn-data-structures-6-2
node: data-structures.6.2
type: qa
step: 1
---
## Q
**常用数据结构 › 字典树（trie） › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶字典树是被别的算法驱动的索引：搜索同步沿树下行剪枝，通配符让查询分叉，节点存聚合信息（最优下标、热度），反转字符串把后缀变前缀；核心不变，节点对应前缀，经过它的词都在子树里。

下图：词典 bad、dad、mad；通配符让查询在一个节点上分叉成多条路径。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 195">
<circle cx="170" cy="22" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">root</text>
<line x1="170" y1="35" x2="80" y2="52" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="80" cy="65" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="80" y1="78" x2="80" y2="97" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="80" cy="110" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="80" y1="123" x2="80" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="80" cy="155" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="98" y="159" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">$</text>
<line x1="170" y1="35" x2="170" y2="52" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="65" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<line x1="170" y1="78" x2="170" y2="97" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="110" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="170" y1="123" x2="170" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="155" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="188" y="159" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">$</text>
<line x1="170" y1="35" x2="260" y2="52" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="260" cy="65" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">m</text>
<line x1="260" y1="78" x2="260" y2="97" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="260" cy="110" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="260" y1="123" x2="260" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="260" cy="155" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="260" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="278" y="159" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">$</text>
<text x="215" y="20" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">"."：每个孩子都试</text>
<text x="170" y="188" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查询 ".ad"：遇到 . 分叉 dfs，任一条走到 $ 即命中</text>
</svg>

```python
class WordDictionary:                # LC 211：通配符
    def __init__(self):
        self.root = {}
    def add_word(self, word):
        cur = self.root
        for c in word:
            cur = cur.setdefault(c, {})
        cur['$'] = True              # 词尾标记
    def search(self, word):
        def dfs(i, node):            # 从 node 匹配 word[i:]
            if i == len(word):
                return '$' in node   # 走完要恰在词尾
            c = word[i]
            if c == '.':             # 通配：每个孩子都试
                for k, v in node.items():
                    if k != '$' and dfs(i + 1, v):
                        return True
                return False
            return c in node and dfs(i + 1, node[c])
        return dfs(0, self.root)
```

**要点。**
- LC 212 怎么做？：词典合成字典树，网格 DFS 带着当前节点下行，`node.get(c)` 为空就剪枝；命中后把词尾标记取走（同一个词只收一次），格子标记 `#` 用完要恢复，叶子用完可从父节点删去。
- LC 3093、LC 642 怎么做？：聚合信息在插入时沿路径更新每个节点；3093 反转单词，节点存「最短、最早」的下标，查询走不通就读最后走通的节点（一个都对不上读根）；642 节点存句子热度，游标随输入下行，取热度降序、字典序升序前三，输入 `#` 重置。
- LC 588 怎么做？：一步是一个路径段（按 `/` 拆开），节点区分目录与文件，文件存内容；`ls` 目录返回排序后的孩子名，文件只返回自己的名字。
- LC 440 怎么做？：`1..n` 本身是十叉前缀树，不建树，写 `count(x)` 逐层算子树里 `<= n` 的个数：若 `size <= k` 跳到兄弟 `cur + 1`，否则下沉 `cur * 10` 且 `k` 减一。

**易错点。**
- LC 212 找到词后不取走：`[["a","a"]]`、`["a"]` 应得 `["a"]`，会得 `["a","a"]`；忘了恢复格子：`[["b"],["a"]]`、`["ab","b"]` 应得两个词。
- LC 211 走完字符就返回真：先加 `bad`，`search("ba")` 应为假；`.` 必须恰好匹配一个字符。
- LC 440 的 `count` 忘了用 `min(n, hi)` 截断：`n = 13`、`k = 2` 应得 `10`，`k = 6` 应得 `2`。

**对应题目。** LC 211 添加与搜索单词、LC 588 设计内存文件系统、LC 642 设计搜索自动补全系统、LC 440 字典序的第 K 小数字、LC 3093 最长公共后缀查询、LC 212 单词搜索 II
