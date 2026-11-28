---
id: lct-learn-data-structures-6-1
node: data-structures.6.1
type: qa
step: 1
---
## Q
**常用数据结构 › 字典树（trie） › 基础**｜学习卡

套路是什么？

## A
**一句话。** 字典树每条边一个字符，公共前缀共用一段路径，走过同样的路就是有同样的前缀，按前缀查询只要沿路径走 `O(L)`，和词典大小无关；节点上挂 `end` 标记或计数。

下图：每条边一个字符，`$` 标记词尾；查前缀就是从根沿路径走，走断即不存在。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<line x1="170" y1="33" x2="110" y2="47" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="33" x2="240" y2="47" stroke-width="1.2" stroke="currentColor"/>
<line x1="110" y1="73" x2="110" y2="87" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="240" y1="73" x2="240" y2="87" stroke-width="1.2" stroke="currentColor"/>
<line x1="110" y1="113" x2="110" y2="127" stroke-width="1.2" stroke="currentColor"/>
<line x1="240" y1="113" x2="240" y2="127" stroke-width="1.2" stroke="currentColor"/>
<line x1="110" y1="153" x2="110" y2="167" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="110" cy="60" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="240" cy="60" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<circle cx="110" cy="100" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<circle cx="240" cy="100" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="110" cy="140" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<circle cx="240" cy="140" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="240" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<circle cx="110" cy="180" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<text x="170" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">root</text>
<text x="130" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">$</text>
<text x="260" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">$</text>
<text x="30" y="75" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">前缀 "ap"</text>
<text x="30" y="89" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">沿路走 2 步</text>
<text x="250" y="185" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">词：app、bat</text>
<text x="130" y="184" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…</text>
</svg>

```python
class Trie:
    def __init__(self):
        self.root = {}               # 字符 -> 子节点；'$' 标记词尾
    def insert(self, word):
        cur = self.root
        for c in word:
            cur = cur.setdefault(c, {})   # 无路就造路
        cur['$'] = True              # 标记整词的结尾
    def find(self, word):            # 0 断路 / 1 前缀 / 2 整词
        cur = self.root
        for c in word:
            if c not in cur:
                return 0             # 这条前缀不存在
            cur = cur[c]
        return 2 if '$' in cur else 1
    def search(self, word):
        return self.find(word) == 2
    def starts_with(self, prefix):
        return self.find(prefix) != 0
```

**要点。**
- 为什么对？：每个节点恰对应一个前缀，插入会建出单词的每个前缀节点，所以 `find(prefix)` 走得通当且仅当存在以它开头的词；`end` 把「是前缀」和「是整词」分开，插入 `apple` 后 `search("app")` 为假、`starts_with("app")` 为真。
- LC 648 怎么改？：对每个单词沿树走，遇到第一个 `$` 就返回 `word[:i + 1]`（最短词根），走不通就原样返回。
- LC 3043 怎么改？：把 `arr1` 的数转字符串插入，`arr2` 的数从高位起沿树走，能走多深就是公共前缀长度，不需要 `$`。
- LC 1268 怎么改？：同一前缀的词排序后连续，可对排序后的数组二分，或排序后插入、每个节点只留前三个词。

**易错点。**
- 把前缀当整词：漏掉 `$` 标记会让 `search("app")` 也为真。
- LC 648 取最长词根：词根 `["cat","cattle"]`，`cattle` 应替换成 `cat`，要遇到第一个结尾就返回。
- LC 3043 从低位起比：`[12]` 与 `[22]` 应得 `0`，前缀必须从高位算。

**对应题目。** LC 3043 最长公共前缀的长度、LC 208 实现 Trie (前缀树)、LC 648 单词替换、LC 1268 搜索推荐系统
