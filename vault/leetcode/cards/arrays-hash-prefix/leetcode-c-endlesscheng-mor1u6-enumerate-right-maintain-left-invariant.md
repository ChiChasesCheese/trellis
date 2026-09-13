---
id: leetcode-c-endlesscheng-mor1u6-enumerate-right-maintain-left-invariant
node: arrays-hash-prefix.enumerate-right-maintain-left
type: cloze
anki: 1787272418007
tags: [concept-cloze, invariant, leetcode, recall]
---
扫描到 j 前，哈希状态只能包含 {{c1::下标小于 j}} 的元素。

处理 nums[j] 前，状态只代表下标小于 j 的元素；查询使用当前右端，更新在查询之后进行

**Evidence**

§0.1 枚举右，维护左

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.01%20-%20%E6%9E%9A%E4%B8%BE%E5%8F%B3%E7%AB%AF%E3%80%81%E7%BB%B4%E6%8A%A4%E5%B7%A6%E7%AB%AF)
