---
id: leetcode-c-endlesscheng-luu0kb-binary-trie-xor-recognition
node: bitwise-tricks.binary-trie-xor
type: cloze
anki: 1787272460880
tags: [concept-cloze, leetcode, recall, recognition]
---
需要在数集合中寻找与 x {{c1::异或最大}} 的元素时，用 0-1 字典树。

按二进制位建立字典树，查询时优先走与当前位相反的分支以最大化 XOR；可配合滑动窗口维护允许集合。

**Evidence**

四、数据结构：0-1 字典树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.18%20-%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%E5%BC%82%E6%88%96%E8%B4%AA%E5%BF%83)
