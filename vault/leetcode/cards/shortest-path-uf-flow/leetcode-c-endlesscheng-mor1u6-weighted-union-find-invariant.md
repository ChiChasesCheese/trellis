---
id: leetcode-c-endlesscheng-mor1u6-weighted-union-find-invariant
node: shortest-path-uf-flow.weighted-union-find
type: cloze
anki: 1787272422805
tags: [concept-cloze, invariant, leetcode, recall]
---
带权并查集中，路径压缩必须同时更新 {{c1::节点到根的相对权重}}。

weight[x] 表示 x 到 parent[x] 或压缩后到根的相对值；find 压缩路径时同步累计 weight；合并两根时新根间权重必须满足新增约束

**Evidence**

§7.6 带权并查集（边权并查集）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.17%20-%20%E5%B8%A6%E6%9D%83%E5%B9%B6%E6%9F%A5%E9%9B%86)
