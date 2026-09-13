---
id: leetcode-c-endlesscheng-luu0kb-binary-trie-xor-invariant
node: bitwise-tricks.binary-trie-xor
type: cloze
anki: 1787272460981
tags: [concept-cloze, invariant, leetcode, recall]
---
查询最大 XOR 的每一位，应优先走当前位的 {{c1::相反分支}}。

每条根到叶路径表示一个已插入数的二进制位；查询每一位先尝试相反位，因高位优先决定 XOR 大小；若支持删除，每个节点维护经过它的计数

**Evidence**

四、数据结构：0-1 字典树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.18%20-%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%E5%BC%82%E6%88%96%E8%B4%AA%E5%BF%83)
