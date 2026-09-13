---
id: leetcode-c-endlesscheng-wr1mjp-prefix-suffix-and-difference-invariant
node: arrays-hash-prefix.prefix-suffix-and-difference
type: cloze
anki: 1787272470580
tags: [concept-cloze, invariant, leetcode, recall]
---
差分 d 的语义是：原数组位置 i 的累计变化等于 {{c1::sum(d[:i + 1])}}。

prefix[i] 只聚合下标小于 i 的信息；差分数组 d 的前缀和等于当前位置的累计增量

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.04%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E3%80%81%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%B7%AE%E5%88%86)
