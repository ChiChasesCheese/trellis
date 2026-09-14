---
id: leetcode-c-endlesscheng-sjfwqi-trie-prefix-tree-invariant
node: strings.trie-prefix-tree
type: cloze
anki: 1788743829487
tags: [concept-cloze, invariant, leetcode, recall]
---
Trie 中一个节点的路径拼接结果表示 {{c1::一个前缀}}，而 is_word 表示该前缀是否恰好是完整单词。

从根走过的路径恰好拼成该节点代表的前缀；is_word 只标记完整单词结束，不代表该节点没有后继

**Evidence**

六、字典树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.07%20-%20Trie%20%E5%89%8D%E7%BC%80%E6%A0%91)
