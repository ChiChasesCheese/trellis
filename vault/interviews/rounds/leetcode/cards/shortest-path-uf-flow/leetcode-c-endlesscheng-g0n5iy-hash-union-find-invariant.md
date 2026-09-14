---
id: leetcode-c-endlesscheng-g0n5iy-hash-union-find-invariant
node: shortest-path-uf-flow.hash-union-find
type: cloze
anki: 1787272479278
tags: [concept-cloze, invariant, leetcode, recall]
---
并查集中两个节点属于同一集合，当且仅当 {{c1::find(a) == find(b)}}。

同一集合所有节点 find 后有相同根；union 只合并不同根，路径压缩不改变集合划分

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.12%20-%20%E5%93%88%E5%B8%8C%E5%B9%B6%E6%9F%A5%E9%9B%86)
