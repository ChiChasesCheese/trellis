---
id: leetcode-c-endlesscheng-txls3i-rerooting-dp-recognition
node: tree-advanced.rerooting-dp
type: cloze
anki: 1787272417007
tags: [concept-cloze, leetcode, recall, recognition]
---
要求每个节点作为根的树答案时，使用 {{c1::换根 DP}}。

先算固定根下的子树贡献，再从父传给子：从父的全局答案排除该子树贡献，作为孩子的外部贡献重新合并。

**Evidence**

§12.4 换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.19%20-%20%E6%8D%A2%E6%A0%B9%20DP)
