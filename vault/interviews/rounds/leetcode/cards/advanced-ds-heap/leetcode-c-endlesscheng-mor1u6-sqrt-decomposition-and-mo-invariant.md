---
id: leetcode-c-endlesscheng-mor1u6-sqrt-decomposition-and-mo-invariant
node: advanced-ds-heap.sqrt-decomposition-and-mo
type: cloze
anki: 1789002116194
tags: [concept-cloze, invariant, leetcode, recall]
---
莫队移动指针后，维护状态必须恰好对应当前 {{c1::[L,R] 区间}}。

块内元素与块聚合一致；莫队当前状态准确对应当前 [L,R]；移动指针一次只应用一个可逆 add/remove

**Evidence**

§10.2 莫队算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.19%20-%20%E5%88%86%E5%9D%97%E3%80%81%E6%A0%B9%E5%8F%B7%E5%88%86%E8%A7%A3%E4%B8%8E%E8%8E%AB%E9%98%9F%E7%AE%97%E6%B3%95)
