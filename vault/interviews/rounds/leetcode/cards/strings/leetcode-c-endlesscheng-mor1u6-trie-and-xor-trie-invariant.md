---
id: leetcode-c-endlesscheng-mor1u6-trie-and-xor-trie-invariant
node: strings.trie-and-xor-trie
type: cloze
anki: 1789002114595
tags: [concept-cloze, invariant, leetcode, recall]
---
Trie 中完整单词是否存在由节点的 {{c1::终止标记}} 决定，而非节点存在。

从根到节点的路径对应唯一前缀；终止标记与前缀节点分离；异或 Trie 从最高有效位到最低位贪心

**Evidence**

§6.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.11%20-%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91)
