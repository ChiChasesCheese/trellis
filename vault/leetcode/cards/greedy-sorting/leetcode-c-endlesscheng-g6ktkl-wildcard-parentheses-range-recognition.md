---
id: leetcode-c-endlesscheng-g6ktkl-wildcard-parentheses-range-recognition
node: greedy-sorting.wildcard-parentheses-range
type: cloze
anki: 1787272435006
tags: [concept-cloze, leetcode, recall, recognition]
---
括号串含可作左、右或空的通配符时，维护未匹配左括号数的 {{c1::最小值 low 与最大值 high}}。

把通配符视为左括号、右括号或空字符，维护当前未匹配左括号数量的最小值和最大值范围；范围为空即不可能合法。

**Evidence**

§3.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.13%20-%20%E9%80%9A%E9%85%8D%E5%90%88%E6%B3%95%E6%8B%AC%E5%8F%B7%E8%8C%83%E5%9B%B4%E8%B4%AA%E5%BF%83)
