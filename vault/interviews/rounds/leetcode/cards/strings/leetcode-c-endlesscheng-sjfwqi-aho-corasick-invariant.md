---
id: leetcode-c-endlesscheng-sjfwqi-aho-corasick-invariant
node: strings.aho-corasick
type: cloze
anki: 1787272448980
tags: [concept-cloze, invariant, leetcode, recall]
---
AC 自动机的 fail[node] 指向该节点字符串的 {{c1::最长真后缀}} 所对应节点。

节点的 fail 指向其字符串的最长真后缀对应的 Trie 节点；文本扫描状态始终是当前文本后缀能匹配的最长 Trie 前缀

**Evidence**

七、AC 自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.07%20-%20AC%20%E8%87%AA%E5%8A%A8%E6%9C%BA%EF%BC%88Aho-Corasick%EF%BC%89)
