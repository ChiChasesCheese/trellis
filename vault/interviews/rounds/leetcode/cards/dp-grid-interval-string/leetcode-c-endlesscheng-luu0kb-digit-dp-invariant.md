---
id: leetcode-c-endlesscheng-luu0kb-digit-dp-invariant
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272458579
tags: [concept-cloze, invariant, leetcode, recall]
---
数位 DP 中 tight=True 表示当前构造前缀与上界前缀 {{c1::完全相等}}。

dfs(pos, state, tight, started) 覆盖此前前缀对应的全部合法选择；tight 为真时当前位不能超过上界该位；区间答案通过 count(R)-count(L-1) 获得

**Evidence**

二、动态规划：数位 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.10%20-%20%E6%95%B0%E4%BD%8D%20DP)
