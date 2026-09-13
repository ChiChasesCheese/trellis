---
id: leetcode-c-endlesscheng-v2rxsn-prefix-suffix-decomposition-recognition
node: arrays-hash-prefix.prefix-suffix-decomposition
type: cloze
anki: 1787272463880
tags: [concept-cloze, leetcode, recall, recognition]
---
每个切分点的答案能由左右两侧独立信息合成时，用 {{c1::前后缀分解}}。

预处理每个切分点左侧和右侧的独立信息，再在线性扫描中组合，避免对每个切分点重复计算。

**Evidence**

一、技巧类题目：前后缀分解

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.05%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%88%86%E8%A7%A3)
