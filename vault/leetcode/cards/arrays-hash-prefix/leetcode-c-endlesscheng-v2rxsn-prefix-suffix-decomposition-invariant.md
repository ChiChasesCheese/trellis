---
id: leetcode-c-endlesscheng-v2rxsn-prefix-suffix-decomposition-invariant
node: arrays-hash-prefix.prefix-suffix-decomposition
type: cloze
anki: 1787272463980
tags: [concept-cloze, invariant, leetcode, recall]
---
前后缀数组必须为同一位置 i 约定一致的 {{c1::切分边界}}。

left[i] 只依赖 i 左侧信息，right[i] 只依赖 i 右侧信息；组合时两个数组的下标对应同一个切分语义

**Evidence**

一、技巧类题目：前后缀分解

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.05%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%88%86%E8%A7%A3)
