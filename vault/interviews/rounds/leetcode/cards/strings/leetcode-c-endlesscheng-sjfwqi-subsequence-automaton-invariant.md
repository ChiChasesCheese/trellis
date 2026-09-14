---
id: leetcode-c-endlesscheng-sjfwqi-subsequence-automaton-invariant
node: strings.subsequence-automaton
type: cloze
anki: 1787272449880
tags: [concept-cloze, invariant, leetcode, recall]
---
子序列自动机的 next_pos[i][c] 保存位置 i 及之后字符 c 的 {{c1::最早出现下标}}。

next_pos[i][c] 是 text 中下标不小于 i 的最早字符 c 位置，缺失为 -1；匹配到 text[pos] 后，下一个查询位置必须是 pos+1，保证顺序严格递增

**Evidence**

九、子序列自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.10%20-%20%E5%AD%90%E5%BA%8F%E5%88%97%E8%87%AA%E5%8A%A8%E6%9C%BA)
