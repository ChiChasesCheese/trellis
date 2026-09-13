---
id: leetcode-c-endlesscheng-mor1u6-enumerate-right-maintain-left-recognition
node: arrays-hash-prefix.enumerate-right-maintain-left
type: cloze
anki: 1787272417905
tags: [concept-cloze, leetcode, recall, recognition]
---
当约束是 i<j 且右端元素能推出左端所需状态时，用 {{c1::枚举右端并维护左侧状态}}。

按右端点扫描，把所有合法左侧信息维护为可查询状态，将双变量匹配降为单次查找。

**Evidence**

§0.1 枚举右，维护左

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.01%20-%20%E6%9E%9A%E4%B8%BE%E5%8F%B3%E7%AB%AF%E3%80%81%E7%BB%B4%E6%8A%A4%E5%B7%A6%E7%AB%AF)
