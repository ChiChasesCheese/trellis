---
id: leetcode-c-endlesscheng-txls3i-rerooting-dp-invariant
node: tree-advanced.rerooting-dp
type: cloze
anki: 1787272417106
tags: [concept-cloze, invariant, leetcode, recall]
---
传给孩子的外部贡献必须 {{c1::去掉该孩子子树的贡献}}。

down[u] 仅使用 u 的子树；向 child 传递的 up 必须排除 child 的 down 贡献

**Evidence**

§12.4 换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.19%20-%20%E6%8D%A2%E6%A0%B9%20DP)
