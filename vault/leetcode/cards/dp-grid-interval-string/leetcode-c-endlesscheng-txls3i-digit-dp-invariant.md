---
id: leetcode-c-endlesscheng-txls3i-digit-dp-invariant
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272415606
tags: [concept-cloze, invariant, leetcode, recall]
---
tight 为真表示此前前缀与 {{c1::边界前缀相等}}。

tight 为真时当前位不能超过边界对应位；只有不受边界限制的状态才会在不同路径重复并适合缓存

**Evidence**

§10.1 统计合法元素的数目

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.14%20-%20%E6%95%B0%E4%BD%8D%20DP%EF%BC%9A%E8%AE%A1%E6%95%B0%E4%B8%8E%E8%B4%A1%E7%8C%AE)
