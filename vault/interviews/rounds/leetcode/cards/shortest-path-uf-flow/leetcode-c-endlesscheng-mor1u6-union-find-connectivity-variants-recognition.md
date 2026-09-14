---
id: leetcode-c-endlesscheng-mor1u6-union-find-connectivity-variants-recognition
node: shortest-path-uf-flow.union-find-connectivity-variants
type: cloze
anki: 1789002114794
tags: [concept-cloze, leetcode, recall, recognition]
---
关系只会合并、频繁查询是否同组时，用 {{c1::并查集}}。

并查集维护只合并不拆分的连通块。中介节点把同组元素的两两连边压缩为连接公共节点；数组/区间变体常让 parent 指向下一个未处理位置以跳过已处理元素。

**Evidence**

§7.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.12%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E8%BF%9E%E9%80%9A%E6%80%A7%E3%80%81%E4%B8%AD%E4%BB%8B%E3%80%81%E8%B7%B3%E8%BF%87%E4%B8%8E%E5%8C%BA%E9%97%B4)
