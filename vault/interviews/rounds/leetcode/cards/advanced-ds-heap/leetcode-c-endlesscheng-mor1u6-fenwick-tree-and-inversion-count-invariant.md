---
id: leetcode-c-endlesscheng-mor1u6-fenwick-tree-and-inversion-count-invariant
node: advanced-ds-heap.fenwick-tree-and-inversion-count
type: cloze
anki: 1789002115219
tags: [concept-cloze, invariant, leetcode, recall]
---
Fenwick 的 update 方向是 i {{c1::+= i & -i}}。

树状数组下标从 1 开始；update 沿 i+=i&-i 覆盖包含 i 的块；prefix 沿 i-=i&-i 分解为不重叠块

**Evidence**

§8.1 树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.14%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E3%80%81%E5%80%BC%E5%9F%9F%E7%BB%9F%E8%AE%A1%E4%B8%8E%E9%80%86%E5%BA%8F%E5%AF%B9)
