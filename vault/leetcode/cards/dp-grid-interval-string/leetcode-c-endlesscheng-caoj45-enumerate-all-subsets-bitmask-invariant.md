---
id: leetcode-c-endlesscheng-caoj45-enumerate-all-subsets-bitmask-invariant
node: dp-grid-interval-string.enumerate-all-subsets-bitmask
type: cloze
anki: 1787272454079
tags: [concept-cloze, invariant, leetcode, recall]
---
区间 range(1 << n) 中的每个整数都唯一对应全集 {0,...,n-1} 的一个子集，二者是 {{c1::一一对应}} 的关系。

整数的二进制表示直接编码了子集的成员关系。

**Evidence**

§4.1 枚举所有集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.05%20-%20%E6%9E%9A%E4%B8%BE%E5%85%A8%E9%9B%86%E7%9A%84%E6%89%80%E6%9C%89%E5%AD%90%E9%9B%86%EF%BC%88%E7%8A%B6%E5%8E%8B%E6%9E%9A%E4%B8%BE%E5%9F%BA%E7%A1%80%EF%BC%89)
