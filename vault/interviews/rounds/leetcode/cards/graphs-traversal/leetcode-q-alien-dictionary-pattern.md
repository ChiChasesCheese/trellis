---
id: leetcode-q-alien-dictionary-pattern
node: graphs-traversal.directed-acyclic-graph
type: qa
anki: 1787102262107
tags: [lc::269, leetcode, pattern, recall]
---
## Q
Alien Dictionary（LC 269）：如何从有序单词列表推导字母间的先后关系并建图？

## A
只比较相邻两个单词的第一个不同字符：ch1 → ch2 连一条有向边（ch1 排在 ch2 前面），并对 ch2 的入度 +1；一旦找到第一个不同字符就 break，后面的字符不再提供顺序信息。特殊校验：如果 word1 是 word2 的前缀但 word1 更长（即两词前 len(word2) 个字符都相同且 word1 更长），说明顺序非法，直接返回空串。建完图后对所有出现过的字符做 Kahn 拓扑排序（入度为 0 入队），若最终拓扑序长度等于字符种类数则合法，否则说明有环，返回空串。

**Evidence**

for ch1, ch2 in zip(word1, word2): 找到第一个不同字符建边后 break；if not found_diff and len(word1) > len(word2): return ""；最后 if len(topo) == len(chars): return "".join(topo) else return ""，与相关题 Course Schedule II 的 Kahn 算法模板完全一致。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F269%20-%20Alien%20Dictionary)
