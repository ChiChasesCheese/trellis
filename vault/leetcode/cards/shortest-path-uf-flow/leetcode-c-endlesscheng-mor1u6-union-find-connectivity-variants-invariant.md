---
id: leetcode-c-endlesscheng-mor1u6-union-find-connectivity-variants-invariant
node: shortest-path-uf-flow.union-find-connectivity-variants
type: cloze
anki: 1789002114896
tags: [concept-cloze, invariant, leetcode, recall]
---
并查集判断同组的依据是 {{c1::find(x)==find(y)}}。

同集合元素 find 后代表元相同；路径压缩后 parent 仍指向同一集合代表元；跳过型并查集的 find(x) 返回第一个未被跳过的位置

**Evidence**

七、并查集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.12%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E8%BF%9E%E9%80%9A%E6%80%A7%E3%80%81%E4%B8%AD%E4%BB%8B%E3%80%81%E8%B7%B3%E8%BF%87%E4%B8%8E%E5%8C%BA%E9%97%B4)
