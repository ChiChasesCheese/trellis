---
id: leetcode-c-endlesscheng-dhn9vk-bit-mask-operations-template
node: bitwise-tricks.bit-mask-operations
type: cloze
anki: 1787272405507
tags: [concept-cloze, leetcode, recall, template]
---
固定 width 位整数的清位模板核心是 {{c1::mask & (full ^ (1 << k))}}。

不能直接依赖 Python 的 ~。

**Evidence**

一、基础题

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F05.01%20-%20%E4%BD%8D%E6%8E%A9%E7%A0%81%E6%93%8D%E4%BD%9C)
