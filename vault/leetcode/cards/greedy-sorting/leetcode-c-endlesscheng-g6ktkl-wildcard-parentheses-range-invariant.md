---
id: leetcode-c-endlesscheng-g6ktkl-wildcard-parentheses-range-invariant
node: greedy-sorting.wildcard-parentheses-range
type: cloze
anki: 1787272435107
tags: [concept-cloze, invariant, leetcode, recall]
---
通配括号扫描中，若 {{c1::high < 0}}，则前缀已经不可能合法。

low 和 high 覆盖处理前缀后所有可能的未匹配左括号数；high 小于零表示任何替换都出现了无法匹配的右括号；low 始终截断为零，因为额外右括号可被通配符当空字符避免

**Evidence**

§3.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.13%20-%20%E9%80%9A%E9%85%8D%E5%90%88%E6%B3%95%E6%8B%AC%E5%8F%B7%E8%8C%83%E5%9B%B4%E8%B4%AA%E5%BF%83)
