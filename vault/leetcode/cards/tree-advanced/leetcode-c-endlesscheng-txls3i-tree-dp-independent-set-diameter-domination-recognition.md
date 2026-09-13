---
id: leetcode-c-endlesscheng-txls3i-tree-dp-independent-set-diameter-domination-recognition
node: tree-advanced.tree-dp-independent-set-diameter-domination
type: cloze
anki: 1787272416704
tags: [concept-cloze, leetcode, recall, recognition]
---
树上选择相邻节点互斥时，使用 {{c1::树上最大独立集 DP}}。

任选根后自底向上汇总子树。不同目标对应不同局部状态：直径保留最长两条向下链，独立集记录选/不选节点，支配集记录覆盖责任。

**Evidence**

§12.2 树上最大独立集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.18%20-%20%E6%A0%91%E5%BD%A2%20DP%EF%BC%9A%E7%9B%B4%E5%BE%84%E3%80%81%E7%8B%AC%E7%AB%8B%E9%9B%86%E4%B8%8E%E6%94%AF%E9%85%8D%E9%9B%86)
