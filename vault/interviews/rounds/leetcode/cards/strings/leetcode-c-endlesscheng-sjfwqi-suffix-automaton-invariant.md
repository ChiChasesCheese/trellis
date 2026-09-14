---
id: leetcode-c-endlesscheng-sjfwqi-suffix-automaton-invariant
node: strings.suffix-automaton
type: cloze
anki: 1787272449581
tags: [concept-cloze, invariant, leetcode, recall]
---
后缀自动机中状态 v 新贡献的不同子串数量为 {{c1::len[v] - len[link[v]]}}。

每个状态对应 endpos 相同的一类子串，并有最大长度 len；link 指向该状态字符串集合的最长真后缀状态；转移保持子串扩展关系

**Evidence**

八、后缀数组/后缀自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.09%20-%20%E5%90%8E%E7%BC%80%E8%87%AA%E5%8A%A8%E6%9C%BA%20%28SAM%29)
