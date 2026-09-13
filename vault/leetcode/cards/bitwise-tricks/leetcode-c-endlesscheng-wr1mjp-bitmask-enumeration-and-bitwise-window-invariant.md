---
id: leetcode-c-endlesscheng-wr1mjp-bitmask-enumeration-and-bitwise-window-invariant
node: bitwise-tricks.bitmask-enumeration-and-bitwise-window
type: cloze
anki: 1787272470880
tags: [concept-cloze, invariant, leetcode, recall]
---
维护“窗口内任意两数按位 AND 为 0”时，mask 表示 {{c1::窗口中已占用的位}}。

掩码 mask 的第 i 位准确表示第 i 个元素是否被选择；窗口位计数大于 1 的位表示该位发生冲突

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.05%20-%20%E4%BD%8D%E8%BF%90%E7%AE%97%E4%B8%8E%E4%BA%8C%E8%BF%9B%E5%88%B6%E6%9E%9A%E4%B8%BE)
