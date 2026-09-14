---
id: leetcode-c-endlesscheng-wr1mjp-digit-dp-invariant
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272471781
tags: [concept-cloze, invariant, leetcode, recall]
---
数位 DP 中 tight=True 表示当前前缀 {{c1::仍与上界前缀完全相同}}。

tight 为真时，已构造前缀与 n 的前缀相同；为假时后续可自由选；状态中保存的信息足以判断最终是否合法且不会遗漏前缀历史

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.08%20-%20%E6%95%B0%E4%BD%8D%20DP)
